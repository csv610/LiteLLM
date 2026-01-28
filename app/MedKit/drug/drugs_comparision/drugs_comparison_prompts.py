#!/usr/bin/env python3
"""
Standalone module for creating drugs comparison prompts.

This module provides a builder class for generating system and user prompts
for drugs comparison analysis using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medicines comparison analysis."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for medicines comparison analysis.

        Returns:
            str: System prompt defining the AI's role and instructions
        """
        return """You are a clinical pharmacology expert specializing in comparative medication analysis. Your role is to provide comprehensive, objective comparisons between medications to help healthcare professionals and patients make informed treatment decisions.

When comparing medications, you must:

1. Compare efficacy and effectiveness based on clinical evidence
2. Analyze safety profiles, side effects, and contraindications
3. Evaluate cost, availability, and insurance coverage considerations
4. Compare mechanisms of action and pharmacokinetics
5. Assess suitability for different patient populations (age, conditions, etc.)
6. Identify key differences in dosing, administration, and monitoring requirements
7. Consider drug interactions and precautions for each medication
8. Provide evidence-based recommendations considering patient-specific factors
9. Base analysis on established medical literature, clinical trials, and regulatory guidance

Always maintain objectivity and present balanced information to support informed decision-making."""

    @staticmethod
    def create_user_prompt(medicine1: str, medicine2: str, context: str) -> str:
        """
        Create the user prompt for medicines comparison analysis.

        Args:
            medicine1: The name of the first medicine
            medicine2: The name of the second medicine
            context: Additional context for the comparison

        Returns:
            str: Formatted user prompt
        """
        return f"Detailed side-by-side comparison between {medicine1} and {medicine2}. {context}"
