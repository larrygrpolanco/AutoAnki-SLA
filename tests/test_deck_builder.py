"""Tests for deck building."""

from pathlib import Path
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from autoanki.core.models import (
    AudioQueries,
    AutoAnkiCards,
    Card1Recognition,
    Card2Cloze,
    Card3Production,
    Card4Comprehension,
    Card5Listening,
    CardTypeSelection,
    ProjectMeta,
    ProjectStatus,
    SourceInfo,
    VocabEntry,
)
from autoanki.core.deck_builder import (
    DeckBuilderError,
    build_and_export,
    build_audio_field,
    build_deck,
    build_note,
    build_note_fields,
    collect_media_files,
    export_deck,
    generate_deck_id,
    generate_note_guid,
    has_any_enabled_card,
)


class TestGUIDGeneration:
    """Tests for stable GUID generation."""

    def test_generate_deck_id_consistency(self):
        """Same deck name should generate same ID."""
        deck_name = "Test Deck"
        id1 = generate_deck_id(deck_name)
        id2 = generate_deck_id(deck_name)
        assert id1 == id2

    def test_generate_deck_id_different_names(self):
        """Different deck names should generate different IDs."""
        id1 = generate_deck_id("Deck One")
        id2 = generate_deck_id("Deck Two")
        assert id1 != id2

    def test_generate_deck_id_is_positive(self):
        """Deck ID should be positive 32-bit integer."""
        deck_id = generate_deck_id("Test")
        assert deck_id > 0
        assert deck_id < 2**31

    def test_generate_note_guid_consistency(self):
        """Same vocab ID should generate same GUID."""
        vocab_id = uuid4()
        guid1 = generate_note_guid(vocab_id)
        guid2 = generate_note_guid(vocab_id)
        assert guid1 == guid2

    def test_generate_note_guid_different_ids(self):
        """Different vocab IDs should generate different GUIDs."""
        guid1 = generate_note_guid(uuid4())
        guid2 = generate_note_guid(uuid4())
        assert guid1 != guid2

    def test_generate_note_guid_is_positive(self):
        """Note GUID should be positive 32-bit integer."""
        vocab_id = uuid4()
        guid = generate_note_guid(vocab_id)
        assert guid > 0
        assert guid < 2**31


class TestAudioFieldBuilding:
    """Tests for audio field building."""

    def test_build_audio_field_with_existing_file(self, tmp_path):
        """Should return [sound:filename.mp3] if file exists."""
        # Create audio file
        audio_dir = tmp_path / "audio"
        audio_dir.mkdir()

        from autoanki.core.tts import get_audio_filename

        text = "test audio"
        filename = get_audio_filename(text)
        (audio_dir / filename).write_bytes(b"fake audio")

        result = build_audio_field(text, tmp_path)
        assert result == f"[sound:{filename}]"

    def test_build_audio_field_with_missing_file(self, tmp_path):
        """Should return empty string if file doesn't exist."""
        result = build_audio_field("test audio", tmp_path)
        assert result == ""

    def test_build_audio_field_with_empty_text(self, tmp_path):
        """Should return empty string for empty text."""
        result = build_audio_field("", tmp_path)
        assert result == ""


class TestHasAnyEnabledCard:
    """Tests for checking if any cards are enabled."""

    def test_all_enabled(self):
        """All cards enabled should return True."""
        card_types = CardTypeSelection(
            card_1_recognition=True,
            card_2_cloze=True,
            card_3_production=True,
            card_4_comprehension=True,
            card_5_listening=True,
        )
        assert has_any_enabled_card(None, card_types) is True

    def test_some_enabled(self):
        """Some cards enabled should return True."""
        card_types = CardTypeSelection(
            card_1_recognition=True,
            card_2_cloze=False,
            card_3_production=True,
            card_4_comprehension=False,
            card_5_listening=True,
        )
        assert has_any_enabled_card(None, card_types) is True

    def test_none_enabled(self):
        """No cards enabled should return False."""
        card_types = CardTypeSelection(
            card_1_recognition=False,
            card_2_cloze=False,
            card_3_production=False,
            card_4_comprehension=False,
            card_5_listening=False,
        )
        assert has_any_enabled_card(None, card_types) is False


class TestBuildNoteFields:
    """Tests for building note field values."""

    def _create_vocab_entry(self) -> VocabEntry:
        """Helper to create a complete vocab entry."""
        return VocabEntry(
            target_word="사다",
            english_translation="to buy",
            part_of_speech="verb",
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

    def test_all_fields_populated_with_all_cards_enabled(self, tmp_path):
        """All fields should be populated when all cards enabled."""
        vocab = self._create_vocab_entry()
        card_types = CardTypeSelection(
            card_1_recognition=True,
            card_2_cloze=True,
            card_3_production=True,
            card_4_comprehension=True,
            card_5_listening=True,
        )

        fields = build_note_fields(vocab, card_types, tmp_path)

        # Check basic fields
        assert fields["TargetWord"] == "사다"
        assert fields["EnglishTranslation"] == "to buy"
        assert fields["PartOfSpeech"] == "verb"

        # Check card 1 fields
        assert "저는 가게에서 과일을" in fields["Sentence1"]
        assert fields["Sentence1English"] == "I buy fruit at the store."

        # Check card 2 fields
        assert "{{c1::" in fields["Sentence2Cloze"]
        assert fields["ClozeHint"] == "to buy"

        # Check card 3 fields
        assert "우리는 어제" in fields["Sentence3"]

        # Check card 4 fields
        assert fields["Sentence4WordContext"] == "buys"

        # Check card 5 fields
        assert fields["Sentence5WordContext"] == "want to buy"

    def test_disabled_card_fields_are_empty(self, tmp_path):
        """Fields for disabled cards should be empty strings."""
        vocab = self._create_vocab_entry()
        card_types = CardTypeSelection(
            card_1_recognition=True,
            card_2_cloze=False,
            card_3_production=False,
            card_4_comprehension=False,
            card_5_listening=False,
        )

        fields = build_note_fields(vocab, card_types, tmp_path)

        # Card 1 should be populated
        assert len(fields["Sentence1"]) > 0

        # Cards 2-5 should be empty
        assert fields["Sentence2Cloze"] == ""
        assert fields["Sentence3"] == ""
        assert fields["Sentence4"] == ""
        assert fields["Sentence5"] == ""


class TestBuildNote:
    """Tests for building genanki notes."""

    def _create_vocab_entry(self) -> VocabEntry:
        """Helper to create a complete vocab entry."""
        return VocabEntry(
            target_word="사다",
            english_translation="to buy",
            part_of_speech="verb",
            card_1_recognition=Card1Recognition(
                sentence_target="저는 가게에서 과일을 사요.",
                sentence_target_highlight="저는 가게에서 과일을 <b>사요</b>.",
                sentence_english="I buy fruit.",
            ),
            card_2_cloze=Card2Cloze(
                sentence_cloze="엄마는 빵을 {{c1::사요}}.",
                sentence_english="Mom buys bread.",
                english_hint="to buy",
            ),
            card_3_production=Card3Production(
                sentence_target="우리는 신발을 샀어요.",
                sentence_english="We bought shoes.",
            ),
            card_4_comprehension=Card4Comprehension(
                sentence_target="형은 커피를 사요.",
                sentence_english="Brother buys coffee.",
                word_in_sentence_highlight="형은 커피를 <b>사요</b>.",
                word_translation_in_context="buys",
            ),
            card_5_listening=Card5Listening(
                sentence_target="저는 선물을 사고 싶어요.",
                sentence_english="I want to buy a gift.",
                word_in_sentence_highlight="저는 선물을 <b>사고 싶어요</b>.",
                word_translation_in_context="want to buy",
            ),
            audio_queries=AudioQueries(
                word_isolated="사다",
                sentence_1="저는 가게에서 과일을 사요.",
                sentence_2="엄마는 빵을 사요.",
                sentence_3="우리는 신발을 샀어요.",
                sentence_4="형은 커피를 사요.",
                sentence_5="저는 선물을 사고 싶어요.",
            ),
        )

    def test_build_note_returns_note_with_all_cards(self, tmp_path):
        """Should return genanki.Note when cards are enabled."""
        try:
            import genanki

            vocab = self._create_vocab_entry()
            card_types = CardTypeSelection(
                card_1_recognition=True,
                card_2_cloze=True,
                card_3_production=True,
                card_4_comprehension=True,
                card_5_listening=True,
            )

            note = build_note(vocab, card_types, tmp_path)

            assert note is not None
            assert isinstance(note, genanki.Note)
            assert len(note.fields) == 24
        except ImportError:
            pytest.skip("genanki not installed")

    def test_build_note_returns_none_when_no_cards_enabled(self, tmp_path):
        """Should return None when no cards are enabled."""
        vocab = self._create_vocab_entry()
        card_types = CardTypeSelection(
            card_1_recognition=False,
            card_2_cloze=False,
            card_3_production=False,
            card_4_comprehension=False,
            card_5_listening=False,
        )

        note = build_note(vocab, card_types, tmp_path)

        assert note is None

    def test_note_has_stable_guid(self, tmp_path):
        """Same vocab entry should generate note with same GUID."""
        try:
            import genanki

            vocab = self._create_vocab_entry()
            card_types = CardTypeSelection(
                card_1_recognition=True,
                card_2_cloze=False,
                card_3_production=False,
                card_4_comprehension=False,
                card_5_listening=False,
            )

            note1 = build_note(vocab, card_types, tmp_path)
            note2 = build_note(vocab, card_types, tmp_path)

            assert note1 is not None
            assert note2 is not None
            assert note1.guid == note2.guid
        except ImportError:
            pytest.skip("genanki not installed")


class TestCollectMediaFiles:
    """Tests for collecting audio media files."""

    def _create_vocab_entry(self) -> VocabEntry:
        """Helper to create a complete vocab entry."""
        return VocabEntry(
            target_word="사다",
            english_translation="to buy",
            part_of_speech="verb",
            card_1_recognition=Card1Recognition(
                sentence_target="저는 가게에서 과일을 사요.",
                sentence_target_highlight="저는 가게에서 과일을 <b>사요</b>.",
                sentence_english="I buy fruit.",
            ),
            card_2_cloze=Card2Cloze(
                sentence_cloze="엄마는 빵을 {{c1::사요}}.",
                sentence_english="Mom buys bread.",
                english_hint="to buy",
            ),
            card_3_production=Card3Production(
                sentence_target="우리는 신발을 샀어요.",
                sentence_english="We bought shoes.",
            ),
            card_4_comprehension=Card4Comprehension(
                sentence_target="형은 커피를 사요.",
                sentence_english="Brother buys coffee.",
                word_in_sentence_highlight="형은 커피를 <b>사요</b>.",
                word_translation_in_context="buys",
            ),
            card_5_listening=Card5Listening(
                sentence_target="저는 선물을 사고 싶어요.",
                sentence_english="I want to buy a gift.",
                word_in_sentence_highlight="저는 선물을 <b>사고 싶어요</b>.",
                word_translation_in_context="want to buy",
            ),
            audio_queries=AudioQueries(
                word_isolated="사다",
                sentence_1="저는 가게에서 과일을 사요.",
                sentence_2="엄마는 빵을 사요.",
                sentence_3="우리는 신발을 샀어요.",
                sentence_4="형은 커피를 사요.",
                sentence_5="저는 선물을 사고 싶어요.",
            ),
        )

    def test_collects_existing_audio_files(self, tmp_path):
        """Should collect audio files that exist."""
        # Create audio directory and files
        audio_dir = tmp_path / "audio"
        audio_dir.mkdir()

        # Create some audio files
        from autoanki.core.tts import get_audio_filename

        texts = ["사다", "저는 가게에서 과일을 사요.", "엄마는 빵을 사요."]
        for text in texts:
            filename = get_audio_filename(text)
            (audio_dir / filename).write_bytes(b"fake audio")

        cards = AutoAnkiCards(
            source_info=SourceInfo(
                title="Test",
                source_language="ko",
                target_language_name="Korean",
                level_description="Test",
                available_vocabulary_context="",
            ),
            vocabulary=[self._create_vocab_entry()],
        )

        card_types = CardTypeSelection(
            card_1_recognition=True,
            card_2_cloze=True,
            card_3_production=False,
            card_4_comprehension=False,
            card_5_listening=False,
        )

        media_files = collect_media_files(cards, card_types, tmp_path)

        # Should have isolated word + sentence 1 + sentence 2 = 3 files
        assert len(media_files) == 3

    def test_skips_missing_audio_files(self, tmp_path):
        """Should skip audio files that don't exist."""
        cards = AutoAnkiCards(
            source_info=SourceInfo(
                title="Test",
                source_language="ko",
                target_language_name="Korean",
                level_description="Test",
                available_vocabulary_context="",
            ),
            vocabulary=[self._create_vocab_entry()],
        )

        card_types = CardTypeSelection(
            card_1_recognition=True,
            card_2_cloze=True,
            card_3_production=True,
            card_4_comprehension=True,
            card_5_listening=True,
        )

        media_files = collect_media_files(cards, card_types, tmp_path)

        # No audio files exist, so should be empty
        assert len(media_files) == 0

    def test_respects_card_type_filtering(self, tmp_path):
        """Should only collect audio for enabled card types."""
        # Create audio directory and files
        audio_dir = tmp_path / "audio"
        audio_dir.mkdir()

        # Create only sentence 1 and sentence 2 audio
        from autoanki.core.tts import get_audio_filename

        (audio_dir / get_audio_filename("저는 가게에서 과일을 사요.")).write_bytes(b"audio1")
        (audio_dir / get_audio_filename("엄마는 빵을 사요.")).write_bytes(b"audio2")

        cards = AutoAnkiCards(
            source_info=SourceInfo(
                title="Test",
                source_language="ko",
                target_language_name="Korean",
                level_description="Test",
                available_vocabulary_context="",
            ),
            vocabulary=[self._create_vocab_entry()],
        )

        # Only enable cards 1 and 2
        card_types = CardTypeSelection(
            card_1_recognition=True,
            card_2_cloze=True,
            card_3_production=False,
            card_4_comprehension=False,
            card_5_listening=False,
        )

        media_files = collect_media_files(cards, card_types, tmp_path)

        # Should only have sentence 1 and sentence 2 (no isolated word because cards 3 and 5 disabled)
        assert len(media_files) == 2


class TestBuildDeck:
    """Tests for building complete decks."""

    def _create_test_cards(self) -> AutoAnkiCards:
        """Helper to create test card data."""
        vocab_entry = VocabEntry(
            target_word="사다",
            english_translation="to buy",
            part_of_speech="verb",
            card_1_recognition=Card1Recognition(
                sentence_target="저는 가게에서 과일을 사요.",
                sentence_target_highlight="저는 가게에서 과일을 <b>사요</b>.",
                sentence_english="I buy fruit.",
            ),
            card_2_cloze=Card2Cloze(
                sentence_cloze="엄마는 빵을 {{c1::사요}}.",
                sentence_english="Mom buys bread.",
                english_hint="to buy",
            ),
            card_3_production=Card3Production(
                sentence_target="우리는 신발을 샀어요.",
                sentence_english="We bought shoes.",
            ),
            card_4_comprehension=Card4Comprehension(
                sentence_target="형은 커피를 사요.",
                sentence_english="Brother buys coffee.",
                word_in_sentence_highlight="형은 커피를 <b>사요</b>.",
                word_translation_in_context="buys",
            ),
            card_5_listening=Card5Listening(
                sentence_target="저는 선물을 사고 싶어요.",
                sentence_english="I want to buy a gift.",
                word_in_sentence_highlight="저는 선물을 <b>사고 싶어요</b>.",
                word_translation_in_context="want to buy",
            ),
            audio_queries=AudioQueries(
                word_isolated="사다",
                sentence_1="저는 가게에서 과일을 사요.",
                sentence_2="엄마는 빵을 사요.",
                sentence_3="우리는 신발을 샀어요.",
                sentence_4="형은 커피를 사요.",
                sentence_5="저는 선물을 사고 싶어요.",
            ),
        )

        return AutoAnkiCards(
            source_info=SourceInfo(
                title="Test Lesson",
                source_language="ko",
                target_language_name="Korean",
                level_description="Beginner",
                available_vocabulary_context="Test",
            ),
            vocabulary=[vocab_entry],
        )

    def test_build_deck_returns_genanki_deck(self, tmp_path):
        """Should return a genanki Deck."""
        try:
            import genanki

            cards = self._create_test_cards()
            meta = ProjectMeta(
                project_name="test",
                deck_name="Test Deck",
                source_filename="test.txt",
                status=ProjectStatus.GENERATED,
                card_types=CardTypeSelection(
                    card_1_recognition=True,
                    card_2_cloze=True,
                    card_3_production=True,
                    card_4_comprehension=True,
                    card_5_listening=True,
                ),
            )

            deck = build_deck(cards, meta, tmp_path)

            assert isinstance(deck, genanki.Deck)
            assert deck.name == "Test Deck"
            assert len(deck.notes) == 1
        except ImportError:
            pytest.skip("genanki not installed")

    def test_build_deck_raises_error_when_no_cards(self, tmp_path):
        """Should raise DeckBuilderError when no cards can be built."""
        cards = AutoAnkiCards(
            source_info=SourceInfo(
                title="Empty",
                source_language="ko",
                target_language_name="Korean",
                level_description="Test",
                available_vocabulary_context="",
            ),
            vocabulary=[],
        )
        meta = ProjectMeta(
            project_name="test",
            deck_name="Test Deck",
            source_filename="test.txt",
            status=ProjectStatus.GENERATED,
            card_types=CardTypeSelection(
                card_1_recognition=True,
                card_2_cloze=True,
                card_3_production=True,
                card_4_comprehension=True,
                card_5_listening=True,
            ),
        )

        with pytest.raises(DeckBuilderError):
            build_deck(cards, meta, tmp_path)

    def test_deck_has_stable_id(self, tmp_path):
        """Same deck name should produce deck with same ID."""
        try:
            import genanki

            cards = self._create_test_cards()
            meta1 = ProjectMeta(
                project_name="test1",
                deck_name="Test Deck",
                source_filename="test.txt",
                status=ProjectStatus.GENERATED,
                card_types=CardTypeSelection(card_1_recognition=True),
            )
            meta2 = ProjectMeta(
                project_name="test2",
                deck_name="Test Deck",
                source_filename="test.txt",
                status=ProjectStatus.GENERATED,
                card_types=CardTypeSelection(card_1_recognition=True),
            )

            deck1 = build_deck(cards, meta1, tmp_path)
            deck2 = build_deck(cards, meta2, tmp_path)

            assert deck1.deck_id == deck2.deck_id
        except ImportError:
            pytest.skip("genanki not installed")


class TestExportDeck:
    """Tests for exporting decks to .apkg files."""

    def test_export_creates_apkg_file(self, tmp_path):
        """Should create .apkg file."""
        try:
            import genanki

            # Create a simple deck
            deck = genanki.Deck(
                deck_id=12345,
                name="Test Deck",
            )

            output_path = tmp_path / "test.apkg"

            export_deck(deck, [], output_path)

            assert output_path.exists()
            assert output_path.stat().st_size > 0
        except ImportError:
            pytest.skip("genanki not installed")

    def test_export_raises_error_on_failure(self, tmp_path):
        """Should raise DeckBuilderError on export failure."""
        try:
            import genanki

            deck = genanki.Deck(
                deck_id=12345,
                name="Test Deck",
            )

            # Try to export to a non-existent directory with bad permissions
            output_path = Path("/nonexistent/directory/test.apkg")

            with pytest.raises(DeckBuilderError):
                export_deck(deck, [], output_path)
        except ImportError:
            pytest.skip("genanki not installed")


class TestBuildAndExport:
    """Tests for the complete build and export workflow."""

    @patch("autoanki.core.deck_builder.load_project_meta")
    @patch("autoanki.core.deck_builder.load_cards")
    @patch("autoanki.core.deck_builder.get_project_path")
    def test_build_and_export_creates_file(
        self, mock_get_path, mock_load_cards, mock_load_meta, tmp_path
    ):
        """Should create .apkg file with timestamp in name."""
        try:
            import genanki

            # Setup mocks
            mock_get_path.return_value = tmp_path

            vocab_entry = VocabEntry(
                target_word="사다",
                english_translation="to buy",
                part_of_speech="verb",
                card_1_recognition=Card1Recognition(
                    sentence_target="저는 가게에서 과일을 사요.",
                    sentence_target_highlight="저는 가게에서 과일을 <b>사요</b>.",
                    sentence_english="I buy fruit.",
                ),
                card_2_cloze=Card2Cloze(
                    sentence_cloze="엄마는 빵을 {{c1::사요}}.",
                    sentence_english="Mom buys bread.",
                    english_hint="to buy",
                ),
                card_3_production=Card3Production(
                    sentence_target="우리는 신발을 샀어요.",
                    sentence_english="We bought shoes.",
                ),
                card_4_comprehension=Card4Comprehension(
                    sentence_target="형은 커피를 사요.",
                    sentence_english="Brother buys coffee.",
                    word_in_sentence_highlight="형은 커피를 <b>사요</b>.",
                    word_translation_in_context="buys",
                ),
                card_5_listening=Card5Listening(
                    sentence_target="저는 선물을 사고 싶어요.",
                    sentence_english="I want to buy a gift.",
                    word_in_sentence_highlight="저는 선물을 <b>사고 싶어요</b>.",
                    word_translation_in_context="want to buy",
                ),
                audio_queries=AudioQueries(
                    word_isolated="사다",
                    sentence_1="저는 가게에서 과일을 사요.",
                    sentence_2="엄마는 빵을 사요.",
                    sentence_3="우리는 신발을 샀어요.",
                    sentence_4="형은 커피를 사요.",
                    sentence_5="저는 선물을 사고 싶어요.",
                ),
            )

            cards = AutoAnkiCards(
                source_info=SourceInfo(
                    title="Test",
                    source_language="ko",
                    target_language_name="Korean",
                    level_description="Beginner",
                    available_vocabulary_context="",
                ),
                vocabulary=[vocab_entry],
            )
            mock_load_cards.return_value = cards

            meta = ProjectMeta(
                project_name="test",
                deck_name="Test Korean Deck",
                source_filename="test.txt",
                status=ProjectStatus.GENERATED,
                card_types=CardTypeSelection(
                    card_1_recognition=True,
                    card_2_cloze=False,
                    card_3_production=False,
                    card_4_comprehension=False,
                    card_5_listening=False,
                ),
            )
            mock_load_meta.return_value = meta

            # Create output directory
            (tmp_path / "output").mkdir()

            # Call build_and_export
            result_path = build_and_export("test")

            # Verify file was created
            assert result_path.exists()
            assert result_path.suffix == ".apkg"
            assert "Test_Korean_Deck" in result_path.name
            assert result_path.stat().st_size > 0
        except ImportError:
            pytest.skip("genanki not installed")

    @patch("autoanki.core.deck_builder.get_project_path")
    @patch("autoanki.core.deck_builder.load_project_meta")
    @patch("autoanki.core.deck_builder.load_cards")
    def test_build_and_export_raises_when_no_cards(
        self, mock_load_cards, mock_load_meta, mock_get_path, tmp_path
    ):
        """Should raise FileNotFoundError when no cards.json exists."""
        mock_get_path.return_value = tmp_path
        mock_load_meta.return_value = None  # Won't be used, just to prevent real call
        mock_load_cards.return_value = None

        with pytest.raises(FileNotFoundError):
            build_and_export("nonexistent")
