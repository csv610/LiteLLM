#!/usr/bin/env python3
"""
Standalone module for creating medical speciality prompts.

This module provides a builder class for generating system and user prompts
for medical speciality generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical speciality generation."""

    @staticmethod
    def create_planner_system_prompt() -> str:
        """Generate the system prompt for the planner agent."""
        return "You are an expert medical taxonomist. Your task is to identify the major distinct categories of medical specialties."

    @staticmethod
    def create_planner_user_prompt() -> str:
        """Generate the user prompt for the planner agent."""
        return "List 5 to 8 major, distinct categories of medical specialties (e.g., Internal Medicine, Surgery, Pediatrics, Diagnostics, Psychiatry/Neurology)."

    @staticmethod
    def create_researcher_system_prompt() -> str:
        """Generate the system prompt for the researcher agent."""
        return "You are an expert in medical education and healthcare systems. Generate a complete and accurate database of medical specialties for a given category."

    @staticmethod
    def create_researcher_user_prompt(category: str) -> str:
        """Generate the user prompt for the researcher agent."""
        return f"""Generate a comprehensive list of medical specialists for the following category: {category}.

For each specialist, provide:
1. Formal specialty name
2. Category name and description (use the provided category or a closely related one)
3. Role description
4. Conditions/diseases treated
5. Common referral reasons
6. Subspecialties
7. Surgical vs non-surgical
8. Patient population focus

Ensure you include both common and highly specialized fields within this category."""

    @staticmethod
    def create_reviewer_system_prompt() -> str:
        """Generate the system prompt for the reviewer/aggregator agent."""
        return "You are a Chief Medical Officer. Review and aggregate the provided lists of medical specialists into a single, cohesive, and comprehensive overview."

    @staticmethod
    def create_reviewer_user_prompt(specialists_data: str) -> str:
        """Generate the user prompt for the reviewer/aggregator agent."""
        return f"Review the following data of medical specialists from different categories. Compile them into a comprehensive, well-structured final document, ensuring consistency and removing any duplicates:\n\n{specialists_data}"
