#!/usr/bin/env python3
"""
Standalone module for creating symptom-to-drug analysis prompts.

This module provides a builder class for generating system and user prompts
for symptom-to-drug analysis using AI models.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PromptStyle(str, Enum):
    DETAILED = "detailed"
    CONCISE = "concise"
    BALANCED = "balanced"


@dataclass
class SymptomInput:
    """Configuration and input for symptom-to-drug analysis."""
    symptom_name: str
    age: Optional[int] = None
    other_conditions: Optional[str] = None
    prompt_style: PromptStyle = PromptStyle.DETAILED

    def __post_init__(self):
        """Validate input parameters."""
        if not self.symptom_name or not self.symptom_name.strip():
            raise ValueError("Symptom name cannot be empty")
            
        if self.age is not None and (self.age < 0 or self.age > 150):
            raise ValueError("Age must be between 0 and 150 years")


class PromptBuilder:
    """Builder class for creating prompts for symptom-to-drug analysis."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for symptom-to-drug analysis.

        Returns:
            str: System prompt defining the LLM's role and instructions
        """
        return """You are a clinical pharmacologist and medical information specialist. Your role is to provide accurate, evidence-based information about medications (generic, OTC, Rx, etc.) typically used to treat or manage specific symptoms.

When listing drugs for a given symptom, you must:

1. **Direct Response**: Start your response immediately with the requested information. Do NOT include any introductory preamble, conversational filler, or boilerplate disclaimers.

2. **Be Thorough and Comprehensive**: Provide a wide-ranging, extensive list of medications. If many different drugs or drug classes are typically used for this symptom, ensure you include a diverse and complete selection of options across all relevant categories (at least 8-12 different medications if available).

3. **Categorize the Medication Type**: Distinguish between Generic, Over-the-Counter (OTC), Prescription (Rx), and Herbal/Supplement options.

4. **Provide Rationale**: Explain why a particular drug is used for that symptom—its pharmacological action and therapeutic role.

5. **Indicate Common Dosage**: Provide standard adult dosage ranges or frequency as a general reference.

6. **Highlight Precautions and Contraindications**: Identify important safety considerations, common side effects, and situations where the drug should be avoided.

7. **Include Non-Pharmacological Recommendations**: Suggest lifestyle changes or home remedies that can complement medication or provide relief.

8. **Specify Red Flags**: Clearly state when the symptom requires urgent professional medical evaluation (emergency signs).

9. **Provide Technical Summary**: Summarize the pharmacological approach to treating this symptom for a healthcare professional audience.

10. **Only List Medically Approved Medicines**: You MUST only list medicines that are medically approved (e.g., by the FDA, EMA, or other equivalent health authorities). Do NOT fabricate or hallucinate any medicine names. If a symptom does not have standard pharmacological treatments, state that clearly rather than providing unverified options.

Base your response on current clinical guidelines (e.g., FDA labels, WHO Essential Medicines, etc.). Prioritize patient safety and evidence-based medicine in all recommendations."""

    @staticmethod
    def create_user_prompt(config: SymptomInput) -> str:
        """
        Create the user prompt for symptom-to-drug analysis.

        Args:
            config: Configuration containing symptom and analysis parameters

        Returns:
            str: User prompt with context and formatted according to the specified style
        """
        # Build context parts
        context_parts = [f"Listing medications for the symptom: {config.symptom_name}"]
        
        if config.age is not None:
            context_parts.append(f"Patient age: {config.age} years")
        if config.other_conditions:
            context_parts.append(f"Other medical conditions to consider: {config.other_conditions}")

        context = ". ".join(context_parts) + "."
        base_query = f"Provide a comprehensive and extensive list of drugs (generic, OTC, Rx, etc.) that may be prescribed or recommended by a doctor for {config.symptom_name}."
        direct_instruction = " Start your response immediately with the analysis, without any preamble or disclaimers."

        if config.prompt_style == PromptStyle.CONCISE:
            return f"{base_query} {context} Provide a focused but thorough list of the most common medications and essential safety warnings.{direct_instruction}"

        elif config.prompt_style == PromptStyle.BALANCED:
            return f"{base_query} {context} Provide a balanced, comprehensive overview including various drug types, their rationale, and key precautions.{direct_instruction}"

        else:  # DETAILED
            return f"{base_query} {context} Provide a detailed and exhaustive list of medications (Generic, OTC, Rx, etc.), detailed rationale for each, common dosage ranges, safety precautions, lifestyle recommendations, and clinical red flags.{direct_instruction}"
