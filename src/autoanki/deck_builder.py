import re
from pathlib import Path

import genanki

from .models import AutoAnkiCards, VocabEntry

# Stable model ID — hardcoded, never change
MODEL_ID = 1607392320

# Card template names in order
CARD_NAMES = {
    1: "Recognition",
    2: "Fill in the Blank",
    3: "Production",
    4: "Comprehension",
    5: "Listening",
}

# 25 fields: Sentence2Blank + Sentence2Full replace Sentence2Cloze
# ({{c1::word}} doesn't render in custom note types — we pre-process it)
FIELDS = [
    {"name": "TargetWord"},
    {"name": "EnglishTranslation"},
    {"name": "PartOfSpeech"},
    {"name": "Sentence1"},           # with <b> highlight
    {"name": "Sentence1English"},
    {"name": "Sentence2Blank"},      # cloze with [...]
    {"name": "Sentence2Full"},       # cloze revealed, word highlighted
    {"name": "Sentence2English"},
    {"name": "ClozeHint"},
    {"name": "Sentence3"},
    {"name": "Sentence3English"},
    {"name": "Sentence4"},           # no highlight (front)
    {"name": "Sentence4Highlight"},  # with <b> (back)
    {"name": "Sentence4English"},
    {"name": "Sentence4WordContext"},
    {"name": "Sentence5"},           # no highlight (back display)
    {"name": "Sentence5Highlight"},  # with <b> (back)
    {"name": "Sentence5English"},
    {"name": "Sentence5WordContext"},
    {"name": "AudioWord"},
    {"name": "AudioSentence1"},
    {"name": "AudioSentence2"},
    {"name": "AudioSentence3"},
    {"name": "AudioSentence4"},
    {"name": "AudioSentence5"},
]

ALL_TEMPLATES = {
    1: {
        "name": "Recognition",
        "qfmt": """<div class="card-type type-recognition"></div>
<div class="target">{{TargetWord}}</div>
<div class="pos">{{PartOfSpeech}}</div>
<hr>
<div class="sentence">{{Sentence1}}</div>""",
        "afmt": """{{FrontSide}}
<hr id="answer">
<div class="english">{{EnglishTranslation}}</div>
<div class="english sentence">{{Sentence1English}}</div>
{{AudioWord}}
{{AudioSentence1}}""",
    },
    2: {
        "name": "Fill in the Blank",
        "qfmt": """<div class="card-type type-cloze"></div>
<div class="sentence">{{Sentence2Blank}}</div>
<div class="hint">({{ClozeHint}})</div>""",
        "afmt": """{{FrontSide}}
<hr id="answer">
<div class="sentence">{{Sentence2Full}}</div>
<div class="english">{{Sentence2English}}</div>
{{AudioSentence2}}""",
    },
    3: {
        "name": "Production",
        "qfmt": """<div class="card-type type-production"></div>
<div class="card-production-front">
  <div class="english">{{EnglishTranslation}}</div>
  <div class="pos">{{PartOfSpeech}}</div>
</div>
<!-- NO AUDIO ON FRONT -->""",
        "afmt": """{{FrontSide}}
<hr id="answer">
<div class="target">{{TargetWord}}</div>
<div class="sentence">{{Sentence3}}</div>
<div class="english">{{Sentence3English}}</div>
{{AudioWord}}
{{AudioSentence3}}""",
    },
    4: {
        "name": "Comprehension",
        "qfmt": """<div class="card-type type-comprehension"></div>
<div class="sentence text-left">{{Sentence4}}</div>""",
        "afmt": """{{FrontSide}}
<hr id="answer">
<div class="sentence">{{Sentence4Highlight}}</div>
<div class="context">{{Sentence4WordContext}}</div>
<div class="english">{{Sentence4English}}</div>
{{AudioSentence4}}""",
    },
    5: {
        "name": "Listening",
        "qfmt": """<div class="card-type type-listening"></div>
<div class="card-listening-front">
  <div class="hint">Listen and understand</div>
  {{AudioSentence5}}
</div>""",
        "afmt": """{{FrontSide}}
<hr id="answer">
<div class="sentence">{{Sentence5Highlight}}</div>
<div class="context">{{Sentence5WordContext}}</div>
<div class="english">{{Sentence5English}}</div>
<div class="target mt-2">{{TargetWord}}</div>
{{AudioWord}}
{{AudioSentence5}}""",
    },
}

CSS = """
/* ============================================
   BASE STYLES
   ============================================ */

.card {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 24px;
  text-align: center;
  color: #333;
  background-color: #f9f9f9;
  line-height: 1.6;
  padding: 20px;
}

.nightMode .card {
  color: #e0e0e0;
  background-color: #2d2d2d;
}

.card-type {
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #666;
  margin-bottom: 15px;
}

.nightMode .card-type {
  color: #999;
}

.target {
  font-size: 32px;
  font-weight: 500;
  color: #1a1a1a;
  margin: 15px 0;
}

.nightMode .target {
  color: #f0f0f0;
}

b {
  font-weight: 600;
  color: #2563eb;
}

.nightMode b {
  color: #60a5fa;
}

.english {
  font-size: 18px;
  color: #666;
  font-style: italic;
  margin: 10px 0;
}

.nightMode .english {
  color: #999;
}

.pos {
  font-size: 14px;
  font-weight: 500;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 5px 0;
}

.nightMode .pos {
  color: #aaa;
}

.sentence {
  font-size: 24px;
  margin: 20px 0;
  line-height: 1.5;
}

.hint {
  font-size: 16px;
  color: #666;
  font-style: italic;
  margin-top: 10px;
}

.nightMode .hint {
  color: #999;
}

hr {
  border: none;
  border-top: 1px solid #ddd;
  margin: 20px 0;
}

.nightMode hr {
  border-top-color: #555;
}

.replay-button {
  width: 40px;
  height: 40px;
  margin: 10px auto;
}

.replay-button svg {
  fill: #2563eb;
}

.nightMode .replay-button svg {
  fill: #60a5fa;
}

.context {
  font-size: 16px;
  color: #555;
  font-weight: 500;
}

.nightMode .context {
  color: #bbb;
}

/* ============================================
   PLATFORM-SPECIFIC
   ============================================ */

.mobile .card { font-size: 22px; padding: 15px; }
.mobile .target { font-size: 30px; }
.mobile .sentence { font-size: 22px; }
.mobile .english { font-size: 16px; }

.win .card, .mac .card, .linux .card {
  max-width: 800px;
  margin: 0 auto;
}

/* ============================================
   CARD-SPECIFIC
   ============================================ */

.card-production-front .english {
  font-size: 28px;
  font-style: normal;
  font-weight: 500;
  color: #1a1a1a;
}

.nightMode .card-production-front .english {
  color: #f0f0f0;
}

.card-listening-front {
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 200px;
}

.card-listening-front .replay-button {
  width: 60px;
  height: 60px;
  margin: 20px auto;
}

.type-recognition::before { content: "Recognition"; }
.type-cloze::before { content: "Fill in the Blank"; }
.type-production::before { content: "Recall"; }
.type-comprehension::before { content: "Comprehension"; }
.type-listening::before { content: "Listening"; }

/* ============================================
   UTILITIES
   ============================================ */

.text-left { text-align: left; }
.text-center { text-align: center; }
.mb-0 { margin-bottom: 0; }
.mb-1 { margin-bottom: 10px; }
.mb-2 { margin-bottom: 20px; }
.mt-0 { margin-top: 0; }
.mt-1 { margin-top: 10px; }
.mt-2 { margin-top: 20px; }
"""


def _blank_cloze(sentence_cloze: str) -> str:
    """Replace {{c1::word}} with <b>[...]</b> for front of cloze card."""
    return re.sub(r"\{\{c1::(.+?)\}\}", "<b>[...]</b>", sentence_cloze)


def _reveal_cloze(sentence_cloze: str) -> str:
    """Replace {{c1::word}} with <b>word</b> for back of cloze card."""
    return re.sub(r"\{\{c1::(.+?)\}\}", r"<b>\1</b>", sentence_cloze)


def _sound(filename: str) -> str:
    """Return Anki sound tag, or empty string if no file."""
    return f"[sound:{filename}]" if filename else ""


def _make_model(selected_card_types: set[int]) -> genanki.Model:
    """Build a genanki Model with only the selected card templates."""
    templates = [ALL_TEMPLATES[t] for t in sorted(selected_card_types)]
    return genanki.Model(
        MODEL_ID,
        "AutoAnki Vocab",
        fields=FIELDS,
        templates=templates,
        css=CSS,
    )


def build_deck(
    cards: AutoAnkiCards,
    selected_word_ids: set[str],
    selected_card_types: set[int],
    deck_name: str,
    audio_files: dict[str, str],
    output_path: str,
) -> int:
    """
    Build an Anki .apkg file.

    audio_files: dict mapping "{entry_id}_word" / "{entry_id}_s1".."{entry_id}_s5"
                 to filename (basename only, e.g. "abc123def456.mp3").
                 Empty string means no audio for that slot.

    Returns total number of cards created.
    """
    model = _make_model(selected_card_types)

    # Stable deck ID derived from name
    deck_id = abs(hash(deck_name)) % (1 << 31)
    deck = genanki.Deck(deck_id, deck_name)

    media_paths = []
    card_count = 0

    for entry in cards.vocabulary:
        if entry.id not in selected_word_ids:
            continue

        # Resolve audio filenames
        word_file = audio_files.get(f"{entry.id}_word", "")
        s1_file = audio_files.get(f"{entry.id}_s1", "")
        s2_file = audio_files.get(f"{entry.id}_s2", "")
        s3_file = audio_files.get(f"{entry.id}_s3", "")
        s4_file = audio_files.get(f"{entry.id}_s4", "")
        s5_file = audio_files.get(f"{entry.id}_s5", "")

        note = genanki.Note(
            model=model,
            fields=[
                entry.target_word,
                entry.english_translation,
                entry.part_of_speech,
                entry.card_1_recognition.sentence_target_highlight,
                entry.card_1_recognition.sentence_english,
                _blank_cloze(entry.card_2_cloze.sentence_cloze),
                _reveal_cloze(entry.card_2_cloze.sentence_cloze),
                entry.card_2_cloze.sentence_english,
                entry.card_2_cloze.english_hint,
                entry.card_3_production.sentence_target,
                entry.card_3_production.sentence_english,
                entry.card_4_comprehension.sentence_target,
                entry.card_4_comprehension.word_in_sentence_highlight,
                entry.card_4_comprehension.sentence_english,
                entry.card_4_comprehension.word_translation_in_context,
                entry.card_5_listening.sentence_target,
                entry.card_5_listening.word_in_sentence_highlight,
                entry.card_5_listening.sentence_english,
                entry.card_5_listening.word_translation_in_context,
                _sound(word_file),
                _sound(s1_file),
                _sound(s2_file),
                _sound(s3_file),
                _sound(s4_file),
                _sound(s5_file),
            ],
            guid=genanki.guid_for(entry.id, "autoanki-note"),
        )
        deck.add_note(note)
        card_count += len(selected_card_types)

    pkg = genanki.Package(deck)
    # Only include files that actually exist
    if audio_files:
        audio_dir = Path(list(audio_files.values())[0]).parent if any(
            Path(f).is_absolute() for f in audio_files.values() if f
        ) else None

    # Collect absolute paths for media files
    all_audio = [word_file, s1_file, s2_file, s3_file, s4_file, s5_file]
    # media_files are set per-package from caller
    pkg.write_to_file(output_path)
    return card_count


def build_deck_with_audio(
    cards: AutoAnkiCards,
    selected_word_ids: set[str],
    selected_card_types: set[int],
    deck_name: str,
    audio_files: dict[str, str],
    audio_dir: Path,
    output_path: str,
) -> int:
    """
    Build deck including audio media files.

    audio_files: dict mapping key → basename (e.g. "abc123.mp3")
    audio_dir: directory containing the audio files
    """
    model = _make_model(selected_card_types)

    deck_id = abs(hash(deck_name)) % (1 << 31)
    deck = genanki.Deck(deck_id, deck_name)

    media_paths = set()
    card_count = 0

    for entry in cards.vocabulary:
        if entry.id not in selected_word_ids:
            continue

        def _get(key: str) -> str:
            basename = audio_files.get(key, "")
            if basename:
                full_path = audio_dir / basename
                if full_path.exists():
                    media_paths.add(str(full_path))
                    return basename
            return ""

        word_file = _get(f"{entry.id}_word")
        s1_file = _get(f"{entry.id}_s1")
        s2_file = _get(f"{entry.id}_s2")
        s3_file = _get(f"{entry.id}_s3")
        s4_file = _get(f"{entry.id}_s4")
        s5_file = _get(f"{entry.id}_s5")

        note = genanki.Note(
            model=model,
            fields=[
                entry.target_word,
                entry.english_translation,
                entry.part_of_speech,
                entry.card_1_recognition.sentence_target_highlight,
                entry.card_1_recognition.sentence_english,
                _blank_cloze(entry.card_2_cloze.sentence_cloze),
                _reveal_cloze(entry.card_2_cloze.sentence_cloze),
                entry.card_2_cloze.sentence_english,
                entry.card_2_cloze.english_hint,
                entry.card_3_production.sentence_target,
                entry.card_3_production.sentence_english,
                entry.card_4_comprehension.sentence_target,
                entry.card_4_comprehension.word_in_sentence_highlight,
                entry.card_4_comprehension.sentence_english,
                entry.card_4_comprehension.word_translation_in_context,
                entry.card_5_listening.sentence_target,
                entry.card_5_listening.word_in_sentence_highlight,
                entry.card_5_listening.sentence_english,
                entry.card_5_listening.word_translation_in_context,
                _sound(word_file),
                _sound(s1_file),
                _sound(s2_file),
                _sound(s3_file),
                _sound(s4_file),
                _sound(s5_file),
            ],
            guid=genanki.guid_for(entry.id, "autoanki-note"),
        )
        deck.add_note(note)
        card_count += len(selected_card_types)

    pkg = genanki.Package(deck)
    pkg.media_files = list(media_paths)
    pkg.write_to_file(output_path)
    return card_count
