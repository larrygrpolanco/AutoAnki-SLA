"""LLM pipeline for card generation (3-step process)."""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Any
from uuid import uuid4

from openai import OpenAI
from pydantic import ValidationError

from autoanki.core.models import (
    AutoAnkiCards,
    Card1Recognition,
    Card2Cloze,
    Card3Production,
    Card4Comprehension,
    Card5Listening,
    CardTypeSelection,
    ProjectMeta,
    SourceInfo,
    VocabEntry,
    AudioQueries,
)

# Default model for all steps
DEFAULT_MODEL = "gpt-4o-mini"

# Maximum retries for JSON validation
MAX_RETRIES = 2

# Retry delay in seconds
RETRY_DELAY = 1


def _load_prompt(prompt_name: str) -> str:
    """Load a prompt file from the prompts directory.

    Args:
        prompt_name: Name of the prompt file (e.g., "card_drafting.txt")

    Returns:
        The prompt text content

    Raises:
        FileNotFoundError: If prompt file doesn't exist
    """
    # Find prompts directory relative to package
    package_dir = Path(__file__).parent.parent.parent
    prompts_dir = package_dir / "prompts"

    if not prompts_dir.exists():
        # Try current working directory
        prompts_dir = Path("prompts")

    prompt_path = prompts_dir / prompt_name

    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    return prompt_path.read_text(encoding="utf-8")


class LLMClient:
    """Wrapper for OpenAI API calls with error handling and retries."""

    def __init__(self, api_key: str | None = None, model: str = DEFAULT_MODEL):
        """Initialize the LLM client.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model to use for generation
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def chat(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> str:
        """Make a chat completion request.

        Args:
            system_prompt: System prompt text
            user_message: User message content
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate

        Returns:
            The generated response text

        Raises:
            LLMError: If the API call fails
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )

            return response.choices[0].message.content or ""

        except Exception as e:
            raise LLMError(f"LLM API call failed: {e}") from e


class LLMError(Exception):
    """Error during LLM API call."""

    pass


class CardGenerationError(Exception):
    """Error during card generation pipeline."""

    pass


def _create_user_message(
    source_text: str,
    available_vocab_context: str,
    level_description: str,
    title: str,
) -> str:
    """Create the user message for the drafting step."""
    return f"""## Source Material

Title: {title}
Level: {level_description}

## Available Vocabulary Context

{available_vocab_context}

## Source Text

{source_text}
"""


def step1_drafting(
    client: LLMClient,
    source_text: str,
    available_vocab_context: str,
    level_description: str,
    title: str,
) -> str:
    """Step 1: Draft cards from source text.

    Args:
        client: LLM client instance
        source_text: Extracted source text
        available_vocab_context: Context about available vocabulary
        level_description: Level description (e.g., "Beginner, Chapter 5")
        title: Title of the source material

    Returns:
        Drafted card content as semi-structured text
    """
    system_prompt = _load_prompt("card_drafting.txt")
    user_message = _create_user_message(
        source_text, available_vocab_context, level_description, title
    )

    return client.chat(
        system_prompt=system_prompt,
        user_message=user_message,
        temperature=0.7,
    )


def step2_review(
    client: LLMClient,
    drafted_content: str,
    source_text: str,
    available_vocab_context: str,
) -> str:
    """Step 2: Review and correct drafted cards.

    Args:
        client: LLM client instance
        drafted_content: Output from Step 1
        source_text: Original source text for cross-reference
        available_vocab_context: Context about available vocabulary

    Returns:
        Reviewed and corrected card content
    """
    system_prompt = _load_prompt("card_review.txt")
    user_message = f"""## Drafted Cards

{drafted_content}

---

## Original Source Text (for reference)

{source_text}

---

## Available Vocabulary Context

{available_vocab_context}
"""

    return client.chat(
        system_prompt=system_prompt,
        user_message=user_message,
        temperature=0.5,  # Lower temperature for review - more deterministic
    )


def step3_structuring(
    client: LLMClient,
    reviewed_content: str,
    source_info: SourceInfo,
) -> str:
    """Step 3: Structure reviewed content into JSON.

    Args:
        client: LLM client instance
        reviewed_content: Output from Step 2
        source_info: Source information for the JSON header

    Returns:
        Valid JSON string matching AutoAnkiCards schema
    """
    system_prompt = _load_prompt("structuring.txt")
    user_message = f"""## Reviewed Card Content

{reviewed_content}

---

## Source Information

Title: {source_info.title}
Source Language: {source_info.source_language}
Target Language: {source_info.target_language_name}
Level: {source_info.level_description}
Available Vocabulary Context: {source_info.available_vocabulary_context}
"""

    return client.chat(
        system_prompt=system_prompt,
        user_message=user_message,
        temperature=0.3,  # Even lower for JSON - strict formatting
    )


def _extract_json_from_response(response: str) -> str:
    """Extract JSON from an LLM response.

    Handles cases where LLM wraps JSON in markdown code blocks.

    Args:
        response: Raw LLM response text

    Returns:
        Clean JSON string
    """
    # Remove markdown code blocks if present
    response = response.strip()

    # Check for markdown code block
    if response.startswith("```json"):
        response = response[7:]  # Remove ```json
    elif response.startswith("```"):
        response = response[3:]  # Remove ```

    if response.endswith("```"):
        response = response[:-3]  # Remove trailing ```

    return response.strip()


def _validate_and_parse_json(json_str: str) -> AutoAnkiCards:
    """Validate JSON string and parse into AutoAnkiCards model.

    Args:
        json_str: JSON string to validate

    Returns:
        Parsed AutoAnkiCards object

    Raises:
        ValueError: If JSON is invalid or doesn't match schema
    """
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

    try:
        return AutoAnkiCards.model_validate(data)
    except ValidationError as e:
        raise ValueError(f"Schema validation failed: {e}") from e


def generate_cards(
    source_text: str,
    available_vocab_context: str,
    level_description: str,
    title: str,
    source_language: str,
    target_language_name: str,
    api_key: str | None = None,
    progress_callback: callable | None = None,
) -> AutoAnkiCards:
    """Generate flashcards from source text using the 3-step LLM pipeline.

    This is the main entry point for Phase 2. It runs the complete pipeline:
    1. Card drafting (extract vocabulary, create sentences)
    2. Quality review (check i+1, cloze ambiguity, etc.)
    3. JSON structuring (convert to valid schema)

    Args:
        source_text: The extracted text from the source material
        available_vocab_context: Description of what vocabulary can be used
        level_description: Level info (e.g., "Beginner, Chapter 5")
        title: Title of the source material
        source_language: ISO 639-1 code (e.g., "ko", "es")
        target_language_name: Human-readable language name (e.g., "Korean")
        api_key: Optional OpenAI API key (defaults to env var)
        progress_callback: Optional callback(step: int, total: int, message: str)

    Returns:
        AutoAnkiCards object with all vocabulary entries

    Raises:
        CardGenerationError: If pipeline fails after all retries
        LLMError: If LLM API calls fail
    """
    client = LLMClient(api_key=api_key)

    def report_progress(step: int, message: str):
        if progress_callback:
            progress_callback(step, 3, message)

    # Step 1: Drafting
    report_progress(1, "Drafting cards from source text...")
    try:
        drafted = step1_drafting(
            client=client,
            source_text=source_text,
            available_vocab_context=available_vocab_context,
            level_description=level_description,
            title=title,
        )
    except LLMError as e:
        raise CardGenerationError(f"Step 1 (drafting) failed: {e}")

    # Step 2: Review
    report_progress(2, "Reviewing card quality...")
    try:
        reviewed = step2_review(
            client=client,
            drafted_content=drafted,
            source_text=source_text,
            available_vocab_context=available_vocab_context,
        )
    except LLMError as e:
        raise CardGenerationError(f"Step 2 (review) failed: {e}")

    # Step 3: Structuring with retry
    report_progress(3, "Structuring into JSON format...")

    source_info = SourceInfo(
        title=title,
        source_language=source_language,
        target_language_name=target_language_name,
        level_description=level_description,
        available_vocabulary_context=available_vocab_context,
    )

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            json_str = step3_structuring(
                client=client,
                reviewed_content=reviewed,
                source_info=source_info,
            )

            # Clean up response
            json_str = _extract_json_from_response(json_str)

            # Validate and parse
            cards = _validate_and_parse_json(json_str)

            # Ensure source_info is set correctly
            cards.source_info = source_info

            return cards

        except (ValidationError, ValueError) as e:
            last_error = e
            if attempt < MAX_RETRIES - 1:
                # Append error to reviewed content and retry
                reviewed += f"\n\n---\n\nJSON VALIDATION ERROR (attempt {attempt + 1}):\n{e}\n\nPlease fix the JSON and ensure it matches the schema exactly."
                time.sleep(RETRY_DELAY)
            continue

    # All retries exhausted
    raise CardGenerationError(
        f"Step 3 (structuring) failed after {MAX_RETRIES} attempts. Last error: {last_error}"
    )


def generate_and_save_cards(
    project_name: str,
    source_text: str,
    available_vocab_context: str,
    level_description: str,
    title: str,
    source_language: str,
    target_language_name: str,
    api_key: str | None = None,
    progress_callback: callable | None = None,
) -> AutoAnkiCards:
    """Generate cards and save them to the project.

    This convenience function combines generate_cards() with project.save_cards().

    Args:
        project_name: Name of the project
        source_text: Source text content
        available_vocab_context: Vocabulary context for LLM
        level_description: Level description
        title: Source material title
        source_language: ISO language code
        target_language_name: Human-readable language name
        api_key: Optional API key
        progress_callback: Optional progress callback

    Returns:
        The generated AutoAnkiCards object
    """
    from autoanki.core import project

    # Generate cards
    cards = generate_cards(
        source_text=source_text,
        available_vocab_context=available_vocab_context,
        level_description=level_description,
        title=title,
        source_language=source_language,
        target_language_name=target_language_name,
        api_key=api_key,
        progress_callback=progress_callback,
    )

    # Save to project
    project.save_cards(project_name, cards)

    # Update project metadata
    meta = project.load_project_meta(project_name)
    meta.status = "generated"  # type: ignore
    meta.vocab_count = len(cards.vocabulary)
    project.save_project_meta(project_name, meta)

    return cards
