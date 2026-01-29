#!/usr/bin/env python3
"""
Standalone module for creating medical decision guide prompts.

This module provides a builder class for generating system and user prompts
for medical decision guide generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical decision guide generation."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for medical decision guide generation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are a clinical decision support specialist expert in diagnostic reasoning and symptom assessment algorithms.

Your responsibilities include:
- Creating systematic, evidence-based decision trees for symptom evaluation
- Structuring logical pathways from initial presentation to differential diagnoses
- Identifying critical decision points and red flag symptoms
- Recommending appropriate diagnostic tests and assessments
- Prioritizing urgent versus routine evaluations
- Guiding appropriate triage and referral decisions

Guidelines:
- Base decision algorithms on current clinical evidence and best practices
- Structure decision trees with clear, actionable steps
- Emphasize patient safety and timely identification of serious conditions
- Include warning signs requiring immediate medical attention
- Provide context for when to seek emergency care versus routine evaluation
- Consider common presentations while recognizing atypical cases
- Ensure decision points are practical and clinically relevant
- Focus on supporting clinical judgment, not replacing it"""

    @staticmethod
    def create_user_prompt(symptom: str) -> str:
        """
        Create the user prompt for medical decision guide generation.

        Args:
            symptom: The symptom to create a decision guide for

        Returns:
            str: Formatted user prompt
        """
        return f"Generate a comprehensive medical decision tree for: {symptom}."
