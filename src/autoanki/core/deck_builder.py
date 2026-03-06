"""Anki deck building using genanki."""

from __future__ import annotations

import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

import genanki

from autoanki.core.models import (
    AutoAnkiCards,
    CardTypeSelection,
    ProjectMeta,
    VocabEntry,
)
from autoanki.core.project import get_project_path, load_cards, load_project_meta
from autoanki.core.tts import get_audio_filename, should_generate_isolated_word_audio
from autoanki.templates.anki_models import create_note_model, get_model


def generate_deck_id(deck_name: str) -> int:
    """Generate stable deck ID from deck name.

    Uses MD5 hash of deck name, truncated to fit in signed 32-bit int.
    This ensures the same deck name always produces the same ID.

    Args:
        deck_name: Name of the deck

    Returns:
        32-bit integer deck ID
    """
    hash_bytes = hashlib.md5(deck_name.encode("utf-8")).digest()
    # Take first 4 bytes and convert to int, ensuring positive value
    deck_id = int.from_bytes(hash_bytes[:4], byteorder="big", signed=False)
    # Ensure it fits in signed 32-bit range that Anki expects
    return deck_id % (2**31)


def generate_note_guid(vocab_id: UUID) -> int:
    """Generate stable note GUID from vocabulary entry ID.

    Args:
        vocab_id: The vocabulary entry UUID

    Returns:
        32-bit integer note GUID
    """
    hash_bytes = hashlib.md5(str(vocab_id).encode("utf-8")).digest()
    guid = int.from_bytes(hash_bytes[:4], byteorder="big", signed=False)
    return guid % (2**31)


def build_audio_field(text: str, project_path: Path) -> str:
    """Build the audio field content for a text string.

    Returns [sound:filename.mp3] if audio file exists, empty string otherwise.

    Args:
        text: The text that was synthesized
        project_path: Path to the project directory

    Returns:
        Audio field content (e.g., "[sound:a1b2c3d4e5f6.mp3]") or ""
    """
    if not text:
        return ""

    filename = get_audio_filename(text)
    audio_path = project_path / "audio" / filename

    if audio_path.exists():
        return f"[sound:{filename}]"
    return ""


def build_note_fields(
    vocab_entry: VocabEntry,
    card_types: CardTypeSelection,
    project_path: Path,
) -> dict[str, str]:
    """Build all 24 field values for a vocabulary entry.

    Args:
        vocab_entry: The vocabulary entry
        card_types: Which card types are enabled
        project_path: Path to project directory (for checking audio files)

    Returns:
        Dictionary mapping field names to values
    """
    fields: dict[str, str] = {}

    # Basic word info (always included)
    fields["TargetWord"] = vocab_entry.target_word
    fields["EnglishTranslation"] = vocab_entry.english_translation
    fields["PartOfSpeech"] = vocab_entry.part_of_speech

    # Card 1: Recognition
    if card_types.card_1_recognition:
        card1 = vocab_entry.card_1_recognition
        fields["Sentence1"] = card1.sentence_target_highlight
        fields["Sentence1English"] = card1.sentence_english
        fields["AudioSentence1"] = build_audio_field(
            vocab_entry.audio_queries.sentence_1, project_path
        )
    else:
        fields["Sentence1"] = ""
        fields["Sentence1English"] = ""
        fields["AudioSentence1"] = ""

    # Card 2: Cloze
    if card_types.card_2_cloze:
        card2 = vocab_entry.card_2_cloze
        fields["Sentence2Cloze"] = card2.sentence_cloze
        fields["Sentence2English"] = card2.sentence_english
        fields["ClozeHint"] = card2.english_hint
        fields["AudioSentence2"] = build_audio_field(
            vocab_entry.audio_queries.sentence_2, project_path
        )
    else:
        fields["Sentence2Cloze"] = ""
        fields["Sentence2English"] = ""
        fields["ClozeHint"] = ""
        fields["AudioSentence2"] = ""

    # Card 3: Production
    if card_types.card_3_production:
        card3 = vocab_entry.card_3_production
        fields["Sentence3"] = card3.sentence_target
        fields["Sentence3English"] = card3.sentence_english
        fields["AudioSentence3"] = build_audio_field(
            vocab_entry.audio_queries.sentence_3, project_path
        )
    else:
        fields["Sentence3"] = ""
        fields["Sentence3English"] = ""
        fields["AudioSentence3"] = ""

    # Card 4: Comprehension
    if card_types.card_4_comprehension:
        card4 = vocab_entry.card_4_comprehension
        fields["Sentence4"] = card4.sentence_target
        fields["Sentence4Highlight"] = card4.word_in_sentence_highlight
        fields["Sentence4English"] = card4.sentence_english
        fields["Sentence4WordContext"] = card4.word_translation_in_context
        fields["AudioSentence4"] = build_audio_field(
            vocab_entry.audio_queries.sentence_4, project_path
        )
    else:
        fields["Sentence4"] = ""
        fields["Sentence4Highlight"] = ""
        fields["Sentence4English"] = ""
        fields["Sentence4WordContext"] = ""
        fields["AudioSentence4"] = ""

    # Card 5: Listening
    if card_types.card_5_listening:
        card5 = vocab_entry.card_5_listening
        fields["Sentence5"] = card5.sentence_target
        fields["Sentence5Highlight"] = card5.word_in_sentence_highlight
        fields["Sentence5English"] = card5.sentence_english
        fields["Sentence5WordContext"] = card5.word_translation_in_context
        fields["AudioSentence5"] = build_audio_field(
            vocab_entry.audio_queries.sentence_5, project_path
        )
    else:
        fields["Sentence5"] = ""
        fields["Sentence5Highlight"] = ""
        fields["Sentence5English"] = ""
        fields["Sentence5WordContext"] = ""
        fields["AudioSentence5"] = ""

    # Isolated word audio (used by Cards 1, 3, 5)
    if should_generate_isolated_word_audio(card_types):
        fields["AudioWord"] = build_audio_field(
            vocab_entry.audio_queries.word_isolated, project_path
        )
    else:
        fields["AudioWord"] = ""

    return fields


def has_any_enabled_card(vocab_entry: VocabEntry, card_types: CardTypeSelection) -> bool:
    """Check if a vocabulary entry has any enabled card types.

    Args:
        vocab_entry: The vocabulary entry (not used but kept for consistency)
        card_types: Card type selection

    Returns:
        True if at least one card type is enabled
    """
    return any(
        [
            card_types.card_1_recognition,
            card_types.card_2_cloze,
            card_types.card_3_production,
            card_types.card_4_comprehension,
            card_types.card_5_listening,
        ]
    )


def build_note(
    vocab_entry: VocabEntry,
    card_types: CardTypeSelection,
    project_path: Path,
) -> genanki.Note | None:
    """Build a single genanki note from a vocabulary entry.

    Args:
        vocab_entry: The vocabulary entry
        card_types: Which card types to include
        project_path: Path to project directory

    Returns:
        genanki.Note or None if no cards enabled for this word
    """
    # Check if any cards are enabled
    if not has_any_enabled_card(vocab_entry, card_types):
        return None

    # Build field values
    fields = build_note_fields(vocab_entry, card_types, project_path)

    # Create field list in correct order
    field_list = [
        fields["TargetWord"],
        fields["EnglishTranslation"],
        fields["PartOfSpeech"],
        fields["Sentence1"],
        fields["Sentence1English"],
        fields["Sentence2Cloze"],
        fields["Sentence2English"],
        fields["ClozeHint"],
        fields["Sentence3"],
        fields["Sentence3English"],
        fields["Sentence4"],
        fields["Sentence4Highlight"],
        fields["Sentence4English"],
        fields["Sentence4WordContext"],
        fields["Sentence5"],
        fields["Sentence5Highlight"],
        fields["Sentence5English"],
        fields["Sentence5WordContext"],
        fields["AudioWord"],
        fields["AudioSentence1"],
        fields["AudioSentence2"],
        fields["AudioSentence3"],
        fields["AudioSentence4"],
        fields["AudioSentence5"],
    ]

    # Generate stable GUID
    note_guid = generate_note_guid(vocab_entry.id)

    return genanki.Note(
        model=get_model(),
        fields=field_list,
        guid=note_guid,
    )


def collect_media_files(
    cards: AutoAnkiCards,
    card_types: CardTypeSelection,
    project_path: Path,
) -> list[str]:
    """Collect all audio file paths that exist and are needed.

    Args:
        cards: The card data
        card_types: Which card types are enabled
        project_path: Path to project directory

    Returns:
        List of audio file paths to include in the package
    """
    media_files = []
    audio_dir = project_path / "audio"

    if not audio_dir.exists():
        return media_files

    for vocab_entry in cards.vocabulary:
        queries = vocab_entry.audio_queries

        # Check isolated word audio
        if should_generate_isolated_word_audio(card_types):
            filename = get_audio_filename(queries.word_isolated)
            audio_path = audio_dir / filename
            if audio_path.exists():
                media_files.append(str(audio_path))

        # Check sentence audio
        for i in range(1, 6):
            sentence_attr = f"sentence_{i}"
            sentence_text = getattr(queries, sentence_attr)

            # Check if this card type is enabled
            if i == 1 and not card_types.card_1_recognition:
                continue
            if i == 2 and not card_types.card_2_cloze:
                continue
            if i == 3 and not card_types.card_3_production:
                continue
            if i == 4 and not card_types.card_4_comprehension:
                continue
            if i == 5 and not card_types.card_5_listening:
                continue

            filename = get_audio_filename(sentence_text)
            audio_path = audio_dir / filename
            if audio_path.exists():
                media_files.append(str(audio_path))

    return media_files


def build_deck(
    cards: AutoAnkiCards,
    project_meta: ProjectMeta,
    project_path: Path,
) -> genanki.Deck:
    """Build complete genanki deck with all notes.

    Args:
        cards: The card data
        project_meta: Project metadata
        project_path: Path to project directory

    Returns:
        genanki.Deck ready for export

    Raises:
        DeckBuilderError: If no cards can be built
    """
    # Generate deck ID from name
    deck_id = generate_deck_id(project_meta.deck_name)

    # Create deck
    deck = genanki.Deck(
        deck_id=deck_id,
        name=project_meta.deck_name,
        description=f"Auto-generated deck for {project_meta.source_filename}",
    )

    # Build notes
    notes_added = 0
    for vocab_entry in cards.vocabulary:
        note = build_note(
            vocab_entry,
            project_meta.card_types,
            project_path,
        )
        if note:
            deck.add_note(note)
            notes_added += 1

    if notes_added == 0:
        raise DeckBuilderError("No cards could be built (check card type selection)")

    return deck


def export_deck(
    deck: genanki.Deck,
    media_files: list[str],
    output_path: Path,
) -> None:
    """Export deck and media to .apkg file.

    Args:
        deck: The genanki deck
        media_files: List of audio file paths to include
        output_path: Where to save the .apkg file

    Raises:
        DeckBuilderError: If export fails
    """
    try:
        package = genanki.Package(deck)
        package.media_files = media_files
        package.write_to_file(str(output_path))
    except Exception as e:
        raise DeckBuilderError(f"Failed to export deck: {e}") from e


def build_and_export(
    project_name: str,
    output_filename: str | None = None,
) -> Path:
    """Complete workflow: load project, build deck, export to .apkg.

    This is the main entry point for deck generation.

    Args:
        project_name: Name of the project
        output_filename: Optional custom filename (default: {deck_name}_{timestamp}.apkg)

    Returns:
        Path to the exported .apkg file

    Raises:
        DeckBuilderError: If deck building or export fails
        FileNotFoundError: If project or cards not found
    """
    # Load project data
    project_path = get_project_path(project_name)
    meta = load_project_meta(project_name)
    cards = load_cards(project_name)

    if cards is None:
        raise FileNotFoundError(f"No cards.json found for project '{project_name}'")

    # Build deck
    deck = build_deck(cards, meta, project_path)

    # Collect media files
    media_files = collect_media_files(cards, meta.card_types, project_path)

    # Determine output filename
    if output_filename is None:
        # Create unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_deck_name = "".join(c if c.isalnum() else "_" for c in meta.deck_name)
        output_filename = f"{safe_deck_name}_{timestamp}.apkg"

    # Ensure .apkg extension
    if not output_filename.endswith(".apkg"):
        output_filename += ".apkg"

    # Output path
    output_dir = project_path / "output"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / output_filename

    # Export
    export_deck(deck, media_files, output_path)

    return output_path


class DeckBuilderError(Exception):
    """Error during deck building or export."""

    pass
