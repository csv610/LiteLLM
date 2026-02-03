"""
Standalone module for creating drug identification prompts.

This module provides a builder class for generating system and user prompts
for identifying if a drug is well-known in the industry.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DrugIdentifierInput:
    """Configuration and input for drug identification."""
    drug_name: str

    def __post_init__(self):
        """Validate input parameters."""
        if not self.drug_name or not self.drug_name.strip():
            raise ValueError("Drug name cannot be empty")


class PromptBuilder:
    """Builder class for creating prompts for drug identification."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for drug identification.

        Returns:
            str: System prompt defining the LLM's role and instructions
        """
        return """You are a pharmaceutical industry expert with extensive knowledge of global drug markets, regulatory approvals, and clinical usage. Your task is to identify if a given drug name is "well-known" in the industry.

A drug is considered "well-known" if it:
1. Has widespread clinical use.
2. Is approved by major regulatory bodies (like FDA, EMA).
3. Is frequently mentioned in medical literature and clinical guidelines.
4. Is a common treatment for a particular condition.

When identifying a drug, you must:
1. Determine its industry recognition status.
2. List its primary medical uses.
3. Note its general regulatory standing.
4. Provide a brief explanation of its industry significance.

If a drug is obscure, experimental, or not well-known, clearly state that and explain why.

Always provide accurate, evidence-based information."""

    @staticmethod
    def create_user_prompt(config: DrugIdentifierInput) -> str:
        """
        Create the user prompt for drug identification.

        Args:
            config: Configuration containing the drug name

        Returns:
            str: User prompt
        """
        return f"Identify the drug '{config.drug_name}' and determine if it is a well-known drug in the pharmaceutical industry. Provide details on its common uses and industry significance."
