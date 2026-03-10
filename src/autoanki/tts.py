import hashlib
import time
from pathlib import Path
from typing import Callable

from openai import OpenAI

from .models import VocabEntry


def _hash_text(text: str) -> str:
    """Generate a 12-char MD5 hash for content-based filename dedup."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:12]


def build_audio_queries(entry: VocabEntry) -> dict[str, str]:
    """
    Return a dict of audio query key → text to speak.
    Keys: "{id}_word", "{id}_s1" through "{id}_s5"
    """
    aq = entry.audio_queries
    return {
        f"{entry.id}_word": aq.word_isolated,
        f"{entry.id}_s1": aq.sentence_1,
        f"{entry.id}_s2": aq.sentence_2,
        f"{entry.id}_s3": aq.sentence_3,
        f"{entry.id}_s4": aq.sentence_4,
        f"{entry.id}_s5": aq.sentence_5,
    }


def generate_audio_batch(
    queries: dict[str, str],
    output_dir: Path,
    progress_callback: Callable[[int, int], None] | None = None,
    tts_model: str = "gpt-4o-mini-tts",
    voice: str = "coral",
    delay: float = 1.0,
    instructions: str = "",
) -> dict[str, str]:
    """
    Generate TTS audio for a batch of text queries.

    queries: dict of key → text_to_speak
    output_dir: directory to save .mp3 files
    instructions: optional TTS instructions (e.g. accent/tone guidance for gpt-4o-mini-tts)

    Returns dict of key → filename (basename only, e.g. "abc123def456.mp3").
    Empty string means generation failed for that entry.
    Skips files that already exist (content-hash dedup).
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    client = OpenAI()
    results: dict[str, str] = {}
    total = len(queries)
    skipped = 0

    for i, (key, text) in enumerate(queries.items()):
        if not text.strip():
            results[key] = ""
            if progress_callback:
                progress_callback(i + 1, total)
            continue

        filename = _hash_text(text) + ".mp3"
        filepath = output_dir / filename

        if filepath.exists():
            # Already cached — no API call needed
            results[key] = filename
            skipped += 1
        else:
            try:
                kwargs = dict(model=tts_model, voice=voice, input=text)
                if instructions:
                    kwargs["instructions"] = instructions
                response = client.audio.speech.create(**kwargs)
                response.stream_to_file(str(filepath))
                results[key] = filename
                time.sleep(delay)
            except Exception as e:
                print(f"[TTS] Failed for key='{key}' text='{text[:40]}...': {e}")
                results[key] = ""

        if progress_callback:
            progress_callback(i + 1, total)

    return results
