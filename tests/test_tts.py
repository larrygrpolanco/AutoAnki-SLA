"""Tests for TTS module."""

import hashlib
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

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
from autoanki.core.tts import (
    DEFAULT_DELAY_SECONDS,
    DEFAULT_VOICE,
    TTSError,
    TTSClient,
    AudioGenerationResult,
    check_audio_exists,
    generate_audio_batch,
    get_audio_filename,
    get_audio_hash,
    get_audio_path,
    get_audio_stats,
    get_required_audio_files,
    should_generate_isolated_word_audio,
    should_generate_sentence_audio,
)


class TestAudioHash:
    """Tests for hash-based filename generation."""

    def test_get_audio_hash_consistency(self):
        """Test that same text produces same hash."""
        text = "사다"
        hash1 = get_audio_hash(text)
        hash2 = get_audio_hash(text)
        assert hash1 == hash2
        assert len(hash1) == 12

    def test_get_audio_hash_different_texts(self):
        """Test that different texts produce different hashes."""
        hash1 = get_audio_hash("사다")
        hash2 = get_audio_hash("먹다")
        assert hash1 != hash2

    def test_get_audio_hash_length(self):
        """Test hash is exactly 12 characters."""
        text = "저는 가게에서 과일을 사요."
        hash_str = get_audio_hash(text)
        assert len(hash_str) == 12
        assert all(c in "0123456789abcdef" for c in hash_str)

    def test_get_audio_filename(self):
        """Test filename generation includes extension."""
        text = "사다"
        filename = get_audio_filename(text)
        assert filename.endswith(".mp3")
        assert len(filename) == 16  # 12 chars + .mp3

    def test_hash_matches_md5_truncation(self):
        """Verify our hash matches MD5 truncation logic."""
        text = "test text"
        expected = hashlib.md5(text.encode("utf-8")).hexdigest()[:12]
        assert get_audio_hash(text) == expected


class TestAudioToggleLogic:
    """Tests for audio toggle logic."""

    def test_should_generate_isolated_word_all_cards_enabled(self):
        """Test isolated word audio with all cards enabled."""
        card_types = CardTypeSelection(
            card_1_recognition=True,
            card_2_cloze=True,
            card_3_production=True,
            card_4_comprehension=True,
            card_5_listening=True,
        )
        assert should_generate_isolated_word_audio(card_types) is True

    def test_should_generate_isolated_word_only_card1(self):
        """Test isolated word audio with only Card 1 enabled."""
        card_types = CardTypeSelection(
            card_1_recognition=True,
            card_2_cloze=False,
            card_3_production=False,
            card_4_comprehension=False,
            card_5_listening=False,
        )
        assert should_generate_isolated_word_audio(card_types) is True

    def test_should_generate_isolated_word_no_relevant_cards(self):
        """Test isolated word audio with no relevant cards enabled."""
        card_types = CardTypeSelection(
            card_1_recognition=False,
            card_2_cloze=True,
            card_3_production=False,
            card_4_comprehension=True,
            card_5_listening=False,
        )
        assert should_generate_isolated_word_audio(card_types) is False

    def test_should_generate_sentence_all_enabled(self):
        """Test all sentences generated when all cards enabled."""
        card_types = CardTypeSelection(
            card_1_recognition=True,
            card_2_cloze=True,
            card_3_production=True,
            card_4_comprehension=True,
            card_5_listening=True,
        )
        for i in range(1, 6):
            assert should_generate_sentence_audio(i, card_types) is True

    def test_should_generate_sentence_subset(self):
        """Test sentence generation with subset of cards."""
        card_types = CardTypeSelection(
            card_1_recognition=True,
            card_2_cloze=False,
            card_3_production=True,
            card_4_comprehension=False,
            card_5_listening=True,
        )
        assert should_generate_sentence_audio(1, card_types) is True
        assert should_generate_sentence_audio(2, card_types) is False
        assert should_generate_sentence_audio(3, card_types) is True
        assert should_generate_sentence_audio(4, card_types) is False
        assert should_generate_sentence_audio(5, card_types) is True


class TestRequiredAudioFiles:
    """Tests for getting required audio files per word."""

    def _create_vocab_entry(self, word: str = "사다") -> VocabEntry:
        """Helper to create a VocabEntry for testing."""
        return VocabEntry(
            target_word=word,
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
                word_isolated=word,
                sentence_1="저는 가게에서 과일을 사요.",
                sentence_2="엄마는 빵을 사요.",
                sentence_3="우리는 신발을 샀어요.",
                sentence_4="형은 커피를 사요.",
                sentence_5="저는 선물을 사고 싶어요.",
            ),
        )

    def test_all_cards_enabled(self):
        """Test getting all audio files when all cards enabled."""
        vocab = self._create_vocab_entry()
        card_types = CardTypeSelection(
            card_1_recognition=True,
            card_2_cloze=True,
            card_3_production=True,
            card_4_comprehension=True,
            card_5_listening=True,
        )

        files = get_required_audio_files(vocab, card_types)

        # Should have: word_isolated + 5 sentences = 6 files
        assert len(files) == 6
        field_names = [f[1] for f in files]
        assert "word_isolated" in field_names
        for i in range(1, 6):
            assert f"sentence_{i}" in field_names

    def test_subset_of_cards(self):
        """Test getting audio files with subset of cards."""
        vocab = self._create_vocab_entry()
        card_types = CardTypeSelection(
            card_1_recognition=True,
            card_2_cloze=False,
            card_3_production=True,
            card_4_comprehension=False,
            card_5_listening=True,
        )

        files = get_required_audio_files(vocab, card_types)

        # Should have: word_isolated + sentences 1, 3, 5 = 4 files
        assert len(files) == 4
        field_names = [f[1] for f in files]
        assert "word_isolated" in field_names
        assert "sentence_1" in field_names
        assert "sentence_2" not in field_names
        assert "sentence_3" in field_names
        assert "sentence_4" not in field_names
        assert "sentence_5" in field_names

    def test_no_isolated_when_irrelevant(self):
        """Test isolated word skipped when only Cards 2 & 4 enabled."""
        vocab = self._create_vocab_entry()
        card_types = CardTypeSelection(
            card_1_recognition=False,
            card_2_cloze=True,
            card_3_production=False,
            card_4_comprehension=True,
            card_5_listening=False,
        )

        files = get_required_audio_files(vocab, card_types)

        # Should only have sentences 2 and 4 (no isolated word)
        assert len(files) == 2
        field_names = [f[1] for f in files]
        assert "word_isolated" not in field_names


class TestTTSClient:
    """Tests for TTSClient wrapper."""

    def test_init_with_api_key(self):
        """Test initialization with explicit API key."""
        client = TTSClient(api_key="test-key")
        assert client.api_key == "test-key"
        assert client.voice == DEFAULT_VOICE
        assert client.delay_seconds == DEFAULT_DELAY_SECONDS

    def test_init_without_api_key_raises(self):
        """Test that initialization without API key raises ValueError."""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="OpenAI API key required"):
                TTSClient()

    def test_init_from_env_var(self):
        """Test initialization from environment variable."""
        with patch.dict("os.environ", {"OPENAI_API_KEY": "env-key"}):
            client = TTSClient()
            assert client.api_key == "env-key"

    def test_custom_voice(self):
        """Test custom voice selection."""
        client = TTSClient(api_key="test", voice="echo")
        assert client.voice == "echo"

    def test_custom_delay(self):
        """Test custom delay setting."""
        client = TTSClient(api_key="test", delay_seconds=2.5)
        assert client.delay_seconds == 2.5

    @patch("autoanki.core.tts.OpenAI")
    def test_generate_audio_success(self, mock_openai_class):
        """Test successful audio generation."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_response = MagicMock()
        mock_response.content = b"fake audio data"
        mock_client.audio.speech.create.return_value = mock_response

        client = TTSClient(api_key="test")
        result = client.generate_audio("test text")

        assert result == b"fake audio data"
        mock_client.audio.speech.create.assert_called_once()

    @patch("autoanki.core.tts.OpenAI")
    def test_generate_audio_error_raises_tts_error(self, mock_openai_class):
        """Test that API errors raise TTSError."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.audio.speech.create.side_effect = Exception("API Error")

        client = TTSClient(api_key="test")
        with pytest.raises(TTSError, match="API Error"):
            client.generate_audio("test text")

    @patch("autoanki.core.tts.OpenAI")
    def test_generate_audio_to_file(self, mock_openai_class, tmp_path):
        """Test generating audio and saving to file."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_response = MagicMock()
        mock_response.content = b"fake audio data"
        mock_client.audio.speech.create.return_value = mock_response

        client = TTSClient(api_key="test")
        output_path = tmp_path / "test.mp3"

        result = client.generate_audio_to_file("test text", output_path)

        assert result is True
        assert output_path.read_bytes() == b"fake audio data"


class TestAudioPathHelpers:
    """Tests for audio path helper functions."""

    def test_get_audio_path(self, tmp_path):
        """Test getting full audio path."""
        text = "test audio"
        path = get_audio_path(tmp_path, text)

        assert path.parent == tmp_path / "audio"
        assert path.name.endswith(".mp3")
        assert len(path.stem) == 12

    def test_check_audio_exists_when_exists(self, tmp_path):
        """Test checking existence when file exists."""
        text = "test audio"
        audio_dir = tmp_path / "audio"
        audio_dir.mkdir()

        filename = get_audio_filename(text)
        audio_file = audio_dir / filename
        audio_file.write_text("dummy")  # Create the file

        assert check_audio_exists(tmp_path, text) is True

    def test_check_audio_exists_when_missing(self, tmp_path):
        """Test checking existence when file doesn't exist."""
        text = "test audio"
        audio_dir = tmp_path / "audio"
        audio_dir.mkdir()

        assert check_audio_exists(tmp_path, text) is False

    def test_get_audio_stats_empty(self, tmp_path):
        """Test audio stats with no files."""
        stats = get_audio_stats(tmp_path)
        assert stats["file_count"] == 0
        assert stats["total_size_bytes"] == 0
        assert stats["total_size_mb"] == 0.0

    def test_get_audio_stats_with_files(self, tmp_path):
        """Test audio stats with files present."""
        audio_dir = tmp_path / "audio"
        audio_dir.mkdir()

        # Create some dummy files
        (audio_dir / "a1b2c3d4e5f6.mp3").write_bytes(b"12345")  # 5 bytes
        (audio_dir / "b2c3d4e5f6a7.mp3").write_bytes(b"67890")  # 5 bytes

        stats = get_audio_stats(tmp_path)
        assert stats["file_count"] == 2
        assert stats["total_size_bytes"] == 10
        assert stats["total_size_mb"] == pytest.approx(0.0, abs=0.001)


class TestAudioGenerationResult:
    """Tests for AudioGenerationResult dataclass."""

    def test_total_processed(self):
        """Test total_processed property."""
        result = AudioGenerationResult(
            generated=["a.mp3", "b.mp3"],
            skipped=["c.mp3"],
            failed=[("text", "error")],
            total_requested=5,
        )
        assert result.total_processed == 4

    def test_success_rate_perfect(self):
        """Test success rate when all succeed."""
        result = AudioGenerationResult(
            generated=["a.mp3", "b.mp3"],
            skipped=["c.mp3"],
            failed=[],
            total_requested=3,
        )
        assert result.success_rate == 100.0

    def test_success_rate_partial(self):
        """Test success rate with some failures."""
        result = AudioGenerationResult(
            generated=["a.mp3"],
            skipped=["b.mp3"],
            failed=[("text1", "error"), ("text2", "error")],
            total_requested=4,
        )
        assert result.success_rate == 50.0

    def test_success_rate_zero_total(self):
        """Test success rate with zero total requested."""
        result = AudioGenerationResult(
            generated=[],
            skipped=[],
            failed=[],
            total_requested=0,
        )
        assert result.success_rate == 100.0


class TestGenerateAudioBatch:
    """Tests for the batch audio generation generator."""

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
                available_vocabulary_context="Test context",
            ),
            vocabulary=[vocab_entry],
        )

    def _create_test_meta(self, audio_enabled: bool = True) -> ProjectMeta:
        """Helper to create test project metadata."""
        return ProjectMeta(
            project_name="test-project",
            deck_name="Test Deck",
            source_filename="test.txt",
            status=ProjectStatus.GENERATED,
            generate_audio=audio_enabled,
            card_types=CardTypeSelection(
                card_1_recognition=True,
                card_2_cloze=True,
                card_3_production=True,
                card_4_comprehension=True,
                card_5_listening=True,
            ),
        )

    @patch("autoanki.core.tts.TTSClient")
    @patch("time.sleep")  # Skip delays for testing
    def test_generate_audio_batch_success(self, mock_sleep, mock_client_class, tmp_path):
        """Test successful batch generation."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        cards = self._create_test_cards()
        meta = self._create_test_meta()

        # Run generator and collect updates
        updates = []
        gen = generate_audio_batch(cards, meta, tmp_path)
        try:
            while True:
                updates.append(next(gen))
        except StopIteration as e:
            result = e.value

        # Should have updates for each file + completion
        assert len(updates) == 7  # 6 files + 1 completion

        # Check completion
        assert updates[-1]["status"] == "complete"
        assert "generated" in updates[-1]["message"].lower()

        # Check result
        assert result.total_requested == 6
        assert len(result.generated) == 6
        assert len(result.skipped) == 0
        assert len(result.failed) == 0

    @patch("autoanki.core.tts.TTSClient")
    def test_generate_audio_batch_skips_existing(self, mock_client_class, tmp_path):
        """Test that existing files are skipped."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        cards = self._create_test_cards()
        meta = self._create_test_meta()

        # Pre-create one audio file
        audio_dir = tmp_path / "audio"
        audio_dir.mkdir()
        text = "사다"
        filename = get_audio_filename(text)
        (audio_dir / filename).write_bytes(b"existing audio")

        updates = []
        gen = generate_audio_batch(cards, meta, tmp_path)
        try:
            while True:
                updates.append(next(gen))
        except StopIteration as e:
            result = e.value

        # Check that one file was skipped
        assert len(result.skipped) == 1
        assert len(result.generated) == 5

        # Find skip update
        skip_updates = [u for u in updates if u["status"] == "skipped"]
        assert len(skip_updates) == 1

    @patch("autoanki.core.tts.TTSClient")
    @patch("time.sleep")
    def test_generate_audio_batch_respects_project_toggle(
        self, mock_sleep, mock_client_class, tmp_path
    ):
        """Test that project-level toggle disables audio."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        cards = self._create_test_cards()
        meta = self._create_test_meta(audio_enabled=False)

        updates = []
        gen = generate_audio_batch(cards, meta, tmp_path)
        try:
            while True:
                updates.append(next(gen))
        except StopIteration as e:
            result = e.value

        # Should immediately complete with no files
        assert len(updates) == 1
        assert updates[0]["status"] == "complete"
        assert "disabled" in updates[0]["message"].lower()
        assert result.total_requested == 0

    @patch("autoanki.core.tts.TTSClient")
    @patch("time.sleep")
    def test_generate_audio_batch_handles_errors(self, mock_sleep, mock_client_class, tmp_path):
        """Test that errors are logged but generation continues."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        # Make first call fail, others succeed
        mock_client.generate_audio_to_file.side_effect = [
            TTSError("API Error"),  # First call fails
            True,  # Rest succeed
            True,
            True,
            True,
            True,
        ]

        cards = self._create_test_cards()
        meta = self._create_test_meta()

        updates = []
        gen = generate_audio_batch(cards, meta, tmp_path)
        try:
            while True:
                updates.append(next(gen))
        except StopIteration as e:
            result = e.value

        # Should have one failure but continue
        assert len(result.failed) == 1
        assert len(result.generated) == 5

        # Check for failure update
        failure_updates = [u for u in updates if u["status"] == "failed"]
        assert len(failure_updates) == 1
        assert "error" in failure_updates[0]

    @patch("autoanki.core.tts.TTSClient")
    @patch("time.sleep")
    def test_generate_audio_batch_respects_word_toggle(
        self, mock_sleep, mock_client_class, tmp_path
    ):
        """Test that per-word audio toggle is respected."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        cards = self._create_test_cards()
        # Disable audio for the word
        cards.vocabulary[0].generate_audio = False

        meta = self._create_test_meta()

        updates = []
        gen = generate_audio_batch(cards, meta, tmp_path)
        try:
            while True:
                updates.append(next(gen))
        except StopIteration as e:
            result = e.value

        # Should complete with no files (word disabled)
        assert result.total_requested == 0
        assert "No audio files" in updates[0]["message"]

    @patch("autoanki.core.tts.TTSClient")
    @patch("time.sleep")
    def test_generate_audio_batch_respects_card_types(
        self, mock_sleep, mock_client_class, tmp_path
    ):
        """Test that card type selection filters audio generation."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        cards = self._create_test_cards()
        meta = self._create_test_meta()
        # Only enable Cards 1 and 5
        meta.card_types.card_1_recognition = True
        meta.card_types.card_2_cloze = False
        meta.card_types.card_3_production = False
        meta.card_types.card_4_comprehension = False
        meta.card_types.card_5_listening = True

        updates = []
        gen = generate_audio_batch(cards, meta, tmp_path)
        try:
            while True:
                updates.append(next(gen))
        except StopIteration as e:
            result = e.value

        # Should have: word_isolated + sentence_1 + sentence_5 = 3 files
        assert result.total_requested == 3
        assert len(result.generated) == 3

    def test_generate_audio_batch_empty_vocabulary(self, tmp_path):
        """Test batch generation with no vocabulary."""
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
        meta = self._create_test_meta()

        updates = []
        gen = generate_audio_batch(cards, meta, tmp_path)
        try:
            while True:
                updates.append(next(gen))
        except StopIteration as e:
            result = e.value

        assert result.total_requested == 0
        assert "No audio files" in updates[0]["message"]
