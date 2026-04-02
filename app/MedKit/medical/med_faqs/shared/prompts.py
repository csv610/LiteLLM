#!/usr/bin/env python3
"""
Standalone module for creating medical FAQ prompts.

This module provides a builder class for generating system and user prompts
for medical FAQ generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical FAQ generation."""

    @staticmethod
    def create_patient_agent_prompts(topic: str) -> tuple[str, str]:
        """Create prompts for the Patient FAQ agent."""
        system = (
            "You are a patient-friendly medical communicator. Your goal is to provide "
            "a brief, welcoming introduction and clear, accessible FAQs for patients. "
            "Use simple language and avoid complex jargon."
        )
        user = f"Generate a patient-friendly introduction and FAQs for: {topic}"
        return system, user

    @staticmethod
    def create_clinical_agent_prompts(topic: str) -> tuple[str, str]:
        """Create prompts for the Clinical agent."""
        system = (
            "You are a clinical medical specialist. Your goal is to provide evidence-based "
            "clinical information for healthcare providers, including clinical overviews, "
            "best practices, quality metrics, and referral criteria."
        )
        user = f"Generate provider-focused clinical content for: {topic}"
        return system, user

    @staticmethod
    def create_safety_agent_prompts(topic: str) -> tuple[str, str]:
        """Create prompts for the Safety & Misconception agent."""
        system = (
            "You are a medical safety and triage specialist. Your goal is to identify "
            "red flags for when a patient should seek urgent care and to debunk common "
            "medical myths or misconceptions related to the topic."
        )
        user = f"Generate safety guidance and debunk misconceptions for: {topic}"
        return system, user

    @staticmethod
    def create_research_agent_prompts(topic: str) -> tuple[str, str]:
        """Create prompts for the Research & Related Topics agent."""
        system = (
            "You are a medical research and diagnostic specialist. Your goal is to "
            "identify related medical topics, diagnostic tests, or medical devices "
            "that provide further context or learning for the patient."
        )
        user = f"Identify related topics, tests, and devices for: {topic}"
        return system, user

    @staticmethod
    def create_compliance_agent_prompts(topic: str, content: str) -> tuple[str, str]:
        """Create prompts for the Compliance Review agent (JSON output)."""
        system = (
            "You are a medical legal and compliance specialist. Your role is to review "
            "the generated FAQ content for regulatory alignment, medical accuracy, and "
            "the presence of mandatory legal disclaimers. Output a structured report "
            "identifying compliance status, specific issues, and required disclaimers."
        )
        user = (
            f"Audit the following medical FAQ for the topic '{topic}' and output a "
            f"structured report:\n\n{content}"
        )
        return system, user

    @staticmethod
    def create_output_agent_prompts(topic: str, specialist_data: str, compliance_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Medical Editor. Your role is to take raw specialist data "
            "and a structured compliance audit, then synthesize them into a FINAL, "
            "polished, and safe Markdown report for the end-user. You MUST apply all "
            "fixes identified in the compliance audit and ensure all mandatory "
            "disclaimers are inserted."
        )
        user = (
            f"Synthesize the final medical FAQ report for '{topic}'.\n\n"
            f"SPECIALIST DATA:\n{specialist_data}\n\n"
            f"COMPLIANCE AUDIT:\n{compliance_data}\n\n"
            "Produce the final Markdown report. Ensure it is human-readable, professional, "
            "and 100% compliant with safety guidelines."
        )
        return system, user

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for FAQ generation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return (
            "You are a medical information specialist creating patient-friendly FAQs. "
            "Your responses should be accurate, clear, and accessible to non-medical audiences. "
            "Organize information in logical sections with concise, informative answers. "
            "Always encourage users to consult healthcare professionals for medical advice."
            "Do not add any preamble, disclaimer or unnecessary information in the output."
        )

    @staticmethod
    def create_user_prompt(topic: str) -> str:
        """Create the user prompt for FAQ generation.

        Args:
            topic: The medical topic to generate FAQs for

        Returns:
            str: Formatted user prompt
        """
        return f"Generate comprehensive patient-friendly FAQs for: {topic}."
