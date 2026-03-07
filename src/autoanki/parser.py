import re
from pathlib import Path

MAX_CHARS = 15000


def extract_text(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return _extract_pdf(path)
    elif suffix == ".txt":
        return path.read_text(encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {suffix}. Use .pdf or .txt")


def _extract_pdf(path: Path) -> str:
    import fitz  # pymupdf
    doc = fitz.open(str(path))
    pages = []
    for page in doc:
        text = page.get_text()
        if text.strip():
            pages.append(text)
    doc.close()
    return "\n\n".join(pages)


def parse_past_vocab(file_path: str) -> list[str]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Past vocab file not found: {file_path}")
    text = path.read_text(encoding="utf-8")
    # Split on newlines, commas, or tabs; strip whitespace; drop empty strings
    words = re.split(r"[\n,\t]+", text)
    return [w.strip() for w in words if w.strip()]


def count_chars(text: str) -> int:
    return len(text)
