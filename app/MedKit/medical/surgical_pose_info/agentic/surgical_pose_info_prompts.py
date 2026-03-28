#!/usr/bin/env python3
"""
Standalone module for creating surgical position information prompts.

This module provides a builder class for generating system and user prompts
for surgical position information generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for surgical position information."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for surgical position information generation."""
        return """You are an expert in perioperative nursing and surgical patient positioning.
Provide comprehensive, accurate, and clinically relevant information about surgical patient positions.
Focus on patient safety, physiological effects, correct setup techniques, and injury prevention. Do not add any reamble, disclaimer or unnecessary information in the report."""

    @staticmethod
    def create_user_prompt(position: str) -> str:
        """Create the user prompt for surgical position information generation.

        Args:
            position: The name of the surgical position to generate information for.

        Returns:
            A comprehensive prompt asking for detailed surgical position information.
        """
        return f"""Generate comprehensive information for the surgical position: {position}.
Include the following details:
- Description and common uses
- Step-by-step patient setup and equipment
- Physiological effects (Respiratory, Cardiovascular)
- Safety considerations (Pressure points, Nerve risks)
- Contraindications and modifications for specific patient populations"""
