"""
Standalone module for creating pathogen identification prompts.

This module provides a builder class for generating system and user prompts
for identifying pathogens.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class PathogenIdentifierInput:
    """Configuration and input for pathogen identification."""
    pathogen_name: str

    def __post_init__(self):
        """Validate input parameters."""
        if not self.pathogen_name or not self.pathogen_name.strip():
            raise ValueError("Pathogen name cannot be empty")


class PromptBuilder:
    """Builder class for creating prompts for pathogen identification."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for pathogen identification.

        Returns:
            str: System prompt defining the LLM's role and instructions
        """
        return """You are a senior clinical microbiologist and infectious disease specialist. Your task is to identify and describe "pathogens" (microorganisms that cause disease).

A pathogen (e.g., Staphylococcus aureus, Influenza A, Candida albicans, Plasmodium falciparum) is considered "well-known" if it:
1. Is a common cause of clinical infections.
2. Is standardly identified in microbiology laboratories.
3. Has established diagnostic and treatment protocols.
4. Is documented in major infectious disease databases (e.g., CDC, WHO).

When identifying a pathogen, you must:
1. Determine if it is a standard, well-known pathogen.
2. Identify its type (e.g., bacteria, virus, fungus, parasite, prion).
3. List common infections or diseases it causes.
4. Briefly explain its clinical significance and general treatment approach.

If a pathogen is extremely rare, emerging, or not well-known, clearly state that and explain why.

Always provide accurate, evidence-based information."""

    @staticmethod
    def create_user_prompt(config: PathogenIdentifierInput) -> str:
        """
        Create the user prompt for pathogen identification.

        Args:
            config: Configuration containing the pathogen name

        Returns:
            str: User prompt
        """
        return f"Identify the pathogen '{config.pathogen_name}' and determine if it is well-known. Provide details on its type, associated infections, and clinical significance."
