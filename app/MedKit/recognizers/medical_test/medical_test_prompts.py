"""
Standalone module for creating medical test identification prompts.

This module provides a builder class for generating system and user prompts
for identifying if a medical test is well-known in the healthcare community.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MedicalTestIdentifierInput:
    """Configuration and input for medical test identification."""
    test_name: str

    def __post_init__(self):
        """Validate input parameters."""
        if not self.test_name or not self.test_name.strip():
            raise ValueError("Test name cannot be empty")


class PromptBuilder:
    """Builder class for creating prompts for medical test identification."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for medical test identification.

        Returns:
            str: System prompt defining the LLM's role and instructions
        """
        return """You are a senior laboratory director and diagnostic specialist with expertise in pathology, radiology, and clinical diagnostics. Your task is to identify if a given "medical test" name is "well-known" in the healthcare field.

A medical test (e.g., lab assay, imaging study, physical examination) is considered "well-known" if it:
1. Is a standard diagnostic tool used in clinical practice.
2. Is widely available in most healthcare settings or specialized centers.
3. Has established reference ranges, sensitivity, and specificity.
4. Is part of standard clinical guidelines for diagnosing or monitoring conditions.

When identifying a test, you must:
1. Determine its recognition status.
2. Identify its type (e.g., biochemical, molecular, radiological).
3. Describe its primary purpose (what it measures or detects).
4. Provide a brief explanation of its clinical utility.

If a test is experimental, highly obscure, or not well-known, clearly state that and explain why.

Always provide accurate, evidence-based information."""

    @staticmethod
    def create_user_prompt(config: MedicalTestIdentifierInput) -> str:
        """
        Create the user prompt for medical test identification.

        Args:
            config: Configuration containing the test name

        Returns:
            str: User prompt
        """
        return f"Identify the medical test '{config.test_name}' and determine if it is well-known in the healthcare community. Provide details on its type, purpose, and clinical utility."
