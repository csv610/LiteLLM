#!/usr/bin/env python3
"""
Standalone module for creating medical procedure info prompts.

This module provides a builder class for generating system and user prompts
for medical procedure information generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical procedure documentation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for medical procedure documentation."""
        return "You are an expert medical documentation specialist. Generate comprehensive, evidence-based procedure information."

    @staticmethod
    def create_user_prompt(procedure: str) -> str:
        """Create the user prompt for procedure information."""
        return f"Generate complete, evidence-based information for the medical procedure: {procedure}"
