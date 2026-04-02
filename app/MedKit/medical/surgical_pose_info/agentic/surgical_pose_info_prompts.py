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
        return f"Focusing on the surgical position '{position}', provide contraindications and population-specific modifications."

    @staticmethod
    def create_compliance_auditor_prompts(position: str, content: str) -> tuple[str, str]:
        """Create prompts for the JSON Compliance Auditor."""
        system = (
            "You are a Senior Surgical Safety Auditor. Your role is to audit surgical "
            "positioning documentation for safety, correctness, and patient risk. "
            "Output a structured JSON report identifying any dangerous positioning, "
            "missed pressure points, or incorrect physiological effects."
        )
        user = (
            f"Audit the following surgical positioning data for '{position}' and output "
            f"a structured JSON report:\n\n{content}"
        )
        return system, user

    @staticmethod
    def create_output_synthesis_prompts(position: str, specialist_data: str, audit_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Perioperative Editor. Your role is to take raw "
            "surgical positioning data and a structured safety audit, then synthesize "
            "them into a FINAL, polished, and safe Markdown report for OR staff. "
            "You MUST apply all safety fixes identified in the audit and ensure "
            "all critical padding and pressure points are clearly highlighted."
        )
        user = (
            f"Synthesize the final surgical positioning report for: '{position}'\n\n"
            f"POSITIONING DATA:\n{specialist_data}\n\n"
            f"SAFETY AUDIT:\n{audit_data}\n\n"
            "Produce the final Markdown report. Ensure it is accurate, professional, "
            "and 100% compliant with surgical safety guidelines."
        )
        return system, user
