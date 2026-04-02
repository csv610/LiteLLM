#!/usr/bin/env python3
"""
Standalone module for creating medical implant information prompts.

This module provides a builder class for generating system and user prompts
for medical implant information generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical implant information."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for medical implant information generation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are a medical device and implant specialist with expertise in biomedical engineering and clinical applications of medical implants.

Your responsibilities include:
- Providing comprehensive, evidence-based information about medical implants and devices
- Explaining device design, materials, and mechanisms of action
- Describing indications, contraindications, and patient selection criteria
- Detailing implantation procedures and technical considerations
- Outlining potential complications, device lifespan, and follow-up requirements
- Discussing regulatory status and clinical outcomes

Guidelines:
- Base all information on current medical device literature and regulatory standards
- Include both technical specifications and clinical perspectives
- Emphasize patient safety, biocompatibility, and long-term outcomes
- Address maintenance, monitoring, and replacement considerations
- Provide balanced information about risks and benefits
- Reference current evidence and clinical guidelines where applicable"""

    @staticmethod
    def create_user_prompt(implant: str) -> str:
        """Create the user prompt for medical implant information."""
        return f"Generate comprehensive information for the medical implant: {implant}."

    @staticmethod
    def get_implant_auditor_prompts(implant: str, implant_content: str) -> tuple[str, str]:
        """Create prompts for the Implant Compliance Auditor (JSON output)."""
        system = (
            "You are a Medical Device Compliance Auditor. Your role is to audit "
            "information about medical implants for technical accuracy, safety warnings, "
            "and regulatory compliance. Output a structured JSON report identifying "
            "any errors or missing critical safety information."
        )
        user = (
            f"Audit the following medical implant information for '{implant}' and "
            f"output a structured JSON report:\n\n{implant_content}"
        )
        return system, user

    @staticmethod
    def get_output_synthesis_prompts(implant: str, specialist_data: str, compliance_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Medical Device Editor. Your role is to take raw "
            "implant technical data and a structured compliance audit, then synthesize "
            "them into a FINAL, polished, and safe Markdown report. You MUST apply all "
            "fixes identified in the audit and ensure all safety disclaimers and "
            "MRI compatibility information are prominently featured."
        )
        user = (
            f"Synthesize the final medical implant report for '{implant}'.\n\n"
            f"IMPLANT DATA:\n{specialist_data}\n\n"
            f"COMPLIANCE AUDIT:\n{compliance_data}\n\n"
            "Produce the final Markdown report. Ensure it is accurate, professional, "
            "and 100% compliant with safety guidelines."
        )
        return system, user
