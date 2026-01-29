#!/usr/bin/env python3
"""
Standalone module for creating medical specialist referral prompts.

This module provides a builder class for generating system and user prompts
for medical specialist recommendation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical specialist recommendation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for specialist recommendation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are a medical assistant. Based on the given medical question, recommend the most suitable specialist doctors.
Some symptoms may require consultation with multiple specialists.

Example format:
- Question: "I have chest pain and shortness of breath."
  Specialists: Cardiologist, Pulmonologist

- Question: "I have severe joint pain and swelling."
  Specialists: Rheumatologist, Orthopedic Surgeon

- Question: "I have blurry vision and headaches."
  Specialists: Ophthalmologist, Neurologist"""

    @staticmethod
    def create_user_prompt(question: str) -> str:
        """Create the user prompt for specialist recommendation.

        Args:
            question: The patient's medical question or symptoms

        Returns:
            str: Formatted user prompt
        """
        return f"""Now, analyze the following question and recommend the best specialists:

Question: "{question}"
Specialists:"""