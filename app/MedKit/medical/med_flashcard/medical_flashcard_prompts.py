#!/usr/bin/env python3
"""
Standalone module for creating medical label explanation prompts.

This module provides a builder class for generating system and user prompts
for medical label explanation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical label explanation."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for medical label explanation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are a medical expert and educator specializing in medical terminology and clinical applications.

Your goal is to provide concise, high-quality explanations for medical terms, devices, or conditions.

Guidelines:
- Each explanation must be between 100 and 200 words.
- Focus specifically on the functionality (how it works or what it does) and its medical importance (why it matters in clinical practice).
- Use professional yet accessible language suitable for medical students or professionals.
- Ensure the information is accurate and evidence-based."""

    @staticmethod
    def create_user_prompt(term: str) -> str:
        """
        Create the user prompt for medical flashcard information.

        Args:
            term: The name of the medical flashcard or term

        Returns:
            str: Formatted user prompt
        """
        return (
            f"Explain the following medical term: {term}. "
            "The explanation must be between 100 and 200 words and "
            "must emphasize its functionality and medical importance."
        )

    @staticmethod
    def create_text_extraction_prompt() -> str:
        """
        Create the prompt for analyzing an image to extract medical terms.

        Returns:
            str: Prompt for image analysis
        """
        return (
            "Analyze this image and extract all the medical terms, "
            "condition names, or device names shown or described. "
            "Return ONLY a comma-separated list of the identified terms. "
            "Do not include any other text or explanation."
        )

    
