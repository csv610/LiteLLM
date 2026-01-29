#!/usr/bin/env python3
"""
Standalone module for creating medical term extraction prompts.

This module provides a builder class for generating system and user prompts
for medical term extraction using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical term extraction."""

    @staticmethod
    def create_system_prompt() -> str:
        """Generate the system prompt for medical term extraction."""
        return "You are an expert medical documentation specialist. Extract medical terms accurately from the provided text."

    @staticmethod
    def create_user_prompt(text: str) -> str:
        """Generate the user prompt for term extraction."""
        return f"""Extract all medical terms from the following text and structure them according to the provided schema.

Text to extract from:
{text}

For each category:
- Extract only relevant terms that appear in the text
- Include the context (the sentence or phrase where it appears)
- For side_effects, include the related_medicine if mentioned
- For causation_relationships, identify connections between medical concepts (e.g., "disease X causes symptom Y")

Be thorough and accurate. Extract ALL medical terms found in the text."""
