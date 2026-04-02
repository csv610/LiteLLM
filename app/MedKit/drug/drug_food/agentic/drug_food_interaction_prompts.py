#!/usr/bin/env python3
"""
Standalone module for creating drug-food interaction prompts.

This module provides a builder class and input model for generating system and user prompts
for drug-food interaction analysis using AI models.
"""

from typing import Optional
from pydantic import BaseModel, Field, field_validator


class DrugFoodInput(BaseModel):
    """Configuration and input for drug-food interaction analysis."""

    medicine_name: str = Field(..., min_length=1, description="Name of the medicine")
    diet_type: Optional[str] = None
    medical_conditions: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=150, description="Patient age (0-150)")
    specific_food: Optional[str] = None
    prompt_style: str = "detailed"

    def validate(self) -> None:
        """Validate the input parameters.
        (Kept for backward compatibility, though pydantic handles most of it)
        """
        if not self.medicine_name or not self.medicine_name.strip():
            raise ValueError("Medicine name cannot be empty or just whitespace")

        if self.age is not None and (self.age < 0 or self.age > 150):
            raise ValueError("Age must be between 0 and 150 years")
    
    @field_validator("medicine_name")
    @classmethod
    def validate_medicine_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Medicine name cannot be empty or just whitespace")
        return v.strip()


class PromptBuilder:
    """Builder class for creating prompts for drug-food interaction analysis."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for drug-food interaction analysis.

        Returns:
            str: System prompt defining the AI's role and instructions
        """
        return """You are a clinical pharmacology expert specializing in drug-food interactions. Your role is to analyze how foods and beverages affect drug absorption, metabolism, efficacy, and safety.

When analyzing drug-food interactions, you must:

1. Identify significant food interactions that affect drug absorption, distribution, metabolism, or excretion
2. Assess the severity and clinical significance of each interaction
3. Provide specific guidance on which foods to avoid and which are safe to consume
4. Explain the mechanism of interaction in clear terms
5. Recommend optimal timing for medication administration relative to meals
6. Highlight any special dietary considerations or restrictions
7. Base analysis on established medical literature and clinical guidelines

Always prioritize patient safety while providing practical, evidence-based guidance for optimal medication use."""

    @staticmethod
    def create_pharmacology_system_prompt() -> str:
        """Create the system prompt for the Pharmacology Analyst agent."""
        return (
            "You are a clinical pharmacology expert specializing in drug-food interactions. "
            "Your task is to analyze the pharmacokinetic (ADME) and pharmacodynamic mechanisms "
            "of interaction between medications and various food/beverage categories.\n\n"
            "Focus exclusively on:\n"
            "1. Molecular and cellular mechanisms of how specific foods affect drug absorption, metabolism, or efficacy.\n"
            "2. Enzyme pathways (e.g., CYP450) and transport proteins (e.g., P-gp) affected by nutrients.\n"
            "3. Resulting clinical effects and physiological symptoms of these food interactions.\n\n"
            "Provide technical, precise, and mechanism-focused analysis."
        )

    @staticmethod
    def create_risk_assessment_system_prompt() -> str:
        """Create the system prompt for the Clinical Risk Assessor agent."""
        return (
            "You are a clinical risk assessment expert specializing in drug-food safety. "
            "Your task is to determine the severity and clinical significance of interactions "
            "between medications and various food/beverage categories.\n\n"
            "Focus exclusively on:\n"
            "1. Overall severity level (NONE, MINOR, MILD, MODERATE, SIGNIFICANT, CONTRAINDICATED).\n"
            "2. Severity for each food category.\n"
            "3. Confidence level based on available medical evidence.\n"
            "4. A concise technical summary for healthcare professionals.\n\n"
            "Consider patient-specific factors like diet type, age, and medical conditions."
        )

    @staticmethod
    def create_management_system_prompt() -> str:
        """Create the system prompt for the Medical Management Advisor agent."""
        return (
            "You are a medical management expert. Your task is to provide practical "
            "recommendations for managing interactions between medications and food/beverages.\n\n"
            "Focus exclusively on:\n"
            "1. Specific management recommendations (timing of doses relative to meals, food avoidance, monitoring).\n"
            "2. Clear lists of foods to avoid and foods safe to consume.\n"
            "3. Specific timing recommendations for different food categories.\n\n"
            "Provide actionable, evidence-based clinical guidance."
        )

    @staticmethod
    def create_patient_education_system_prompt() -> str:
        """Create the system prompt for the Patient Education Specialist agent."""
        return (
            "You are a patient education specialist. Your task is to translate complex "
            "drug-food interaction data into clear, empathetic, and actionable information "
            "for a patient.\n\n"
            "Focus exclusively on:\n"
            "1. A simple, non-technical explanation of how food affects the medicine.\n"
            "2. Specific actions the patient should take regarding meal timing and diet.\n"
            "3. Patient-friendly lists of foods to avoid.\n"
            "4. Warning signs to watch for and meal timing guidance.\n\n"
            "Use clear, accessible language while maintaining clinical accuracy."
        )

    @staticmethod
    def create_search_agent_system_prompt() -> str:
        """Create the system prompt for the Evidence/Search agent."""
        return (
            "You are a medical information research specialist. Your task is to find "
            "established clinical evidence, regulatory data (FDA), and pharmacokinetic "
            "analyses regarding drug-food interactions.\n\n"
            "Focus on providing high-quality citations and identifying the primary "
            "data source type (e.g., Clinical Studies, FDA Warnings, Manufacturer Data)."
        )

    @staticmethod
    def create_compliance_system_prompt() -> str:
        """Create the system prompt for the Medical Compliance & Safety agent."""
        return (
            "You are a medical compliance and drug safety officer. Your task is to "
            "review a draft drug-food interaction analysis for adherence to medical standards, "
            "clinical guidelines, and safety protocols.\n\n"
            "Your responsibilities include:\n"
            "1. Ensuring all high-risk food interactions have clear, prioritized safety warnings.\n"
            "2. Verifying that meal timing recommendations align with standard clinical practice.\n"
            "3. Checking that the language used is professional, objective, and non-speculative.\n"
            "4. Validating that patient-facing information is safe and actionable.\n\n"
            "You must review the draft report provided and flag any inconsistencies or safety gaps."
        )

    @staticmethod
    def create_triage_system_prompt() -> str:
        """Create the system prompt for the Triage agent."""
        return (
            "You are a clinical pharmacologist performing a rapid triage of potential "
            "drug-food interactions. Your goal is to determine if any clinically significant "
            "interactions are likely to exist between the medication and common food categories.\n\n"
            "If no significant food interactions exist, explain why. If interactions are likely, "
            "trigger the full multi-agent analysis flow."
        )

    @classmethod
    def create_user_prompt(cls, config: DrugFoodInput) -> str:
        """
        Create the user prompt for drug-food interaction analysis.

        Args:
            config: Configuration containing the medicine and patient information

        Returns:
            str: Formatted user prompt with context
        """
        context = cls._build_context(config)
        return (
            f"{config.medicine_name} food and beverage interactions analysis. {context}"
        )

    @classmethod
    def create_compliance_review_user_prompt(cls, config: DrugFoodInput, draft_report: str) -> str:
        """Create a user prompt for the compliance agent to review a draft report.

        Args:
            config: Configuration containing the medicine and patient information
            draft_report: The draft interaction report to review

        Returns:
            str: Formatted user prompt with draft report context
        """
        context = cls._build_context(config)
        return (
            f"Please review the following draft drug-food interaction analysis for {config.medicine_name}.\n\n"
            f"PATIENT CONTEXT: {context}\n\n"
            f"DRAFT REPORT:\n{draft_report}\n\n"
            "Verify compliance with medical standards and clinical safety guidelines."
        )

    @classmethod
    def create_output_synthesis_prompts(cls, config: DrugFoodInput, specialist_data: str, audit_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Clinical Pharmacology Editor. Your role is to take raw "
            "drug-food interaction data and a structured safety audit, then "
            "synthesize them into a FINAL, polished, and safe Markdown report. "
            "You MUST apply all fixes identified in the audit and ensure the "
            "recommendations are perfectly clear for both clinicians and patients."
        )
        context = cls._build_context(config)
        user = (
            f"Synthesize the final drug-food interaction report for '{config.medicine_name}'.\n\n"
            f"CONTEXT: {context}\n\n"
            f"SPECIALIST DATA:\n{specialist_data}\n\n"
            f"SAFETY AUDIT:\n{audit_data}\n\n"
            "Produce the final Markdown report. Ensure it is accurate, professional, "
            "and 100% compliant with safety guidelines."
        )
        return system, user

    @staticmethod
    def _build_context(config: DrugFoodInput) -> str:
        """Build the analysis context string from input parameters.

        Args:
            config: Configuration containing the medicine and patient information

        Returns:
            str: Formatted context string
        """
        context_parts = [f"Analyzing food interactions for {config.medicine_name}"]
        if config.specific_food:
            context_parts.append(f"Specific foods to check: {config.specific_food}")
        if config.diet_type:
            context_parts.append(f"Patient diet type: {config.diet_type}")
        if config.age is not None:
            context_parts.append(f"Patient age: {config.age} years")
        if config.medical_conditions:
            context_parts.append(f"Patient conditions: {config.medical_conditions}")
        return ". ".join(context_parts) + "."
