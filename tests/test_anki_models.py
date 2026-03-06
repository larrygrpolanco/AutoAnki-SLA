"""Tests for Anki model definitions."""

import pytest

from autoanki.templates.anki_models import (
    MODEL_ID,
    MODEL_NAME,
    FIELDS,
    TEMPLATES,
    CSS,
    CARD_1_NAME,
    CARD_2_NAME,
    CARD_3_NAME,
    CARD_4_NAME,
    CARD_5_NAME,
    create_note_model,
    get_model,
)


class TestModelConstants:
    """Tests for model constants."""

    def test_model_id_is_positive(self):
        """Model ID must be positive 32-bit integer."""
        assert MODEL_ID > 0
        assert MODEL_ID < 2**31

    def test_model_name(self):
        """Model name should be AutoAnki Vocab."""
        assert MODEL_NAME == "AutoAnki Vocab"

    def test_field_count(self):
        """Should have exactly 24 fields."""
        assert len(FIELDS) == 24

    def test_template_count(self):
        """Should have exactly 5 templates (one per card type)."""
        assert len(TEMPLATES) == 5

    def test_css_not_empty(self):
        """CSS should not be empty."""
        assert len(CSS) > 0
        assert ".card" in CSS


class TestFieldDefinitions:
    """Tests for field definitions."""

    def test_fields_have_names(self):
        """All fields must have 'name' key."""
        for field in FIELDS:
            assert "name" in field
            assert isinstance(field["name"], str)
            assert len(field["name"]) > 0

    def test_basic_word_info_fields(self):
        """First 3 fields are basic word info."""
        assert FIELDS[0]["name"] == "TargetWord"
        assert FIELDS[1]["name"] == "EnglishTranslation"
        assert FIELDS[2]["name"] == "PartOfSpeech"

    def test_audio_fields_at_end(self):
        """Last 6 fields should be audio fields."""
        audio_fields = FIELDS[-6:]
        names = [f["name"] for f in audio_fields]
        assert "AudioWord" in names
        assert "AudioSentence1" in names
        assert "AudioSentence2" in names
        assert "AudioSentence3" in names
        assert "AudioSentence4" in names
        assert "AudioSentence5" in names


class TestTemplates:
    """Tests for card templates."""

    def test_all_templates_have_required_keys(self):
        """All templates must have name, qfmt, and afmt."""
        for template in TEMPLATES:
            assert "name" in template
            assert "qfmt" in template
            assert "afmt" in template

    def test_card_names(self):
        """Templates should have correct names."""
        names = [t["name"] for t in TEMPLATES]
        assert CARD_1_NAME in names
        assert CARD_2_NAME in names
        assert CARD_3_NAME in names
        assert CARD_4_NAME in names
        assert CARD_5_NAME in names

    def test_card_1_structure(self):
        """Card 1 (Recognition) should show target word and sentence on front."""
        template = TEMPLATES[0]
        assert template["name"] == CARD_1_NAME
        assert "{{TargetWord}}" in template["qfmt"]
        assert "{{Sentence1}}" in template["qfmt"]
        # Back should have audio
        assert "{{AudioWord}}" in template["afmt"]
        assert "{{AudioSentence1}}" in template["afmt"]

    def test_card_2_structure(self):
        """Card 2 (Cloze) should show cloze deletion on front."""
        template = TEMPLATES[1]
        assert template["name"] == CARD_2_NAME
        assert "{{Sentence2Cloze}}" in template["qfmt"]
        assert "{{ClozeHint}}" in template["qfmt"]

    def test_card_3_structure(self):
        """Card 3 (Production) should show only English on front."""
        template = TEMPLATES[2]
        assert template["name"] == CARD_3_NAME
        # Front should only have English translation
        assert "{{EnglishTranslation}}" in template["qfmt"]
        # Front should NOT have audio (production card safety)
        assert "{{AudioWord}}" not in template["qfmt"]
        assert "{{AudioSentence3}}" not in template["qfmt"]
        # Back should have audio
        assert "{{AudioWord}}" in template["afmt"]
        assert "{{AudioSentence3}}" in template["afmt"]

    def test_card_4_structure(self):
        """Card 4 (Comprehension) should show sentence without highlight on front."""
        template = TEMPLATES[3]
        assert template["name"] == CARD_4_NAME
        assert "{{Sentence4}}" in template["qfmt"]
        assert "{{Sentence4Highlight}}" in template["afmt"]

    def test_card_5_structure(self):
        """Card 5 (Listening) should have audio on front."""
        template = TEMPLATES[4]
        assert template["name"] == CARD_5_NAME
        assert "{{AudioSentence5}}" in template["qfmt"]
        # Should have listening-front class
        assert "listening-front" in template["qfmt"]


class TestCSSStyling:
    """Tests for CSS styling."""

    def test_css_has_target_lang_styling(self):
        """CSS should style target language prominently."""
        assert ".target-lang" in CSS

    def test_css_has_english_styling(self):
        """CSS should style English as secondary."""
        assert ".english" in CSS

    def test_css_has_highlight_styling(self):
        """CSS should style highlighted words."""
        assert "highlight" in CSS or "b," in CSS or "strong" in CSS

    def test_css_has_card_type_label(self):
        """CSS should have card type label styling."""
        assert ".card-type" in CSS

    def test_css_has_mobile_responsive(self):
        """CSS should have mobile responsive rules."""
        assert "@media" in CSS


class TestModelCreation:
    """Tests for create_note_model function."""

    def test_create_note_model_returns_genanki_model(self):
        """Should return a genanki Model instance."""
        try:
            import genanki

            model = create_note_model()
            assert isinstance(model, genanki.Model)
        except ImportError:
            pytest.skip("genanki not installed")

    def test_model_has_correct_id(self):
        """Model should have the correct ID."""
        try:
            model = create_note_model()
            assert model.model_id == MODEL_ID
        except ImportError:
            pytest.skip("genanki not installed")

    def test_model_has_correct_name(self):
        """Model should have the correct name."""
        try:
            model = create_note_model()
            assert model.name == MODEL_NAME
        except ImportError:
            pytest.skip("genanki not installed")

    def test_model_has_all_fields(self):
        """Model should have all 24 fields."""
        try:
            model = create_note_model()
            assert len(model.fields) == 24
        except ImportError:
            pytest.skip("genanki not installed")

    def test_model_has_all_templates(self):
        """Model should have all 5 templates."""
        try:
            model = create_note_model()
            assert len(model.templates) == 5
        except ImportError:
            pytest.skip("genanki not installed")

    def test_model_has_css(self):
        """Model should have CSS."""
        try:
            model = create_note_model()
            assert len(model.css) > 0
        except ImportError:
            pytest.skip("genanki not installed")


class TestGetModel:
    """Tests for get_model convenience function."""

    def test_get_model_returns_same_model(self):
        """get_model should return a valid model."""
        try:
            import genanki

            model = get_model()
            assert isinstance(model, genanki.Model)
        except ImportError:
            pytest.skip("genanki not installed")

    def test_get_model_returns_consistent_model(self):
        """Multiple calls should return models with same properties."""
        try:
            model1 = get_model()
            model2 = get_model()
            assert model1.model_id == model2.model_id
            assert model1.name == model2.name
        except ImportError:
            pytest.skip("genanki not installed")
