"""Pydantic models for AutoAnki data structures."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

# Schema version for migration tracking
SCHEMA_VERSION = 1


class ProjectStatus(str, Enum):
    """Status of a project through the generation pipeline."""

    IMPORTED = "imported"  # Text extracted, not yet sent to LLM
    CONFIGURED = "configured"  # User has set card types and optional past vocab
    GENERATED = "generated"  # LLM has produced cards
    REVIEWED = "reviewed"  # User has reviewed/edited
    EXPORTED = "exported"  # Deck has been built


class CardTypeSelection(BaseModel):
    """Which of the 5 card types to generate. All default to True."""

    card_1_recognition: bool = True
    card_2_cloze: bool = True
    card_3_production: bool = True
    card_4_comprehension: bool = True
    card_5_listening: bool = True

    def enabled_types(self) -> list[int]:
        """Returns list of enabled card type numbers, e.g. [1, 2, 5]."""
        types = []
        if self.card_1_recognition:
            types.append(1)
        if self.card_2_cloze:
            types.append(2)
        if self.card_3_production:
            types.append(3)
        if self.card_4_comprehension:
            types.append(4)
        if self.card_5_listening:
            types.append(5)
        return types


class ProjectMeta(BaseModel):
    """Metadata for an AutoAnki project stored in meta.json."""

    schema_version: int = SCHEMA_VERSION
    project_name: str
    deck_name: str
    source_language: str = ""  # e.g. "ko", "es", "ar"
    target_language_name: str = ""  # e.g. "Korean", "Spanish"
    level_description: str = ""  # e.g. "Beginner, Chapter 5"
    source_filename: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: ProjectStatus
    generate_audio: bool = True
    card_types: CardTypeSelection = Field(default_factory=CardTypeSelection)
    has_past_vocab: bool = False
    available_vocabulary_context: str = ""  # Description for LLM: what vocab is available
    vocab_count: int = 0


class SourceInfo(BaseModel):
    """Information about the source material."""

    title: str
    source_language: str  # ISO 639-1 code
    target_language_name: str
    level_description: str
    available_vocabulary_context: str  # Describes what words the LLM may use in sentences


class Card1Recognition(BaseModel):
    """Card 1: Recognition - See the word, recall the meaning."""

    sentence_target: str  # Full sentence in target language
    sentence_target_highlight: str  # Same sentence with target word in <b> tags
    sentence_english: str  # English translation


class Card2Cloze(BaseModel):
    """Card 2: Contextual Recall (Cloze) - Fill in the blank from context + hint."""

    sentence_cloze: str  # Sentence with {{c1::word}} syntax
    sentence_english: str
    english_hint: str  # English meaning of blanked word (mandatory)


class Card3Production(BaseModel):
    """Card 3: Production - See English, produce the target word."""

    sentence_target: str  # New example sentence
    sentence_english: str


class Card4Comprehension(BaseModel):
    """Card 4: Sentence Comprehension - Read full sentence, understand the word."""

    sentence_target: str  # Sentence without highlight (front)
    sentence_english: str
    word_in_sentence_highlight: str  # Same sentence with target word in <b> (back)
    word_translation_in_context: str  # Contextual translation e.g. "buys"


class Card5Listening(BaseModel):
    """Card 5: Listening - Hear the word, understand it."""

    sentence_target: str  # Sentence text (for back display + TTS)
    sentence_english: str
    word_in_sentence_highlight: str  # Highlighted version (back)
    word_translation_in_context: str  # Contextual translation


class AudioQueries(BaseModel):
    """Pre-cleaned target-language text for TTS. No cloze syntax, no HTML, no English."""

    word_isolated: str
    sentence_1: str
    sentence_2: str
    sentence_3: str
    sentence_4: str
    sentence_5: str


class VocabEntry(BaseModel):
    """A single vocabulary entry with all card types and audio queries."""

    id: UUID = Field(default_factory=uuid4)  # Stable UUID
    target_word: str  # Dictionary/base form
    target_word_romanization: str = ""  # Optional, never shown on cards
    english_translation: str  # Concise (1-4 words)
    part_of_speech: str  # noun, verb, adjective, etc.
    category: str = "General"  # Thematic grouping
    notes: str = ""  # Optional user annotations
    generate_audio: bool = True  # Per-word audio toggle

    # Card data — all five are always present in JSON even if the user
    # chose not to generate certain card types. This keeps the schema
    # stable. The deck builder skips disabled card types at export time.
    card_1_recognition: Card1Recognition
    card_2_cloze: Card2Cloze
    card_3_production: Card3Production
    card_4_comprehension: Card4Comprehension
    card_5_listening: Card5Listening

    audio_queries: AudioQueries


class AutoAnkiCards(BaseModel):
    """Complete card data for a project - the single source of truth.

    This is the root model stored in cards.json. It contains all vocabulary
    entries with their associated card data and audio queries.
    """

    schema_version: int = SCHEMA_VERSION
    source_info: SourceInfo
    vocabulary: list[VocabEntry] = []


# Legacy alias for backwards compatibility (renamed from FlashForgeCards)
FlashForgeCards = AutoAnkiCards
