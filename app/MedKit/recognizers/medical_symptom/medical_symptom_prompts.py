"""
Standalone module for creating medical symptom identification prompts.

This module provides a builder class for generating system and user prompts
for identifying if a medical symptom is well-known in the healthcare community.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MedicalSymptomIdentifierInput:
    """Configuration and input for medical symptom identification."""
    symptom_name: str

    def __post_init__(self):
        """Validate input parameters."""
        if not self.symptom_name or not self.symptom_name.strip():
            raise ValueError("Symptom name cannot be empty")


class PromptBuilder:
    """Builder class for creating prompts for medical symptom identification."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for medical symptom identification.

        Returns:
            str: System prompt defining the LLM's role and instructions
        """
        return """You are a senior triage nurse and clinical diagnostician with extensive experience in symptom assessment and emergency medicine. Your task is to identify if a given "medical symptom" name is "well-known" in the healthcare field.

A medical symptom (e.g., dyspnea, jaundice, vertigo, hemoptysis) is considered "well-known" if it:
1. Is a standard clinical sign or subjective experience reported by patients.
2. Is documented in medical textbooks and triage protocols.
3. Has a clear association with specific physiological or pathological processes.
4. Is used by clinicians to differentiate between various medical conditions.

When identifying a symptom, you must:
1. Determine its recognition status.
2. List common conditions associated with it.
3. Identify "red flag" severity indicators.
4. Provide a brief clinical description.

If a symptom is extremely vague, highly specialized, or not well-known, clearly state that and explain why.

Always provide accurate, evidence-based information."""

    @staticmethod
    def create_user_prompt(symptom_name) -> str:
        """
        Create the user prompt for medical symptom identification.

        Args:
            config: Configuration containing the symptom name

        Returns:
            str: User prompt
        """
        return f"Identify the medical symptom '{symptom_name}' and determine if it is well-known in the healthcare community. Provide details on its associated conditions, severity indicators, and clinical manifestation."
