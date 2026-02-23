"""
Standalone module for creating medical abbreviation identification prompts.

This module provides a builder class for generating system and user prompts
for identifying and expanding medical abbreviations.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class AbbreviationIdentifierInput:
    """Configuration and input for abbreviation identification."""
    abbreviation: str

    def __post_init__(self):
        """Validate input parameters."""
        if not self.abbreviation or not self.abbreviation.strip():
            raise ValueError("Abbreviation cannot be empty")


class PromptBuilder:
    """Builder class for creating prompts for abbreviation identification."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for abbreviation identification.

        Returns:
            str: System prompt defining the LLM's role and instructions
        """
        return """You are a senior medical scribe and clinical documentation specialist. Your task is to identify and expand "medical abbreviations" or "clinical shorthand" commonly used in healthcare.

A medical abbreviation (e.g., BID, PRN, COPD, CHF, NPO) is considered "well-known" if it:
1. Is part of standard clinical documentation protocols.
2. Is widely used in electronic health records (EHRs) or handwritten notes.
3. Has a universally accepted expansion within the medical community.
4. Represents a specific frequency, condition, procedure, or instruction.

When identifying an abbreviation, you must:
1. Determine if it is a standard, well-known abbreviation.
2. Provide its full expanded form.
3. Describe the typical context of use.
4. Briefly explain its clinical meaning.

If an abbreviation is ambiguous, highly localized, or not well-known, clearly state that and explain the potential interpretations.

Always provide accurate, evidence-based information."""

    @staticmethod
    def create_user_prompt(config: AbbreviationIdentifierInput) -> str:
        """
        Create the user prompt for abbreviation identification.

        Args:
            config: Configuration containing the abbreviation

        Returns:
            str: User prompt
        """
        return f"Identify and expand the medical abbreviation '{config.abbreviation}'. Determine if it is well-known and provide its full form, context of use, and clinical meaning."
