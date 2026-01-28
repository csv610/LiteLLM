#!/usr/bin/env python3
"""
Standalone module for creating medical FAQ prompts.

This module provides a builder class for generating system and user prompts
for medical FAQ generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical FAQ generation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for FAQ generation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return (
            "You are a medical information specialist creating patient-friendly FAQs. "
            "Your responses should be accurate, clear, and accessible to non-medical audiences. "
            "Organize information in logical sections with concise, informative answers. "
            "Always encourage users to consult healthcare professionals for medical advice."
        )

    @staticmethod
    def create_user_prompt(topic: str) -> str:
        """Create the user prompt for FAQ generation.

        Args:
            topic: The medical topic to generate FAQs for

        Returns:
            str: Formatted user prompt
        """
        return f"Generate comprehensive patient-friendly FAQs for: {topic}."
