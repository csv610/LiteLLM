"""
Standalone module for creating supplement identification prompts.

This module provides a builder class for generating system and user prompts
for identifying supplements and nutrients.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class SupplementIdentifierInput:
    """Configuration and input for supplement identification."""
    supplement_name: str

    def __post_init__(self):
        """Validate input parameters."""
        if not self.supplement_name or not self.supplement_name.strip():
            raise ValueError("Supplement name cannot be empty")


class PromptBuilder:
    """Builder class for creating prompts for supplement identification."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for supplement identification.

        Returns:
            str: System prompt defining the LLM's role and instructions
        """
        return """You are a senior clinical nutritionist and integrative medicine specialist. Your task is to identify and describe "dietary supplements", "vitamins", "minerals", and "herbal products".

A supplement (e.g., Vitamin C, Magnesium, Omega-3, Elderberry, Zinc) is considered "well-known" if it:
1. Is a common component of human nutrition or traditional herbal medicine.
2. Is widely available as an over-the-counter (OTC) product.
3. Has established dietary reference intakes (DRIs) or traditional use profiles.
4. Is frequently discussed in clinical nutrition and wellness literature.

When identifying a supplement, you must:
1. Determine if it is a standard, well-known supplement or nutrient.
2. Identify its primary nutrients or active ingredients.
3. List common uses or health claims.
4. Briefly describe its regulatory standing (e.g., DSHEA in the US).

If a supplement is experimental, highly niche, or not well-known, clearly state that and explain why.

Always provide accurate, evidence-based information."""

    @staticmethod
    def create_user_prompt(config: SupplementIdentifierInput) -> str:
        """
        Create the user prompt for supplement identification.

        Args:
            config: Configuration containing the supplement name

        Returns:
            str: User prompt
        """
        return f"Identify the dietary supplement or nutrient '{config.supplement_name}' and determine if it is well-known. Provide details on active ingredients, common uses, and regulatory standing."
