"""
Standalone module for creating medical specialty identification prompts.

This module provides a builder class for generating system and user prompts
for identifying if a medical specialty is well-known in the healthcare community.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MedicalSpecialtyIdentifierInput:
    """Configuration and input for medical specialty identification."""
    specialty_name: str

    def __post_init__(self):
        """Validate input parameters."""
        if not self.specialty_name or not self.specialty_name.strip():
            raise ValueError("Specialty name cannot be empty")


class PromptBuilder:
    """Builder class for creating prompts for medical specialty identification."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for medical specialty identification.

        Returns:
            str: System prompt defining the LLM's role and instructions
        """
        return """You are a senior medical director and academic dean responsible for overseeing clinical departments and medical residency programs. Your task is to identify if a given "medical specialty" name is "well-known" in the healthcare field.

A medical specialty (e.g., Cardiology, Nephrology, Orthopedic Surgery, Pediatrics) is considered "well-known" if it:
1. Is a recognized field of medical practice with dedicated residency and fellowship training.
2. Has its own professional board (e.g., American Board of Internal Medicine).
3. Focuses on specific body systems, patient populations, or types of medical interventions.
4. Is a standard department in major hospitals and clinics.

When identifying a specialty, you must:
1. Determine its recognition status.
2. Identify the major organs or systems it treats.
3. List common procedures performed within the specialty.
4. Provide a brief description of its clinical scope.

If a specialty is highly niche, experimental, or not well-known, clearly state that and explain why.

Always provide accurate, evidence-based information."""

    @staticmethod
    def create_user_prompt(name) -> str:
        """
        Create the user prompt for medical specialty identification.

        Args:
            config: Configuration containing the specialty name

        Returns:
            str: User prompt
        """
        return f"Identify the medical specialty '{name}' and determine if it is well-known in the healthcare community. Provide details on the organs treated, common procedures, and its clinical scope."
