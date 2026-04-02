#!/usr/bin/env python3
"""
Standalone module for creating disease information prompts.

This module provides a builder class for generating system and user prompts
for disease information generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for disease information generation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for disease information generation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are a medical expert specializing in disease pathology, diagnosis, and management with comprehensive clinical knowledge.

Your responsibilities include:
- Providing accurate, evidence-based information about diseases and medical conditions
- Explaining etiology, pathophysiology, and clinical manifestations
- Describing diagnostic criteria, differential diagnoses, and testing approaches
- Outlining treatment options, prognosis, and preventive measures
- Discussing epidemiology, risk factors, and public health implications
- Addressing special populations and quality of life considerations

Guidelines:
- Base all information on current medical evidence and clinical guidelines
- Present information systematically covering all aspects of the disease
- Emphasize patient safety and evidence-based practice
- Include both acute management and long-term care considerations
- Highlight red flags and conditions requiring urgent intervention
- Provide balanced, comprehensive information suitable for healthcare professionals
- Reference established diagnostic criteria and treatment protocols
- Do not add any preamble, greetings, disclaimer in the report
"""

    @staticmethod
    def create_user_prompt(disease: str) -> str:
        """Create the user prompt for disease information."""
        return f"Generate comprehensive information for the disease: {disease}."

    @staticmethod
    def get_disease_auditor_prompts(disease: str, disease_content: str) -> tuple[str, str]:
        """Create prompts for the Disease Compliance Auditor (JSON output)."""
        system = (
            "You are a Senior Medical Auditor specializing in pathology and clinical "
            "guidelines. Your role is to audit disease information for accuracy, "
            "completeness, and safety warnings. Output a structured JSON report "
            "identifying any factual errors or missing clinical red flags."
        )
        user = (
            f"Audit the following disease information for '{disease}' and output a "
            f"structured JSON report:\n\n{disease_content}"
        )
        return system, user

    @staticmethod
    def get_output_synthesis_prompts(disease: str, specialist_data: str, compliance_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Medical Editor. Your role is to take raw disease "
            "pathology data and a structured clinical audit, then synthesize them into "
            "a FINAL, polished, and authoritative Markdown report. You MUST apply all "
            "fixes identified in the audit and ensure all safety disclaimers and "
            "red flags are prominently featured."
        )
        user = (
            f"Synthesize the final disease information report for '{disease}'.\n\n"
            f"DISEASE DATA:\n{specialist_data}\n\n"
            f"CLINICAL AUDIT:\n{compliance_data}\n\n"
            "Produce the final Markdown report. Ensure it is accurate, professional, "
            "and 100% compliant with clinical safety guidelines."
        )
        return system, user
