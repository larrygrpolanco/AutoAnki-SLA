# FlashForge — Technical Plan

A TUI-based tool that takes educational text content and generates pedagogically-structured Anki flashcard decks with high-quality TTS audio.

---

## Architecture Overview

### Data Flow

```
Input (PDF/text) → Parser → Raw Text
                          → [Optional] Past Vocabulary Upload
                          → Card Type Selection (user picks which of 5 card types to generate)
                          → LLM Pipeline (3 steps: Draft → Review → Structure)
                          → Structured JSON (validated by Pydantic)
                          → User Review/Edit (TUI)
                          → TTS Generation
                          → genanki
                          → .apkg
```

### Core Principle

**The JSON file is the single source of truth.** Every project is a folder on disk. The TUI reads from and writes to JSON. Deck generation always rebuilds from JSON. No in-memory-only state.

### Tech Stack

| Component        | Tool                        | Why                                                    |
| ---------------- | --------------------------- | ------------------------------------------------------ |
| Language         | Python 3.10+                | genanki requirement, ecosystem                         |
| TUI Framework    | Textual                     | Rich widgets, pip-installable, cross-platform, mouse support |
| LLM              | OpenAI API (gpt-4o-mini)    | Good instruction following, cheap, JSON mode            |
| TTS              | OpenAI TTS (gpt-4o-mini-tts) | High quality for language learning, same API key       |
| PDF Extraction   | pymupdf (fitz)              | Handles most textbook PDFs well                        |
| Deck Building    | genanki                     | Standard Anki deck generation                          |
| Validation       | Pydantic                    | JSON schema enforcement                                |
| Config           | python-dotenv               | .env-based API key management                          |
| Packaging        | pyproject.toml + pip        | `pip install .` gives users a `flashforge` command     |

---

## Project Structure

```
flashforge/
├── pyproject.toml
├── README.md
├── .env.example                  # OPENAI_API_KEY=sk-...
├── flashcard-philosophy.md       # Card design rationale (maintained separately)
├── src/
│   └── flashforge/
│       ├── __init__.py
│       ├── __main__.py           # Entry point: `python -m flashforge`
│       ├── cli.py                # Argument parsing, launches TUI
│       │
│       ├── core/
│       │   ├── __init__.py
│       │   ├── models.py         # Pydantic models (JSON schema)
│       │   ├── parser.py         # PDF/text extraction
│       │   ├── llm.py            # Three-prompt LLM pipeline
│       │   ├── tts.py            # OpenAI TTS generation
│       │   ├── deck_builder.py   # genanki integration
│       │   └── project.py        # Project CRUD (load/save/list)
│       │
│       ├── prompts/
│       │   ├── card_drafting.txt    # Prompt 1: pedagogical card drafting
│       │   ├── card_review.txt      # Prompt 2: quality review & correction
│       │   └── structuring.txt      # Prompt 3: JSON structuring
│       │
│       ├── templates/
│       │   └── anki_models.py      # Anki note models, CSS, card templates
│       │
│       └── tui/
│           ├── __init__.py
│           ├── app.py            # Main Textual App
│           ├── screens/
│           │   ├── home.py       # Project list
│           │   ├── import_screen.py  # File input + text preview
│           │   ├── config_screen.py  # Past vocab upload + card type selection
│           │   ├── review.py     # Card review/edit (main screen)
│           │   └── export.py     # TTS + deck generation progress
│           └── widgets/
│               └── card_editor.py  # Reusable card editing widget
│
├── tests/
│   ├── test_parser.py
│   ├── test_llm.py
│   ├── test_deck_builder.py
│   └── fixtures/
│       ├── sample_chapter.txt
│       └── sample_chapter.pdf
│
└── docs/
    └── getting-started.md
```

### User Data Directory

```
~/.flashforge/
├── config.toml              # User preferences (optional, future)
└── projects/
    └── <project-name>/
        ├── source.txt       # Extracted text from input
        ├── past_vocab.txt   # [Optional] User-uploaded past vocabulary list
        ├── cards.json       # LLM output + user edits (THE source of truth)
        ├── meta.json        # Deck name, language, dates, audio toggle, card types, status
        ├── audio/           # Generated TTS .mp3 files (named by content hash)
        └── output/          # Final .apkg file
```

---

## Pydantic Models (JSON Schema)

FlashForge is **vocabulary-only**. Grammar cards, reading passage cards, and dialogue cards are out of scope (see `flashcard-philosophy.md`, Section 8). Each vocabulary word generates up to five card types, each targeting a different dimension of word knowledge.

```python
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

SCHEMA_VERSION = 1

class ProjectStatus(str, Enum):
    IMPORTED = "imported"       # Text extracted, not yet sent to LLM
    CONFIGURED = "configured"   # User has set card types and optional past vocab
    GENERATED = "generated"     # LLM has produced cards
    REVIEWED = "reviewed"       # User has reviewed/edited
    EXPORTED = "exported"       # Deck has been built

class CardTypeSelection(BaseModel):
    """Which of the 5 card types to generate. All default to True."""
    card_1_recognition: bool = True
    card_2_cloze: bool = True
    card_3_production: bool = True
    card_4_comprehension: bool = True
    card_5_listening: bool = True

    def enabled_types(self) -> list[int]:
        """Returns list of enabled card type numbers, e.g. [1, 2, 5]."""
        types = []
        if self.card_1_recognition: types.append(1)
        if self.card_2_cloze: types.append(2)
        if self.card_3_production: types.append(3)
        if self.card_4_comprehension: types.append(4)
        if self.card_5_listening: types.append(5)
        return types

class ProjectMeta(BaseModel):
    schema_version: int = SCHEMA_VERSION
    project_name: str
    deck_name: str
    source_language: str = ""               # e.g. "ko", "es", "ar" — detected/set by LLM or user
    target_language_name: str = ""          # e.g. "Korean", "Spanish" — human-readable
    level_description: str = ""             # e.g. "Beginner, Chapter 5"
    source_filename: str
    created_at: str                         # ISO timestamp
    updated_at: str
    status: ProjectStatus
    generate_audio: bool = True             # Project-level audio toggle
    card_types: CardTypeSelection = CardTypeSelection()
    has_past_vocab: bool = False            # Whether user uploaded past vocabulary
    available_vocabulary_context: str = ""  # Description for LLM: what vocab is available
    vocab_count: int = 0

class SourceInfo(BaseModel):
    title: str
    source_language: str                    # ISO 639-1 code
    target_language_name: str
    level_description: str
    available_vocabulary_context: str       # Describes what words the LLM may use in sentences

class Card1Recognition(BaseModel):
    sentence_target: str                    # Full sentence in target language
    sentence_target_highlight: str          # Same sentence with target word in <b> tags
    sentence_english: str                   # English translation

class Card2Cloze(BaseModel):
    sentence_cloze: str                     # Sentence with {{c1::word}} syntax
    sentence_english: str
    english_hint: str                       # English meaning of blanked word (mandatory)

class Card3Production(BaseModel):
    sentence_target: str                    # New example sentence
    sentence_english: str

class Card4Comprehension(BaseModel):
    sentence_target: str                    # Sentence without highlight (front)
    sentence_english: str
    word_in_sentence_highlight: str         # Same sentence with target word in <b> (back)
    word_translation_in_context: str        # Contextual translation e.g. "buys"

class Card5Listening(BaseModel):
    sentence_target: str                    # Sentence text (for back display + TTS)
    sentence_english: str
    word_in_sentence_highlight: str         # Highlighted version (back)
    word_translation_in_context: str        # Contextual translation

class AudioQueries(BaseModel):
    """Pre-cleaned target-language text for TTS. No cloze syntax, no HTML, no English."""
    word_isolated: str
    sentence_1: str
    sentence_2: str
    sentence_3: str
    sentence_4: str
    sentence_5: str

class VocabEntry(BaseModel):
    id: str                                 # Stable UUID
    target_word: str                        # Dictionary/base form
    target_word_romanization: str = ""      # Optional, never shown on cards
    english_translation: str                # Concise (1-4 words)
    part_of_speech: str                     # noun, verb, adjective, etc.
    category: str = "General"               # Thematic grouping
    notes: str = ""                         # Optional user annotations
    generate_audio: bool = True             # Per-word audio toggle

    # Card data — all five are always present in JSON even if the user
    # chose not to generate certain card types. This keeps the schema
    # stable. The deck builder skips disabled card types at export time.
    card_1_recognition: Card1Recognition
    card_2_cloze: Card2Cloze
    card_3_production: Card3Production
    card_4_comprehension: Card4Comprehension
    card_5_listening: Card5Listening

    audio_queries: AudioQueries

class FlashForgeCards(BaseModel):
    schema_version: int = SCHEMA_VERSION
    source_info: SourceInfo
    vocabulary: list[VocabEntry] = []
```

---

## Past Vocabulary (Optional Feature)

### Purpose

When generating example sentences, the LLM is constrained to use only words from the current source material plus basic universally-known words (the i+1 rule from `flashcard-philosophy.md`, Section 3.1). This can be limiting — the LLM has a small pool of known words to work with, which sometimes forces repetitive or awkward sentences.

By uploading a **past vocabulary list**, the user expands the pool of words the LLM is permitted to use in example sentences. These are words the student has already learned in previous chapters or courses. This gives the LLM more creative freedom while still respecting the i+1 rule, and it gives the student incidental review of previously learned words.

### User Flow

1. On the **Config Screen** (after import, before generation), the user sees an optional field: "Past Vocabulary (optional)"
2. The user can provide a path to a `.txt` file containing previously learned words
3. The file is a simple plain-text list — one word per line, or comma-separated, or any reasonable format. Flexible parsing.
4. The file is copied into the project folder as `past_vocab.txt`
5. The contents are appended to the `available_vocabulary_context` field in `source_info`, which is passed to the LLM prompts

### Format

The past vocabulary file is intentionally low-ceremony. Accepted formats:
- One word per line (most common)
- Comma-separated
- Tab-separated
- Mixed (the parser splits on newlines, commas, and tabs, then strips whitespace)

Example `past_vocab.txt`:
```
사람
집
학교
가다
오다
먹다
하다
```

### How It Integrates

The parsed words are added to the `available_vocabulary_context` string in `source_info`. For example:

```
"available_vocabulary_context": "Words from chapters 1-5 may be used in example sentences. 
Previously learned vocabulary that may also be used: 사람, 집, 학교, 가다, 오다, 먹다, 하다. 
Basic universally-known Korean words (pronouns, common verbs, basic nouns) are also permitted."
```

This context string is included in the LLM prompts for Steps 1 and 2, expanding the pool of permitted words without changing the fundamental rule: the target word should be the **only** challenging element.

---

## Card Type Selection

### Purpose

Not every learner wants all five card types. A user might only want recognition and listening cards (Cards 1 & 5), or cloze and production cards (Cards 2 & 3), or any other combination. This feature lets the user choose before generation.

### User Flow

1. On the **Config Screen** (after import, before generation), the user sees checkboxes for each card type:
   - ☑ Card 1: Recognition
   - ☑ Card 2: Contextual Recall (Cloze)
   - ☑ Card 3: Production
   - ☑ Card 4: Sentence Comprehension
   - ☑ Card 5: Listening Comprehension
2. All are checked by default
3. At least one must be selected (enforce in UI)
4. The selection is stored in `meta.json` as `card_types`

### How It Integrates

**LLM Pipeline:** The LLM **always generates all 5 card types** regardless of the user's selection. This is intentional:
- It keeps the JSON schema stable (all 5 card blocks always present)
- It lets the user change their mind later without re-running the LLM
- The cost difference is negligible (the sentences are short)
- It simplifies the LLM prompts (no conditional logic)

**Deck Builder:** The `card_types` selection is applied at **export time**. The deck builder reads `meta.json.card_types` and only creates Anki cards for the enabled types. Disabled card types are simply skipped — their data remains in `cards.json` but no Anki card is generated.

**TTS Generation:** Audio is only generated for sentences belonging to enabled card types. For example, if the user disables Card 3 (Production), then `sentence_3` audio is skipped. The isolated word audio is generated if *any* card type that uses it is enabled (Cards 1, 3, or 5).

**Review Screen:** The review screen shows all card data regardless of the selection (the user might want to edit sentences even for disabled types), but disabled card types are visually dimmed or marked with a note like "(not included in export)".

---

## Three-Prompt LLM Pipeline

### Why Three Prompts

The original two-step pipeline (create → structure) missed a critical failure mode: the LLM generates sentences that look fine individually but violate the i+1 rule or contain ambiguous cloze deletions. These errors are invisible at creation time and only become obvious during targeted review. Adding a dedicated review step catches these issues before they reach the learner.

The review step also has access to the *original source text*, which lets it verify that example sentences only use vocabulary from the source material (plus past vocabulary, if provided). Step 1 might "know" this rule but still drift; Step 2 explicitly checks it.

### Prompt 1: Card Drafting (Pedagogical Focus)

- **Model:** `gpt-4o-mini` (or `gpt-4o` if budget allows)
- **System prompt:** Loaded from `prompts/card_drafting.txt`. References principles from `flashcard-philosophy.md`. Instructs the model to act as an experienced language teacher designing vocabulary flashcards.
- **Included context:**
  - The `available_vocabulary_context` string (which includes past vocabulary if uploaded)
  - The sentence generation constraints from `flashcard-philosophy.md` Section 6.3
- **User message:** The extracted source text.
- **Task:** Identify vocabulary words, generate English translations, write all five example sentences per word, create cloze versions with English hints.
- **Output:** Semi-structured text with card content. Does NOT need to be valid JSON. Focus is entirely on content quality — good translations, natural sentences, correct difficulty level.

### Prompt 2: Review & Quality Check (QA Focus)

- **Model:** `gpt-4o-mini`
- **System prompt:** Loaded from `prompts/card_review.txt`. Instructs the LLM to act as a quality reviewer checking against the specific criteria from `flashcard-philosophy.md` Section 6.3.
- **Included context:**
  - The original extracted source text (for cross-reference)
  - The `available_vocabulary_context` string
- **User message:** The Step 1 output.
- **Task:** Review every sentence against the review checklist:
  1. Does every non-target word appear in the source text, the past vocabulary list, or qualify as universally basic?
  2. For each cloze: given only the sentence and the English hint, is there exactly one correct answer?
  3. Are all five sentences genuinely different contexts?
  4. Is any sentence longer than 15 words? Simplify if so.
  5. Would any audio placement give away an answer? (Verify against card design.)
- **Output:** Corrected, reviewed card content. Fixes applied inline.

### Prompt 3: Structuring (Formatting Focus)

- **Model:** `gpt-4o-mini`
- **System prompt:** Loaded from `prompts/structuring.txt`. Contains the exact JSON schema (matching the `VocabEntry` Pydantic model). Instructs strict JSON-only output.
- **User message:** The reviewed output from Step 2.
- **Task:** Convert the reviewed content into valid JSON matching the schema:
  - Generate stable UUIDs for each vocabulary entry
  - Compute `audio_queries` by stripping HTML, cloze syntax, and English from sentences
  - Generate `sentence_target_highlight` versions with `<b>` tags around the target word
  - Populate all card type blocks
- **Output:** Valid JSON. Validated by Pydantic. If validation fails, retry once with the error message appended.

### Token Limit / Input Size

- **Hard limit:** ~15,000 characters of extracted text (~4,000 tokens). This keeps us well within context windows and encourages chapter-sized inputs.
- **UI enforcement:** Show character count during import. Block submission with a clear message if over limit. Suggest the user trim their input.
- **Rationale:** Smaller focused decks > massive unfocused ones. This is a feature, not a limitation.

---

## TTS Integration

- **Provider:** OpenAI TTS (`gpt-4o-mini-tts`)
- **Audio format:** MP3
- **File naming:** Content hash based — `{md5(text)[:12]}.mp3`. Natural deduplication and resume capability.
- **Audio files per word:** Up to 6 unique files (1 isolated word + 5 sentences). The isolated word audio is shared across Cards 1, 3, and 5 (back). See `flashcard-philosophy.md` Section 4.1 for the full audio mapping.
- **Audio toggles:**
  - Project level: `meta.json` → `generate_audio: bool`
  - Card level: Each vocab entry has `generate_audio: bool`
  - Card type level: Only generate audio for sentences belonging to enabled card types
  - If project-level is `False`, skip all audio regardless of other settings
- **Audio placement rules (enforced at deck build time):**
  - Cards 1–4: Audio on back only
  - Card 5: Audio on front (sentence, auto-play) and back (replay + isolated word)
  - Card 3 production: **NEVER** audio on front (this was a real bug in earlier designs)
- **Resume/retry:** Before generating, check if `audio/{hash}.mp3` exists. Skip if it does.
- **Rate limiting:** Configurable delay between requests (default 1s). Show progress in TUI.
- **Error handling:** If a single TTS request fails, log it, mark as missing, continue. Show summary of failures. User can rerun to retry only missing ones.
- **TTS query cleaning:** Before sending to TTS, strip all cloze syntax (`{{c1::word}}` → `word`), HTML tags, English text, and trailing whitespace. The `audio_queries` field in the JSON is pre-cleaned at structuring time (Step 3).

---

## TUI Screen Flow

### Screen 1: Home (Project List)

```
┌─────────────────────────────────────────────┐
│  FlashForge                                 │
│─────────────────────────────────────────────│
│  Your Projects:                             │
│                                             │
│  📁 Korean Ch.3 - Greetings    [Generated]  │
│     Updated: 2025-06-15  │  32 words        │
│                                             │
│  📁 Korean Ch.4 - Family       [Exported]   │
│     Updated: 2025-06-14  │  28 words        │
│                                             │
│  📁 Spanish Ch.1 - Basics      [Imported]   │
│     Updated: 2025-06-13  │  0 words         │
│                                             │
│  [N] New Project    [Q] Quit                │
└─────────────────────────────────────────────┘
```

- List all projects from `~/.flashforge/projects/`
- Show name, status, word count, last updated
- Select to open → goes to Review screen (or Import/Config if earlier status)
- `N` to create new → goes to Import screen

### Screen 2: Import

```
┌─────────────────────────────────────────────┐
│  New Project                                │
│─────────────────────────────────────────────│
│  Project Name: [korean-ch5-shopping      ]  │
│  File Path:    [/home/user/textbook-ch5.pdf] │
│                                             │
│  ── Extracted Text Preview ──────────────── │
│  │ Chapter 5: Shopping                    │ │
│  │ In this chapter, you will learn        │ │
│  │ vocabulary for shopping and prices...  │ │
│  │                                        │ │
│  │ 사다 (sada) - to buy                   │ │
│  │ 비싸다 (bissada) - to be expensive     │ │
│  │ ...                                    │ │
│  ──────────────────────── 3,241 / 15,000 ── │
│                                             │
│  [C] Continue to Settings    [B] Back       │
└─────────────────────────────────────────────┘
```

- User enters a project name and file path (or pastes text directly)
- PDF/text extraction runs immediately, preview shows result
- Character count displayed — red if over limit
- User reviews extracted text to catch parsing issues before burning API tokens
- "Continue to Settings" → goes to Config screen

### Screen 3: Config (Pre-Generation Settings)

```
┌─────────────────────────────────────────────────┐
│  Project Settings: korean-ch5-shopping          │
│─────────────────────────────────────────────────│
│                                                 │
│  ── Card Types to Generate ──────────────────── │
│  ☑ Card 1: Recognition                         │
│  ☑ Card 2: Contextual Recall (Cloze)           │
│  ☑ Card 3: Production                          │
│  ☑ Card 4: Sentence Comprehension              │
│  ☑ Card 5: Listening Comprehension             │
│                                                 │
│  ── Past Vocabulary (optional) ──────────────── │
│  Upload a text file with words the student      │
│  already knows. These will be available for     │
│  use in example sentences.                      │
│                                                 │
│  File: [                                     ]  │
│  Status: No file uploaded                       │
│                                                 │
│  ── Level Description ───────────────────────── │
│  [Beginner, Chapter 5                        ]  │
│                                                 │
│  [G] Generate Cards    [B] Back                 │
└─────────────────────────────────────────────────┘
```

- Checkboxes for card type selection (all checked by default, at least 1 required)
- Optional past vocabulary file upload field
- Level description field (used in LLM prompts for calibrating sentence difficulty)
- "Generate Cards" triggers the 3-step LLM pipeline with a loading indicator
- On completion, transitions to Review screen

### Screen 4: Review / Edit (Main Screen)

```
┌─────────────────────────────────────────────────┐
│  Korean Ch.5 - Shopping                         │
│  Deck Name: [Korean Lesson 05 - Shopping     ]  │
│  Language: Korean  │  Audio: ON                  │
│  Card Types: 1, 2, 3, 4, 5                      │
│─────────────────────────────────────────────────│
│  # │ Word     │ English          │ POS  │ 🔊 │  │
│  1 │ 사다     │ to buy           │ verb │ ✓  │  │
│  2 │ 비싸다   │ to be expensive  │ adj  │ ✓  │  │
│  3 │ 싸다     │ to be cheap      │ adj  │ ✓  │  │
│  4 │ ...      │ ...              │      │    │  │
│─────────────────────────────────────────────────│
│  ── Editing: 사다 (to buy) ─────────────────── │
│                                                 │
│  Card 1 (Recognition):                          │
│    Sentence: [저는 가게에서 과일을 사요.      ]  │
│    English:  [I buy fruit at the store.       ]  │
│                                                 │
│  Card 2 (Cloze):                                │
│    Cloze:    [엄마는 토요일마다 빵을 {{c1::사요}}.] │
│    English:  [My mom buys bread every Saturday.]  │
│    Hint:     [to buy                          ]  │
│                                                 │
│  Card 3 (Production):           (dimmed if disabled)
│    Sentence: [우리는 어제 새 신발을 샀어요.   ]  │
│    English:  [We bought new shoes yesterday.  ]  │
│                                                 │
│  ... (Card 4, Card 5)                           │
│                                                 │
│  Audio: [✓] Generate  │  Category: [Shopping]    │
│─────────────────────────────────────────────── │
│                                                 │
│  [E] Export Deck    [D] Delete Word    [B] Back │
└─────────────────────────────────────────────────┘
```

- Single flat list of vocabulary words (no tabs — vocabulary only)
- Click/select a word to expand all 5 card blocks for editing
- Disabled card types shown dimmed with "(not included in export)"
- Per-word audio toggle
- Deck name editable at top
- Delete individual words
- "Export Deck" → goes to Export screen

### Screen 5: Export

```
┌─────────────────────────────────────────────┐
│  Exporting: Korean Lesson 05 - Shopping     │
│─────────────────────────────────────────────│
│                                             │
│  Generating Audio...                        │
│  ████████████░░░░░░░░  42/78  (54%)        │
│                                             │
│  ✓ Isolated words:  12/14                   │
│  ✓ Sentence audio:  30/56                   │
│  ⏳ Remaining:       36                      │
│                                             │
│  Building deck...                           │
│                                             │
│  [C] Cancel                                 │
└─────────────────────────────────────────────┘

        ↓ (on completion)

┌─────────────────────────────────────────────┐
│  Export Complete!                            │
│─────────────────────────────────────────────│
│                                             │
│  ✓ Audio: 76/78 generated (2 skipped)       │
│  ✓ Cards: 70 cards from 14 words            │
│    (5 card types × 14 words)                │
│  ✓ Deck saved to:                           │
│    ~/.flashforge/projects/korean-ch5/       │
│    output/Korean_Lesson_05.apkg             │
│                                             │
│  ⚠ 2 audio files failed. Rerun export to   │
│    retry only the missing files.            │
│                                             │
│  [O] Open Folder    [B] Back to Project     │
└─────────────────────────────────────────────┘
```

- Progress bar for TTS generation
- Shows audio generation status
- Card count reflects card type selection (e.g., 3 types × 14 words = 42 cards)
- Skips existing audio files automatically
- Summary on completion with failures
- Clear path to output file

---

## Anki Note Model

FlashForge uses a single Anki note type that generates up to five cards via card templates. One note with many fields produces multiple cards, each showing different fields on front and back.

**Note Type Name:** `FlashForge Vocab`

**Fields (24):**
1. `TargetWord` — The word in the target language
2. `EnglishTranslation` — English meaning
3. `PartOfSpeech` — Part of speech tag
4. `Sentence1` — Card 1 sentence (with `<b>` highlight)
5. `Sentence1English` — Card 1 English translation
6. `Sentence2Cloze` — Card 2 cloze sentence (with `{{c1::}}` syntax)
7. `Sentence2English` — Card 2 English translation
8. `ClozeHint` — English hint for the cloze (mandatory)
9. `Sentence3` — Card 3 sentence (target language)
10. `Sentence3English` — Card 3 English translation
11. `Sentence4` — Card 4 sentence (no highlight, for front)
12. `Sentence4Highlight` — Card 4 sentence (with `<b>` highlight, for back)
13. `Sentence4English` — Card 4 English translation
14. `Sentence4WordContext` — Target word's contextual translation in Card 4
15. `Sentence5` — Card 5 sentence (target language, for back text display)
16. `Sentence5Highlight` — Card 5 sentence (with `<b>` highlight, for back)
17. `Sentence5English` — Card 5 English translation
18. `Sentence5WordContext` — Target word's contextual translation in Card 5
19. `AudioWord` — `[sound:filename.mp3]` for isolated word pronunciation
20. `AudioSentence1` — `[sound:filename.mp3]` for sentence 1
21. `AudioSentence2` — `[sound:filename.mp3]` for sentence 2
22. `AudioSentence3` — `[sound:filename.mp3]` for sentence 3
23. `AudioSentence4` — `[sound:filename.mp3]` for sentence 4
24. `AudioSentence5` — `[sound:filename.mp3]` for sentence 5

**Card Templates:**

| Template | Front Shows | Back Shows |
|----------|-------------|------------|
| 1: Recognition | TargetWord + Sentence1 (highlighted) | EnglishTranslation + Sentence1English + AudioWord + AudioSentence1 |
| 2: Cloze | Sentence2Cloze + ClozeHint | Revealed word + Sentence2English + AudioSentence2 |
| 3: Production | EnglishTranslation only (no audio, no hints) | TargetWord + Sentence3 + Sentence3English + AudioWord + AudioSentence3 |
| 4: Comprehension | Sentence4 (no highlight) | Sentence4Highlight + Sentence4English + Sentence4WordContext + AudioSentence4 |
| 5: Listening | AudioSentence5 (auto-play, no text) | Sentence5Highlight + Sentence5English + Sentence5WordContext + AudioWord + AudioSentence5 |

**Audio placement rules (non-negotiable):**
- Cards 1–4: Audio on **back only**
- Card 5: Audio on **front** (sentence auto-play) and **back** (replay + isolated word)
- Card 3: **NEVER** audio on front — audio on a production card gives away the answer

**CSS guidelines (from `flashcard-philosophy.md` Section 7.3):**
- Target word highlights: bold + subtle color (not distracting)
- Card type label: small text at top ("Recognition", "Cloze", etc.)
- Generous font size for target language text (especially non-Latin scripts)
- English text visually secondary (smaller, lighter color)
- Audio buttons large and obvious on Card 5 front

---

## Key Design Decisions

### Vocabulary Only

FlashForge generates vocabulary flashcards exclusively. Grammar cards, reading comprehension cards, and dialogue cards are explicitly out of scope. See `flashcard-philosophy.md` Section 8 for the rationale. This simplifies the data model, the LLM prompts, the TUI, and the Anki note type.

### All 5 Cards Always Generated by LLM

Even when the user selects only a subset of card types, the LLM generates all 5. The selection is applied at export time by the deck builder. This keeps the schema stable, lets users change their mind without re-running the pipeline, and simplifies the prompts.

### Rebuild-Everything on Export

When the user hits "Export Deck," the system:
1. Reads `cards.json` (the source of truth)
2. Reads `meta.json` for card type selection and audio settings
3. Generates TTS for enabled card types with `generate_audio: True` (skipping existing files)
4. Builds genanki notes, creating only Anki cards for enabled card types
5. Packages into `.apkg`

For a chapter-sized deck (~15–30 words), the full rebuild takes seconds for notes. TTS is the only expensive part, and hash-based file naming handles caching.

### Stable IDs Everywhere

- **Project folders:** Named by the user
- **Vocab entry IDs:** UUIDs assigned during LLM structuring (Step 3), preserved through edits
- **Anki GUIDs:** Derived from vocab entry ID + card type number
- **Audio filenames:** `{md5(text)[:12]}.mp3`
- **Deck IDs:** Hash of deck name

### Input Size Limit

Hard cap at ~15,000 characters. Intentional, not just a technical constraint. Smaller focused decks > massive unfocused ones.

### Schema Versioning

`cards.json` and `meta.json` both include `schema_version`. On load, check version. If older than current, run migration. Start with version 1.

---

## Packaging & Distribution

### pyproject.toml

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "flashforge"
version = "0.1.0"
description = "Generate pedagogically-structured Anki vocabulary decks from educational text"
requires-python = ">=3.10"
dependencies = [
    "textual>=0.40",
    "genanki>=0.13",
    "openai>=1.0",
    "pymupdf>=1.23",
    "pydantic>=2.0",
    "python-dotenv>=1.0",
]

[project.scripts]
flashforge = "flashforge.cli:main"
```

### User Install Flow

```bash
git clone https://github.com/you/flashforge.git
cd flashforge
pip install .
# Copy .env.example to .env, add API key
flashforge
```

---

## Phases

### Phase 1: Foundation

**Goal:** Core data models, project management, and basic file parsing — no LLM, no TUI yet.

**Build:**
- [ ] Project scaffolding (`pyproject.toml`, directory structure, `__main__.py`)
- [ ] Pydantic models in `core/models.py` — `FlashForgeCards`, `VocabEntry`, all card type models, `ProjectMeta`, `CardTypeSelection` (matching the schema in this document)
- [ ] Project manager in `core/project.py` — create, save, load, list projects in `~/.flashforge/projects/`
- [ ] Text parser in `core/parser.py` — extract text from `.txt` and `.pdf` (using pymupdf), enforce character limit
- [ ] Past vocabulary parser — parse `.txt` file into word list (split on newlines/commas/tabs, strip whitespace)
- [ ] `.env.example` file and dotenv loading for `OPENAI_API_KEY`
- [ ] Schema version field in all JSON files

**Manual Tests:**
1. Run `pip install -e .` from the repo root. Confirm `flashforge` command is available.
2. Create a test `.txt` file with ~500 characters. Call `parser.extract("test.txt")`. Confirm it returns the text content.
3. Create a test `.pdf` with text content. Call `parser.extract("test.pdf")`. Confirm extracted text is readable.
4. Call `parser.extract()` on a file exceeding 15,000 characters. Confirm it raises an appropriate error or returns a truncation warning.
5. Create a project via `ProjectManager.create(...)`. Confirm project folder exists with `source.txt` and `meta.json`.
6. Load the project back. Confirm the returned `ProjectMeta` object matches what was saved, including default `card_types` (all True).
7. Test past vocabulary parsing with various formats (one-per-line, comma-separated, mixed). Confirm correct word list extraction.
8. Validate that `meta.json` contains `"schema_version": 1` and `"card_types"` with all 5 booleans.

---

### Phase 2: LLM Pipeline

**Goal:** Three-prompt pipeline that takes extracted text and returns validated, structured card JSON.

**Build:**
- [ ] LLM client wrapper in `core/llm.py` — handles OpenAI API calls, error handling, retries
- [ ] Prompt 1 template in `prompts/card_drafting.txt` — pedagogical card drafting with sentence generation constraints from `flashcard-philosophy.md` Section 6.3
- [ ] Prompt 2 template in `prompts/card_review.txt` — quality review with review checklist from `flashcard-philosophy.md` Section 6.3
- [ ] Prompt 3 template in `prompts/structuring.txt` — JSON structuring with exact schema
- [ ] Pipeline function: `generate_cards(source_text: str, available_vocab_context: str) -> FlashForgeCards` — runs all 3 prompts in sequence
- [ ] Step 2 receives both Step 1 output AND original source text for cross-reference
- [ ] Pydantic validation of Step 3 output with one automatic retry on failure (append error to prompt)
- [ ] Save result as `cards.json` in the project folder
- [ ] Update `meta.json` status to `generated` and populate `vocab_count`

**Manual Tests:**
1. Set `OPENAI_API_KEY` in `.env`. Run pipeline with a short sample text (~500 chars of language textbook content). Confirm it returns a valid `FlashForgeCards` object.
2. Inspect returned vocabulary entries — confirm each has all 5 card blocks populated with different sentences.
3. Inspect cloze cards — confirm `sentence_cloze` contains proper `{{c1::...}}` syntax and `english_hint` is present.
4. Inspect `audio_queries` — confirm no HTML, no cloze syntax, no English text.
5. Run with past vocabulary context included. Confirm sentences use some past vocabulary words.
6. Reload `cards.json` with Pydantic: `FlashForgeCards.model_validate_json(...)`. Confirm it parses without errors.
7. Feed deliberately malformed text. Confirm graceful handling.
8. Test retry logic: temporarily break the structuring prompt to produce invalid JSON. Confirm retry.

---

### Phase 3: TTS Integration

**Goal:** Generate audio files from card content using OpenAI TTS with caching and resume support.

**Build:**
- [ ] TTS generator in `core/tts.py` — wraps OpenAI TTS API (`gpt-4o-mini-tts`)
- [ ] Hash-based filename generation: `{md5(text)[:12]}.mp3`
- [ ] Skip existing files (resume support)
- [ ] Respect audio toggles: project-level, per-word, and card-type-level
- [ ] Only generate audio for sentences belonging to enabled card types
- [ ] Generate isolated word audio if any card type using it is enabled (Cards 1, 3, or 5)
- [ ] Configurable delay between requests (default: ~1s)
- [ ] Batch generation function: takes `FlashForgeCards` + `CardTypeSelection`, returns `audio_map: Dict[str, str]`
- [ ] Error handling: log failures per-file, continue, return summary

**Manual Tests:**
1. Generate single audio file. Confirm `.mp3` is created and playable.
2. Call again with same text. Confirm it skips (file exists).
3. Generate batch for a small project (~5 words). Confirm expected `.mp3` files created.
4. Set a word's `generate_audio = False`. Rerun. Confirm that word's audio is skipped.
5. Set project-level `generate_audio = False`. Rerun. Confirm zero audio generated.
6. Disable Card 3 in `card_types`. Rerun. Confirm `sentence_3` audio is not generated.
7. Simulate a failure. Confirm batch continues and summary reports failures.
8. Rerun after fixing. Confirm only failed files are regenerated.

---

### Phase 4: Deck Builder

**Goal:** Take `cards.json` + `meta.json` + audio files and produce a working `.apkg` file.

**Build:**
- [ ] Anki note model in `templates/anki_models.py` — `FlashForge Vocab` note type with 24 fields, 5 card templates, CSS (per `flashcard-philosophy.md` Section 7)
- [ ] Deck builder in `core/deck_builder.py` — reads `FlashForgeCards`, creates genanki notes
- [ ] Card type filtering: only create Anki cards for types enabled in `meta.json.card_types`
- [ ] Stable GUID generation from vocab entry ID + card type number
- [ ] Stable deck ID from deck name hash
- [ ] Audio file inclusion — only include files that exist on disk
- [ ] Output to project's `output/` directory

**Manual Tests:**
1. Build deck with all 5 card types enabled. Import into Anki. Confirm 5 cards per word.
2. Disable Card 3. Rebuild. Import. Confirm only 4 cards per word, no production cards.
3. Confirm audio plays on correct card sides (back for 1–4, front for 5).
4. Confirm Card 3 has NO audio on front.
5. Confirm Card 5 auto-plays audio on front.
6. Edit a word in `cards.json`. Rebuild. Re-import. Confirm edit appears, no duplicates (stable GUIDs).
7. Rebuild without changes. Re-import. Confirm no duplicates.
8. Build with zero audio (project toggle off). Confirm valid `.apkg` imports cleanly.

---

### Phase 5: TUI — Shell & Navigation

**Goal:** Basic Textual app with screen navigation. No functionality wired yet — just screens and transitions.

**Build:**
- [ ] Main Textual app in `tui/app.py` with screen routing
- [ ] Home screen (`tui/screens/home.py`) — project list display, new project button, quit
- [ ] Import screen (`tui/screens/import_screen.py`) — text input fields for project name and file path, text preview area, character counter, continue button
- [ ] Config screen (`tui/screens/config_screen.py`) — card type checkboxes, past vocab file field, level description, generate button
- [ ] Review screen (`tui/screens/review.py`) — vocabulary list, expandable card editor per word, export button
- [ ] Export screen (`tui/screens/export.py`) — progress bar, status text, completion summary
- [ ] Screen transitions: Home → Import → Config → Review → Export, with Back navigation
- [ ] App launch from CLI entry point: `flashforge` command opens the TUI

**Manual Tests:**
1. Run `flashforge`. Confirm TUI launches with Home screen.
2. Navigate through all screens: Home → Import → Config → Review → Export.
3. Confirm Back navigation works from each screen.
4. Press `Q` on Home. Confirm clean exit.
5. Confirm card type checkboxes render and toggle on Config screen.
6. Resize terminal. Confirm TUI reflows without crashing.

---

### Phase 6: TUI — Wire Everything Together

**Goal:** Connect core pipeline to TUI screens. Full working application.

**Build:**
- [ ] Home screen: load and display real projects from `~/.flashforge/projects/`
- [ ] Import screen: real file path input, PDF/text extraction with preview, character count enforcement, transitions to Config
- [ ] Config screen: card type checkboxes save to `meta.json`, past vocabulary file upload parses and saves to project folder, level description saves, "Generate" triggers 3-step LLM pipeline with loading indicator, transitions to Review
- [ ] Review screen: load `cards.json` into vocabulary list, expand word to edit all 5 card blocks, disabled card types shown dimmed, per-word audio toggle, deck name editing, delete word, auto-save edits to disk
- [ ] Export screen: TTS generation respecting card type selection, deck building with card type filtering, progress bar, completion summary, error handling
- [ ] Session persistence: opening existing project loads current state

**Manual Tests:**
1. Full end-to-end: Launch → New Project → enter name/file → text preview → Config → select card types 1,2,5 → upload past vocab → Generate → Review → verify cards → Export → confirm .apkg.
2. Import into Anki. Confirm only Cards 1, 2, and 5 are present (no 3 or 4).
3. Edit a word's sentence. Navigate away and back. Confirm edit persisted.
4. Toggle audio off for one word. Confirm toggle saves.
5. Quit and relaunch. Confirm project appears with correct status and all edits intact.
6. Re-export with different card type selection. Confirm deck reflects new selection.
7. Test with PDF input. Confirm extraction and full pipeline work.
8. Test exceeding 15,000 characters. Confirm UI blocks generation.
9. Test with no API key. Confirm clear error message.
10. Test with past vocabulary file. Confirm sentences use past vocabulary words where appropriate.

---

### Phase 7: Polish & Release Prep

**Goal:** Error handling, edge cases, documentation, and clean release.

**Build:**
- [ ] Comprehensive error handling: network failures, malformed PDFs, API errors, disk full, invalid JSON
- [ ] Clear error messages in TUI (not stack traces)
- [ ] `README.md` — project description, screenshots/GIF of TUI, install instructions, usage guide, link to `flashcard-philosophy.md`
- [ ] `docs/getting-started.md` — step-by-step first-run guide including API key setup
- [ ] `.env.example` with instructions
- [ ] Handle edge case: user deletes project folder externally
- [ ] Handle edge case: `cards.json` manually corrupted — show validation error, offer to regenerate
- [ ] Handle edge case: past vocab file with encoding issues — show clear error
- [ ] Confirm `pip install .` works on macOS and Linux
- [ ] `--version` flag
- [ ] License file

**Manual Tests:**
1. Fresh clone → `pip install .` → `flashforge`. Confirm clean launch.
2. Follow `getting-started.md` exactly. Confirm zero-to-apkg works.
3. Disconnect internet mid-TTS. Confirm clear error and retry works.
4. Delete `cards.json` externally. Open project. Confirm helpful error.
5. Run `flashforge --version`. Confirm version prints.
6. Have someone unfamiliar follow the README. Note friction points.
