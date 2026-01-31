"""
Standalone module for creating medical anatomy identification prompts.

This module provides a builder class for generating system and user prompts
for identifying if an anatomical structure is well-known in the medical community.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MedicalAnatomyIdentifierInput:
    """Configuration and input for medical anatomy identification."""
    structure_name: str

    def __post_init__(self):
        """Validate input parameters."""
        if not self.structure_name or not self.structure_name.strip():
            raise ValueError("Structure name cannot be empty")


class PromptBuilder:
    """Builder class for creating prompts for medical anatomy identification."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for medical anatomy identification.

        Returns:
            str: System prompt defining the LLM's role and instructions
        """
        return """You are a senior anatomist and clinical professor with deep expertise in human anatomy, histology, and regional anatomy. Your task is to identify if a given "anatomical structure" name is "well-known" in the medical field.

An anatomical structure (e.g., heart, femur, vagus nerve, hypothalamus) is considered "well-known" if it:
1. Is a standard part of the human body documented in major anatomical atlases (like Netter or Gray's).
2. Is a primary focus in medical education and clinical practice.
3. Has a clear physiological or structural role.
4. Is frequently relevant to clinical diagnosis, surgery, or pathology.

When identifying a structure, you must:
1. Determine its recognition status.
2. Identify the body system it belongs to.
3. Describe its general location.
4. Provide a brief explanation of its clinical significance.

If a structure is extremely minor, a rare variation, or not well-known, clearly state that and explain why.

Always provide accurate, evidence-based information."""

    @staticmethod
    def create_user_prompt(config: MedicalAnatomyIdentifierInput) -> str:
        """
        Create the user prompt for medical anatomy identification.

        Args:
            config: Configuration containing the structure name

        Returns:
            str: User prompt
        """
        return f"Identify the anatomical structure '{config.structure_name}' and determine if it is well-known in the medical community. Provide details on its system, location, and clinical significance."
