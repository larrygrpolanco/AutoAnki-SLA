# AutoAnki

A TUI-based tool that transforms educational text content into pedagogically-structured Anki flashcard decks with high-quality TTS audio. Built for serious language learners who want effective, research-backed vocabulary acquisition.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## What is AutoAnki?

AutoAnki generates **five different flashcard types** for every vocabulary word, each targeting a distinct dimension of word knowledge:

1. **Recognition** – See the word, recall the meaning
2. **Cloze** – Fill in the blank from context + hint
3. **Production** – See English, produce the target word
4. **Sentence Comprehension** – Read full sentence, understand the word in context
5. **Listening** – Hear the word, understand it

Each card uses a **unique example sentence**, giving you 5 distinct contextual encounters with every word—the research-backed minimum needed for stable vocabulary acquisition.


## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/autoanki.git
cd autoanki

# Install the package
pip install .

# Set up your API key
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Usage

```bash
# Launch the TUI
autoanki
```

1. **Create a new project** – Name it and select your source file (PDF or TXT)
2. **Review extracted text** – Preview and verify the content
3. **Configure settings** – Choose which card types to generate, optionally upload past vocabulary
4. **Generate cards** – The LLM creates 5 cards per word following pedagogical constraints
5. **Review and edit** – Customize sentences, translations, or remove unwanted words
6. **Export to Anki** – Generate audio and build your `.apkg` deck

## Project Structure

```
autoanki/
├── pyproject.toml           # Package configuration
├── README.md               # This file
├── .env.example            # API key template
├── prompts/                # LLM prompt files
│   ├── card_drafting.txt   # Step 1: Pedagogical drafting
│   ├── card_review.txt     # Step 2: Quality review
│   └── structuring.txt     # Step 3: JSON structuring
├── src/
│   └── autoanki/           # Main package
│       ├── __init__.py
│       ├── __main__.py     # Entry point
│       ├── cli.py          # Command-line interface
│       ├── core/           # Core logic
│       │   ├── models.py   # Pydantic data models
│       │   ├── parser.py   # PDF/text extraction
│       │   ├── llm.py      # LLM pipeline
│       │   ├── tts.py      # TTS generation
│       │   ├── deck_builder.py  # Anki deck creation
│       │   └── project.py  # Project management
│       ├── templates/      # Anki templates
│       │   └── anki_models.py
│       └── tui/            # Textual UI
│           ├── app.py
│           └── screens/
├── tests/                  # Test suite
└── docs/                   # Documentation
    ├── getting-started.md
    └── anki-css-styling.md
```

## User Data

AutoAnki stores your projects in `~/.autoanki/projects/`:

```
~/.autoanki/
├── config.toml             # User preferences (optional)
└── projects/
    └── <project-name>/
        ├── source.txt      # Extracted text
        ├── past_vocab.txt  # Optional past vocabulary
        ├── cards.json      # Flashcard data (source of truth)
        ├── meta.json       # Project metadata
        ├── audio/          # Generated MP3 files
        └── output/         # Final .apkg files
```

## Documentation

- [Getting Started](docs/getting-started.md) – Step-by-step first-run guide
- [Flashcard Philosophy](Flashcard-Philosophy.md) – Pedagogical rationale and design principles
- [Anki CSS Styling](docs/anki-css-styling.md) – Card template customization guide
- [Technical Plan](AutoAnki-SLA-technical-plan.md) – Implementation details and architecture

## Requirements

- Python 3.10+
- OpenAI API key (for LLM and TTS)
- Anki desktop or mobile app (to import .apkg files)

## Pedagogical Foundation

AutoAnki is built on established second language acquisition research:

- **Nation (2013)**: 18 dimensions of word knowledge across form, meaning, and use
- **Krashen's i+1**: Learners need 90–98% known vocabulary for acquisition
- **Webb (2007)**: 8–12 encounters needed for stable mental representation
- **Karpicke & Roediger (2008)**: Retrieval practice dramatically outperforms passive review
- **Barcroft (2004)**: Multimodal presentation improves retention

See [Flashcard-Philosophy.md](Flashcard-Philosophy.md) for detailed citations and rationale.

## Card Types Explained

### Card 1: Recognition
**Front**: Target word + highlighted sentence  
**Back**: English translation + audio  
**Tests**: Can I recognize this word and know its meaning?

### Card 2: Cloze (Contextual Recall)
**Front**: Sentence with blank + English hint  
**Back**: Revealed word + translation + audio  
**Tests**: Can I produce the word from context + meaning?

### Card 3: Production
**Front**: English word only (no audio!)  
**Back**: Target word + new sentence + audio  
**Tests**: Can I recall the target word from English?

### Card 4: Sentence Comprehension
**Front**: Full sentence (no highlight)  
**Back**: Highlighted word + translation + audio  
**Tests**: Can I understand the word in natural context?

### Card 5: Listening
**Front**: Audio only (auto-plays)  
**Back**: Full text + highlighted word + replay audio  
**Tests**: Can I understand the spoken word?

## Limitations & Constraints

- **Input size**: ~15,000 characters maximum (chapter-sized chunks)
- **Vocabulary only**: Grammar cards and dialogue cards are out of scope
- **No romanization**: Target script only (develops reading fluency)
- **No images**: Text + audio only

These are intentional design choices, not technical limitations.

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on code style, testing, and the pull request process.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Textual](https://textual.textualize.io/) for the TUI
- Deck generation via [genanki](https://github.com/kerrickstaley/genanki)
- TTS powered by [OpenAI](https://platform.openai.com/)

---

**Built for learners who want to actually acquire vocabulary, not just memorize it.**
