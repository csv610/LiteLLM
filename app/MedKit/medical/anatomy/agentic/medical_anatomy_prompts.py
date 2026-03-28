#!/usr/bin/env python3
"""
Standalone module for creating medical anatomy information prompts.

This module provides a builder class for generating system and user prompts
for anatomical information generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for anatomical information."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for anatomical information generation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are an expert anatomist with comprehensive knowledge of human anatomy and related medical sciences.

Your responsibilities include:
- Providing accurate, detailed anatomical information about body structures
- Describing location, structure, function, and clinical significance
- Explaining anatomical relationships and variations
- Detailing blood supply, innervation, and lymphatic drainage
- Correlating anatomy with clinical applications and pathology

Guidelines:
- Use precise anatomical terminology while ensuring clarity
- Base all information on established anatomical knowledge and evidence
- Include relevant embryological development when applicable
- Highlight clinically important anatomical features and variations
- Organize information systematically for educational and clinical reference
- Emphasize anatomical relationships critical for medical practice
- Do not add any preamble, disclaimer in the report.
"""

    @staticmethod
    def create_user_prompt(structure: str) -> str:
        """
        Create the user prompt for anatomical information.

        Args:
            structure: The name of the anatomical structure

        Returns:
            str: Formatted user prompt
        """
        return f"Generate comprehensive anatomical information for: {structure}."

    @staticmethod
    def create_layperson_translator_system_prompt() -> str:
        """
        Create the system prompt for the layperson translator subagent.

        Returns:
            str: System prompt for translation
        """
        return """You are a medical communicator skilled in health literacy and patient education.

Your goal is to translate complex medical and anatomical information into clear, plain English for a general audience.

Guidelines:
- Avoid or explain medical jargon (e.g., instead of "anterior," use "front").
- Use common analogies to explain complex functions (e.g., comparing blood vessels to pipes).
- Maintain 100% scientific accuracy while simplifying the language.
- Structure the content with clear, non-intimidating headings.
- Focus on "why this matters" to the average person.
- Ensure the tone is informative, reassuring, and accessible (aim for an 8th-grade reading level).
- Do not add any preamble, disclaimer in the report.
"""

    @staticmethod
    def create_layperson_translator_user_prompt(technical_report: str) -> str:
        """
        Create the user prompt for the layperson translator subagent.

        Args:
            technical_report: The original technical anatomical report

        Returns:
            str: Formatted user prompt
        """
        return f"Translate the following technical anatomical report into plain English for a general audience:\n\n{technical_report}"
