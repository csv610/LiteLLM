"""
Standalone module for creating disease identification prompts.

This module provides a builder class for generating system and user prompts
for identifying if a disease is well-known in the medical community.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DiseaseIdentifierInput:
    """Configuration and input for disease identification."""
    disease_name: str

    def __post_init__(self):
        """Validate input parameters."""
        if not self.disease_name or not self.disease_name.strip():
            raise ValueError("Disease name cannot be empty")


class PromptBuilder:
    """Builder class for creating prompts for disease identification."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for disease identification.

        Returns:
            str: System prompt defining the LLM's role and instructions
        """
        return """You are a medical expert and epidemiologist with extensive knowledge of global health, pathology, and clinical medicine. Your task is to identify if a given disease name is "well-known" in the medical community.

A disease is considered "well-known" if it:
1. Has a clear clinical definition and diagnostic criteria.
2. Is frequently encountered in medical practice or studied in medical education.
3. Is documented in major medical databases (like ICD-10/11).
4. Has established treatment protocols or public health management strategies.

When identifying a disease, you must:
1. Determine its medical recognition status.
2. List its primary symptoms.
3. Note its general prevalence and public health impact.
4. Provide a brief explanation of its medical significance.

If a condition is obscure, extremely rare, or not well-known, clearly state that and explain why.

Always provide accurate, evidence-based information."""

    @staticmethod
    def create_user_prompt(config: DiseaseIdentifierInput) -> str:
        """
        Create the user prompt for disease identification.

        Args:
            config: Configuration containing the disease name

        Returns:
            str: User prompt
        """
        return f"Identify the disease '{config.disease_name}' and determine if it is a well-known disease in the medical community. Provide details on its common symptoms and medical significance."
