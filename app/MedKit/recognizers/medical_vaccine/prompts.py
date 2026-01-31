"""
Standalone module for creating vaccine identification prompts.

This module provides a builder class for generating system and user prompts
for identifying vaccines.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class VaccineIdentifierInput:
    """Configuration and input for vaccine identification."""
    vaccine_name: str

    def __post_init__(self):
        """Validate input parameters."""
        if not self.vaccine_name or not self.vaccine_name.strip():
            raise ValueError("Vaccine name cannot be empty")


class PromptBuilder:
    """Builder class for creating prompts for vaccine identification."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for vaccine identification.

        Returns:
            str: System prompt defining the LLM's role and instructions
        """
        return """You are a senior public health official and immunization specialist. Your task is to identify and describe "vaccines" and immunization agents.

A vaccine (e.g., MMR, Polio, BCG, Influenza, HPV) is considered "well-known" if it:
1. Is part of standard national or international immunization schedules (e.g., CDC, WHO).
2. Is approved by major regulatory bodies (e.g., FDA, EMA).
3. Has established protocols for administration and storage.
4. Is widely used in public health programs.

When identifying a vaccine, you must:
1. Determine if it is a standard, well-known vaccine.
2. Identify the target diseases it prevents.
3. Describe its type (e.g., mRNA, Live-attenuated, Inactivated, Viral Vector, Toxoid).
4. Provide a brief overview of the standard administration schedule.

If a vaccine is experimental, developmental, or not well-known, clearly state that and explain why.

Always provide accurate, evidence-based information."""

    @staticmethod
    def create_user_prompt(config: VaccineIdentifierInput) -> str:
        """
        Create the user prompt for vaccine identification.

        Args:
            config: Configuration containing the vaccine name

        Returns:
            str: User prompt
        """
        return f"Identify the vaccine '{config.vaccine_name}' and determine if it is well-known. Provide details on target diseases, vaccine type, and its standard schedule."
