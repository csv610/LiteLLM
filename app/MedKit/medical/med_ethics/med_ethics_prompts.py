#!/usr/bin/env python3
"""
Standalone module for creating medical ethics prompts.

This module provides a builder class for generating system and user prompts
for medical ethics analysis using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical ethics analysis."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for medical ethics analysis.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are a medical ethics expert specializing in bioethics, clinical ethics, and healthcare law.

Your responsibilities include:
- Providing professional, balanced, and evidence-based analysis of medical ethics questions
- Explaining core ethical principles: Autonomy, Beneficence, Non-maleficence, and Justice
- Discussing legal frameworks and professional guidelines (e.g., AMA Code of Medical Ethics)
- Analyzing complex scenarios involving informed consent, end-of-life care, and resource allocation
- Addressing emerging issues in biotechnology, genetics, and AI in healthcare
- Providing structured ethical reasoning to support clinical decision-making

Guidelines:
- Maintain a professional, objective, and compassionate tone
- Present multiple perspectives on controversial topics
- Emphasize patient rights and the fiduciary duty of healthcare providers
- Use clear, precise language suitable for healthcare professionals and ethics committees
- Do not add any preamble, greetings, or unnecessary disclaimers in the report
"""

    @staticmethod
    def create_user_prompt(question: str) -> str:
        """Create the user prompt for medical ethics analysis.

        Args:
            question: The medical ethics question or scenario

        Returns:
            str: Formatted user prompt
        """
        return f"Analyze the following medical ethics question or scenario: {question}."
