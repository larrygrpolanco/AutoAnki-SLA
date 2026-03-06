"""Anki note model definitions with 5 card templates."""

from __future__ import annotations

import genanki

# Stable model ID - must remain constant across all deck generations
# Using a hash of "AutoAnki Vocab" to get a consistent 32-bit integer
MODEL_ID = 1684351209  # hash("AutoAnki Vocab") % 2**31

# Model name
MODEL_NAME = "AutoAnki Vocab"

# Field definitions (24 fields total)
FIELDS = [
    # Basic word info (1-3)
    {"name": "TargetWord"},
    {"name": "EnglishTranslation"},
    {"name": "PartOfSpeech"},
    # Card 1: Recognition (4-5)
    {"name": "Sentence1"},
    {"name": "Sentence1English"},
    # Card 2: Cloze (6-8)
    {"name": "Sentence2Cloze"},
    {"name": "Sentence2English"},
    {"name": "ClozeHint"},
    # Card 3: Production (9-10)
    {"name": "Sentence3"},
    {"name": "Sentence3English"},
    # Card 4: Comprehension (11-14)
    {"name": "Sentence4"},
    {"name": "Sentence4Highlight"},
    {"name": "Sentence4English"},
    {"name": "Sentence4WordContext"},
    # Card 5: Listening (15-18)
    {"name": "Sentence5"},
    {"name": "Sentence5Highlight"},
    {"name": "Sentence5English"},
    {"name": "Sentence5WordContext"},
    # Audio fields (19-24)
    {"name": "AudioWord"},
    {"name": "AudioSentence1"},
    {"name": "AudioSentence2"},
    {"name": "AudioSentence3"},
    {"name": "AudioSentence4"},
    {"name": "AudioSentence5"},
]

# CSS shared across all cards
CSS = """
/* Base styles */
.card {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans", "Helvetica Neue", Arial, sans-serif;
    font-size: 28px;
    text-align: center;
    color: #2c3e50;
    background-color: #fafafa;
    padding: 20px;
    line-height: 1.6;
}

/* Target language - large and prominent */
.target-lang {
    font-size: 32px;
    font-weight: 500;
    color: #1a1a1a;
    margin-bottom: 16px;
}

/* English text - secondary, smaller */
.english {
    font-size: 20px;
    color: #7f8c8d;
    margin-top: 12px;
}

/* Highlighted words */
highlight {
    font-weight: bold;
    color: #2980b9;
}

b, strong {
    font-weight: bold;
    color: #2980b9;
}

/* Card type label */
.card-type {
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #95a5a6;
    margin-bottom: 16px;
}

/* Cloze deletion styling */
.cloze {
    font-weight: bold;
    color: #2980b9;
}

/* Hint styling */
.hint {
    font-size: 18px;
    color: #7f8c8d;
    font-style: italic;
    margin-top: 8px;
}

/* Audio button styling */
.replay-button {
    width: 60px;
    height: 60px;
    font-size: 24px;
}

/* Listening card front - large audio */
.listening-front .replay-button {
    width: 80px;
    height: 80px;
    font-size: 36px;
}

/* Mobile responsiveness */
@media (max-width: 600px) {
    .card {
        font-size: 24px;
        padding: 12px;
    }
    .target-lang {
        font-size: 28px;
    }
    .english {
        font-size: 18px;
    }
}
"""

# Card 1: Recognition
CARD_1_NAME = "Recognition"
CARD_1_FRONT = """
<div class="card-type">Recognition</div>
<div class="target-lang">{{TargetWord}}</div>
<div class="target-lang">{{Sentence1}}</div>
"""
CARD_1_BACK = """
<div class="card-type">Recognition</div>
<div class="target-lang">{{TargetWord}}</div>
<div class="target-lang">{{Sentence1}}</div>
<hr>
<div class="english">{{EnglishTranslation}}</div>
<div class="english">{{Sentence1English}}</div>
<div>{{AudioWord}}</div>
<div>{{AudioSentence1}}</div>
"""

# Card 2: Contextual Recall (Cloze)
CARD_2_NAME = "Cloze"
CARD_2_FRONT = """
<div class="card-type">Cloze</div>
<div class="target-lang">{{Sentence2Cloze}}</div>
<div class="hint">{{ClozeHint}}</div>
"""
CARD_2_BACK = """
<div class="card-type">Cloze</div>
<div class="target-lang">{{Sentence2Cloze}}</div>
<div class="hint">{{ClozeHint}}</div>
<hr>
<div class="target-lang">{{EnglishTranslation}}</div>
<div class="english">{{Sentence2English}}</div>
<div>{{AudioSentence2}}</div>
"""

# Card 3: Production
CARD_3_NAME = "Production"
CARD_3_FRONT = """
<div class="card-type">Production</div>
<div class="english">{{EnglishTranslation}}</div>
"""
CARD_3_BACK = """
<div class="card-type">Production</div>
<div class="english">{{EnglishTranslation}}</div>
<hr>
<div class="target-lang">{{TargetWord}}</div>
<div class="target-lang">{{Sentence3}}</div>
<div class="english">{{Sentence3English}}</div>
<div>{{AudioWord}}</div>
<div>{{AudioSentence3}}</div>
"""

# Card 4: Sentence Comprehension
CARD_4_NAME = "Comprehension"
CARD_4_FRONT = """
<div class="card-type">Comprehension</div>
<div class="target-lang">{{Sentence4}}</div>
"""
CARD_4_BACK = """
<div class="card-type">Comprehension</div>
<div class="target-lang">{{Sentence4}}</div>
<hr>
<div class="target-lang">{{Sentence4Highlight}}</div>
<div class="english">{{Sentence4English}}</div>
<div class="english">Word meaning: {{Sentence4WordContext}}</div>
<div>{{AudioSentence4}}</div>
"""

# Card 5: Listening
CARD_5_NAME = "Listening"
CARD_5_FRONT = """
<div class="card-type listening-front">Listening</div>
<div>{{AudioSentence5}}</div>
"""
CARD_5_BACK = """
<div class="card-type">Listening</div>
<div>{{AudioSentence5}}</div>
<hr>
<div class="target-lang">{{Sentence5Highlight}}</div>
<div class="english">{{Sentence5English}}</div>
<div class="english">Word meaning: {{Sentence5WordContext}}</div>
<div>{{AudioWord}}</div>
"""

# All templates
TEMPLATES = [
    {
        "name": CARD_1_NAME,
        "qfmt": CARD_1_FRONT,
        "afmt": CARD_1_BACK,
    },
    {
        "name": CARD_2_NAME,
        "qfmt": CARD_2_FRONT,
        "afmt": CARD_2_BACK,
    },
    {
        "name": CARD_3_NAME,
        "qfmt": CARD_3_FRONT,
        "afmt": CARD_3_BACK,
    },
    {
        "name": CARD_4_NAME,
        "qfmt": CARD_4_FRONT,
        "afmt": CARD_4_BACK,
    },
    {
        "name": CARD_5_NAME,
        "qfmt": CARD_5_FRONT,
        "afmt": CARD_5_BACK,
    },
]


def create_note_model() -> genanki.Model:
    """Create the AutoAnki Vocab note model.

    Returns:
        genanki.Model with 24 fields and 5 card templates
    """
    return genanki.Model(
        model_id=MODEL_ID,
        name=MODEL_NAME,
        fields=FIELDS,
        templates=TEMPLATES,
        css=CSS,
    )


def get_model() -> genanki.Model:
    """Get the singleton model instance.

    This is a convenience function that always returns the same model.
    """
    return create_note_model()
