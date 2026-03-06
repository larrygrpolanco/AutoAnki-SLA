"""Tests for PDF and text parsing."""

import tempfile
from pathlib import Path

import pytest

from autoanki.core.parser import (
    MAX_CHARS,
    TextExtractionError,
    TextTooLongError,
    extract_text,
    get_text_stats,
    parse_past_vocab,
    parse_past_vocab_text,
    validate_length,
)


class TestValidateLength:
    """Tests for validate_length function."""

    def test_valid_text_passes(self):
        """Text under the limit should pass validation."""
        text = "a" * 1000
        assert validate_length(text) is True

    def test_text_at_limit_passes(self):
        """Text exactly at limit should pass validation."""
        text = "a" * MAX_CHARS
        assert validate_length(text) is True

    def test_text_over_limit_raises(self):
        """Text over the limit should raise TextTooLongError."""
        text = "a" * (MAX_CHARS + 1)
        with pytest.raises(TextTooLongError) as exc_info:
            validate_length(text)

        assert exc_info.value.length == MAX_CHARS + 1
        assert exc_info.value.max_chars == MAX_CHARS

    def test_custom_limit(self):
        """Should respect custom limit."""
        text = "a" * 100
        with pytest.raises(TextTooLongError):
            validate_length(text, max_chars=50)


class TestParsePastVocabText:
    """Tests for parse_past_vocab_text function."""

    def test_empty_text(self):
        """Empty text should return empty list."""
        assert parse_past_vocab_text("") == []
        assert parse_past_vocab_text("   ") == []

    def test_one_per_line(self):
        """One word per line format."""
        text = "사람\n집\n학교"
        result = parse_past_vocab_text(text)
        assert result == ["사람", "집", "학교"]

    def test_comma_separated(self):
        """Comma-separated format."""
        text = "사람, 집, 학교"
        result = parse_past_vocab_text(text)
        assert result == ["사람", "집", "학교"]

    def test_tab_separated(self):
        """Tab-separated format."""
        text = "사람\t집\t학교"
        result = parse_past_vocab_text(text)
        assert result == ["사람", "집", "학교"]

    def test_mixed_format(self):
        """Mixed format with newlines, commas, and tabs."""
        text = "사람, 집\n학교\t가다"
        result = parse_past_vocab_text(text)
        assert result == ["사람", "집", "학교", "가다"]

    def test_whitespace_stripping(self):
        """Should strip whitespace from words."""
        text = "  사람  \n  집  "
        result = parse_past_vocab_text(text)
        assert result == ["사람", "집"]

    def test_duplicate_removal(self):
        """Should remove duplicates while preserving order."""
        text = "사람\n집\n사람\n학교\n집"
        result = parse_past_vocab_text(text)
        assert result == ["사람", "집", "학교"]

    def test_internal_whitespace_normalization(self):
        """Should normalize internal whitespace."""
        text = "new   york\nmultiple   spaces"
        result = parse_past_vocab_text(text)
        assert result == ["new york", "multiple spaces"]


class TestParsePastVocab:
    """Tests for parse_past_vocab function."""

    def test_file_not_found(self):
        """Should raise FileNotFoundError for non-existent file."""
        with pytest.raises(FileNotFoundError):
            parse_past_vocab("/nonexistent/path/vocab.txt")

    def test_valid_file(self, tmp_path: Path):
        """Should read and parse valid file."""
        vocab_file = tmp_path / "vocab.txt"
        vocab_file.write_text("사람\n집\n학교", encoding="utf-8")

        result = parse_past_vocab(vocab_file)
        assert result == ["사람", "집", "학교"]


class TestExtractText:
    """Tests for extract_text function."""

    def test_file_not_found(self):
        """Should raise FileNotFoundError for non-existent file."""
        with pytest.raises(FileNotFoundError):
            extract_text("/nonexistent/file.txt")

    def test_extract_txt_file(self, tmp_path: Path):
        """Should read text from .txt file."""
        text_file = tmp_path / "test.txt"
        content = "Hello, World!\nThis is a test."
        text_file.write_text(content, encoding="utf-8")

        result = extract_text(text_file)
        assert result == content

    def test_extract_markdown_file(self, tmp_path: Path):
        """Should read text from .md file."""
        md_file = tmp_path / "test.md"
        content = "# Heading\n\nSome content."
        md_file.write_text(content, encoding="utf-8")

        result = extract_text(md_file)
        assert result == content

    def test_text_too_long(self, tmp_path: Path):
        """Should raise TextTooLongError for text over limit."""
        text_file = tmp_path / "long.txt"
        text_file.write_text("a" * (MAX_CHARS + 1), encoding="utf-8")

        with pytest.raises(TextTooLongError):
            extract_text(text_file)


class TestGetTextStats:
    """Tests for get_text_stats function."""

    def test_basic_stats(self):
        """Should return correct stats for basic text."""
        text = "Hello World\nThis is a test.\n\nAnother line."
        stats = get_text_stats(text)

        assert stats["characters"] == 42
        assert stats["lines"] == 4
        assert stats["words"] == 8
        assert stats["non_empty_lines"] == 3

    def test_empty_text(self):
        """Should handle empty text."""
        stats = get_text_stats("")

        assert stats["characters"] == 0
        assert stats["lines"] == 1  # Empty string has one empty line
        assert stats["words"] == 0
        assert stats["non_empty_lines"] == 0


# Skip PDF tests if fitz is not available (requires pymupdf)
try:
    import fitz  # noqa: F401

    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False


@pytest.mark.skipif(not HAS_FITZ, reason="pymupdf not installed")
class TestPDFExtraction:
    """Tests for PDF extraction (requires pymupdf)."""

    def test_pdf_extraction_mock(self, tmp_path: Path, monkeypatch):
        """Mock test for PDF extraction to avoid needing real PDF."""
        # Create a minimal mock that returns text
        from unittest.mock import MagicMock, patch

        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Test content from PDF"
        mock_doc.__enter__ = MagicMock(return_value=mock_doc)
        mock_doc.__exit__ = MagicMock(return_value=False)
        mock_doc.__iter__ = MagicMock(return_value=iter([mock_page]))

        with patch("fitz.open", return_value=mock_doc):
            pdf_file = tmp_path / "test.pdf"
            pdf_file.touch()  # Create empty file, mock handles content

            result = extract_text(pdf_file)
            assert "Test content from PDF" in result
