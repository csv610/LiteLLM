"""
unsolved_problems_prompts.py - Prompt builder for unsolved problems.

Contains prompts for both the research agent and the review agent.
"""

import json
from typing import Dict


class PromptBuilder:
    """Builder class for creating prompts for unsolved problems information."""

    @staticmethod
    def get_generation_system_prompt() -> str:
        """System prompt for the research agent."""
        return (
            "You are a research agent producing academically recognized unsolved problems. "
            "Return valid JSON only. Prefer established open problems over speculative claims. "
            "Do not include solved or discredited items. Keep fields concise and factual."
        )

    @staticmethod
    def get_generation_user_prompt(topic: str, num_problems: int) -> str:
        """User prompt for the research agent."""
        return f"""Provide a list of {num_problems} famous unsolved problems in {topic}.

For each problem, provide:
1. Title: The name of the problem
2. Description: A brief, clear explanation of what the problem is and why it matters
3. Field: The specific field or subfield it belongs to
4. Difficulty: Estimated difficulty level (Elementary, Moderate, or Advanced)
5. First Posed: When or by whom the problem was first posed (if known)
6. Prize Money: Any prize money associated with solving it (if applicable)
7. Significance: Why solving this problem would be significant for the field
8. Current Status: The best known results or current status as of today (describe recent progress, partial solutions, or approaches)

Focus on well-known, legitimate unsolved problems in {topic}. Use objective language and avoid speculation.
Ensure the problems are academically recognized and well-documented."""

    @staticmethod
    def get_review_system_prompt() -> str:
        """System prompt for the review agent."""
        return (
            "You are a review agent validating structured research output. "
            "Return valid JSON only. Remove duplicates, fix weak phrasing, normalize fields, "
            "and keep only legitimate unsolved problems. Preserve the requested topic."
        )

    @staticmethod
    def get_review_user_prompt(topic: str, num_problems: int, draft_payload: Dict) -> str:
        """User prompt for the review agent."""
        draft_json = json.dumps(draft_payload, indent=2, ensure_ascii=False)
        return f"""Review the following draft list of unsolved problems for {topic}.

Requirements:
1. Keep exactly {num_problems} problems if the draft contains at least that many valid entries.
2. Remove duplicates and any item that appears solved, fictional, or poorly specified.
3. Normalize wording so fields are clear, compact, and academically grounded.
4. Preserve the required schema and return only valid JSON.

Draft JSON:
{draft_json}"""
