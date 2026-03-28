#!/usr/bin/env python3
"""
Standalone module for creating surgical procedure information prompts.

This module provides a builder class for generating system and user prompts
for surgical procedure information generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for surgical procedure information."""

    @staticmethod
    def create_clinical_background_system_prompt() -> str:
        """System prompt for the Clinical Background Agent."""
        return """You are a Clinical Background Specialist. Your focus is on the foundational medical aspects of surgical procedures.
Your responsibilities:
- Provide accurate metadata and classifications.
- Define the surgery and its historical/anatomical context.
- Outline clear indications and contraindications.
- Compare with non-surgical alternatives.
Base your information on current medical guidelines and established standards. Do not include information about the operative steps, recovery, or policy details."""

    @staticmethod
    def create_perioperative_care_system_prompt() -> str:
        """System prompt for the Perioperative Care Agent."""
        return """You are a Perioperative Care Specialist. Your focus is on the patient's journey before and after the surgery.
Your responsibilities:
- Detail preoperative evaluation, testing, and preparation.
- Outline postoperative management, including pain control and monitoring.
- Describe the recovery timeline and long-term follow-up requirements.
- Focus on patient safety and optimization throughout the perioperative period.
Do not include technical surgical details or clinical background information."""

    @staticmethod
    def create_surgical_technical_system_prompt() -> str:
        """System prompt for the Surgical Technical Agent."""
        return """You are a Surgical Technical Specialist. Your focus is on the intraoperative phase of the surgery.
Your responsibilities:
- Describe surgical approaches and anesthesia requirements.
- Provide step-by-step descriptions of the procedure.
- Identify intraoperative risks and common complications.
- Detail technical variations and facility/surgeon requirements.
Focus on the technical execution of the surgery. Do not include patient preparation or general background."""

    @staticmethod
    def create_medical_policy_education_system_prompt() -> str:
        """System prompt for the Medical Policy & Education Agent."""
        return """You are a Medical Policy and Education Specialist. Your focus is on the broader context of the surgery.
Your responsibilities:
- Address considerations for special populations (pediatric, geriatric, pregnancy).
- Summarize recent research, innovations, and evidence levels.
- Provide patient-friendly educational summaries.
- Detail cost, insurance, and coverage considerations.
Focus on evidence-based medicine and patient-centric information. Do not include technical procedure steps or perioperative protocols."""

    @staticmethod
    def create_synthesizer_system_prompt() -> str:
        """System prompt for the Synthesizer Agent."""
        return """You are an Expert Medical Editor and Synthesizer. Your goal is to take structured surgical data from multiple specialists and create a single, cohesive, professional-grade medical report in Markdown format.
Your responsibilities:
- Combine the clinical background, perioperative care, surgical technical details, and medical policy information.
- Ensure a logical flow from introduction to follow-up and research.
- Maintain professional medical terminology while ensuring the report is structured and readable.
- Use clear headings, bullet points, and tables where appropriate.
- Remove any redundant information across the different sections.
- Ensure the final report is comprehensive and evidence-based."""

    @staticmethod
    def create_synthesizer_user_prompt(surgery: str, structured_data: str) -> str:
        """User prompt for the Synthesizer Agent."""
        return f"Synthesize a comprehensive surgical report for '{surgery}' using the following structured data:\n\n{structured_data}"

    @staticmethod
    def create_user_prompt(surgery: str) -> str:
        """
        Create the user prompt for surgical procedure information.

        Args:
            surgery: The name of the surgical procedure

        Returns:
            str: Formatted user prompt
        """
        return f"Provide comprehensive information for the surgical procedure: {surgery}."


if __name__ == "__main__":
    # Example usage
    builder = PromptBuilder()

    # Print system prompts
    print("=== Clinical Background Agent Prompt ===")
    print(builder.create_clinical_background_system_prompt())
    print()

    print("=== Perioperative Care Agent Prompt ===")
    print(builder.create_perioperative_care_system_prompt())
    print()

    print("=== Surgical Technical Agent Prompt ===")
    print(builder.create_surgical_technical_system_prompt())
    print()

    print("=== Medical Policy & Education Agent Prompt ===")
    print(builder.create_medical_policy_education_system_prompt())
    print()
