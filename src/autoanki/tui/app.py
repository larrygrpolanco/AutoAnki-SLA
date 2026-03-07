import subprocess
import tempfile
from pathlib import Path

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer, Vertical
from textual.screen import ModalScreen, Screen
from textual.widgets import (
    Button,
    Checkbox,
    DirectoryTree,
    Footer,
    Header,
    Input,
    Label,
    LoadingIndicator,
    ProgressBar,
    Static,
)
from textual.worker import Worker, WorkerState

from ..deck_builder import build_deck_with_audio
from ..llm import run_pipeline
from ..models import AutoAnkiCards
from ..parser import MAX_CHARS, count_chars, extract_text, parse_past_vocab
from ..tts import build_audio_queries, generate_audio_batch


# ─── File Browser Modal ──────────────────────────────────────────────────────


class FileBrowserModal(ModalScreen[str | None]):
    """Modal file browser. Returns selected path or None on cancel."""

    DEFAULT_CSS = """
    FileBrowserModal {
        align: center middle;
    }
    FileBrowserModal > Vertical {
        width: 70%;
        height: 80%;
        border: solid $accent;
        background: $surface;
        padding: 1 2;
    }
    FileBrowserModal DirectoryTree {
        height: 1fr;
    }
    FileBrowserModal .modal-buttons {
        height: 3;
        margin-top: 1;
    }
    FileBrowserModal Label {
        margin-bottom: 1;
        color: $text-muted;
    }
    """

    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, filter_extensions: tuple[str, ...] = (".pdf", ".txt")):
        super().__init__()
        self._filter = filter_extensions

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("Select a file (.pdf or .txt)")
            yield DirectoryTree(Path.home(), id="file-tree")
            with Horizontal(classes="modal-buttons"):
                yield Button("Cancel", variant="default", id="btn-cancel")

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        path = event.path
        if path.suffix.lower() in self._filter:
            self.dismiss(str(path))
        else:
            self.query_one("#file-tree", DirectoryTree).focus()

    @on(Button.Pressed, "#btn-cancel")
    def action_cancel(self) -> None:
        self.dismiss(None)


# ─── Screen 1: Input ─────────────────────────────────────────────────────────


class InputScreen(Screen):
    """Screen 1: Enter source file and optional past vocab, then generate."""

    DEFAULT_CSS = """
    InputScreen {
        align: center middle;
    }
    InputScreen > Vertical {
        width: 70;
        height: auto;
        border: solid $accent;
        background: $surface;
        padding: 2 3;
    }
    InputScreen .title {
        text-align: center;
        text-style: bold;
        margin-bottom: 2;
        color: $accent;
    }
    InputScreen .field-label {
        margin-top: 1;
        margin-bottom: 0;
        color: $text-muted;
    }
    InputScreen .file-row {
        height: 3;
        margin-bottom: 1;
    }
    InputScreen .file-row Input {
        width: 1fr;
    }
    InputScreen .file-row Button {
        width: 10;
        margin-left: 1;
    }
    InputScreen .char-count {
        color: $text-muted;
        margin-bottom: 1;
    }
    InputScreen .char-count.-warn {
        color: $error;
    }
    InputScreen .error-msg {
        color: $error;
        display: none;
        margin-top: 1;
    }
    InputScreen .error-msg.-visible {
        display: block;
    }
    InputScreen .loading-area {
        display: none;
        align: center middle;
        height: 5;
    }
    InputScreen .loading-area.-visible {
        display: block;
    }
    InputScreen .action-row {
        margin-top: 2;
        height: 3;
        align: center middle;
    }
    InputScreen .optional-label {
        color: $text-muted;
        text-style: italic;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("AutoAnki", classes="title")

            yield Label("Source File  (.pdf or .txt)", classes="field-label")
            with Horizontal(classes="file-row"):
                yield Input(placeholder="Path to your source file...", id="source-input")
                yield Button("Browse", id="btn-browse-source")

            yield Label("0 characters", id="char-count", classes="char-count")

            yield Label(
                "Past Vocabulary  (optional)", classes="field-label optional-label"
            )
            with Horizontal(classes="file-row"):
                yield Input(
                    placeholder="Path to past vocabulary file (optional)...",
                    id="vocab-input",
                )
                yield Button("Browse", id="btn-browse-vocab")

            yield Label("", id="error-msg", classes="error-msg")

            with Container(classes="loading-area", id="loading-area"):
                yield LoadingIndicator()
                yield Label("Preparing...", id="loading-label")

            with Horizontal(classes="action-row"):
                yield Button("Generate", variant="primary", id="btn-generate")

    # ── File browsing ──

    @on(Button.Pressed, "#btn-browse-source")
    def browse_source(self) -> None:
        self.app.push_screen(FileBrowserModal(), self._on_source_selected)

    def _on_source_selected(self, path: str | None) -> None:
        if path:
            self.query_one("#source-input", Input).value = path
            self._update_char_count(path)

    @on(Button.Pressed, "#btn-browse-vocab")
    def browse_vocab(self) -> None:
        self.app.push_screen(FileBrowserModal(filter_extensions=(".txt",)), self._on_vocab_selected)

    def _on_vocab_selected(self, path: str | None) -> None:
        if path:
            self.query_one("#vocab-input", Input).value = path

    @on(Input.Changed, "#source-input")
    def on_source_changed(self, event: Input.Changed) -> None:
        self._update_char_count(event.value)

    def _update_char_count(self, file_path: str) -> None:
        label = self.query_one("#char-count", Label)
        p = Path(file_path)
        if not p.exists() or not p.is_file():
            label.update("0 characters")
            label.remove_class("-warn")
            return
        try:
            text = extract_text(file_path)
            n = count_chars(text)
            label.update(f"{n:,} characters")
            if n > MAX_CHARS:
                label.add_class("-warn")
                label.update(f"{n:,} characters  (over {MAX_CHARS:,} limit — trim your input)")
            else:
                label.remove_class("-warn")
        except Exception:
            label.update("Could not read file")

    # ── Generate ──

    @on(Button.Pressed, "#btn-generate")
    def on_generate(self) -> None:
        source_path = self.query_one("#source-input", Input).value.strip()
        error = self._validate(source_path)
        if error:
            self._show_error(error)
            return

        self._hide_error()
        self._show_loading("Step 1/3: Drafting cards...")
        self._source_path = source_path
        self._vocab_path = self.query_one("#vocab-input", Input).value.strip()
        self._run_llm_pipeline()

    def _validate(self, source_path: str) -> str | None:
        if not source_path:
            return "Please select a source file."
        p = Path(source_path)
        if not p.exists():
            return f"File not found: {source_path}"
        if p.suffix.lower() not in (".pdf", ".txt"):
            return "Only .pdf and .txt files are supported."
        try:
            text = extract_text(source_path)
            if count_chars(text) > MAX_CHARS:
                return f"File is too long ({count_chars(text):,} chars). Maximum is {MAX_CHARS:,}."
            if count_chars(text) < 50:
                return "File appears to be empty or too short."
        except Exception as e:
            return f"Could not read file: {e}"
        return None

    @work(thread=True, exclusive=True)
    def _run_llm_pipeline(self) -> None:
        source_path = self._source_path
        vocab_path = self._vocab_path

        text = extract_text(source_path)
        past_vocab = []
        if vocab_path:
            try:
                past_vocab = parse_past_vocab(vocab_path)
            except Exception:
                pass

        def progress(msg: str) -> None:
            self.app.call_from_thread(self._update_loading_label, msg)

        cards = run_pipeline(text, past_vocab, progress_callback=progress)
        self.app.call_from_thread(self._pipeline_done, cards)

    def _pipeline_done(self, cards: AutoAnkiCards) -> None:
        self._hide_loading()
        self.app.push_screen(ReviewScreen(cards))

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.state == WorkerState.ERROR:
            error = str(event.worker.error)
            self._hide_loading()
            self._show_error(f"Generation failed: {error}")

    # ── UI helpers ──

    def _show_loading(self, msg: str = "Working...") -> None:
        self.query_one("#loading-area").add_class("-visible")
        self.query_one("#btn-generate", Button).disabled = True
        self.query_one("#loading-label", Label).update(msg)

    def _hide_loading(self) -> None:
        self.query_one("#loading-area").remove_class("-visible")
        self.query_one("#btn-generate", Button).disabled = False

    def _update_loading_label(self, msg: str) -> None:
        self.query_one("#loading-label", Label).update(msg)

    def _show_error(self, msg: str) -> None:
        label = self.query_one("#error-msg", Label)
        label.update(msg)
        label.add_class("-visible")

    def _hide_error(self) -> None:
        self.query_one("#error-msg", Label).remove_class("-visible")


# ─── Screen 2: Review & Select ───────────────────────────────────────────────


class VocabItem(Static):
    """A single vocab word row with checkbox."""

    DEFAULT_CSS = """
    VocabItem {
        height: 3;
        border-bottom: solid $surface-darken-1;
        padding: 0 1;
    }
    VocabItem Horizontal {
        height: 3;
        align: left middle;
    }
    VocabItem .word {
        width: 18;
        text-style: bold;
    }
    VocabItem .translation {
        width: 20;
        color: $text-muted;
    }
    VocabItem .pos {
        width: 12;
        color: $text-muted;
        text-style: italic;
    }
    """

    def __init__(self, entry_id: str, word: str, translation: str, pos: str):
        super().__init__()
        self._entry_id = entry_id
        self._word = word
        self._translation = translation
        self._pos = pos

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Checkbox(label="", value=True, id=f"vocab-{self._entry_id}")
            yield Label(self._word, classes="word")
            yield Label(self._translation, classes="translation")
            yield Label(self._pos, classes="pos")


class ReviewScreen(Screen):
    """Screen 2: Review vocabulary, select card types, set deck name."""

    DEFAULT_CSS = """
    ReviewScreen {
        align: center middle;
    }
    ReviewScreen > Vertical {
        width: 80%;
        height: 90%;
        border: solid $accent;
        background: $surface;
        padding: 1 2;
    }
    ReviewScreen .title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
        color: $accent;
    }
    ReviewScreen .section-label {
        text-style: bold;
        margin-top: 1;
        margin-bottom: 0;
        color: $text;
    }
    ReviewScreen .card-types-row {
        height: 3;
        margin-bottom: 1;
    }
    ReviewScreen .vocab-header {
        height: 2;
        padding: 0 1;
        background: $surface-darken-1;
        margin-bottom: 0;
    }
    ReviewScreen .vocab-header Label {
        color: $text-muted;
        text-style: bold;
    }
    ReviewScreen .header-word { width: 18; margin-left: 4; }
    ReviewScreen .header-translation { width: 20; }
    ReviewScreen .header-pos { width: 12; }
    ReviewScreen .vocab-list {
        height: 1fr;
        border: solid $surface-darken-2;
    }
    ReviewScreen .error-msg {
        color: $error;
        display: none;
    }
    ReviewScreen .error-msg.-visible {
        display: block;
    }
    ReviewScreen .action-row {
        height: 3;
        margin-top: 1;
        align: right middle;
    }
    ReviewScreen .action-row Button {
        margin-left: 1;
    }
    ReviewScreen Input {
        margin-bottom: 1;
    }
    """

    BINDINGS = [("ctrl+a", "select_all", "Select All"), ("ctrl+d", "deselect_all", "Deselect All")]

    def __init__(self, cards: AutoAnkiCards):
        super().__init__()
        self._cards = cards

    def compose(self) -> ComposeResult:
        title = self._cards.source_info.title
        word_count = len(self._cards.vocabulary)

        with Vertical():
            yield Static("AutoAnki — Review", classes="title")

            yield Label("Deck Name", classes="section-label")
            yield Input(value=title, id="deck-name")

            yield Label("Card Types", classes="section-label")
            with Horizontal(classes="card-types-row"):
                yield Checkbox("Recognition", value=True, id="ct-1")
                yield Checkbox("Cloze", value=True, id="ct-2")
                yield Checkbox("Production", value=True, id="ct-3")
                yield Checkbox("Comprehension", value=True, id="ct-4")
                yield Checkbox("Listening", value=True, id="ct-5")

            yield Label(
                f"Vocabulary  ({word_count} words found)", classes="section-label"
            )

            with Horizontal(classes="vocab-header"):
                yield Label("", classes="header-word")
                yield Label("Word", classes="header-word")
                yield Label("Translation", classes="header-translation")
                yield Label("POS", classes="header-pos")

            with ScrollableContainer(classes="vocab-list"):
                for entry in self._cards.vocabulary:
                    yield VocabItem(
                        entry.id,
                        entry.target_word,
                        entry.english_translation,
                        entry.part_of_speech,
                    )

            yield Label("", id="review-error", classes="error-msg")

            with Horizontal(classes="action-row"):
                yield Button("Cancel", variant="default", id="btn-cancel")
                yield Button("Export Deck", variant="primary", id="btn-export")

    def action_select_all(self) -> None:
        for cb in self.query("Checkbox"):
            cb.value = True

    def action_deselect_all(self) -> None:
        for entry in self._cards.vocabulary:
            cb = self.query_one(f"#vocab-{entry.id}", Checkbox)
            cb.value = False

    @on(Button.Pressed, "#btn-cancel")
    def on_cancel(self) -> None:
        self.app.pop_screen()

    @on(Button.Pressed, "#btn-export")
    def on_export(self) -> None:
        deck_name = self.query_one("#deck-name", Input).value.strip()
        if not deck_name:
            self._show_error("Please enter a deck name.")
            return

        selected_card_types = set()
        for i in range(1, 6):
            if self.query_one(f"#ct-{i}", Checkbox).value:
                selected_card_types.add(i)

        if not selected_card_types:
            self._show_error("Select at least one card type.")
            return

        selected_word_ids = set()
        for entry in self._cards.vocabulary:
            cb = self.query_one(f"#vocab-{entry.id}", Checkbox)
            if cb.value:
                selected_word_ids.add(entry.id)

        if not selected_word_ids:
            self._show_error("Select at least one word.")
            return

        self._hide_error()
        self.app.push_screen(
            ExportScreen(
                cards=self._cards,
                deck_name=deck_name,
                selected_word_ids=selected_word_ids,
                selected_card_types=selected_card_types,
            )
        )

    def _show_error(self, msg: str) -> None:
        label = self.query_one("#review-error", Label)
        label.update(msg)
        label.add_class("-visible")

    def _hide_error(self) -> None:
        self.query_one("#review-error", Label).remove_class("-visible")


# ─── Screen 3: Export ────────────────────────────────────────────────────────


class ExportScreen(Screen):
    """Screen 3: Generate TTS audio and build the deck."""

    DEFAULT_CSS = """
    ExportScreen {
        align: center middle;
    }
    ExportScreen > Vertical {
        width: 60;
        height: auto;
        border: solid $accent;
        background: $surface;
        padding: 2 3;
    }
    ExportScreen .title {
        text-align: center;
        text-style: bold;
        margin-bottom: 2;
        color: $accent;
    }
    ExportScreen .status {
        margin-bottom: 1;
        text-align: center;
    }
    ExportScreen ProgressBar {
        margin-bottom: 1;
    }
    ExportScreen .result {
        display: none;
        text-align: center;
        margin-top: 1;
    }
    ExportScreen .result.-visible {
        display: block;
    }
    ExportScreen .result-path {
        color: $text-muted;
        text-style: italic;
        margin-bottom: 1;
    }
    ExportScreen .action-row {
        height: 3;
        margin-top: 1;
        align: center middle;
        display: none;
    }
    ExportScreen .action-row.-visible {
        display: block;
    }
    ExportScreen .action-row Button {
        margin: 0 1;
    }
    ExportScreen .error-msg {
        color: $error;
        display: none;
        margin-top: 1;
        text-align: center;
    }
    ExportScreen .error-msg.-visible {
        display: block;
    }
    """

    def __init__(
        self,
        cards: AutoAnkiCards,
        deck_name: str,
        selected_word_ids: set[str],
        selected_card_types: set[int],
    ):
        super().__init__()
        self._cards = cards
        self._deck_name = deck_name
        self._selected_word_ids = selected_word_ids
        self._selected_card_types = selected_card_types
        self._output_path: str = ""
        self._audio_dir: Path | None = None

    def compose(self) -> ComposeResult:
        selected_count = len(self._selected_word_ids)
        total_audio = selected_count * 6  # 6 audio files per word

        with Vertical():
            yield Static("AutoAnki — Exporting", classes="title")
            yield Label("Generating audio...", id="status-label", classes="status")
            yield ProgressBar(total=total_audio, show_eta=False, id="progress")

            yield Label("", id="result-label", classes="result")
            yield Label("", id="result-path", classes="result result-path")

            yield Label("", id="error-msg", classes="error-msg")

            with Horizontal(classes="action-row", id="action-row"):
                yield Button("Open Folder", variant="default", id="btn-open")
                yield Button("New Deck", variant="default", id="btn-new")
                yield Button("Quit", variant="error", id="btn-quit")

    def on_mount(self) -> None:
        self._run_export()

    @work(thread=True, exclusive=True)
    def _run_export(self) -> None:
        import os

        # Create temp dir for audio files
        tmp_dir = Path(tempfile.mkdtemp(prefix="autoanki_audio_"))
        self._audio_dir = tmp_dir

        # Build all audio queries for selected words
        all_queries: dict[str, str] = {}
        for entry in self._cards.vocabulary:
            if entry.id in self._selected_word_ids:
                all_queries.update(build_audio_queries(entry))

        total = len(all_queries)

        def on_progress(completed: int, total_count: int) -> None:
            self.app.call_from_thread(self._update_progress, completed, total_count)

        # Generate TTS
        audio_files = generate_audio_batch(
            queries=all_queries,
            output_dir=tmp_dir,
            progress_callback=on_progress,
        )

        # Build deck
        self.app.call_from_thread(
            self.query_one("#status-label", Label).update, "Building deck..."
        )

        # Determine output path
        safe_name = self._deck_name.replace(" ", "_").replace("/", "-")[:50]
        output_path = str(Path.cwd() / f"{safe_name}.apkg")
        self._output_path = output_path

        card_count = build_deck_with_audio(
            cards=self._cards,
            selected_word_ids=self._selected_word_ids,
            selected_card_types=self._selected_card_types,
            deck_name=self._deck_name,
            audio_files=audio_files,
            audio_dir=tmp_dir,
            output_path=output_path,
        )

        word_count = len(self._selected_word_ids)
        self.app.call_from_thread(self._export_done, card_count, word_count, output_path)

    def _update_progress(self, completed: int, total: int) -> None:
        self.query_one(ProgressBar).progress = completed

    def _export_done(self, card_count: int, word_count: int, output_path: str) -> None:
        self.query_one("#status-label", Label).update("Done!")

        result = self.query_one("#result-label", Label)
        result.update(f"✓ {card_count} cards from {word_count} words")
        result.add_class("-visible")

        path_label = self.query_one("#result-path", Label)
        path_label.update(f"Saved: {output_path}")
        path_label.add_class("-visible")

        self.query_one("#action-row").add_class("-visible")

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.state == WorkerState.ERROR:
            error = str(event.worker.error)
            self.query_one("#error-msg", Label).update(
                f"Export failed: {error}"
            )
            self.query_one("#error-msg", Label).add_class("-visible")
            self.query_one("#action-row").add_class("-visible")

    @on(Button.Pressed, "#btn-open")
    def open_folder(self) -> None:
        folder = str(Path(self._output_path).parent)
        try:
            import sys
            if sys.platform == "darwin":
                subprocess.run(["open", folder])
            elif sys.platform == "win32":
                subprocess.run(["explorer", folder])
            else:
                subprocess.run(["xdg-open", folder])
        except Exception:
            pass

    @on(Button.Pressed, "#btn-new")
    def new_deck(self) -> None:
        self.app.pop_screen()  # ExportScreen
        self.app.pop_screen()  # ReviewScreen
        # Back at InputScreen

    @on(Button.Pressed, "#btn-quit")
    def quit_app(self) -> None:
        self.app.exit()


# ─── Main App ────────────────────────────────────────────────────────────────


class AutoAnkiApp(App):
    TITLE = "AutoAnki"
    SUB_TITLE = "Vocabulary Deck Generator"

    CSS = """
    Screen {
        background: $background;
    }
    """

    def on_mount(self) -> None:
        self.push_screen(InputScreen())
