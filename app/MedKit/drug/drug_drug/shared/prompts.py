#!/usr/bin/env python3
"""
Standalone module for creating drug-drug interaction prompts.

This module provides a builder class and input model for generating system and user prompts
for drug-drug interaction analysis using AI models.
"""

from enum import Enum

from pydantic import BaseModel, Field, field_validator


class PromptStyle(str, Enum):
    DETAILED = "detailed"
    CONCISE = "concise"
    BALANCED = "balanced"


class DrugDrugInput(BaseModel):
    """Configuration and input for drug-drug interaction analysis."""

    medicine1: str = Field(..., min_length=1, description="Name of the first medicine")
    medicine2: str = Field(..., min_length=1, description="Name of the second medicine")
    age: int | None = Field(None, ge=0, le=150, description="Patient age (0-150)")
    dosage1: str | None = None
    dosage2: str | None = None
    medical_conditions: str | None = None
    prompt_style: PromptStyle = PromptStyle.DETAILED

    @field_validator("medicine1", "medicine2")
    @classmethod
    def validate_medicine_name(cls, v: str) -> str:
        """Validate that medicine names are not empty.

        Args:
            v: Medicine name to validate.

        Returns:
            str: Trimmed medicine name.

        Raises:
            ValueError: If medicine name is empty or just whitespace.
        """
        if not v.strip():
            msg = "Medicine name cannot be empty or just whitespace"
            raise ValueError(msg)
        return v.strip()


class DrugDrugPromptBuilder:
    """Builder class for creating prompts for drug-drug interaction analysis."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for drug-drug interaction analysis.

        Returns:
            str: System prompt defining the AI's role and instructions
        """
        return (
            "You are a clinical pharmacology expert specializing in drug-drug "
            "interactions. Analyze how medications interact with each other, "
            "affecting their efficacy, safety, and metabolism.\n\n"
            "When analyzing drug-drug interactions, you must:\n\n"
            "1. Identify pharmacokinetic interactions (absorption, distribution, "
            "metabolism, excretion)\n"
            "2. Identify pharmacodynamic interactions (additive, synergistic, "
            "antagonistic effects)\n"
            "3. Assess the severity and clinical significance of each interaction\n"
            "4. Explain the mechanism of interaction clearly\n"
            "5. Evaluate the risk level and potential adverse effects\n"
            "6. Provide specific management recommendations and monitoring "
            "parameters\n"
            "7. Consider patient-specific factors such as age, dosage, and "
            "medical conditions\n"
            "8. Base analysis on established medical literature, clinical "
            "guidelines, and databases\n\n"
            "Always prioritize patient safety while providing practical, "
            "evidence-based guidance for medication management."
        )

    @staticmethod
    def create_pharmacology_system_prompt() -> str:
        """Create the system prompt for the Pharmacology Analyst agent."""
        return (
            "You are a clinical pharmacology expert. Your task is to analyze the "
            "pharmacokinetic (ADME) and pharmacodynamic mechanisms of interaction "
            "between two medications.\n\n"
            "Focus exclusively on:\n"
            "1. Molecular and cellular mechanisms of interaction.\n"
            "2. Enzyme pathways (e.g., CYP450) and transport proteins involved.\n"
            "3. Resulting clinical effects and physiological symptoms.\n\n"
            "Provide technical, precise, and mechanism-focused analysis."
        )

    @staticmethod
    def create_risk_assessment_system_prompt() -> str:
        """Create the system prompt for the Clinical Risk Assessor agent."""
        return (
            "You are a clinical risk assessment expert. Your task is to determine "
            "the severity and clinical significance of a drug-drug interaction.\n\n"
            "Focus exclusively on:\n"
            "1. Severity level (NONE, MINOR, MILD, MODERATE, SIGNIFICANT, CONTRAINDICATED).\n"
            "2. Confidence level based on available medical evidence.\n"
            "3. A concise technical summary for healthcare professionals.\n\n"
            "Consider patient-specific factors like age and medical conditions."
        )

    @staticmethod
    def create_management_system_prompt() -> str:
        """Create the system prompt for the Medical Management Advisor agent."""
        return (
            "You are a medical management expert. Your task is to provide practical "
            "recommendations for managing a specific drug-drug interaction.\n\n"
            "Focus exclusively on:\n"
            "1. Specific management recommendations (dose adjustments, monitoring, timing).\n"
            "2. Safer alternative medicines if the combination is high-risk.\n\n"
            "Provide actionable, evidence-based clinical guidance."
        )

    @staticmethod
    def create_patient_education_system_prompt() -> str:
        """Create the system prompt for the Patient Education Specialist agent."""
        return (
            "You are a patient education specialist. Your task is to translate complex "
            "medical interaction data into clear, empathetic, and actionable information "
            "for a patient.\n\n"
            "Focus exclusively on:\n"
            "1. A simple, non-technical explanation of the interaction.\n"
            "2. Specific actions the patient should take.\n"
            "3. Warning signs to watch for and when to seek medical help.\n\n"
            "Use clear, accessible language while maintaining clinical accuracy."
        )

    @staticmethod
    def create_search_agent_system_prompt() -> str:
        """Create the system prompt for the Evidence/Search agent."""
        return (
            "You are a medical information research specialist. Your task is to find "
            "established clinical evidence, regulatory data (FDA/EMA), and peer-reviewed "
            "references regarding drug-drug interactions.\n\n"
            "Focus on providing high-quality citations and identifying the primary "
            "data source type (e.g., Clinical Studies, Regulatory Data)."
        )

    @staticmethod
    def create_compliance_system_prompt() -> str:
        """Create the system prompt for the Medical Compliance & Safety agent."""
        return (
            "You are a medical compliance and drug safety officer. Your task is to "
            "review a draft drug-drug interaction analysis for adherence to medical standards, "
            "clinical guidelines, and safety protocols.\n\n"
            "Your responsibilities include:\n"
            "1. Ensuring all high-risk interactions have clear, prioritized safety warnings.\n"
            "2. Verifying that management recommendations align with standard clinical practice.\n"
            "3. Checking that the language used is professional, objective, and non-speculative.\n"
            "4. Validating that patient-facing information is safe and does not encourage "
            "self-adjustment of medication without clinical supervision.\n\n"
            "You must review the draft report provided and flag any inconsistencies or safety gaps."
        )

    @staticmethod
    def create_triage_system_prompt() -> str:
        """Create the system prompt for the Triage agent."""
        return (
            "You are a clinical pharmacologist performing a rapid triage of a potential "
            "drug-drug interaction. Your goal is to determine if a clinically significant "
            "interaction is likely to exist between two medications.\n\n"
            "If no interaction exists, explain why. If an interaction is likely, "
            "trigger the full multi-agent analysis flow."
        )

    @classmethod
    def create_user_prompt(cls, config: DrugDrugInput) -> str:
        """Create the user prompt for drug-drug interaction analysis.

        Args:
            config: Configuration containing the drugs and patient information

        Returns:
            str: Formatted user prompt with context
        """
        context = cls._build_context(config)
        return (
            f"{config.medicine1} and {config.medicine2} interaction analysis. {context}"
        )

    @classmethod
    def create_compliance_review_user_prompt(cls, config: DrugDrugInput, draft_report: str) -> str:
        """Create a user prompt for the compliance agent to review a draft report.

        Args:
            config: Configuration containing the drugs and patient information
            draft_report: The draft interaction report to review

        Returns:
            str: Formatted user prompt with draft report context
        """
        context = cls._build_context(config)
        return (
            f"Please review the following draft interaction analysis for {config.medicine1} "
            f"and {config.medicine2}.\n\n"
            f"PATIENT CONTEXT: {context}\n\n"
            f"DRAFT REPORT:\n{draft_report}\n\n"
            "Verify compliance with medical standards and clinical safety guidelines."
        )

    @classmethod
    def create_output_synthesis_prompts(cls, config: DrugDrugInput, specialist_data: str, audit_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Clinical Pharmacology Editor. Your role is to take raw "
            "drug-drug interaction data and a structured safety audit, then "
            "synthesize them into a FINAL, polished, and safe Markdown report. "
            "You MUST apply all fixes identified in the audit and ensure the "
            "management strategy is perfectly clear for both clinicians and patients."
        )
        context = cls._build_context(config)
        user = (
            f"Synthesize the final drug-drug interaction report for '{config.medicine1}' and '{config.medicine2}'.\n\n"
            f"CONTEXT: {context}\n\n"
            f"SPECIALIST DATA:\n{specialist_data}\n\n"
            f"SAFETY AUDIT:\n{audit_data}\n\n"
            "Produce the final Markdown report. Ensure it is accurate, professional, "
            "and 100% compliant with safety standards."
        )
        return system, user

    @staticmethod
    def _build_context(config: DrugDrugInput) -> str:
        """Build the analysis context string from input parameters.

        Args:
            config: Configuration containing the drugs and patient information

        Returns:
            str: Formatted context string
        """
        context_parts = [
            f"Checking interaction between {config.medicine1} and {config.medicine2}"
        ]

        if config.age is not None:
            context_parts.append(f"Patient age: {config.age} years")
        if config.dosage1:
            context_parts.append(f"{config.medicine1} dosage: {config.dosage1}")
        if config.dosage2:
            context_parts.append(f"{config.medicine2} dosage: {config.dosage2}")
        if config.medical_conditions:
            context_parts.append(f"Patient conditions: {config.medical_conditions}")

        return ". ".join(context_parts) + "."
