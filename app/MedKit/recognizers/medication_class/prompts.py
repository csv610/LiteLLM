"""
Standalone module for creating medication class identification prompts.

This module provides a builder class for generating system and user prompts
for identifying medication classes.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MedicationClassIdentifierInput:
    """Configuration and input for medication class identification."""
    class_name: str

    def __post_init__(self):
        """Validate input parameters."""
        if not self.class_name or not self.class_name.strip():
            raise ValueError("Class name cannot be empty")


class PromptBuilder:
    """Builder class for creating prompts for medication class identification."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for medication class identification.

        Returns:
            str: System prompt defining the LLM's role and instructions
        """
        return """You are a senior clinical pharmacologist and pharmacy professor. Your task is to identify and describe "medication classes" (groups of drugs with similar chemical structures or mechanisms of action).

A medication class (e.g., Beta-blockers, ACE Inhibitors, SSRIs, NSAIDs) is considered "well-known" if it:
1. Is a standard classification in pharmacology textbooks (e.g., Goodman & Gilman).
2. Is used by clinicians to describe groups of treatments.
3. Has a clearly defined mechanism of action common to its members.
4. Contains multiple widely used therapeutic agents.

When identifying a class, you must:
1. Determine if it is a standard, well-known medication class.
2. Describe its primary mechanism of action.
3. List common examples of drugs within the class.
4. Identify the primary therapeutic uses.

If a class is experimental, obsolete, or not well-known, clearly state that and explain why.

Always provide accurate, evidence-based information."""

    @staticmethod
    def create_user_prompt(config: MedicationClassIdentifierInput) -> str:
        """
        Create the user prompt for medication class identification.

        Args:
            config: Configuration containing the class name

        Returns:
            str: User prompt
        """
        return f"Identify the medication class '{config.class_name}' and determine if it is well-known. Provide details on its mechanism of action, common examples, and therapeutic uses."
