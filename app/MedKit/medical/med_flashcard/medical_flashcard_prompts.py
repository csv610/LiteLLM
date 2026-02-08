#!/usr/bin/env python3
"""
Standalone module for creating medical flashcard information prompts.

This module provides a builder class for generating system and user prompts
for medical flashcard information generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical flashcard information."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for medical flashcard information generation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are a medical device and flashcard specialist with expertise in biomedical engineering and clinical applications of medical flashcards.

Your responsibilities include:
- Providing comprehensive, evidence-based information about medical flashcards and devices
- Explaining device design, materials, and mechanisms of action
- Describing indications, contraindications, and patient selection criteria
- Detailing flashcardation procedures and technical considerations
- Outlining potential complications, device lifespan, and follow-up requirements
- Discussing regulatory status and clinical outcomes

Guidelines:
- Base all information on current medical device literature and regulatory standards
- Include both technical specifications and clinical perspectives
- Emphasize patient safety, biocompatibility, and long-term outcomes
- Address maintenance, monitoring, and replacement considerations
- Provide balanced information about risks and benefits
- Reference current evidence and clinical guidelines where applicable"""

    @staticmethod
    def create_user_prompt(term: str) -> str:
        """
        Create the user prompt for medical flashcard information.

        Args:
            term: The name of the medical flashcard or term

        Returns:
            str: Formatted user prompt
        """
        return f"Generate comprehensive information for the medical flashcard: {term}."

    @staticmethod
    def create_image_analysis_prompt() -> str:
        """
        Create the prompt for analyzing an image to extract medical terms.

        Returns:
            str: Prompt for image analysis
        """
        return (
            "Analyze this medical flashcard image and extract all the medical terms, "
            "condition names, or device names shown or described. "
            "Return ONLY a comma-separated list of the identified terms. "
            "Do not include any other text or explanation."
        )
