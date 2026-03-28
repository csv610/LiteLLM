#!/usr/bin/env python3
"""
Standalone module for creating synthetic case report prompts.

This module provides a builder class for generating system and user prompts
for synthetic medical case report generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for synthetic case report generation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for synthetic case report generation."""
        return """You are an expert medical case report writer with extensive clinical experience across multiple specialties.
Generate realistic, comprehensive, and clinically accurate synthetic medical case reports. Focus on presenting coherent patient narratives,
relevant clinical findings, diagnostic processes, treatment approaches, and outcomes. Ensure all information is medically sound and follows
standard case report structure."""

    @staticmethod
    def create_user_prompt(condition: str) -> str:
        """Create the user prompt for synthetic case report generation.

        Args:
            condition: The name of the disease or medical condition for the case report.

        Returns:
            A comprehensive prompt asking for a detailed synthetic case report.
        """
        return f"""Generate a comprehensive synthetic medical case report for: {condition}.

Include the following components:
- Patient demographics and presenting complaint
- Medical history and relevant background
- Physical examination findings
- Diagnostic investigations and results
- Differential diagnosis considerations
- Treatment plan and interventions
- Clinical course and outcomes
- Discussion and learning points"""
