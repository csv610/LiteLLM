"""
Standalone module for creating medical condition identification prompts.

This module provides a builder class for generating system and user prompts
for identifying if a medical condition is well-known in the healthcare community.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MedicalConditionIdentifierInput:
    """Configuration and input for medical condition identification."""
    condition_name: str

    def __post_init__(self):
        """Validate input parameters."""
        if not self.condition_name or not self.condition_name.strip():
            raise ValueError("Condition name cannot be empty")


class PromptBuilder:
    """Builder class for creating prompts for medical condition identification."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for medical condition identification.

        Returns:
            str: System prompt defining the LLM's role and instructions
        """
        return """You are a senior medical consultant with broad expertise across internal medicine, surgery, and specialized care. Your task is to identify if a given "medical condition" name is "well-known" in the healthcare field.

A medical condition (which may be a disease, disorder, syndrome, or injury) is considered "well-known" if it:
1. Is a standard diagnosis recognized by major healthcare organizations (e.g., WHO, Mayo Clinic).
2. Has established clinical guidelines or pathways for management.
3. Is commonly discussed in medical education or patient education materials.
4. Has a clear impact on patient health and requires clinical attention.

When identifying a condition, you must:
1. Determine its recognition status.
2. Identify its category (e.g., chronic disease, acute injury, mental health disorder).
3. List its key characteristics or symptoms.
4. Provide a brief explanation of its clinical significance.

If a condition is extremely rare, poorly defined, or not well-known, clearly state that and explain why.

Always provide accurate, evidence-based information."""

    @staticmethod
    def create_user_prompt(config: MedicalConditionIdentifierInput) -> str:
        """
        Create the user prompt for medical condition identification.

        Args:
            config: Configuration containing the condition name

        Returns:
            str: User prompt
        """
        return f"Identify the medical condition '{config.condition_name}' and determine if it is well-known in the healthcare community. Provide details on its category, characteristics, and clinical significance."
