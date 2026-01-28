#!/usr/bin/env python3
"""
Standalone module for creating medical topic prompts.

This module provides a builder class for generating system and user prompts
for medical topic information generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical topic information."""

    @staticmethod
    def create_system_prompt() -> str:
        """Creates the system prompt for medical topic generation."""
        return """You are a medical information expert specializing in providing comprehensive, accurate, and well-structured information about medical topics.

Your task is to generate detailed medical topic information including:
- Clear definitions and descriptions
- Key concepts and terminology
- Clinical significance and applications
- Related conditions or concepts
- Current understanding and research perspectives

Provide information that is:
- Medically accurate and evidence-based
- Well-organized and easy to understand
- Comprehensive yet concise
- Appropriate for healthcare professionals and students"""

    @staticmethod
    def create_user_prompt(topic: str) -> str:
        """Creates the user prompt for medical topic generation.

        Args:
            topic: The name of the medical topic to generate information for

        Returns:
            A formatted user prompt string
        """
        return f"Generate comprehensive information for the medical topic: {topic}."
