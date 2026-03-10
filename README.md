# AutoAnki

AutoAnki turns a PDF or text file into a ready-to-import Anki vocabulary deck. Drop in a chapter from your textbook, and it extracts the vocabulary, writes five unique example sentences per word, generates TTS audio, and packages everything as an `.apkg` file.

Built on second language acquisition research: comprehensible input (Krashen's i+1), spaced retrieval practice, and scaffolded card types that move from recognition to production.

---

## What You Get

Each vocabulary word produces **5 cards** from a single Anki note, each with its own example sentence:

| Card | What it tests | Front | Back |
|------|--------------|-------|------|
| 1 — Recognition | See the word → recall its meaning | Word + highlighted sentence | English translation + audio |
| 2 — Fill in Blank | Recall the word from context | Gapped sentence + English hint | Complete sentence + audio |
| 3 — Production | English → produce the target word | English only (no audio) | Word + new sentence + audio |
| 4 — Comprehension | Read a sentence → understand usage | Plain sentence | Translation + word in context + audio |
| 5 — Listening | Hear a sentence → understand | Auto-play audio | Written sentence + audio |

---

## Prerequisites

- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys) (used for the LLM pipeline and TTS audio)

---

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-username/AutoAnki-SLA.git
cd AutoAnki-SLA

# 2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install
pip install -e .

# 4. Add your API key
cp .env.example .env
# Open .env and set: OPENAI_API_KEY=sk-your-key-here
```

---

## Usage

### 1. Add your lesson file

Drop a `.pdf` or `.txt` file into the `Lessons/` folder.

```
Lessons/
  chapter5_shopping.pdf
  lesson7_food.txt
```

Optionally, add a `.txt` file of previously learned words to `PreviousVocab/`. The LLM will use those words in example sentences so your old vocabulary gets incidental review alongside the new.

```
PreviousVocab/
  korean_ch1-4.txt    # one word per line, or comma/tab-separated
```

### 2. Run

```bash
autoanki
```

The CLI walks you through each step:

1. **Select lesson file** — choose from `Lessons/` with arrow keys
2. **Select past vocabulary** — choose from `PreviousVocab/` or skip
3. **LLM pipeline** — 3-step process runs with a live spinner (takes 1–3 minutes)
4. **Pick vocabulary** — all words shown with translation and part of speech; uncheck anything you don't want
5. **Pick card types** — all 5 types on by default; uncheck any you want to skip
6. **Confirm deck name** — auto-filled from the source material, editable
7. **Export** — TTS audio generates, deck builds, `.apkg` saved to `Output/`

### 3. Import into Anki

Open Anki → **File → Import** → select the `.apkg` from `Output/`.

---

## Folder Structure

```
AutoAnki-SLA/
├── Lessons/               ← put your lesson PDFs and TXTs here
├── PreviousVocab/         ← optional: past vocabulary .txt files
├── Output/                ← generated .apkg files appear here
│
├── src/autoanki/
│   ├── cli.py             ← CLI interface (Rich + questionary)
│   ├── llm.py             ← 3-step LLM pipeline
│   ├── tts.py             ← OpenAI TTS audio generation
│   ├── deck_builder.py    ← genanki deck assembly + Anki CSS templates
│   ├── models.py          ← Pydantic data models
│   ├── parser.py          ← PDF/text extraction
│   └── prompts/
│       ├── card_drafting.txt   ← Step 1: extract vocab + write sentences
│       ├── card_review.txt     ← Step 2: i+1 quality check
│       └── structuring.txt     ← Step 3: convert to validated JSON
│
├── tests/
│   └── test_pipeline.py   ← run the LLM pipeline without the CLI
└── pyproject.toml
```

---

## Customization

### Changing the language or difficulty

The prompts in `src/autoanki/prompts/` are plain text files — edit them directly.

- **`card_drafting.txt`** — controls how vocabulary is extracted and how sentences are written. Adjust the sentence length rules, difficulty level, or add language-specific instructions here.
- **`card_review.txt`** — the quality-check step. Add extra criteria if needed.
- **`structuring.txt`** — converts reviewed content to JSON. Includes the full schema and an example. Rarely needs editing.

### Changing the LLM model

In `src/autoanki/llm.py`, the default model is `gpt-4o-mini`. Change the `model` parameter in `run_pipeline()` to use a different OpenAI model.

### Changing the TTS voice

In `src/autoanki/tts.py`, `generate_audio_batch()` defaults to `voice="alloy"`. OpenAI TTS supports: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`.

### Changing card styling

The CSS and HTML card templates are in `src/autoanki/deck_builder.py` (the `CSS` and `ALL_TEMPLATES` constants). The full styling reference is in [anki-css-styling.md](anki-css-styling.md).

### Input size limit

The LLM pipeline handles up to **15,000 characters** of source text. For longer chapters, split the text into sections or summarize it first. The CLI warns you if your file exceeds this limit.

---

## Running the Pipeline Without the CLI

Useful for testing or scripting:

```bash
python -m tests.test_pipeline path/to/file.txt
# Outputs: test_output.apkg and test_output.json
```

---

## How It Works

```
Lesson file (PDF or TXT)
    │
    ▼
extract_text()           — pymupdf for PDF, plain read for TXT
    │
    ▼
run_pipeline()           — 3 LLM calls via OpenAI API
  Step 1: Draft          — extract vocabulary, write 5 sentences per word
  Step 2: Review         — check i+1 rule, fix ambiguous cloze, ensure sentence variety
  Step 3: Structure      — convert to validated JSON (Pydantic)
    │
    ▼
User selects             — which words, which card types, deck name
    │
    ▼
generate_audio_batch()   — OpenAI TTS, MD5-hash filenames for deduplication
    │
    ▼
build_deck_with_audio()  — genanki assembles the .apkg with bundled audio
    │
    ▼
Output/DeckName.apkg
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `rich` | Terminal display (panels, progress bars, spinners) |
| `questionary` | Interactive prompts (selection lists, checkboxes) |
| `openai` | LLM pipeline (gpt-4o-mini) + TTS audio |
| `genanki` | Anki `.apkg` file generation |
| `pymupdf` | PDF text extraction |
| `pydantic` | JSON schema validation |
| `python-dotenv` | `.env` API key loading |

---

## Cost Estimate

For a typical lesson (10–15 vocabulary words):

| Step | Model | Approximate cost |
|------|-------|-----------------|
| LLM pipeline (3 steps) | gpt-4o-mini | ~$0.01–0.03 |
| TTS audio (6 files × 15 words) | tts-1 | ~$0.05–0.10 |

Total: roughly **$0.06–0.13 per lesson deck**.
