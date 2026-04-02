#!/usr/bin/env python3
"""
Standalone module for creating patient medical history prompts.

This module provides a builder class for generating system and user prompts
for patient medical history question generation using AI models.
"""

from dataclasses import dataclass


@dataclass
class MedicalHistoryInput:
    exam: str
    age: int
    gender: str
    purpose: str = "physical_exam"


class PromptBuilder:
    """Builder class for creating prompts for patient medical history questions."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for medical history question generation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return "You are an expert medical documentation specialist. Generate trauma-informed, clinically relevant medical history questions."

    @staticmethod
    def create_user_prompt(medical_history_input: MedicalHistoryInput) -> str:
        """Create the user prompt for medical history question generation."""
        return f"""Generate comprehensive medical history questions for a {medical_history_input.age}-year-old {medical_history_input.gender} patient undergoing a {medical_history_input.exam} exam for the purpose of {medical_history_input.purpose}."""

    @staticmethod
    def get_history_auditor_prompts(user_input: MedicalHistoryInput, history_content: str) -> tuple[str, str]:
        """Create prompts for the History Compliance Auditor (JSON output)."""
        system = (
            "You are a Senior Medical Documentation Auditor. Your role is to audit "
            "medical history questions for clinical relevance, trauma-informed "
            "language, and completeness. Output a structured JSON report identifying "
            "any biased language, missing sections, or clinical inaccuracies."
        )
        user = (
            f"Audit the following medical history questions for a {user_input.age}yo "
            f"{user_input.gender} for a {user_input.exam} and output a structured "
            f"JSON report:\n\n{history_content}"
        )
        return system, user

    @staticmethod
    def get_output_synthesis_prompts(user_input: MedicalHistoryInput, specialist_data: str, compliance_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Medical Documentation Editor. Your role is to take raw "
            "medical history questions and a structured quality audit, then synthesize "
            "them into a FINAL, professional, and trauma-informed Markdown questionnaire. "
            "You MUST apply all fixes identified in the audit and ensure the tone is "
            "perfectly respectful and patient-centric."
        )
        user = (
            f"Synthesize the final medical history questionnaire for: {user_input.exam}\n\n"
            f"QUESTION DATA:\n{specialist_data}\n\n"
            f"QUALITY AUDIT:\n{compliance_data}\n\n"
            "Produce the final Markdown questionnaire. Ensure it is professional, "
            "easy for patients to complete, and clinically comprehensive."
        )
        return system, user
