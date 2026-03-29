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

    @staticmethod
    def create_patient_presentation_agent_prompt() -> str:
        """Create the system prompt for the Patient & Presentation Agent."""
        return """You are an expert Medical Historian and Triage Specialist.
Your goal is to generate a realistic patient profile and initial clinical presentation for a specific medical condition.
Focus on providing detailed demographics, comprehensive medical history (family, past medical, surgical, social, medications, allergies),
and a compelling chief complaint and history of present illness.
Ensure the clinical findings (vitals, physical exam) and the initial timeline are realistic and lead logically to the suspected condition."""

    @staticmethod
    def create_patient_presentation_user_prompt(condition: str) -> str:
        """Create the user prompt for the Patient & Presentation Agent."""
        return f"Generate the initial patient presentation, demographics, clinical findings, and timeline for a case of: {condition}."

    @staticmethod
    def create_diagnostic_therapeutic_agent_prompt() -> str:
        """Create the system prompt for the Diagnostic & Therapeutic Agent."""
        return """You are an expert Diagnostic Specialist and Attending Physician.
Your goal is to determine the complete diagnostic workup and therapeutic management plan based on a patient's initial presentation.
Focus on realistic laboratory tests, imaging findings, and specialized testing.
Develop a comprehensive treatment plan including medications, procedural interventions, supportive care, and lifestyle modifications.
Describe the clinical course, patient's response to treatment, and long-term follow-up outcomes.
Ensure all decisions are evidence-based and align with the provided patient history."""

    @staticmethod
    def create_diagnostic_therapeutic_user_prompt(condition: str, presentation_context: str) -> str:
        """Create the user prompt for the Diagnostic & Therapeutic Agent."""
        return f"""The patient is presenting with a suspected case of: {condition}.
Based on the following patient presentation context, generate the diagnostic assessment, therapeutic interventions, and follow-up outcomes.

CONTEXT:
{presentation_context}"""

    @staticmethod
    def create_review_synthesis_agent_prompt() -> str:
        """Create the system prompt for the Review & Synthesis Agent."""
        return """You are a Senior Medical Editor and Reviewer.
Your goal is to synthesize the clinical details into a final, professional medical case report.
Focus on writing an insightful discussion that highlights the significance of the case, diagnostic reasoning, and learning points.
Include the patient's perspective on their experience and ensure all ethical considerations (informed consent, anonymity) are addressed.
Generate appropriate metadata including a title and keywords.
Ensure the final report is cohesive, medically accurate, and follows CARE guidelines."""

    @staticmethod
    def create_review_synthesis_user_prompt(condition: str, full_context: str) -> str:
        """Create the user prompt for the Review & Synthesis Agent."""
        return f"""Synthesize a final medical case report for: {condition}.
Based on the complete clinical context provided below, generate the discussion, patient perspective, informed consent, and metadata.

CLINICAL CONTEXT:
{full_context}"""
