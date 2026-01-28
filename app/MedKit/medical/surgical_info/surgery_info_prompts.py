#!/usr/bin/env python3
"""
Standalone module for creating surgical procedure information prompts.

This module provides a builder class for generating system and user prompts
for surgical procedure information generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for surgical procedure information."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for surgical procedure information generation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are an expert surgical information specialist with comprehensive knowledge of surgical procedures and perioperative care.

Your responsibilities include:
- Providing accurate, evidence-based information about surgical procedures
- Explaining indications, contraindications, and procedural steps
- Describing risks, complications, and expected outcomes
- Outlining preoperative preparation and postoperative care requirements
- Emphasizing patient safety and current best practices

Guidelines:
- Base all information on current medical evidence and established surgical standards
- Present information clearly for both healthcare professionals and patients
- Include relevant anatomical considerations and technical details
- Highlight critical safety considerations and risk factors
- Maintain professional medical terminology while ensuring comprehension"""

    @staticmethod
    def create_user_prompt(surgery: str) -> str:
        """
        Create the user prompt for surgical procedure information.

        Args:
            surgery: The name of the surgical procedure

        Returns:
            str: Formatted user prompt
        """
        return (
            f"Generate comprehensive information for the surgical procedure: {surgery}."
        )


if __name__ == "__main__":
    # Example usage
    builder = PromptBuilder()

    # Print system prompt
    print("=== System Prompt ===")
    print(builder.create_system_prompt())
    print()

    # Example with different surgical procedures
    procedures = ["appendectomy", "cholecystectomy", "hernia repair"]

    for procedure in procedures:
        print(f"=== User Prompt for {procedure.title()} ===")
        print(builder.create_user_prompt(procedure))
        print()
