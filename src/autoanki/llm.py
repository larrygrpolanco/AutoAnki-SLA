import json
from pathlib import Path
from typing import Callable

from openai import OpenAI
from pydantic import ValidationError

from .models import AutoAnkiCards

PROMPTS_DIR = Path(__file__).parent / "prompts"


def run_pipeline(
    text: str,
    past_vocab: list[str] | None = None,
    progress_callback: Callable[[str], None] | None = None,
    model: str = "gpt-4o-mini",
) -> AutoAnkiCards:
    client = OpenAI()

    def _notify(msg: str):
        if progress_callback:
            progress_callback(msg)

    # Build vocabulary context string
    vocab_context = "Use only words from the source text and basic, universally-known words at the learner's level."
    if past_vocab:
        word_list = ", ".join(past_vocab[:200])
        vocab_context += f" Previously learned vocabulary (may be used in example sentences): {word_list}."

    # Load prompt files
    drafting_prompt = (PROMPTS_DIR / "card_drafting.txt").read_text(encoding="utf-8")
    review_prompt = (PROMPTS_DIR / "card_review.txt").read_text(encoding="utf-8")
    structuring_prompt = (PROMPTS_DIR / "structuring.txt").read_text(encoding="utf-8")

    # Step 1: Card Drafting
    _notify("Step 1/3: Drafting cards...")
    step1_response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": drafting_prompt},
            {
                "role": "user",
                "content": f"Vocabulary context: {vocab_context}\n\nSource text:\n{text}",
            },
        ],
        max_completion_tokens=4096,
    )
    step1_output = step1_response.choices[0].message.content

    # Step 2: Review & Quality Check
    _notify("Step 2/3: Reviewing card quality...")
    step2_response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": review_prompt},
            {
                "role": "user",
                "content": (
                    f"Original source text:\n{text}\n\n"
                    f"Generated cards to review:\n{step1_output}"
                ),
            },
        ],
        max_completion_tokens=4096,
    )
    step2_output = step2_response.choices[0].message.content

    # Step 3: Structuring (JSON output, retry once on failure)
    _notify("Step 3/3: Structuring output...")
    last_error = None
    for attempt in range(2):
        step3_response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": structuring_prompt},
                {"role": "user", "content": step2_output},
            ],
            response_format={"type": "json_object"},
            max_completion_tokens=4096,
        )
        raw_json = step3_response.choices[0].message.content
        try:
            data = json.loads(raw_json)
            return AutoAnkiCards.model_validate(data)
        except (json.JSONDecodeError, ValidationError) as e:
            last_error = e
            if attempt == 0:
                _notify("Step 3/3: Retrying structuring...")

    raise RuntimeError(
        f"LLM failed to produce valid JSON after 2 attempts.\n"
        f"Last error: {last_error}\n"
        f"Raw output (first 500 chars): {raw_json[:500]}"
    )
