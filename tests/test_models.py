"""Tests for Pydantic models."""

import json
from uuid import UUID

import pytest

from autoanki.core.models import (
    AutoAnkiCards,
    Card1Recognition,
    Card2Cloze,
    Card3Production,
    Card4Comprehension,
    Card5Listening,
    AudioQueries,
    CardTypeSelection,
    FlashForgeCards,  # Legacy alias
    ProjectMeta,
    ProjectStatus,
    SourceInfo,
    VocabEntry,
)


class TestProjectStatus:
    """Tests for ProjectStatus enum."""

    def test_status_values(self):
        """Status should have expected values."""
        assert ProjectStatus.IMPORTED == "imported"
        assert ProjectStatus.CONFIGURED == "configured"
        assert ProjectStatus.GENERATED == "generated"
        assert ProjectStatus.REVIEWED == "reviewed"
        assert ProjectStatus.EXPORTED == "exported"


class TestCardTypeSelection:
    """Tests for CardTypeSelection model."""

    def test_defaults(self):
        """All card types should default to True."""
        selection = CardTypeSelection()
        assert selection.card_1_recognition is True
        assert selection.card_2_cloze is True
        assert selection.card_3_production is True
        assert selection.card_4_comprehension is True
        assert selection.card_5_listening is True

    def test_enabled_types_all(self):
        """Should return all types when all enabled."""
        selection = CardTypeSelection()
        assert selection.enabled_types() == [1, 2, 3, 4, 5]

    def test_enabled_types_subset(self):
        """Should return only enabled types."""
        selection = CardTypeSelection(
            card_1_recognition=True,
            card_2_cloze=False,
            card_3_production=True,
            card_4_comprehension=False,
            card_5_listening=True,
        )
        assert selection.enabled_types() == [1, 3, 5]

    def test_enabled_types_none(self):
        """Should return empty list when all disabled."""
        selection = CardTypeSelection(
            card_1_recognition=False,
            card_2_cloze=False,
            card_3_production=False,
            card_4_comprehension=False,
            card_5_listening=False,
        )
        assert selection.enabled_types() == []


class TestProjectMeta:
    """Tests for ProjectMeta model."""

    def test_required_fields(self):
        """Should require project_name and status."""
        with pytest.raises(ValueError):
            ProjectMeta()

    def test_basic_creation(self):
        """Should create with required fields."""
        meta = ProjectMeta(
            project_name="Test",
            status=ProjectStatus.IMPORTED,
            deck_name="Test Deck",
            source_filename="test.txt",
        )
        assert meta.project_name == "Test"
        assert meta.status == ProjectStatus.IMPORTED
        assert meta.schema_version == 1

    def test_defaults(self):
        """Should have appropriate defaults."""
        meta = ProjectMeta(
            project_name="Test",
            status=ProjectStatus.IMPORTED,
            deck_name="Test Deck",
            source_filename="test.txt",
        )
        assert meta.generate_audio is True
        assert meta.card_types.enabled_types() == [1, 2, 3, 4, 5]
        assert meta.has_past_vocab is False
        assert meta.vocab_count == 0

    def test_timestamps(self):
        """Should auto-generate timestamps."""
        meta = ProjectMeta(
            project_name="Test",
            status=ProjectStatus.IMPORTED,
            deck_name="Test Deck",
            source_filename="test.txt",
        )
        assert meta.created_at is not None
        assert meta.updated_at is not None
        assert isinstance(meta.created_at, str)
        assert isinstance(meta.updated_at, str)


class TestCardModels:
    """Tests for individual card type models."""

    def test_card1_recognition(self):
        """Card1Recognition should work."""
        card = Card1Recognition(
            sentence_target="저는 가게에서 과일을 사요.",
            sentence_target_highlight="저는 가게에서 과일을 <b>사요</b>.",
            sentence_english="I buy fruit at the store.",
        )
        assert card.sentence_target == "저는 가게에서 과일을 사요."
        assert "<b>" in card.sentence_target_highlight

    def test_card2_cloze(self):
        """Card2Cloze should work with cloze syntax."""
        card = Card2Cloze(
            sentence_cloze="엄마는 토요일마다 빵을 {{c1::사요}}.",
            sentence_english="My mom buys bread every Saturday.",
            english_hint="to buy",
        )
        assert "{{c1::" in card.sentence_cloze
        assert card.english_hint == "to buy"

    def test_card3_production(self):
        """Card3Production should work."""
        card = Card3Production(
            sentence_target="우리는 어제 새 신발을 샀어요.",
            sentence_english="We bought new shoes yesterday.",
        )
        assert card.sentence_target == "우리는 어제 새 신발을 샀어요."

    def test_card4_comprehension(self):
        """Card4Comprehension should work."""
        card = Card4Comprehension(
            sentence_target="형은 매일 커피를 사요.",
            sentence_english="My older brother buys coffee every day.",
            word_in_sentence_highlight="형은 매일 커피를 <b>사요</b>.",
            word_translation_in_context="buys",
        )
        assert card.word_translation_in_context == "buys"

    def test_card5_listening(self):
        """Card5Listening should work."""
        card = Card5Listening(
            sentence_target="저는 친구에게 줄 선물을 사고 싶어요.",
            sentence_english="I want to buy a gift for my friend.",
            word_in_sentence_highlight="저는 친구에게 줄 선물을 <b>사고 싶어요</b>.",
            word_translation_in_context="want to buy",
        )
        assert "<b>" in card.word_in_sentence_highlight


class TestAudioQueries:
    """Tests for AudioQueries model."""

    def test_all_fields(self):
        """Should have all required audio fields."""
        queries = AudioQueries(
            word_isolated="사다",
            sentence_1="저는 가게에서 과일을 사요.",
            sentence_2="엄마는 토요일마다 빵을 사요.",
            sentence_3="우리는 어제 새 신발을 샀어요.",
            sentence_4="형은 매일 커피를 사요.",
            sentence_5="저는 친구에게 줄 선물을 사고 싶어요.",
        )
        assert queries.word_isolated == "사다"
        assert len(queries.sentence_1) > 0


class TestVocabEntry:
    """Tests for VocabEntry model."""

    def test_required_fields(self):
        """Should require target_word and english_translation."""
        with pytest.raises(ValueError):
            VocabEntry()

    def test_full_vocab_entry(self):
        """Should create complete vocab entry."""
        entry = VocabEntry(
            target_word="사다",
            english_translation="to buy",
            part_of_speech="verb",
            category="Shopping",
            card_1_recognition=Card1Recognition(
                sentence_target="저는 가게에서 과일을 사요.",
                sentence_target_highlight="저는 가게에서 과일을 <b>사요</b>.",
                sentence_english="I buy fruit at the store.",
            ),
            card_2_cloze=Card2Cloze(
                sentence_cloze="엄마는 토요일마다 빵을 {{c1::사요}}.",
                sentence_english="My mom buys bread every Saturday.",
                english_hint="to buy",
            ),
            card_3_production=Card3Production(
                sentence_target="우리는 어제 새 신발을 샀어요.",
                sentence_english="We bought new shoes yesterday.",
            ),
            card_4_comprehension=Card4Comprehension(
                sentence_target="형은 매일 커피를 사요.",
                sentence_english="My older brother buys coffee every day.",
                word_in_sentence_highlight="형은 매일 커피를 <b>사요</b>.",
                word_translation_in_context="buys",
            ),
            card_5_listening=Card5Listening(
                sentence_target="저는 친구에게 줄 선물을 사고 싶어요.",
                sentence_english="I want to buy a gift for my friend.",
                word_in_sentence_highlight="저는 친구에게 줄 선물을 <b>사고 싶어요</b>.",
                word_translation_in_context="want to buy",
            ),
            audio_queries=AudioQueries(
                word_isolated="사다",
                sentence_1="저는 가게에서 과일을 사요.",
                sentence_2="엄마는 토요일마다 빵을 사요.",
                sentence_3="우리는 어제 새 신발을 샀어요.",
                sentence_4="형은 매일 커피를 사요.",
                sentence_5="저는 친구에게 줄 선물을 사고 싶어요.",
            ),
        )

        assert entry.target_word == "사다"
        assert entry.english_translation == "to buy"
        assert entry.part_of_speech == "verb"
        assert entry.generate_audio is True
        assert isinstance(entry.id, UUID)

    def test_defaults(self):
        """Should have appropriate defaults."""
        entry = VocabEntry(
            target_word="사람",
            english_translation="person",
            part_of_speech="noun",
            card_1_recognition=Card1Recognition(
                sentence_target="",
                sentence_target_highlight="",
                sentence_english="",
            ),
            card_2_cloze=Card2Cloze(
                sentence_cloze="",
                sentence_english="",
                english_hint="",
            ),
            card_3_production=Card3Production(
                sentence_target="",
                sentence_english="",
            ),
            card_4_comprehension=Card4Comprehension(
                sentence_target="",
                sentence_english="",
                word_in_sentence_highlight="",
                word_translation_in_context="",
            ),
            card_5_listening=Card5Listening(
                sentence_target="",
                sentence_english="",
                word_in_sentence_highlight="",
                word_translation_in_context="",
            ),
            audio_queries=AudioQueries(
                word_isolated="",
                sentence_1="",
                sentence_2="",
                sentence_3="",
                sentence_4="",
                sentence_5="",
            ),
        )
        assert entry.category == "General"
        assert entry.notes == ""
        assert entry.generate_audio is True
        assert entry.target_word_romanization == ""


class TestSourceInfo:
    """Tests for SourceInfo model."""

    def test_required_fields(self):
        """Should require all fields."""
        with pytest.raises(ValueError):
            SourceInfo()

    def test_valid_creation(self):
        """Should create with all required fields."""
        info = SourceInfo(
            title="Korean Lesson 5",
            source_language="ko",
            target_language_name="Korean",
            level_description="Beginner",
            available_vocabulary_context="Chapters 1-5",
        )
        assert info.source_language == "ko"
        assert info.target_language_name == "Korean"


class TestAutoAnkiCards:
    """Tests for AutoAnkiCards root model."""

    def test_minimal_creation(self):
        """Should create with just source_info."""
        cards = AutoAnkiCards(
            source_info=SourceInfo(
                title="Test",
                source_language="ko",
                target_language_name="Korean",
                level_description="Test",
                available_vocabulary_context="Test vocab",
            ),
        )
        assert cards.schema_version == 1
        assert cards.vocabulary == []

    def test_with_vocab(self):
        """Should create with vocabulary entries."""
        cards = AutoAnkiCards(
            source_info=SourceInfo(
                title="Test",
                source_language="ko",
                target_language_name="Korean",
                level_description="Test",
                available_vocabulary_context="Test vocab",
            ),
            vocabulary=[
                VocabEntry(
                    target_word="사람",
                    english_translation="person",
                    part_of_speech="noun",
                    card_1_recognition=Card1Recognition(
                        sentence_target="저는 사람입니다.",
                        sentence_target_highlight="저는 <b>사람</b>입니다.",
                        sentence_english="I am a person.",
                    ),
                    card_2_cloze=Card2Cloze(
                        sentence_cloze="그는 좋은 {{c1::사람}}입니다.",
                        sentence_english="He is a good person.",
                        english_hint="person",
                    ),
                    card_3_production=Card3Production(
                        sentence_target="저는 사람을 만났어요.",
                        sentence_english="I met a person.",
                    ),
                    card_4_comprehension=Card4Comprehension(
                        sentence_target="그 사람은 친절해요.",
                        sentence_english="That person is kind.",
                        word_in_sentence_highlight="그 <b>사람</b>은 친절해요.",
                        word_translation_in_context="person",
                    ),
                    card_5_listening=Card5Listening(
                        sentence_target="새로운 사람을 만났어요.",
                        sentence_english="I met a new person.",
                        word_in_sentence_highlight="새로운 <b>사람</b>을 만났어요.",
                        word_translation_in_context="person",
                    ),
                    audio_queries=AudioQueries(
                        word_isolated="사람",
                        sentence_1="저는 사람입니다.",
                        sentence_2="그는 좋은 사람입니다.",
                        sentence_3="저는 사람을 만났어요.",
                        sentence_4="그 사람은 친절해요.",
                        sentence_5="새로운 사람을 만났어요.",
                    ),
                ),
            ],
        )
        assert len(cards.vocabulary) == 1
        assert cards.vocabulary[0].target_word == "사람"

    def test_json_serialization(self):
        """Should serialize to JSON correctly."""
        cards = AutoAnkiCards(
            source_info=SourceInfo(
                title="Test",
                source_language="ko",
                target_language_name="Korean",
                level_description="Test",
                available_vocabulary_context="Test vocab",
            ),
            vocabulary=[],
        )

        json_str = cards.model_dump_json()
        data = json.loads(json_str)

        assert data["schema_version"] == 1
        assert data["source_info"]["source_language"] == "ko"
        assert "vocabulary" in data


class TestFlashForgeCardsAlias:
    """Tests for the FlashForgeCards legacy alias."""

    def test_alias_exists(self):
        """FlashForgeCards should be an alias for AutoAnkiCards."""
        assert FlashForgeCards is AutoAnkiCards
