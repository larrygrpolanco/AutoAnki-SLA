"""Tests for LLM pipeline."""

import json
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from autoanki.core.llm import (
    LLMClient,
    LLMError,
    CardGenerationError,
    _extract_json_from_response,
    _load_prompt,
    _validate_and_parse_json,
    generate_cards,
    step1_drafting,
    step2_review,
    step3_structuring,
)
from autoanki.core.models import AutoAnkiCards, SourceInfo


class TestLoadPrompt:
    """Tests for prompt file loading."""

    def test_load_existing_prompt(self):
        """Test loading an existing prompt file."""
        prompt = _load_prompt("card_drafting.txt")
        assert "Card Drafting Prompt" in prompt
        assert "Step 1" in prompt

    def test_load_card_review_prompt(self):
        """Test loading the card review prompt."""
        prompt = _load_prompt("card_review.txt")
        assert "Card Review Prompt" in prompt
        assert "Step 2" in prompt

    def test_load_structuring_prompt(self):
        """Test loading the structuring prompt."""
        prompt = _load_prompt("structuring.txt")
        assert "Structuring Prompt" in prompt
        assert "Step 3" in prompt

    def test_load_nonexistent_prompt_raises(self):
        """Test that loading a nonexistent prompt raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            _load_prompt("nonexistent.txt")


class TestLLMClient:
    """Tests for LLM client wrapper."""

    def test_init_with_api_key(self):
        """Test initialization with explicit API key."""
        client = LLMClient(api_key="test-key")
        assert client.api_key == "test-key"
        assert client.model == "gpt-4o-mini"

    def test_init_without_api_key_raises(self):
        """Test that initialization without API key raises ValueError."""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="OpenAI API key required"):
                LLMClient()

    def test_init_from_env_var(self):
        """Test initialization from environment variable."""
        with patch.dict("os.environ", {"OPENAI_API_KEY": "env-key"}):
            client = LLMClient()
            assert client.api_key == "env-key"

    @patch("autoanki.core.llm.OpenAI")
    def test_chat_success(self, mock_openai_class):
        """Test successful chat completion."""
        # Setup mock
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_response

        # Test
        client = LLMClient(api_key="test-key")
        result = client.chat(
            system_prompt="System prompt",
            user_message="User message",
        )

        assert result == "Test response"
        mock_client.chat.completions.create.assert_called_once()

    @patch("autoanki.core.llm.OpenAI")
    def test_chat_error_raises_llm_error(self, mock_openai_class):
        """Test that API errors raise LLMError."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        client = LLMClient(api_key="test-key")
        with pytest.raises(LLMError, match="API Error"):
            client.chat("System", "User")


class TestExtractJsonFromResponse:
    """Tests for JSON extraction from LLM responses."""

    def test_plain_json(self):
        """Test extracting plain JSON."""
        response = '{"key": "value"}'
        result = _extract_json_from_response(response)
        assert result == '{"key": "value"}'

    def test_json_with_markdown_code_block(self):
        """Test extracting JSON from markdown code block."""
        response = '```json\n{"key": "value"}\n```'
        result = _extract_json_from_response(response)
        assert result == '{"key": "value"}'

    def test_json_with_generic_code_block(self):
        """Test extracting JSON from generic code block."""
        response = '```\n{"key": "value"}\n```'
        result = _extract_json_from_response(response)
        assert result == '{"key": "value"}'

    def test_whitespace_stripping(self):
        """Test that whitespace is properly stripped."""
        response = '   ```json\n{"key": "value"}\n```   '
        result = _extract_json_from_response(response)
        assert result == '{"key": "value"}'


class TestValidateAndParseJson:
    """Tests for JSON validation and parsing."""

    def test_valid_json(self):
        """Test validating valid JSON."""
        json_str = json.dumps(
            {
                "schema_version": 1,
                "source_info": {
                    "title": "Test",
                    "source_language": "ko",
                    "target_language_name": "Korean",
                    "level_description": "Beginner",
                    "available_vocabulary_context": "Test context",
                },
                "vocabulary": [],
            }
        )

        result = _validate_and_parse_json(json_str)
        assert isinstance(result, AutoAnkiCards)
        assert result.schema_version == 1

    def test_invalid_json_raises(self):
        """Test that invalid JSON raises ValueError."""
        with pytest.raises(ValueError):
            _validate_and_parse_json("not valid json")

    def test_missing_required_field_raises(self):
        """Test that missing required fields raise ValueError."""
        json_str = json.dumps(
            {
                "schema_version": 1,
                "source_info": {
                    "title": "Test"
                    # Missing other required fields
                },
                "vocabulary": [],
            }
        )

        with pytest.raises(ValueError):
            _validate_and_parse_json(json_str)


class TestStep1Drafting:
    """Tests for Step 1: Card drafting."""

    @patch("autoanki.core.llm._load_prompt")
    def test_step1_calls_llm_with_correct_params(self, mock_load_prompt):
        """Test that step1 calls LLM with correct parameters."""
        mock_load_prompt.return_value = "System prompt"
        mock_client = MagicMock()
        mock_client.chat.return_value = "Drafted content"

        result = step1_drafting(
            client=mock_client,
            source_text="Source text",
            available_vocab_context="Context",
            level_description="Beginner",
            title="Test Title",
        )

        assert result == "Drafted content"
        mock_load_prompt.assert_called_once_with("card_drafting.txt")
        mock_client.chat.assert_called_once()


class TestStep2Review:
    """Tests for Step 2: Card review."""

    @patch("autoanki.core.llm._load_prompt")
    def test_step2_calls_llm_with_correct_params(self, mock_load_prompt):
        """Test that step2 calls LLM with correct parameters."""
        mock_load_prompt.return_value = "System prompt"
        mock_client = MagicMock()
        mock_client.chat.return_value = "Reviewed content"

        result = step2_review(
            client=mock_client,
            drafted_content="Drafted content",
            source_text="Original source",
            available_vocab_context="Context",
        )

        assert result == "Reviewed content"
        mock_load_prompt.assert_called_once_with("card_review.txt")
        mock_client.chat.assert_called_once()


class TestStep3Structuring:
    """Tests for Step 3: JSON structuring."""

    @patch("autoanki.core.llm._load_prompt")
    def test_step3_calls_llm_with_correct_params(self, mock_load_prompt):
        """Test that step3 calls LLM with correct parameters."""
        mock_load_prompt.return_value = "System prompt"
        mock_client = MagicMock()
        mock_client.chat.return_value = '{"schema_version": 1}'

        source_info = SourceInfo(
            title="Test",
            source_language="ko",
            target_language_name="Korean",
            level_description="Beginner",
            available_vocabulary_context="Context",
        )

        result = step3_structuring(
            client=mock_client,
            reviewed_content="Reviewed content",
            source_info=source_info,
        )

        assert result == '{"schema_version": 1}'
        mock_load_prompt.assert_called_once_with("structuring.txt")
        mock_client.chat.assert_called_once()


class TestGenerateCards:
    """Tests for the main generate_cards function."""

    @patch("autoanki.core.llm.LLMClient")
    @patch("autoanki.core.llm.step1_drafting")
    @patch("autoanki.core.llm.step2_review")
    @patch("autoanki.core.llm.step3_structuring")
    @patch("autoanki.core.llm._validate_and_parse_json")
    def test_generate_cards_success(
        self,
        mock_validate,
        mock_step3,
        mock_step2,
        mock_step1,
        mock_client_class,
    ):
        """Test successful card generation."""
        # Setup mocks
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_step1.return_value = "Drafted"
        mock_step2.return_value = "Reviewed"
        mock_step3.return_value = "{}"

        mock_cards = MagicMock(spec=AutoAnkiCards)
        mock_cards.vocabulary = []
        mock_validate.return_value = mock_cards

        progress_calls = []

        def progress_callback(step, total, message):
            progress_calls.append((step, total, message))

        result = generate_cards(
            source_text="Source",
            available_vocab_context="Context",
            level_description="Beginner",
            title="Test",
            source_language="ko",
            target_language_name="Korean",
            progress_callback=progress_callback,
        )

        assert result == mock_cards
        assert len(progress_calls) == 3
        mock_step1.assert_called_once()
        mock_step2.assert_called_once()
        mock_step3.assert_called_once()

    @patch("autoanki.core.llm.LLMClient")
    @patch("autoanki.core.llm.step1_drafting")
    def test_generate_cards_step1_failure(self, mock_step1, mock_client_class):
        """Test handling of Step 1 failure."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_step1.side_effect = LLMError("API failed")

        with pytest.raises(CardGenerationError, match="Step 1"):
            generate_cards(
                source_text="Source",
                available_vocab_context="Context",
                level_description="Beginner",
                title="Test",
                source_language="ko",
                target_language_name="Korean",
            )

    @patch("autoanki.core.llm.LLMClient")
    @patch("autoanki.core.llm.step1_drafting")
    @patch("autoanki.core.llm.step2_review")
    def test_generate_cards_step2_failure(self, mock_step2, mock_step1, mock_client_class):
        """Test handling of Step 2 failure."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_step1.return_value = "Drafted"
        mock_step2.side_effect = LLMError("API failed")

        with pytest.raises(CardGenerationError, match="Step 2"):
            generate_cards(
                source_text="Source",
                available_vocab_context="Context",
                level_description="Beginner",
                title="Test",
                source_language="ko",
                target_language_name="Korean",
            )

    @patch("autoanki.core.llm.LLMClient")
    @patch("autoanki.core.llm.step1_drafting")
    @patch("autoanki.core.llm.step2_review")
    @patch("autoanki.core.llm.step3_structuring")
    @patch("autoanki.core.llm._validate_and_parse_json")
    @patch("time.sleep")  # Speed up retries
    def test_generate_cards_retry_on_validation_failure(
        self,
        mock_sleep,
        mock_validate,
        mock_step3,
        mock_step2,
        mock_step1,
        mock_client_class,
    ):
        """Test that validation failures trigger retries."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_step1.return_value = "Drafted"
        mock_step2.return_value = "Reviewed"
        mock_step3.return_value = "{}"

        # First call fails, second succeeds
        mock_cards = MagicMock(spec=AutoAnkiCards)
        mock_cards.vocabulary = []
        mock_validate.side_effect = [
            ValueError("Invalid"),
            mock_cards,
        ]

        result = generate_cards(
            source_text="Source",
            available_vocab_context="Context",
            level_description="Beginner",
            title="Test",
            source_language="ko",
            target_language_name="Korean",
        )

        assert result == mock_cards
        # Should have called step3 twice (initial + 1 retry)
        assert mock_step3.call_count == 2

    @patch("autoanki.core.llm.LLMClient")
    @patch("autoanki.core.llm.step1_drafting")
    @patch("autoanki.core.llm.step2_review")
    @patch("autoanki.core.llm.step3_structuring")
    @patch("autoanki.core.llm._validate_and_parse_json")
    @patch("time.sleep")
    def test_generate_cards_all_retries_exhausted(
        self,
        mock_sleep,
        mock_validate,
        mock_step3,
        mock_step2,
        mock_step1,
        mock_client_class,
    ):
        """Test that all retries exhausted raises CardGenerationError."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_step1.return_value = "Drafted"
        mock_step2.return_value = "Reviewed"
        mock_step3.return_value = "{}"

        # All validation attempts fail
        mock_validate.side_effect = ValueError("Invalid JSON")

        with pytest.raises(CardGenerationError, match="failed after 2 attempts"):
            generate_cards(
                source_text="Source",
                available_vocab_context="Context",
                level_description="Beginner",
                title="Test",
                source_language="ko",
                target_language_name="Korean",
            )


class TestIntegration:
    """Integration-style tests that verify full pipeline behavior."""

    def test_json_with_vocabulary_entries(self):
        """Test parsing JSON with actual vocabulary entries."""
        json_str = json.dumps(
            {
                "schema_version": 1,
                "source_info": {
                    "title": "Korean Lesson 1",
                    "source_language": "ko",
                    "target_language_name": "Korean",
                    "level_description": "Beginner, Chapter 1",
                    "available_vocabulary_context": "Basic greetings",
                },
                "vocabulary": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "target_word": "사다",
                        "target_word_romanization": "",
                        "english_translation": "to buy",
                        "part_of_speech": "verb",
                        "category": "Shopping",
                        "notes": "",
                        "generate_audio": True,
                        "card_1_recognition": {
                            "sentence_target": "저는 가게에서 과일을 사요.",
                            "sentence_target_highlight": "저는 가게에서 과일을 <b>사요</b>.",
                            "sentence_english": "I buy fruit at the store.",
                        },
                        "card_2_cloze": {
                            "sentence_cloze": "엄마는 토요일마다 빵을 {{c1::사요}}.",
                            "sentence_english": "My mom buys bread every Saturday.",
                            "english_hint": "to buy",
                        },
                        "card_3_production": {
                            "sentence_target": "우리는 어제 새 신발을 샀어요.",
                            "sentence_english": "We bought new shoes yesterday.",
                        },
                        "card_4_comprehension": {
                            "sentence_target": "형은 매일 커피를 사요.",
                            "sentence_english": "My older brother buys coffee every day.",
                            "word_in_sentence_highlight": "형은 매일 커피를 <b>사요</b>.",
                            "word_translation_in_context": "buys",
                        },
                        "card_5_listening": {
                            "sentence_target": "저는 친구에게 줄 선물을 사고 싶어요.",
                            "sentence_english": "I want to buy a gift for my friend.",
                            "word_in_sentence_highlight": "저는 친구에게 줄 선물을 <b>사고 싶어요</b>.",
                            "word_translation_in_context": "want to buy",
                        },
                        "audio_queries": {
                            "word_isolated": "사다",
                            "sentence_1": "저는 가게에서 과일을 사요.",
                            "sentence_2": "엄마는 토요일마다 빵을 사요.",
                            "sentence_3": "우리는 어제 새 신발을 샀어요.",
                            "sentence_4": "형은 매일 커피를 사요.",
                            "sentence_5": "저는 친구에게 줄 선물을 사고 싶어요.",
                        },
                    }
                ],
            }
        )

        result = _validate_and_parse_json(json_str)
        assert len(result.vocabulary) == 1
        assert result.vocabulary[0].target_word == "사다"
        assert (
            result.vocabulary[0].card_1_recognition.sentence_english == "I buy fruit at the store."
        )
