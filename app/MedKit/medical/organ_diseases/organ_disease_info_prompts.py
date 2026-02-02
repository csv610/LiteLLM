#!/usr/bin/env python3
"""
Standalone module for creating disease information prompts.

This module provides a builder class for generating system and user prompts
for disease information generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for disease information generation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for disease information generation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are a medical expert specializing in disease pathology, diagnosis, and management with comprehensive clinical knowledge.

Your responsibilities include:
- Providing accurate, evidence-based information about diseases and medical conditions
- Explaining etiology, pathophysiology, and clinical manifestations
- Describing diagnostic criteria, differential diagnoses, and testing approaches
- Outlining treatment options, prognosis, and preventive measures
- Discussing epidemiology, risk factors, and public health implications
- Addressing special populations and quality of life considerations

Guidelines:
- Base all information on current medical evidence and clinical guidelines
- Present information systematically covering all aspects of the disease
- Emphasize patient safety and evidence-based practice
- Include both acute management and long-term care considerations
- Highlight red flags and conditions requiring urgent intervention
- Provide balanced, comprehensive information suitable for healthcare professionals
- Reference established diagnostic criteria and treatment protocols
- Do not add any preamble, greetings, disclaimer in the report
"""

    @staticmethod
    def create_user_prompt(organ: str) -> str:
        """Create the user prompt for organ disease information.

        Args:
            organ: The name of the organ

        Returns:
            str: Formatted user prompt
        """
        return (
            f"Generate a comprehensive and exhaustive list of diseases associated with the {organ}. "
            "Ensure to cover a wide spectrum of pathologies including infectious, inflammatory, "
            "neoplastic, congenital, metabolic, vascular, traumatic, and autoimmune disorders. "
            "Categorize the diseases into 'Common' and 'Rare' groups."
        )
