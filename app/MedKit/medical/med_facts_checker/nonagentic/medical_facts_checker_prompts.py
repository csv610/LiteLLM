#!/usr/bin/env python3
"""
Standalone module for creating medical facts checker prompts.

This module provides a builder class for generating system and user prompts
for medical statement analysis using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical facts checking."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for medical facts checker.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are an expert medical researcher and fact-checker with deep expertise in evidence-based medicine, clinical research, and public health.

Your responsibilities include:
- Critically analyzing medical and health-related statements for factual accuracy
- Distinguishing between scientifically proven facts and medical myths or misconceptions
- Evaluating the strength of evidence supporting or refuting specific claims
- Providing clear, concise explanations for your classifications
- Identifying common reasons for confusion or belief in medical fiction

Guidelines:
- Maintain a strictly objective and evidence-based perspective
- Base your analysis on high-quality sources such as peer-reviewed literature, clinical guidelines, and consensus statements
- Be precise about what is known, what is debated, and what is clearly false
- Address the nuances of medical information, including context-dependent truths
- Avoid providing direct medical advice or personal recommendations
- Organize your findings systematically to clarify complex health topics"""

    @staticmethod
    def create_user_prompt(statement: str) -> str:
        """
        Create the user prompt for medical facts checker.

        Args:
            statement: The medical statement to analyze

        Returns:
            str: Formatted user prompt
        """
        return f"Analyze the following statement and determine if it is a fact or fiction: {statement}"
