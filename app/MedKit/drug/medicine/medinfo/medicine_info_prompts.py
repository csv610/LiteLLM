"""Prompt templates for Medicine Information module.

This module contains the PromptBuilder class for generating consistent prompts
for medicine information generation.
"""

from utils.cli_base import BasePromptBuilder


class PromptBuilder(BasePromptBuilder):
    """Builder class for creating prompts for medicine information generation.

    Inherits from BasePromptBuilder and implements the abstract methods
    for domain-specific prompt creation.
    """

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for medicine information generation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are a pharmaceutical information specialist with expertise in pharmacology,
pharmacokinetics, and clinical application of medicines. Provide comprehensive, accurate, and
evidence-based information about medicines suitable for both healthcare professionals and
informed patients. Ensure all information reflects current medical knowledge and regulatory standards."""

    @staticmethod
    def create_user_prompt(medicine_name: str) -> str:
        """Create the user prompt for medicine information.

        Args:
            medicine_name: The name of the medicine

        Returns:
            str: Formatted user prompt
        """
        return f"Provide detailed information about the medicine {medicine_name}."
