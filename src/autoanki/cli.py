"""
AutoAnki CLI — Rich + questionary based interface.
Sequential flow: select file → LLM pipeline → pick words → pick card types → export.
"""

import os
import sys
import tempfile
from pathlib import Path

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn
from rich.table import Table
from rich.text import Text

from .deck_builder import build_deck_with_audio
from .llm import run_pipeline
from .models import AutoAnkiCards
from .parser import MAX_CHARS, count_chars, extract_text, parse_past_vocab
from .tts import build_audio_queries, generate_audio_batch

console = Console()

CARD_TYPE_NAMES = {
    1: "Recognition    — See the word, recall its meaning",
    2: "Fill in Blank  — Gapped sentence, recall the target word",
    3: "Production     — See English meaning, produce the target word",
    4: "Comprehension  — Read a sentence, understand how the word is used",
    5: "Listening      — Hear a sentence, understand and identify the word",
}

STEP_LABELS = {
    "Step 1/3: Drafting cards...": "[1/3] Drafting vocabulary cards",
    "Step 2/3: Reviewing card quality...": "[2/3] Reviewing card quality",
    "Step 3/3: Structuring output...": "[3/3] Structuring output as JSON",
    "Step 3/3: Retrying structuring...": "[3/3] Retrying JSON structuring",
}


def run() -> None:
    """Main entry point — orchestrates the full CLI flow."""
    _show_welcome()
    language = _get_target_language()
    source_path = _select_lesson_file()
    past_vocab = _select_past_vocab()
    cards = _run_llm_pipeline(source_path, past_vocab, language)
    selected_ids = _select_vocabulary(cards)
    selected_types = _select_card_types()
    deck_name = _confirm_deck_name(cards)
    _export_deck(cards, selected_ids, selected_types, deck_name, language)


# ---------------------------------------------------------------------------
# Step 1: Welcome
# ---------------------------------------------------------------------------

def _show_welcome() -> None:
    console.print()
    console.print(
        Panel(
            Text("AutoAnki", justify="center", style="bold cyan")
            .__add__(Text("\nVocabulary Deck Generator", justify="center", style="cyan")),
            subtitle="[dim]PDF / TXT  →  LLM pipeline  →  Anki deck with TTS audio[/dim]",
            border_style="cyan",
            padding=(1, 6),
        )
    )
    console.print()


# ---------------------------------------------------------------------------
# Language selection
# ---------------------------------------------------------------------------

def _get_target_language() -> str:
    """Return the target language from .env or prompt the user."""
    lang = os.getenv("TARGET_LANGUAGE", "").strip()
    if lang:
        console.print(f"[dim]  Language: {lang} (from .env)[/dim]\n")
        return lang

    lang = questionary.text(
        "What language are you studying? (e.g. Korean, Spanish, Japanese):",
        validate=lambda x: True if x.strip() else "Please enter a language.",
    ).ask()

    if not lang:
        sys.exit(0)

    console.print()
    return lang.strip()


# ---------------------------------------------------------------------------
# Step 2: Lesson file selection
# ---------------------------------------------------------------------------

def _scan_folder(folder: Path, extensions: tuple[str, ...]) -> list[Path]:
    if not folder.exists():
        return []
    return sorted(
        f for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in extensions
    )


def _select_lesson_file() -> str:
    lessons_dir = Path.cwd() / "Lessons"
    files = _scan_folder(lessons_dir, (".pdf", ".txt"))

    console.print("[bold]Step 1 — Select Lesson File[/bold]")

    if not files:
        console.print(
            "[yellow]  Lessons/ folder is empty or missing. Enter a file path manually.[/yellow]"
        )
        path = questionary.path(
            "Source file path:",
            validate=lambda p: Path(p).exists() or "File not found",
        ).ask()
        if not path:
            sys.exit(0)
        return _validate_lesson_file(path)

    # Show table of available files
    table = Table(show_header=True, header_style="bold dim", box=None, padding=(0, 2))
    table.add_column("File", style="cyan")
    table.add_column("Size", justify="right", style="dim")

    for f in files:
        size_kb = f.stat().st_size // 1024 or 1
        table.add_row(f.name, f"{size_kb} KB")

    console.print(table)
    console.print()

    choices = [
        questionary.Choice(title=f.name, value=str(f))
        for f in files
    ]
    selected = questionary.select(
        "Select a lesson file:",
        choices=choices,
    ).ask()

    if not selected:
        sys.exit(0)

    return _validate_lesson_file(selected)


def _validate_lesson_file(path: str) -> str:
    try:
        text = extract_text(path)
        n = count_chars(text)
    except Exception as e:
        console.print(f"[red]  Could not read file: {e}[/red]")
        sys.exit(1)

    if n > MAX_CHARS:
        console.print(
            f"[red]  File has {n:,} characters — exceeds the {MAX_CHARS:,} character limit.[/red]"
        )
        sys.exit(1)

    console.print(f"[dim]  {n:,} characters[/dim]\n")
    return path


# ---------------------------------------------------------------------------
# Step 3: Past vocabulary (optional)
# ---------------------------------------------------------------------------

def _select_past_vocab() -> list[str]:
    vocab_dir = Path.cwd() / "PreviousVocab"
    files = _scan_folder(vocab_dir, (".txt",))

    if not files:
        return []

    console.print("[bold]Step 2 — Previous Vocabulary (optional)[/bold]")

    choices = [questionary.Choice(title="Skip — no past vocabulary", value=None)]
    choices += [questionary.Choice(title=f.name, value=str(f)) for f in files]

    selected = questionary.select(
        "Select a previous vocabulary file:",
        choices=choices,
    ).ask()

    if selected is None:
        console.print("[dim]  Skipping past vocabulary.[/dim]\n")
        return []

    try:
        words = parse_past_vocab(selected)
        console.print(f"[dim]  Loaded {len(words)} past vocabulary words.[/dim]\n")
        return words
    except Exception as e:
        console.print(f"[yellow]  Could not read vocab file ({e}) — proceeding without it.[/yellow]\n")
        return []


# ---------------------------------------------------------------------------
# Step 4: LLM pipeline
# ---------------------------------------------------------------------------

def _run_llm_pipeline(source_path: str, past_vocab: list[str], language: str = "") -> AutoAnkiCards:
    console.print("[bold]Step 3 — Generating Flashcards[/bold]")
    console.print("[dim]  This usually takes 1–3 minutes.[/dim]\n")

    text = extract_text(source_path)
    cards: AutoAnkiCards | None = None

    with console.status(
        "[bold cyan]  [1/3] Drafting vocabulary cards...", spinner="dots"
    ) as status:

        def progress_callback(msg: str) -> None:
            label = STEP_LABELS.get(msg, msg)
            status.update(f"[bold cyan]  {label}...")

        try:
            cards = run_pipeline(text, past_vocab, progress_callback=progress_callback, language=language)
        except Exception as e:
            console.print(f"\n[red]  Pipeline failed: {e}[/red]")
            sys.exit(1)

    console.print("  [green]✓[/green] [dim][1/3] Drafting          done[/dim]")
    console.print("  [green]✓[/green] [dim][2/3] Quality review     done[/dim]")
    console.print("  [green]✓[/green] [dim][3/3] JSON structuring   done[/dim]")
    console.print(f"\n  Found [bold]{len(cards.vocabulary)}[/bold] vocabulary words.\n")

    return cards


# ---------------------------------------------------------------------------
# Step 5: Vocabulary selection
# ---------------------------------------------------------------------------

def _select_vocabulary(cards: AutoAnkiCards) -> set[str]:
    console.print("[bold]Step 4 — Select Vocabulary Words[/bold]")
    console.print("[dim]  Space to toggle · Enter to confirm · All selected by default.[/dim]\n")

    choices = [
        questionary.Choice(
            title=f"{entry.target_word}  |  {entry.english_translation}  |  {entry.part_of_speech}",
            value=entry.id,
            checked=True,
        )
        for entry in cards.vocabulary
    ]

    selected_ids = questionary.checkbox(
        "Choose words to include:",
        choices=choices,
        validate=lambda x: True if x else "Select at least one word.",
    ).ask()

    if not selected_ids:
        console.print("[yellow]  No words selected. Exiting.[/yellow]")
        sys.exit(0)

    console.print(
        f"\n  [dim]{len(selected_ids)} of {len(cards.vocabulary)} words selected.[/dim]\n"
    )
    return set(selected_ids)


# ---------------------------------------------------------------------------
# Step 6: Card type selection
# ---------------------------------------------------------------------------

def _select_card_types() -> set[int]:
    console.print("[bold]Step 5 — Select Card Types[/bold]")
    console.print("[dim]  Space to toggle · Enter to confirm · All selected by default.[/dim]\n")

    choices = [
        questionary.Choice(title=label, value=num, checked=True)
        for num, label in CARD_TYPE_NAMES.items()
    ]

    selected = questionary.checkbox(
        "Choose card types to generate:",
        choices=choices,
        validate=lambda x: True if x else "Select at least one card type.",
    ).ask()

    if not selected:
        console.print("[yellow]  No card types selected. Exiting.[/yellow]")
        sys.exit(0)

    console.print(f"\n  [dim]{len(selected)} card type(s) selected.[/dim]\n")
    return set(selected)


# ---------------------------------------------------------------------------
# Step 7: Deck name
# ---------------------------------------------------------------------------

def _confirm_deck_name(cards: AutoAnkiCards) -> str:
    name = questionary.text(
        "Deck name:",
        default=cards.source_info.title,
        validate=lambda x: True if x.strip() else "Deck name cannot be empty.",
    ).ask()

    if not name:
        sys.exit(0)

    console.print()
    return name.strip()


# ---------------------------------------------------------------------------
# Step 8: Export (TTS + deck build)
# ---------------------------------------------------------------------------

def _export_deck(
    cards: AutoAnkiCards,
    selected_word_ids: set[str],
    selected_card_types: set[int],
    deck_name: str,
    language: str = "",
) -> None:
    console.print("[bold]Step 6 — Exporting Deck[/bold]\n")

    # Collect audio queries for selected words only
    all_queries: dict[str, str] = {}
    for entry in cards.vocabulary:
        if entry.id in selected_word_ids:
            all_queries.update(build_audio_queries(entry))

    total_audio = len(all_queries)
    tmp_dir = Path(tempfile.mkdtemp(prefix="autoanki_audio_"))
    audio_files: dict[str, str] = {}

    tts_instructions = ""
    if language:
        tts_instructions = (
            f"Speak naturally in {language} with a clear, native {language} accent "
            f"and pronunciation. Use a calm, measured pace suitable for language learners."
        )

    # TTS generation with progress bar
    with Progress(
        SpinnerColumn(),
        TextColumn("  [progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("[dim]{task.completed}/{task.total}[/dim]"),
        console=console,
        transient=False,
    ) as progress:
        task = progress.add_task("[cyan]Generating TTS audio...", total=total_audio)

        def on_audio_progress(completed: int, total: int) -> None:
            progress.update(task, completed=completed)

        try:
            audio_files = generate_audio_batch(
                queries=all_queries,
                output_dir=tmp_dir,
                progress_callback=on_audio_progress,
                instructions=tts_instructions,
            )
        except Exception as e:
            console.print(f"[red]  TTS generation failed: {e}[/red]")
            sys.exit(1)

    # Build deck
    console.print("  [dim]Building Anki deck...[/dim]")

    output_dir = Path.cwd() / "Output"
    output_dir.mkdir(exist_ok=True)

    safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in deck_name).strip()
    safe_name = safe_name.replace(" ", "_")[:60] or "AutoAnki_Deck"
    output_path = str(output_dir / f"{safe_name}.apkg")

    try:
        card_count = build_deck_with_audio(
            cards=cards,
            selected_word_ids=selected_word_ids,
            selected_card_types=selected_card_types,
            deck_name=deck_name,
            audio_files=audio_files,
            audio_dir=tmp_dir,
            output_path=output_path,
        )
    except Exception as e:
        console.print(f"[red]  Deck build failed: {e}[/red]")
        sys.exit(1)

    # Success summary
    word_count = len(selected_word_ids)

    summary = Table.grid(padding=(0, 3))
    summary.add_column(style="dim")
    summary.add_column(style="bold")
    summary.add_row("Words", str(word_count))
    summary.add_row("Cards", str(card_count))
    summary.add_row("Card types", str(len(selected_card_types)))
    summary.add_row("Output", output_path)

    console.print()
    console.print(
        Panel(
            summary,
            title="[bold green]✓  Deck Created Successfully[/bold green]",
            border_style="green",
            padding=(1, 3),
        )
    )
    console.print(
        "\n[dim]  Open Anki → File → Import to load your new deck.[/dim]\n"
    )
