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

    @classmethod
    def create_user_prompt(cls, config: DrugDrugInput) -> str:
        """Create the user prompt for drug-drug interaction analysis.

        Args:
            config: Configuration containing the drugs and patient information

        Returns:
            str: Formatted user prompt with context
        """
        context = cls._build_context(config)
        return f"{config.medicine1} and {config.medicine2} interaction analysis. {context}"
        
    @staticmethod
    def _build_context(config: DrugDrugInput) -> str:
        """Build the analysis context string from input parameters.
        
        Args:
            config: Configuration containing the drugs and patient information
            
        Returns:
            str: Formatted context string
        """
        context_parts = [f"Checking interaction between {config.medicine1} and {config.medicine2}"]

        if config.age is not None:
            context_parts.append(f"Patient age: {config.age} years")
        if config.dosage1:
            context_parts.append(f"{config.medicine1} dosage: {config.dosage1}")
        if config.dosage2:
            context_parts.append(f"{config.medicine2} dosage: {config.dosage2}")
        if config.medical_conditions:
            context_parts.append(f"Patient conditions: {config.medical_conditions}")

        return ". ".join(context_parts) + "."
