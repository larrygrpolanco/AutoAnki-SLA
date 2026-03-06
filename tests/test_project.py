"""Tests for project management."""

import json
from pathlib import Path

import pytest

from autoanki.core.models import (
    CardTypeSelection,
    ProjectMeta,
    ProjectStatus,
)
from autoanki.core.project import (
    PROJECTS_DIR,
    create_project,
    delete_project,
    get_project_path,
    list_projects,
    load_cards,
    load_past_vocab,
    load_project_meta,
    load_source_text,
    project_exists,
    save_cards,
    save_past_vocab,
    save_project_meta,
)


class TestCreateProject:
    """Tests for create_project function."""

    def test_create_basic_project(self, tmp_path, monkeypatch):
        """Test creating a basic project."""
        # Mock the projects directory
        monkeypatch.setattr("autoanki.core.project.PROJECTS_DIR", tmp_path / "projects")

        meta = create_project(
            project_name="Test Project",
            deck_name="Test Deck",
            source_filename="test.txt",
            level_description="Beginner",
            source_text="Sample text content",
        )

        assert meta.project_name == "Test Project"
        assert meta.deck_name == "Test Deck"
        assert meta.source_filename == "test.txt"
        assert meta.level_description == "Beginner"
        assert meta.status == ProjectStatus.IMPORTED
        assert meta.schema_version == 1

        # Verify directory structure
        project_path = tmp_path / "projects" / "test-project"
        assert project_path.exists()
        assert (project_path / "audio").exists()
        assert (project_path / "output").exists()

        # Verify source.txt
        assert (project_path / "source.txt").exists()
        assert (project_path / "source.txt").read_text() == "Sample text content"

        # Verify meta.json
        assert (project_path / "meta.json").exists()

    def test_duplicate_project_raises(self, tmp_path, monkeypatch):
        """Creating duplicate project should raise ValueError."""
        monkeypatch.setattr("autoanki.core.project.PROJECTS_DIR", tmp_path / "projects")

        create_project(project_name="Test", source_filename="test.txt")

        with pytest.raises(ValueError, match="already exists"):
            create_project(project_name="Test", source_filename="test.txt")

    def test_default_deck_name(self, tmp_path, monkeypatch):
        """Deck name should default to project name."""
        monkeypatch.setattr("autoanki.core.project.PROJECTS_DIR", tmp_path / "projects")

        meta = create_project(project_name="My Project", source_filename="test.txt")
        assert meta.deck_name == "My Project"

    def test_project_name_sanitization(self, tmp_path, monkeypatch):
        """Project names should be sanitized for filesystem."""
        monkeypatch.setattr("autoanki.core.project.PROJECTS_DIR", tmp_path / "projects")

        create_project(project_name="My Project With Spaces!", source_filename="test.txt")

        project_path = tmp_path / "projects" / "my-project-with-spaces"
        assert project_path.exists()


class TestLoadSaveProjectMeta:
    """Tests for loading and saving project metadata."""

    def test_save_and_load_roundtrip(self, tmp_path, monkeypatch):
        """Should be able to save and reload metadata."""
        monkeypatch.setattr("autoanki.core.project.PROJECTS_DIR", tmp_path / "projects")

        # Create project first
        meta = create_project(project_name="Test", source_filename="test.txt")

        # Modify metadata
        meta.status = ProjectStatus.CONFIGURED
        meta.vocab_count = 42
        save_project_meta("Test", meta)

        # Reload and verify
        loaded = load_project_meta("Test")
        assert loaded.status == ProjectStatus.CONFIGURED
        assert loaded.vocab_count == 42
        assert loaded.project_name == "Test"

    def test_load_nonexistent_project(self, tmp_path, monkeypatch):
        """Should raise ValueError for non-existent project."""
        monkeypatch.setattr("autoanki.core.project.PROJECTS_DIR", tmp_path / "projects")

        with pytest.raises(ValueError, match="does not exist"):
            load_project_meta("NonExistent")

    def test_updated_at_changes_on_save(self, tmp_path, monkeypatch):
        """updated_at should change when saving."""
        monkeypatch.setattr("autoanki.core.project.PROJECTS_DIR", tmp_path / "projects")

        meta = create_project(project_name="Test", source_filename="test.txt")
        original_updated = meta.updated_at

        # Save again
        save_project_meta("Test", meta)

        loaded = load_project_meta("Test")
        assert loaded.updated_at != original_updated

    def test_default_card_types(self, tmp_path, monkeypatch):
        """Card types should default to all True."""
        monkeypatch.setattr("autoanki.core.project.PROJECTS_DIR", tmp_path / "projects")

        meta = create_project(project_name="Test", source_filename="test.txt")

        assert meta.card_types.card_1_recognition is True
        assert meta.card_types.card_2_cloze is True
        assert meta.card_types.card_3_production is True
        assert meta.card_types.card_4_comprehension is True
        assert meta.card_types.card_5_listening is True


class TestListProjects:
    """Tests for list_projects function."""

    def test_empty_list(self, tmp_path, monkeypatch):
        """Should return empty list when no projects exist."""
        monkeypatch.setattr("autoanki.core.project.PROJECTS_DIR", tmp_path / "projects")

        assert list_projects() == []

    def test_list_returns_project_names(self, tmp_path, monkeypatch):
        """Should return list of project names."""
        monkeypatch.setattr("autoanki.core.project.PROJECTS_DIR", tmp_path / "projects")

        create_project(project_name="Project A", source_filename="a.txt")
        create_project(project_name="Project B", source_filename="b.txt")

        projects = list_projects()
        assert sorted(projects) == ["project-a", "project-b"]


class TestDeleteProject:
    """Tests for delete_project function."""

    def test_delete_existing_project(self, tmp_path, monkeypatch):
        """Should delete existing project."""
        monkeypatch.setattr("autoanki.core.project.PROJECTS_DIR", tmp_path / "projects")

        create_project(project_name="ToDelete", source_filename="test.txt")
        assert project_exists("ToDelete")

        delete_project("ToDelete")
        assert not project_exists("ToDelete")

    def test_delete_nonexistent_raises(self, tmp_path, monkeypatch):
        """Should raise ValueError for non-existent project."""
        monkeypatch.setattr("autoanki.core.project.PROJECTS_DIR", tmp_path / "projects")

        with pytest.raises(ValueError, match="does not exist"):
            delete_project("NonExistent")


class TestCardsSaveLoad:
    """Tests for saving and loading card data."""

    def test_save_and_load_cards(self, tmp_path, monkeypatch):
        """Should save and load card data."""
        monkeypatch.setattr("autoanki.core.project.PROJECTS_DIR", tmp_path / "projects")

        from autoanki.core.models import AutoAnkiCards, SourceInfo, VocabEntry

        create_project(project_name="Test", source_filename="test.txt")

        cards = AutoAnkiCards(
            source_info=SourceInfo(
                title="Test Source",
                source_language="ko",
                target_language_name="Korean",
                level_description="Beginner",
                available_vocabulary_context="Chapters 1-5",
            ),
            vocabulary=[],
        )

        save_cards("Test", cards)

        loaded = load_cards("Test")
        assert loaded is not None
        assert loaded.source_info.title == "Test Source"
        assert loaded.source_info.source_language == "ko"
        assert loaded.schema_version == 1

    def test_load_cards_missing(self, tmp_path, monkeypatch):
        """Should return None when cards.json doesn't exist."""
        monkeypatch.setattr("autoanki.core.project.PROJECTS_DIR", tmp_path / "projects")

        create_project(project_name="Test", source_filename="test.txt")

        assert load_cards("Test") is None


class TestPastVocab:
    """Tests for past vocabulary save/load."""

    def test_save_and_load_past_vocab(self, tmp_path, monkeypatch):
        """Should save and load past vocabulary."""
        monkeypatch.setattr("autoanki.core.project.PROJECTS_DIR", tmp_path / "projects")

        create_project(project_name="Test", source_filename="test.txt")

        words = ["사람", "집", "학교"]
        save_past_vocab("Test", words)

        loaded = load_past_vocab("Test")
        assert loaded == words

    def test_load_past_vocab_missing(self, tmp_path, monkeypatch):
        """Should return None when no past vocab exists."""
        monkeypatch.setattr("autoanki.core.project.PROJECTS_DIR", tmp_path / "projects")

        create_project(project_name="Test", source_filename="test.txt")

        assert load_past_vocab("Test") is None


class TestLoadSourceText:
    """Tests for loading source text."""

    def test_load_source_text(self, tmp_path, monkeypatch):
        """Should load source text."""
        monkeypatch.setattr("autoanki.core.project.PROJECTS_DIR", tmp_path / "projects")

        create_project(
            project_name="Test",
            source_filename="test.txt",
            source_text="Hello, World!",
        )

        text = load_source_text("Test")
        assert text == "Hello, World!"

    def test_load_missing_source_raises(self, tmp_path, monkeypatch):
        """Should raise ValueError if source.txt missing."""
        monkeypatch.setattr("autoanki.core.project.PROJECTS_DIR", tmp_path / "projects")

        # Create project WITH source text first
        create_project(
            project_name="Test",
            source_filename="test.txt",
            source_text="Some content to create the file",
        )
        # Manually delete source.txt
        (tmp_path / "projects" / "test" / "source.txt").unlink()

        with pytest.raises(ValueError, match="has no source text"):
            load_source_text("Test")


class TestProjectExists:
    """Tests for project_exists function."""

    def test_existing_project(self, tmp_path, monkeypatch):
        """Should return True for existing project."""
        monkeypatch.setattr("autoanki.core.project.PROJECTS_DIR", tmp_path / "projects")

        create_project(project_name="Test", source_filename="test.txt")
        assert project_exists("Test") is True

    def test_nonexistent_project(self, tmp_path, monkeypatch):
        """Should return False for non-existent project."""
        monkeypatch.setattr("autoanki.core.project.PROJECTS_DIR", tmp_path / "projects")

        assert project_exists("NonExistent") is False


class TestCardTypeSelection:
    """Tests for CardTypeSelection model."""

    def test_all_enabled_by_default(self):
        """All card types should be True by default."""
        selection = CardTypeSelection()
        assert selection.enabled_types() == [1, 2, 3, 4, 5]

    def test_enabled_types_subset(self):
        """Should return only enabled types."""
        selection = CardTypeSelection(
            card_1_recognition=True,
            card_2_cloze=True,
            card_3_production=False,
            card_4_comprehension=False,
            card_5_listening=True,
        )
        assert selection.enabled_types() == [1, 2, 5]

    def test_all_disabled(self):
        """Should handle all disabled (empty list)."""
        selection = CardTypeSelection(
            card_1_recognition=False,
            card_2_cloze=False,
            card_3_production=False,
            card_4_comprehension=False,
            card_5_listening=False,
        )
        assert selection.enabled_types() == []

    def test_json_serialization(self):
        """Should serialize/deserialize correctly."""
        selection = CardTypeSelection(
            card_1_recognition=True,
            card_2_cloze=False,
        )
        json_str = selection.model_dump_json()
        data = json.loads(json_str)

        assert data["card_1_recognition"] is True
        assert data["card_2_cloze"] is False
