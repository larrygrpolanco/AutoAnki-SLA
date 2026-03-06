"""PDF and text file parsing utilities."""

import re
from pathlib import Path

import fitz  # pymupdf

# Maximum character limit for input text
MAX_CHARS = 15000


class TextExtractionError(Exception):
    """Error extracting text from a file."""

    pass


class TextTooLongError(Exception):
    """Text exceeds the maximum character limit."""

    def __init__(self, length: int, max_chars: int = MAX_CHARS):
        self.length = length
        self.max_chars = max_chars
        super().__init__(f"Text is {length} characters, exceeding limit of {max_chars}")


def validate_length(text: str, max_chars: int = MAX_CHARS) -> bool:
    """Validate that text length is within the allowed limit.

    Args:
        text: The text to validate
        max_chars: Maximum allowed characters (default: 15000)

    Returns:
        True if text is within limit

    Raises:
        TextTooLongError: If text exceeds the limit
    """
    length = len(text)
    if length > max_chars:
        raise TextTooLongError(length, max_chars)
    return True


def extract_text(file_path: str | Path) -> str:
    """Extract text from a PDF or text file.

    Args:
        file_path: Path to the file (PDF or plain text)

    Returns:
        The extracted text content

    Raises:
        TextExtractionError: If file cannot be read or parsed
        TextTooLongError: If extracted text exceeds 15000 characters
        FileNotFoundError: If file doesn't exist
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path.is_file():
        raise TextExtractionError(f"Path is not a file: {file_path}")

    # Determine file type by extension
    suffix = file_path.suffix.lower()

    try:
        if suffix == ".pdf":
            text = _extract_from_pdf(file_path)
        elif suffix in (".txt", ".text", ".md", ".rst"):
            text = _extract_from_text(file_path)
        else:
            # Try as text file by default
            text = _extract_from_text(file_path)
    except Exception as e:
        if isinstance(e, TextTooLongError):
            raise
        raise TextExtractionError(f"Failed to extract text from {file_path}: {e}")

    # Validate length
    validate_length(text)

    return text


def _extract_from_pdf(file_path: Path) -> str:
    """Extract text from a PDF file using pymupdf.

    Args:
        file_path: Path to the PDF file

    Returns:
        Extracted text content
    """
    text_parts = []

    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text = page.get_text()
                if text.strip():
                    text_parts.append(text)
    except Exception as e:
        raise TextExtractionError(f"Failed to parse PDF: {e}")

    # Join with newlines and clean up
    full_text = "\n\n".join(text_parts)
    return _clean_extracted_text(full_text)


def _extract_from_text(file_path: Path) -> str:
    """Extract text from a plain text file.

    Args:
        file_path: Path to the text file

    Returns:
        File content as string
    """
    try:
        # Try UTF-8 first
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # Fall back to latin-1 if UTF-8 fails
        try:
            return file_path.read_text(encoding="latin-1")
        except Exception as e:
            raise TextExtractionError(f"Failed to read text file: {e}")


def _clean_extracted_text(text: str) -> str:
    """Clean up extracted text from PDF.

    Removes excessive whitespace, normalizes line endings, etc.

    Args:
        text: Raw extracted text

    Returns:
        Cleaned text
    """
    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Replace multiple consecutive newlines with double newline
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Replace multiple consecutive spaces with single space
    text = re.sub(r" +", " ", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


def parse_past_vocab(file_path: str | Path) -> list[str]:
    """Parse a past vocabulary file into a list of words.

    The file can be in any of these formats:
    - One word per line
    - Comma-separated words
    - Tab-separated words
    - Mixed format

    Args:
        file_path: Path to the vocabulary file

    Returns:
        List of unique words (cleaned and stripped)

    Raises:
        FileNotFoundError: If file doesn't exist
        TextExtractionError: If file cannot be read
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Vocabulary file not found: {file_path}")

    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception as e:
        raise TextExtractionError(f"Failed to read vocabulary file: {e}")

    return parse_past_vocab_text(text)


def parse_past_vocab_text(text: str) -> list[str]:
    """Parse vocabulary text into a list of words.

    Splits on newlines, commas, and tabs, then cleans and deduplicates.

    Args:
        text: Raw text containing vocabulary words

    Returns:
        List of unique, cleaned words
    """
    if not text or not text.strip():
        return []

    # Split on common delimiters: newlines, commas, tabs
    delimiters = r"[\n,\t]+"
    raw_words = re.split(delimiters, text)

    # Clean each word: strip whitespace, remove extra spaces
    cleaned = []
    for word in raw_words:
        word = word.strip()
        # Remove extra internal spaces
        word = re.sub(r"\s+", " ", word)
        if word:
            cleaned.append(word)

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for word in cleaned:
        if word not in seen:
            seen.add(word)
            unique.append(word)

    return unique


def get_text_stats(text: str) -> dict[str, int]:
    """Get statistics about a text.

    Args:
        text: The text to analyze

    Returns:
        Dictionary with character count, word count, line count, etc.
    """
    lines = text.split("\n")
    words = text.split()

    return {
        "characters": len(text),
        "lines": len(lines),
        "words": len(words),
        "non_empty_lines": len([l for l in lines if l.strip()]),
    }
