#!/usr/bin/env python3
"""
Standalone module for creating medical specialist referral prompts.

This module provides a builder class for generating system and user prompts
for medical specialist recommendation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical specialist recommendation."""

    @staticmethod
    def create_speciality_agent_prompts(speciality: str) -> tuple[str, str]:
        """Create the prompts for the Speciality Agent."""
        system = (
            "You are a medical knowledge assistant. Your task is to provide detailed information "
            "about the roles and responsibilities of a specific medical specialist."
        )
        user = f"Provide detailed information about the roles and responsibilities of: {speciality}"
        return system, user

    @staticmethod
    def create_compliance_agent_prompts(speciality: str, content: str) -> tuple[str, str]:
        """Create prompts for the Compliance Review agent (JSON output)."""
        system = (
            "You are a medical legal and compliance specialist. Your role is to review "
            "the generated specialist role information for regulatory alignment, "
            "medical accuracy, and the presence of mandatory legal disclaimers. "
            "Output a structured report identifying compliance status, specific issues, "
            "and required disclaimers."
        )
        user = (
            f"Audit the following specialist role information for '{speciality}' and "
            f"output a structured report:\n\n{content}"
        )
        return system, user

    @staticmethod
    def create_output_agent_prompts(speciality: str, specialist_data: str, compliance_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Medical Editor. Your role is to take raw specialist data "
            "and a structured compliance audit, then synthesize them into a FINAL, "
            "polished, and safe Markdown report for the end-user. You MUST apply all "
            "fixes identified in the compliance audit and ensure all mandatory "
            "disclaimers are inserted."
        )
        user = (
            f"Synthesize the final medical specialist roles report for '{speciality}'.\n\n"
            f"SPECIALIST DATA:\n{specialist_data}\n\n"
            f"COMPLIANCE AUDIT:\n{compliance_data}\n\n"
            "Produce the final Markdown report. Ensure it is human-readable, professional, "
            "and 100% compliant with safety guidelines."
        )
        return system, user

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for speciality role description.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are a medical knowledge assistant. Your task is to provide detailed information about the roles and responsibilities of a specific medical specialist.
For a given medical speciality, you should list:
1.  **Primary Focus:** What body systems or conditions they focus on.
2.  **Key Responsibilities:** What they generally do (diagnose, treat, manage).
3.  **Common Procedures:** Examples of procedures or tests they perform.

Example format:
- Speciality: "Cardiologist"
  Roles:
  - **Primary Focus:** Heart and cardiovascular system.
  - **Key Responsibilities:** Diagnosing and treating heart defects, coronary artery disease, heart failure, and valvular heart disease.
  - **Common Procedures:** EKG, Echocardiogram, Cardiac Catheterization."""

    @staticmethod
    def create_user_prompt(speciality: str) -> str:
        """Create the user prompt for speciality role description.

        Args:
            speciality: The medical speciality to describe

        Returns:
            str: Formatted user prompt
        """
        return f"""Please describe the key roles and responsibilities of a: "{speciality}"
"""
