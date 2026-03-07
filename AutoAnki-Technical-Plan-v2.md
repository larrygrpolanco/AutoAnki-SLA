# AutoAnki — Simplified Technical Plan (v2)

A simple TUI tool that takes a PDF or text file and generates a high-quality Anki vocabulary deck with TTS audio.

---

## Design Philosophy

**Simple to code, simple to use.** AutoAnki is a pipeline with one decision point in the middle. No project management, no editing, no saved state between sessions. You feed it a file, it shows you what it found, you pick what you want, it builds the deck.

The flashcard pedagogy (5 card types, i+1 sentences, strategic audio placement) stays exactly the same — that's the good part. What changes is everything around it.

---

## User Flow

```
$ autoanki

┌──────────────────────────────────────────┐
│  AutoAnki                                │
│──────────────────────────────────────────│
│                                          │
│  Source File: [path/to/chapter5.pdf    ] │
│                                          │
│  Past Vocab (optional):                  │
│  [path/to/past_words.txt              ]  │
│                                          │
│  [Generate]                              │
│                                          │
└──────────────────────────────────────────┘

        ↓  (LLM runs 3-step pipeline)

┌──────────────────────────────────────────┐
│  AutoAnki — Review                       │
│──────────────────────────────────────────│
│                                          │
│  Deck Name: [Korean Ch5 - Shopping    ]  │
│                                          │
│  Card Types:                             │
│  ☑ Recognition  ☑ Cloze  ☑ Production   │
│  ☑ Comprehension  ☑ Listening            │
│                                          │
│  Vocabulary (14 words found):            │
│  ☑ 사다        to buy          verb      │
│  ☑ 비싸다      to be expensive  adj      │
│  ☑ 싸다        to be cheap      adj      │
│  ☑ 팔다        to sell          verb     │
│  ☐ 돈          money            noun     │
│  ☑ 얼마        how much         adverb   │
│  ...                                     │
│                                          │
│  [Export Deck]              [Cancel]      │
│                                          │
└──────────────────────────────────────────┘

        ↓  (TTS + genanki build)

┌──────────────────────────────────────────┐
│  AutoAnki — Exporting                    │
│──────────────────────────────────────────│
│                                          │
│  Generating audio...                     │
│  ████████████░░░░░░░░  42/78  (54%)     │
│                                          │
│  Building deck...                        │
│                                          │
└──────────────────────────────────────────┘

        ↓

┌──────────────────────────────────────────┐
│  Done!                                   │
│──────────────────────────────────────────│
│                                          │
│  ✓ 65 cards from 13 words               │
│  ✓ Saved: Korean_Ch5_Shopping.apkg       │
│                                          │
│  [Open Folder]    [New Deck]    [Quit]   │
│                                          │
└──────────────────────────────────────────┘
```

**That's the whole app.** Three screens, one decision point.

---

## What's In vs. What's Out

### In (keep from original plan)
- 5 card types with full pedagogy (Recognition, Cloze, Production, Comprehension, Listening)
- 3-step LLM pipeline (Draft → Review → Structure)
- JSON schema + Pydantic validation
- TTS audio generation (OpenAI)
- genanki deck building with proper CSS/templates
- Past vocabulary upload (expands LLM's word pool for sentences)
- Card type selection (checkboxes)
- Vocabulary selection (uncheck words you don't want)
- PDF and text file extraction

### Out (removed)
- Project management system (no `~/.autoanki/projects/`, no meta.json, no status tracking)
- Card editing / review screen (no per-sentence editing in the TUI)
- Persistent state between sessions (each run is self-contained)
- The 5-screen TUI (replaced with 3 simple screens)
- Per-word audio toggles
- Schema versioning / migrations

---

## Architecture

### Data Flow

```
Input (PDF/text) → Parser → Raw Text
                          → [Optional] Past Vocabulary file
                          → LLM Pipeline (3 steps: Draft → Review → Structure)
                          → Structured JSON (validated by Pydantic)
                          → User selects vocabulary + card types (TUI)
                          → TTS Generation (only for selected words + card types)
                          → genanki builds .apkg
                          → Output file saved to working directory
```

### Tech Stack

| Component      | Tool                    | Why                                          |
|----------------|-------------------------|----------------------------------------------|
| Language       | Python 3.10+            | genanki requirement, ecosystem               |
| TUI Framework  | Textual                 | Simple widgets, pip-installable               |
| LLM            | OpenAI API (gpt-4o-mini)| Cheap, good at structured output             |
| TTS            | OpenAI TTS              | High quality, same API key                   |
| PDF Extraction | pymupdf (fitz)          | Handles most textbook PDFs                   |
| Deck Building  | genanki                 | Standard Anki deck generation                |
| Validation     | Pydantic                | JSON schema enforcement                      |
| Config         | python-dotenv           | .env-based API key                           |

### Project Structure

```
autoanki/
├── pyproject.toml
├── .env.example              # OPENAI_API_KEY=sk-...
├── src/
│   └── autoanki/
│       ├── __init__.py
│       ├── __main__.py       # Entry point
│       ├── parser.py         # PDF/text extraction + past vocab parsing
│       ├── llm.py            # 3-step LLM pipeline
│       ├── tts.py            # OpenAI TTS generation
│       ├── deck_builder.py   # genanki integration + Anki note model + CSS
│       ├── models.py         # Pydantic models (JSON schema)
│       ├── prompts/
│       │   ├── card_drafting.txt
│       │   ├── card_review.txt
│       │   └── structuring.txt
│       └── tui/
│           ├── __init__.py
│           └── app.py        # The entire TUI — 3 screens in one file
└── tests/
    └── test_pipeline.py
```

**~12 files total.** Compare to the original plan's ~25+ files.

---

## Pydantic Models

Same schema as the original plan. This is the good part — don't change it.

```python
from pydantic import BaseModel
from typing import Optional

class SourceInfo(BaseModel):
    title: str
    source_language: str
    target_language_name: str
    level_description: str
    available_vocabulary_context: str

class Card1Recognition(BaseModel):
    sentence_target: str
    sentence_target_highlight: str     # with <b> tags
    sentence_english: str

class Card2Cloze(BaseModel):
    sentence_cloze: str                # with {{c1::word}}
    sentence_english: str
    english_hint: str

class Card3Production(BaseModel):
    sentence_target: str
    sentence_english: str

class Card4Comprehension(BaseModel):
    sentence_target: str
    sentence_english: str
    word_in_sentence_highlight: str
    word_translation_in_context: str

class Card5Listening(BaseModel):
    sentence_target: str
    sentence_english: str
    word_in_sentence_highlight: str
    word_translation_in_context: str

class AudioQueries(BaseModel):
    word_isolated: str
    sentence_1: str
    sentence_2: str
    sentence_3: str
    sentence_4: str
    sentence_5: str

class VocabEntry(BaseModel):
    id: str
    target_word: str
    target_word_romanization: str = ""
    english_translation: str
    part_of_speech: str
    category: str = "General"
    notes: str = ""

    card_1_recognition: Card1Recognition
    card_2_cloze: Card2Cloze
    card_3_production: Card3Production
    card_4_comprehension: Card4Comprehension
    card_5_listening: Card5Listening
    audio_queries: AudioQueries

class AutoAnkiCards(BaseModel):
    schema_version: int = 1
    source_info: SourceInfo
    vocabulary: list[VocabEntry] = []
```

---

## The 3-Step LLM Pipeline

Unchanged from original. This is the core value of the tool.

### Step 1: Card Drafting
- System prompt references the flashcard philosophy (i+1 rule, sentence constraints, 5 unique contexts per word)
- Includes `available_vocabulary_context` (source text vocab + past vocab if provided)
- Input: extracted source text
- Output: semi-structured card content (doesn't need to be JSON)

### Step 2: Review & Quality Check
- Reviews every sentence against the i+1 rule using the original source text
- Checks cloze ambiguity, sentence variety, length
- Input: Step 1 output + original source text
- Output: corrected card content

### Step 3: Structuring
- Converts reviewed content to valid JSON matching the Pydantic schema
- Generates UUIDs, audio_queries, highlight versions
- Input: Step 2 output
- Output: valid JSON, validated by Pydantic (retry once on failure)

### Input Size Limit
~15,000 characters. Show count in the TUI. Block if over limit.

---

## TTS Generation

- Provider: OpenAI TTS
- File naming: `{md5(text)[:12]}.mp3` (content-hash for natural dedup)
- Store audio in a temp directory during the session
- Only generate audio for selected words and selected card types
- Isolated word audio generated if any card using it is enabled (Cards 1, 3, 5)
- Skip existing files (if rerunning)
- Rate limit: ~1s delay between requests
- On failure: log it, skip it, continue. Show summary at end.

---

## Deck Builder

Uses genanki with one note type (`AutoAnki Vocab`), 24 fields, 5 card templates.

- Card type filtering: only create Anki cards for types the user checked
- Vocab filtering: only include words the user checked
- Stable GUIDs from vocab entry ID + card type number
- CSS from `anki-css-styling.md` (already written)
- Audio files bundled into the .apkg package
- Output: single `.apkg` file in the current working directory

### Audio Placement (non-negotiable)
| Card | Front Audio | Back Audio |
|------|-------------|------------|
| 1: Recognition | None | Word + Sentence |
| 2: Cloze | None | Sentence |
| 3: Production | **NEVER** | Word + Sentence |
| 4: Comprehension | None | Sentence |
| 5: Listening | Sentence (auto-play) | Sentence + Word |

---

## TUI Design

### Screen 1: Input

Simple form with two fields:
- **Source File** — path to PDF or text file (required)
- **Past Vocabulary** — path to a text file with previously learned words (optional)
- **Generate** button — triggers extraction + LLM pipeline
- Show a loading/progress indicator while LLM is running

Past vocab file format: one word per line, comma-separated, or tab-separated. Flexible parsing (split on newlines/commas/tabs, strip whitespace).

### Screen 2: Review & Select

This is the one meaningful interaction screen. Shows:
- **Deck Name** — editable text field (auto-populated from source info)
- **Card Type checkboxes** — all 5 checked by default, at least 1 required
- **Vocabulary list** — checkboxes next to each word with its translation and part of speech. All checked by default. User unchecks words they don't want.
- **Export Deck** button
- **Cancel** button (goes back or quits)

No sentence editing. No card preview. Just pick what you want and go.

### Screen 3: Export Progress + Done

- Progress bar for TTS generation
- "Building deck..." status
- On completion: card count, file path, and options to open folder, start new, or quit

### TUI Implementation Notes

- All three screens can live in a single `app.py` file (or one file per screen if cleaner)
- Use Textual's built-in widgets: `Input`, `Checkbox`, `Button`, `ProgressBar`, `DataTable` or `ListView`
- No custom widgets needed
- Screen transitions via Textual's `push_screen` / `pop_screen`

---

## Past Vocabulary Integration

When the user provides a past vocab file:
1. Parse the file (split on whitespace/commas/tabs, strip)
2. Append the word list to the `available_vocabulary_context` string
3. Pass this context to LLM Steps 1 and 2
4. Result: LLM can use these words in example sentences, giving the student incidental review of old vocabulary while keeping sentences comprehensible

Example context string:
```
Words from the source text may be used in example sentences.
Previously learned vocabulary: 사람, 집, 학교, 가다, 오다, 먹다, 하다.
Basic universally-known words are also permitted.
```

---

## Build Phases

### Phase 1: Core Pipeline (no TUI)

Build the pipeline as importable Python functions. Test from a script.

**Files to create:**
- `models.py` — Pydantic models
- `parser.py` — PDF/text extraction, past vocab parsing
- `llm.py` — 3-step pipeline
- `deck_builder.py` — genanki note model + CSS + deck building
- Prompt files in `prompts/`

**Test:** Write a `test_pipeline.py` that takes a sample text file, runs the LLM pipeline, validates the JSON, and builds a deck (without audio). Import into Anki and verify the cards look right.

**Skip TTS for now** — get the cards right first.

### Phase 2: TTS

**Files to create:**
- `tts.py` — OpenAI TTS wrapper with hashing, caching, batch generation

**Test:** Generate audio for a small set of words. Rebuild the deck with audio. Import into Anki. Verify audio plays on correct card sides.

### Phase 3: TUI

**Files to create:**
- `tui/app.py` — All 3 screens
- `__main__.py` — Entry point

**Test:** Full end-to-end: launch TUI → enter file path → LLM runs → review screen shows words → select/deselect → export → .apkg file works in Anki.

### Phase 4: Polish

- Error handling (no API key, bad file path, LLM failure, TTS failure)
- Clear error messages in the TUI
- README with install instructions
- `pyproject.toml` for `pip install .`

---

## Key Differences from v1

| Aspect | v1 (Original) | v2 (This Plan) |
|--------|---------------|----------------|
| TUI screens | 5 (Home, Import, Config, Review, Export) | 3 (Input, Select, Export) |
| Project management | Full (save/load/list projects) | None (single-session) |
| Card editing | Per-sentence editing in TUI | None (trust the LLM or edit JSON) |
| File count | ~25+ files | ~12 files |
| Build phases | 7 phases | 4 phases |
| Persistent state | Projects saved to ~/.flashforge/ | Nothing saved between sessions |
| Per-word audio toggle | Yes | No (all selected words get audio) |
| Past vocabulary | Yes | Yes (kept) |
| Card type selection | Yes | Yes (kept) |
| Vocab selection | No | Yes (added — simpler than editing) |
| Schema versioning | Yes | No (premature for v1) |

---

## Dependencies

```toml
[project]
dependencies = [
    "textual>=0.40",
    "genanki>=0.13",
    "openai>=1.0",
    "pymupdf>=1.23",
    "pydantic>=2.0",
    "python-dotenv>=1.0",
]
```

---

## Reference Documents

These files contain the detailed specifications that this plan builds on:

- **Flashcard-Philosophy.md** — The pedagogical rationale, 5 card type specs, sentence rules, audio placement rules, quality checklist. The LLM prompts should reference this heavily.
- **anki-css-styling.md** — The complete CSS and HTML templates for all 5 card types. Used directly by `deck_builder.py`.
- **flashcard-schema-template.json** — Example JSON output showing exactly what the LLM should produce. Used in the Step 3 (structuring) prompt.
- **Genanki-Docs.md** — How to use genanki for deck generation. Reference for `deck_builder.py`.
