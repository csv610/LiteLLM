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

    @staticmethod
    def create_basics_agent_prompt(position: str) -> str:
        """Prompt for Basics and Indications Agent."""
        return f"""Focusing on the surgical position '{position}', provide:
1. Official name, alternative names, and general category.
2. Common surgical uses, specific procedures, anatomical access, and medical specialties.
Ensure clinical accuracy."""

    @staticmethod
    def create_setup_agent_prompt(position: str) -> str:
        """Prompt for Patient Setup and Post-Op Care Agent."""
        return f"""Focusing on the surgical position '{position}', provide:
1. Detailed equipment needed and step-by-step patient placement.
2. Specific positioning for head/neck, upper extremities, and lower extremities.
3. Padding requirements and post-operative care/repositioning monitoring."""

    @staticmethod
    def create_safety_physiology_agent_prompt(position: str) -> str:
        """Prompt for Safety and Physiology Agent."""
        return f"""Focusing on the surgical position '{position}', provide:
1. Critical pressure points and nerve injury risks.
2. Prevention strategies and safety check-points.
3. Detailed respiratory and cardiovascular physiological effects."""

    @staticmethod
    def create_contraindications_agent_prompt(position: str) -> str:
        """Prompt for Contraindications and Modifications Agent."""
        return f"""Focusing on the surgical position '{position}', provide:
1. Absolute and relative contraindications.
2. Specific modifications for obese, pediatric, and elderly populations."""
