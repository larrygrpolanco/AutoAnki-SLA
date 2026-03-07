"""
Phase 1 test: Run the LLM pipeline on test.txt and build a .apkg (no audio).

Usage:
    cd /path/to/AutoAnki-SLA
    python -m tests.test_pipeline

Or with a specific file:
    python -m tests.test_pipeline path/to/your/file.txt
"""

import sys
from pathlib import Path

# Allow running from repo root without installing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dotenv import load_dotenv
load_dotenv()

import os
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY not set. Add it to .env or environment.")
    sys.exit(1)


def main():
    source = sys.argv[1] if len(sys.argv) > 1 else "test.txt"
    source_path = Path(source)

    if not source_path.exists():
        print(f"Error: {source_path} not found.")
        sys.exit(1)

    from autoanki.parser import extract_text, count_chars, MAX_CHARS
    from autoanki.llm import run_pipeline
    from autoanki.deck_builder import build_deck_with_audio

    print(f"Reading: {source_path}")
    text = extract_text(str(source_path))
    n = count_chars(text)
    print(f"  {n:,} characters")

    if n > MAX_CHARS:
        print(f"  Warning: over {MAX_CHARS:,} char limit — this may produce poor results")

    print("\nRunning LLM pipeline...")
    def progress(msg):
        print(f"  {msg}")

    cards = run_pipeline(text, progress_callback=progress)

    print(f"\nGenerated {len(cards.vocabulary)} vocabulary entries:")
    for entry in cards.vocabulary:
        print(f"  {entry.target_word:15}  {entry.english_translation:20}  [{entry.part_of_speech}]")

    print("\nBuilding deck (no audio)...")
    output_path = "test_output.apkg"
    card_count = build_deck_with_audio(
        cards=cards,
        selected_word_ids={e.id for e in cards.vocabulary},
        selected_card_types={1, 2, 3, 4, 5},
        deck_name=cards.source_info.title,
        audio_files={},
        audio_dir=Path("."),
        output_path=output_path,
    )

    print(f"\nDone! {card_count} cards written to: {output_path}")
    print("Import this file into Anki to verify the cards look correct.")

    # Also save the raw JSON for inspection
    json_path = "test_output.json"
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(cards.model_dump_json(indent=2))
    print(f"Raw JSON saved to: {json_path}")


if __name__ == "__main__":
    main()
