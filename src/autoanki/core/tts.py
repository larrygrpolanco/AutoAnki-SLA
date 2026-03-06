"""Text-to-speech generation using OpenAI TTS."""

from __future__ import annotations

import hashlib
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Generator

from openai import OpenAI

from autoanki.core.models import (
    AutoAnkiCards,
    CardTypeSelection,
    ProjectMeta,
    VocabEntry,
)

# Default voice for TTS
DEFAULT_VOICE = "alloy"

# Default delay between TTS requests (seconds)
DEFAULT_DELAY_SECONDS = 1.0

# Audio file extension
AUDIO_EXTENSION = ".mp3"


@dataclass
class AudioGenerationResult:
    """Result of audio generation batch."""

    generated: list[str]  # Successfully created file paths
    skipped: list[str]  # Already existed (not regenerated)
    failed: list[tuple[str, str]]  # (text, error_message) pairs
    total_requested: int

    @property
    def total_processed(self) -> int:
        """Total files processed (generated + skipped + failed)."""
        return len(self.generated) + len(self.skipped) + len(self.failed)

    @property
    def success_rate(self) -> float:
        """Percentage of successful generations (0.0 - 100.0)."""
        if self.total_requested == 0:
            return 100.0
        successful = len(self.generated) + len(self.skipped)
        return (successful / self.total_requested) * 100


class TTSClient:
    """Wrapper for OpenAI TTS API."""

    def __init__(
        self,
        api_key: str | None = None,
        voice: str = DEFAULT_VOICE,
        delay_seconds: float = DEFAULT_DELAY_SECONDS,
    ):
        """Initialize the TTS client.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            voice: Voice to use for TTS (default: "alloy")
            delay_seconds: Delay between API calls in seconds (default: 1.0)

        Raises:
            ValueError: If no API key is provided or found in environment
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.voice = voice
        self.delay_seconds = delay_seconds
        self.client = OpenAI(api_key=self.api_key)

    def generate_audio(self, text: str) -> bytes:
        """Generate audio for a single text string.

        Args:
            text: Clean target-language text to synthesize

        Returns:
            Audio data as bytes (MP3 format)

        Raises:
            TTSError: If the API call fails
        """
        try:
            response = self.client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice=self.voice,  # type: ignore
                input=text,
            )
            return response.content
        except Exception as e:
            raise TTSError(f"TTS generation failed for text '{text[:50]}...': {e}") from e

    def generate_audio_to_file(
        self,
        text: str,
        output_path: Path,
    ) -> bool:
        """Generate audio and save to file.

        Args:
            text: Clean target-language text to synthesize
            output_path: Path where to save the MP3 file

        Returns:
            True if successful, False if failed

        Raises:
            TTSError: If the API call fails
        """
        audio_data = self.generate_audio(text)
        output_path.write_bytes(audio_data)
        return True

    def delay(self) -> None:
        """Wait for the configured delay period."""
        if self.delay_seconds > 0:
            time.sleep(self.delay_seconds)


class TTSError(Exception):
    """Error during TTS generation."""

    pass


def get_audio_hash(text: str) -> str:
    """Generate MD5 hash for audio filename.

    Creates a content-addressable filename: {hash[:12]}.mp3
    This provides natural deduplication and resume support.

    Args:
        text: Clean target-language text

    Returns:
        12-character hex hash string
    """
    hash_bytes = hashlib.md5(text.encode("utf-8")).digest()
    return hash_bytes.hex()[:12]


def get_audio_filename(text: str) -> str:
    """Get the audio filename for a text string.

    Args:
        text: Clean target-language text

    Returns:
        Filename like "a1b2c3d4e5f6.mp3"
    """
    return f"{get_audio_hash(text)}{AUDIO_EXTENSION}"


def should_generate_isolated_word_audio(card_types: CardTypeSelection) -> bool:
    """Check if isolated word audio should be generated.

    Isolated word audio is used by Cards 1, 3, and 5 (back side).
    It should be generated if ANY of these card types are enabled.

    Args:
        card_types: Card type selection from project meta

    Returns:
        True if isolated word audio should be generated
    """
    return any(
        [
            card_types.card_1_recognition,
            card_types.card_3_production,
            card_types.card_5_listening,
        ]
    )


def should_generate_sentence_audio(
    sentence_num: int,
    card_types: CardTypeSelection,
) -> bool:
    """Check if a specific sentence's audio should be generated.

    Args:
        sentence_num: Sentence number (1-5, corresponding to card type)
        card_types: Card type selection from project meta

    Returns:
        True if this sentence's audio should be generated
    """
    mapping = {
        1: card_types.card_1_recognition,
        2: card_types.card_2_cloze,
        3: card_types.card_3_production,
        4: card_types.card_4_comprehension,
        5: card_types.card_5_listening,
    }
    return mapping.get(sentence_num, False)


def get_required_audio_files(
    vocab_entry: VocabEntry,
    card_types: CardTypeSelection,
) -> list[tuple[str, str]]:
    """Get list of audio files needed for a vocabulary entry.

    Returns list of (audio_query_text, field_name) tuples.

    Args:
        vocab_entry: The vocabulary entry
        card_types: Card type selection

    Returns:
        List of (text, field_name) tuples for audio generation
    """
    files = []
    queries = vocab_entry.audio_queries

    # Isolated word audio (used by Cards 1, 3, 5)
    if should_generate_isolated_word_audio(card_types):
        files.append((queries.word_isolated, "word_isolated"))

    # Sentence audio (1-5)
    for i in range(1, 6):
        if should_generate_sentence_audio(i, card_types):
            sentence_attr = f"sentence_{i}"
            sentence_text = getattr(queries, sentence_attr)
            files.append((sentence_text, sentence_attr))

    return files


def generate_audio_batch(
    cards: AutoAnkiCards,
    project_meta: ProjectMeta,
    project_path: Path,
    api_key: str | None = None,
    voice: str = DEFAULT_VOICE,
    delay_seconds: float = DEFAULT_DELAY_SECONDS,
) -> Generator[dict, None, AudioGenerationResult]:
    """Generate all audio files for a project with progress updates.

    This is a generator that yields progress updates and returns the final
    result. It's designed for TUI integration where you can show real-time
    progress.

    Yields dict with keys:
        - status: "generating", "skipped", "failed", "complete"
        - current: int (current file number)
        - total: int (total files to process)
        - text: str (text being processed, truncated)
        - filename: str (audio filename)
        - error: str (only on failure)

    Args:
        cards: The card data containing vocabulary entries
        project_meta: Project metadata with audio toggles
        project_path: Path to the project directory
        api_key: Optional OpenAI API key
        voice: Voice to use (default: "alloy")
        delay_seconds: Delay between requests (default: 1.0)

    Returns:
        AudioGenerationResult with final summary

    Example:
        >>> for update in generate_audio_batch(cards, meta, path):
        ...     print(f"{update['current']}/{update['total']}: {update['status']}")
        >>> result = generate_audio_batch(cards, meta, path)  # Get final result
    """
    # Check project-level audio toggle
    if not project_meta.generate_audio:
        yield {
            "status": "complete",
            "current": 0,
            "total": 0,
            "message": "Audio generation disabled at project level",
        }
        return AudioGenerationResult(generated=[], skipped=[], failed=[], total_requested=0)

    # Initialize TTS client
    client = TTSClient(api_key=api_key, voice=voice, delay_seconds=0)  # Delay handled manually

    # Build list of all required audio files
    audio_tasks = []  # List of (text, filename, word_id, field_name)

    for vocab_entry in cards.vocabulary:
        # Check per-word audio toggle
        if not vocab_entry.generate_audio:
            continue

        # Get required audio files for this word
        required = get_required_audio_files(vocab_entry, project_meta.card_types)

        for text, field_name in required:
            filename = get_audio_filename(text)
            audio_tasks.append((text, filename, str(vocab_entry.id), field_name))

    # Deduplicate by filename (same text = same file)
    seen_filenames = set()
    unique_tasks = []
    for text, filename, word_id, field_name in audio_tasks:
        if filename not in seen_filenames:
            seen_filenames.add(filename)
            unique_tasks.append((text, filename, word_id, field_name))

    total = len(unique_tasks)

    if total == 0:
        yield {
            "status": "complete",
            "current": 0,
            "total": 0,
            "message": "No audio files to generate",
        }
        return AudioGenerationResult(generated=[], skipped=[], failed=[], total_requested=0)

    # Setup audio directory
    audio_dir = project_path / "audio"
    audio_dir.mkdir(exist_ok=True)

    # Track results
    generated = []
    skipped = []
    failed = []

    # Process each audio file
    for i, (text, filename, word_id, field_name) in enumerate(unique_tasks, 1):
        output_path = audio_dir / filename

        # Check if file already exists (resume support)
        if output_path.exists():
            skipped.append(str(output_path))
            yield {
                "status": "skipped",
                "current": i,
                "total": total,
                "text": text[:50] + "..." if len(text) > 50 else text,
                "filename": filename,
                "word_id": word_id,
                "field_name": field_name,
            }
            continue

        # Generate audio
        try:
            client.generate_audio_to_file(text, output_path)
            generated.append(str(output_path))
            yield {
                "status": "generating",
                "current": i,
                "total": total,
                "text": text[:50] + "..." if len(text) > 50 else text,
                "filename": filename,
                "word_id": word_id,
                "field_name": field_name,
            }

            # Apply delay between requests (but not after the last one)
            if i < total:
                client.delay()

        except TTSError as e:
            failed.append((text, str(e)))
            yield {
                "status": "failed",
                "current": i,
                "total": total,
                "text": text[:50] + "..." if len(text) > 50 else text,
                "filename": filename,
                "word_id": word_id,
                "field_name": field_name,
                "error": str(e),
            }

            # Still apply delay after failures to be nice to the API
            if i < total:
                client.delay()

    # Final completion update
    yield {
        "status": "complete",
        "current": total,
        "total": total,
        "message": f"Audio generation complete: {len(generated)} generated, {len(skipped)} skipped, {len(failed)} failed",
    }

    return AudioGenerationResult(
        generated=generated,
        skipped=skipped,
        failed=failed,
        total_requested=total,
    )


def get_audio_path(project_path: Path, text: str) -> Path:
    """Get the full path for an audio file.

    Args:
        project_path: Path to the project directory
        text: The text that was synthesized

    Returns:
        Full path to the audio file
    """
    filename = get_audio_filename(text)
    return project_path / "audio" / filename


def check_audio_exists(project_path: Path, text: str) -> bool:
    """Check if audio file already exists.

    Args:
        project_path: Path to the project directory
        text: The text that would be synthesized

    Returns:
        True if the audio file already exists
    """
    audio_path = get_audio_path(project_path, text)
    return audio_path.exists()


def get_audio_stats(project_path: Path) -> dict[str, int | float]:
    """Get statistics about audio files in a project.

    Args:
        project_path: Path to the project directory

    Returns:
        Dictionary with file count and total size
    """
    audio_dir = project_path / "audio"

    if not audio_dir.exists():
        return {"file_count": 0, "total_size_bytes": 0, "total_size_mb": 0.0}

    files = list(audio_dir.glob(f"*{AUDIO_EXTENSION}"))
    total_size = sum(f.stat().st_size for f in files)

    return {
        "file_count": len(files),
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / (1024 * 1024), 2),
    }
