# AutoAnki Getting Started Guide

Welcome to AutoAnki! This guide will walk you through your first deck creation.

## Prerequisites

1. **Python 3.10+** installed
2. **Anki** desktop or mobile app installed
3. **OpenAI API key** ([Get one here](https://platform.openai.com/api-keys))

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/autoanki.git
cd autoanki

# Install the package
pip install .

# Set up your API key
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-api-key-here
```

## Quick Start

### 1. Launch AutoAnki

```bash
autoanki
```

You'll see the home screen with your projects.

### 2. Create a New Project

Press `N` or click "New Project":
- **Project Name**: e.g., `korean-ch5-shopping`
- **Source File**: Path to your textbook PDF or a .txt file with vocabulary

### 3. Review Extracted Text

AutoAnki will show you the extracted text. Verify it looks correct:
- Check that vocabulary words are present
- Ensure the text isn't garbled
- Note the character count (must be under 15,000)

### 4. Configure Settings

Choose which card types to generate:
- ☑ Recognition
- ☑ Cloze
- ☑ Production
- ☑ Sentence Comprehension
- ☑ Listening Comprehension

All are selected by default. Uncheck any you don't want.

**Optional**: Upload past vocabulary
- If you have a list of words you've already learned, upload it
- This helps the AI create better example sentences
- File format: one word per line, or comma-separated

### 5. Generate Cards

Click "Generate Cards". AutoAnki will:
1. Send your text to the AI (Step 1: Drafting)
2. Review the cards for quality (Step 2: Review)
3. Structure them into JSON (Step 3: Structuring)

This takes 30-60 seconds depending on text length.

### 6. Review and Edit

You'll see a list of all vocabulary words. Click any word to:
- Edit example sentences
- Change translations
- Toggle audio on/off for that word
- Delete the word if you don't want it

Changes auto-save to your project.

### 7. Export to Anki

Click "Export Deck":
- Audio files are generated (one per word + 5 sentences)
- Anki deck is built
- File saved to `~/.autoanki/projects/<name>/output/`

### 8. Import into Anki

1. Open Anki desktop or mobile
2. File → Import (or tap import on mobile)
3. Select the `.apkg` file from the output folder
4. Start studying!

## Tips for Best Results

### Input Text
- Use **chapter-sized chunks** (not entire books)
- Ensure the text is clean and readable
- PDFs work best when text is selectable (not scanned images)

### Card Types
- Start with all 5 types to see what works for you
- **Listening cards** are especially valuable for pronunciation
- **Production cards** are hardest but build active recall

### Past Vocabulary
- Upload vocab lists from previous chapters
- This gives the AI more words to use in example sentences
- Results in more natural, varied sentences

### Editing Cards
- Trust your instincts—if a sentence feels awkward, change it
- Keep sentences simple and concrete
- Ensure cloze blanks have only one possible answer

## Troubleshooting

### "Text extraction failed"
- Ensure your PDF has selectable text (not an image scan)
- Try converting to a .txt file first

### "API key error"
- Check that `.env` file exists in the project root
- Verify the key starts with `sk-`
- Ensure there are no spaces or quotes around the key

### "Cards not importing into Anki"
- Make sure you're importing the `.apkg` file, not `.json`
- Check that Anki is updated to the latest version

### "Audio not playing"
- Check that audio files exist in the `audio/` folder
- On mobile, ensure media is synced if using AnkiWeb

## Next Steps

- Read [Flashcard-Philosophy.md](../Flashcard-Philosophy.md) to understand the research behind the design
- Check out [anki-css-styling.md](anki-css-styling.md) to customize your card appearance
- See [AutoAnki-SLA-technical-plan.md](../AutoAnki-SLA-technical-plan.md) for technical details

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/autoanki/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/autoanki/discussions)

Happy learning!
