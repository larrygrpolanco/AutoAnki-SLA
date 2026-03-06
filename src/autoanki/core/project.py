"""Project management (CRUD operations)."""

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from autoanki.core.models import AutoAnkiCards, ProjectMeta, ProjectStatus

# Base directory for user data
USER_DATA_DIR = Path.home() / ".autoanki"
PROJECTS_DIR = USER_DATA_DIR / "projects"


def _ensure_directories() -> None:
    """Ensure the base data directories exist."""
    USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)


def _sanitize_project_name(name: str) -> str:
    """Sanitize a project name for use as a directory name.

    Replaces spaces with dashes, removes special characters, lowercases.
    """
    sanitized = name.lower().strip()
    # Replace spaces and underscores with dashes
    sanitized = sanitized.replace(" ", "-").replace("_", "-")
    # Remove any non-alphanumeric characters except dashes
    sanitized = "".join(c for c in sanitized if c.isalnum() or c == "-")
    # Remove multiple consecutive dashes
    while "--" in sanitized:
        sanitized = sanitized.replace("--", "-")
    # Trim dashes from ends
    sanitized = sanitized.strip("-")
    return sanitized or "untitled-project"


def _get_project_path(project_name: str) -> Path:
    """Get the directory path for a project."""
    sanitized = _sanitize_project_name(project_name)
    return PROJECTS_DIR / sanitized


def _now_iso() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def create_project(
    project_name: str,
    deck_name: str | None = None,
    source_filename: str = "",
    level_description: str = "",
    source_text: str = "",
) -> ProjectMeta:
    """Create a new AutoAnki project.

    Args:
        project_name: Name of the project (used for directory)
        deck_name: Name for the Anki deck (defaults to project_name)
        source_filename: Name of the source file that was imported
        level_description: Description of the level (e.g., "Beginner, Chapter 5")
        source_text: The extracted text content from the source file

    Returns:
        ProjectMeta object for the created project

    Raises:
        ValueError: If project already exists
    """
    _ensure_directories()

    project_path = _get_project_path(project_name)

    if project_path.exists():
        raise ValueError(f"Project '{project_name}' already exists at {project_path}")

    # Create project directory structure
    project_path.mkdir(parents=True)
    (project_path / "audio").mkdir()
    (project_path / "output").mkdir()

    # Create metadata
    meta = ProjectMeta(
        project_name=project_name,
        deck_name=deck_name or project_name,
        source_filename=source_filename,
        level_description=level_description,
        status=ProjectStatus.IMPORTED,
    )

    # Save source text
    if source_text:
        source_path = project_path / "source.txt"
        source_path.write_text(source_text, encoding="utf-8")

    # Save metadata
    meta_path = project_path / "meta.json"
    meta_path.write_text(meta.model_dump_json(indent=2), encoding="utf-8")

    return meta


def save_project_meta(project_name: str, meta: ProjectMeta) -> None:
    """Save project metadata to disk.

    Updates the updated_at timestamp automatically.
    """
    project_path = _get_project_path(project_name)
    if not project_path.exists():
        raise ValueError(f"Project '{project_name}' does not exist")

    # Update timestamp
    meta.updated_at = _now_iso()

    meta_path = project_path / "meta.json"
    meta_path.write_text(meta.model_dump_json(indent=2), encoding="utf-8")


def load_project_meta(project_name: str) -> ProjectMeta:
    """Load project metadata from disk.

    Args:
        project_name: Name of the project to load

    Returns:
        ProjectMeta object

    Raises:
        ValueError: If project doesn't exist or meta.json is missing/corrupted
    """
    project_path = _get_project_path(project_name)

    if not project_path.exists():
        raise ValueError(f"Project '{project_name}' does not exist at {project_path}")

    meta_path = project_path / "meta.json"

    if not meta_path.exists():
        raise ValueError(f"Project '{project_name}' has no metadata file")

    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        return ProjectMeta.model_validate(data)
    except (json.JSONDecodeError, Exception) as e:
        raise ValueError(f"Failed to load project metadata: {e}")


def save_cards(project_name: str, cards: AutoAnkiCards) -> None:
    """Save card data to cards.json.

    Args:
        project_name: Name of the project
        cards: AutoAnkiCards object to save
    """
    project_path = _get_project_path(project_name)
    if not project_path.exists():
        raise ValueError(f"Project '{project_name}' does not exist")

    cards_path = project_path / "cards.json"
    cards_path.write_text(cards.model_dump_json(indent=2), encoding="utf-8")


def load_cards(project_name: str) -> AutoAnkiCards | None:
    """Load card data from cards.json.

    Args:
        project_name: Name of the project to load

    Returns:
        AutoAnkiCards object, or None if cards.json doesn't exist

    Raises:
        ValueError: If cards.json exists but is corrupted
    """
    project_path = _get_project_path(project_name)
    cards_path = project_path / "cards.json"

    if not cards_path.exists():
        return None

    try:
        data = json.loads(cards_path.read_text(encoding="utf-8"))
        return AutoAnkiCards.model_validate(data)
    except (json.JSONDecodeError, Exception) as e:
        raise ValueError(f"Failed to load cards data: {e}")


def load_source_text(project_name: str) -> str:
    """Load the source text for a project.

    Args:
        project_name: Name of the project

    Returns:
        The source text content

    Raises:
        ValueError: If source.txt doesn't exist
    """
    project_path = _get_project_path(project_name)
    source_path = project_path / "source.txt"

    if not source_path.exists():
        raise ValueError(f"Project '{project_name}' has no source text")

    return source_path.read_text(encoding="utf-8")


def list_projects() -> list[str]:
    """List all project names.

    Returns:
        List of project names (directory names in projects folder)
    """
    _ensure_directories()

    if not PROJECTS_DIR.exists():
        return []

    return [p.name for p in PROJECTS_DIR.iterdir() if p.is_dir() and (p / "meta.json").exists()]


def delete_project(project_name: str) -> None:
    """Delete a project and all its data.

    Args:
        project_name: Name of the project to delete

    Raises:
        ValueError: If project doesn't exist
    """
    project_path = _get_project_path(project_name)

    if not project_path.exists():
        raise ValueError(f"Project '{project_name}' does not exist")

    shutil.rmtree(project_path)


def get_project_path(project_name: str) -> Path:
    """Get the full path to a project directory.

    Args:
        project_name: Name of the project

    Returns:
        Path to the project directory
    """
    return _get_project_path(project_name)


def save_past_vocab(project_name: str, vocab_words: list[str]) -> None:
    """Save past vocabulary list to the project.

    Args:
        project_name: Name of the project
        vocab_words: List of words to save
    """
    project_path = _get_project_path(project_name)
    if not project_path.exists():
        raise ValueError(f"Project '{project_name}' does not exist")

    vocab_path = project_path / "past_vocab.txt"
    vocab_path.write_text("\n".join(vocab_words), encoding="utf-8")


def load_past_vocab(project_name: str) -> list[str] | None:
    """Load past vocabulary list from the project.

    Args:
        project_name: Name of the project

    Returns:
        List of words, or None if no past_vocab.txt exists
    """
    project_path = _get_project_path(project_name)
    vocab_path = project_path / "past_vocab.txt"

    if not vocab_path.exists():
        return None

    # Parse using the same logic as the vocab parser
    from autoanki.core.parser import parse_past_vocab_text

    return parse_past_vocab_text(vocab_path.read_text(encoding="utf-8"))


def project_exists(project_name: str) -> bool:
    """Check if a project exists.

    Args:
        project_name: Name of the project

    Returns:
        True if the project exists
    """
    project_path = _get_project_path(project_name)
    return project_path.exists() and (project_path / "meta.json").exists()
