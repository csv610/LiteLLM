#!/usr/bin/env python3
"""
Standalone module for creating surgical tool information prompts.

This module provides a builder class for generating system and user prompts
for surgical tool information generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for surgical tool information."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for surgical tool information generation."""
        return """You are an expert surgical instrument specialist with extensive knowledge of medical surgical tools and instruments.
Provide comprehensive, accurate, and clinically relevant information about surgical tools. Focus on practical applications,
safety considerations, and clinical usage."""

    @staticmethod
    def create_user_prompt(tool: str) -> str:
        """Create the user prompt for surgical tool information generation.

        Args:
            tool: The name of the surgical tool to generate information for.

        Returns:
            A comprehensive prompt asking for detailed surgical tool information.
        """
        return f"""Generate comprehensive information for the surgical tool: {tool}.
Include the following details:
- Description and purpose
- Key features and specifications
- Clinical applications
- Proper handling and sterilization
- Safety considerations
- Common variants or related instruments"""
