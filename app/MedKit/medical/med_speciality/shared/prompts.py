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
        """Generate the system prompt for the JSON Compliance Auditor."""
        return "You are a Chief Medical Officer and Quality Auditor. Review and audit the provided medical specialty data for accuracy and completeness. Output a structured JSON report."

    @staticmethod
    def create_reviewer_user_prompt(specialists_data: str) -> str:
        """Generate the user prompt for the JSON Compliance Auditor."""
        return f"Audit the following medical specialty data and output a structured JSON report:\n\n{specialists_data}"

    @staticmethod
    def create_output_synthesis_prompts(database_data: str, audit_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Medical Taxonomist. Your role is to take raw specialty "
            "data and a structured quality audit, then synthesize them into a FINAL, "
            "polished, and comprehensive Markdown database of medical specialties. "
            "You MUST apply all fixes identified in the audit and ensure a "
            "logical, easy-to-navigate structure."
        )
        user = (
            f"Synthesize the final medical specialty database.\n\n"
            f"SPECIALTY DATA:\n{database_data}\n\n"
            f"QUALITY AUDIT:\n{audit_data}\n\n"
            "Produce the final Markdown database report. Ensure it is professional, "
            "accurate, and ready for healthcare system use."
        )
        return system, user
