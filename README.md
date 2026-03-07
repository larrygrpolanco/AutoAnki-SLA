# AutoAnki

A TUI tool that takes a PDF or text file and generates a high-quality Anki vocabulary deck with TTS audio. Built on SLA research: 5 card types per word, i+1 sentences, strategic audio placement.

---

## Current Status

**All 4 phases are built. Phase 1 (core pipeline) is verified working.**

| Phase | Status | Description |
|-------|--------|-------------|
| 1 — Core Pipeline | **Done + Verified** | LLM pipeline → .apkg (no audio) |
| 2 — TTS | Built, not yet tested | OpenAI TTS audio generation |
| 3 — TUI | Built, not yet tested | Full 3-screen Textual interface |
| 4 — Polish | Built | Error handling, entry point |

**Next step: import `test_output.apkg` into Anki and verify cards look correct, then test TTS (`Phase 2`), then launch the TUI (`Phase 3`).**

---

## Setup

```bash
# Clone and enter the repo
cd AutoAnki-SLA

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install
pip install -e .

# Configure API key
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-your-key-here
```

---

## Usage

### Launch the TUI
```bash
autoanki
# or
python -m autoanki
```

The app is 3 screens:
1. **Input** — pick your source file (Browse button), optional past vocab file, hit Generate
2. **Review** — see all found vocabulary words, select/deselect, choose card types, name your deck
3. **Export** — TTS generates audio, deck builds, .apkg saved to current directory

### Run without TUI (testing)
```bash
python -m tests.test_pipeline test.txt
# Outputs: test_output.apkg and test_output.json
```

---

## File Structure

```
src/autoanki/
├── __init__.py
├── __main__.py          # Entry point (loads .env, launches TUI)
├── models.py            # Pydantic models (VocabEntry, AutoAnkiCards, etc.)
├── parser.py            # PDF/text extraction (pymupdf + plain text)
├── llm.py               # 3-step LLM pipeline (Draft → Review → Structure)
├── tts.py               # OpenAI TTS, MD5-hash dedup, batch generation
├── deck_builder.py      # genanki: 25-field note type, 5 card templates, CSS
├── prompts/
│   ├── card_drafting.txt    # Step 1: vocabulary extraction + sentence writing
│   ├── card_review.txt      # Step 2: i+1 quality check
│   └── structuring.txt      # Step 3: convert to JSON (includes full schema + example)
└── tui/
    ├── __init__.py
    └── app.py           # All 3 screens + FileBrowserModal in one file
tests/
└── test_pipeline.py     # Phase 1 smoke test (no TUI, no audio)
```

---

## The 5 Card Types

Each vocabulary word generates 5 cards from a single note, each with a unique example sentence:

| Card | Tests | Front | Back |
|------|-------|-------|------|
| 1 Recognition | See word → know meaning | Word + highlighted sentence | English + audio |
| 2 Cloze | Know meaning → produce word | Sentence with `[...]` + hint | Full sentence + audio |
| 3 Production | English → target word | English only (no audio) | Word + sentence + audio |
| 4 Comprehension | Read sentence → understand | Plain sentence | Translation + audio |
| 5 Listening | Hear sentence → understand | Auto-play audio | Written sentence + audio |

---

## Key Implementation Notes

### Cloze Card Display Fix
`{{c1::word}}` syntax only works in Anki's built-in Cloze note type. In our custom note type it renders as literal text. Fixed in `deck_builder.py`:
- `Sentence2Blank`: `{{c1::운동}}` → `<b>[...]</b>` (shown on front)
- `Sentence2Full`: `{{c1::운동}}` → `<b>운동</b>` (shown on back)

### Card Type Filtering
The genanki `Model` is built dynamically with only the templates the user selected. Anki only generates cards for included templates — no empty/suppressed cards.

### LLM Pipeline
- Step 1 (temperature 0.7): extract vocab + write 5 sentences per word
- Step 2 (temperature 0.3): QA review against i+1 rule
- Step 3 (temperature 0, `json_object` mode): convert to validated JSON, retry once on failure

### Audio Dedup
Audio files are named by `MD5(text)[:12].mp3`. Same sentence across multiple runs = same filename = skipped (cached).

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `textual` | TUI framework |
| `genanki` | Anki .apkg generation |
| `openai` | LLM pipeline + TTS |
| `pymupdf` | PDF text extraction |
| `pydantic` | JSON schema validation |
| `python-dotenv` | .env API key loading |

---

## Reference Documents

| File | Purpose |
|------|---------|
| `AutoAnki-Technical-Plan-v2.md` | Architecture spec |
| `Flashcard-Philosophy.md` | SLA pedagogy + card design rationale |
| `anki-css-styling.md` | CSS + HTML templates for all 5 card types |
| `flashcard-schema-template.json` | Example JSON output (used in LLM prompt) |
| `Genanki-Docs.md` | genanki API reference |
| `Textual-Basics-Docs.md` | Textual framework reference |
| `test.txt` | Korean Chapter 9 (Sports) — used for testing |

---

## What to Test Next

**Phase 1 — Verify .apkg in Anki** (free, do this first):
```bash
python -m tests.test_pipeline test.txt
# Import test_output.apkg into Anki
# Check: Card 2 shows [...] on front, word revealed on back
# Check: Card 3 shows English only on front (no audio button)
# Check: Card 5 shows audio play button on front
```

**Phase 2 — TTS** (costs ~$0.05 for 7 words × 6 audio files):
```bash
python -m tests.test_pipeline test.txt
# test_pipeline doesn't call TTS — add a quick script or use the TUI
```

**Phase 3 — Full TUI**:
```bash
autoanki
# Browse to test.txt → Generate → Review → Export Deck
```
