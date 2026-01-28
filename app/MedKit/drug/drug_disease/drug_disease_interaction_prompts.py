#!/usr/bin/env python3
"""
Standalone module for creating drug-disease interaction prompts.

This module provides a builder class for generating system and user prompts
for drug-disease interaction analysis using AI models.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PromptStyle(str, Enum):
    DETAILED = "detailed"
    CONCISE = "concise"
    BALANCED = "balanced"


@dataclass
class DrugDiseaseInput:
    """Configuration and input for drug-disease interaction analysis."""
    medicine_name: str
    condition_name: str
    condition_severity: Optional[str] = None
    age: Optional[int] = None
    other_medications: Optional[str] = None
    prompt_style: PromptStyle = PromptStyle.DETAILED

    def __post_init__(self):
        """Validate input parameters."""
        if not self.medicine_name or not self.medicine_name.strip():
            raise ValueError("Medicine name cannot be empty")
        if not self.condition_name or not self.condition_name.strip():
            raise ValueError("Condition name cannot be empty")
        if self.age is not None and (self.age < 0 or self.age > 150):
            raise ValueError("Age must be between 0 and 150 years")


class PromptBuilder:
    """Builder class for creating prompts for drug-disease interaction analysis."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for drug-disease interaction analysis.

        Returns:
            str: System prompt defining the LLM's role and instructions
        """
        return """You are a clinical pharmacology expert specializing in drug-disease interactions. Your role is to analyze how medical conditions affect drug efficacy, safety, and metabolism.

When analyzing drug-disease interactions, you must:

1. **Assess Overall Interaction Severity**: Determine if the drug is contraindicated, requires caution, or is safe to use with the condition.

2. **Explain the Mechanism**: Describe the pharmacological and pathophysiological mechanisms underlying the interaction.

3. **Evaluate Efficacy Impact**: Analyze whether the disease affects the drug's therapeutic effectiveness, including:
   - Reduced efficacy due to disease state
   - Altered drug absorption, distribution, metabolism, or excretion
   - Disease-specific factors affecting treatment response

4. **Assess Safety Concerns**: Identify potential risks and adverse effects, including:
   - Increased risk of side effects or toxicity
   - Disease complications that may worsen with drug use
   - Monitoring requirements for safe use

5. **Provide Dosage Guidance**: Recommend dose adjustments if needed based on:
   - Organ function (hepatic, renal, cardiac)
   - Disease severity
   - Risk-benefit considerations

6. **Recommend Management Strategies**: Offer clinical recommendations for safe and effective use, including:
   - Monitoring parameters
   - Alternative therapies if contraindicated
   - Patient counseling points

7. **Create Patient-Friendly Guidance**: Translate technical information into clear, accessible language that patients can understand and act upon.

Base your analysis on established medical literature, clinical guidelines, and pharmacological principles. If data is limited or unavailable, clearly indicate this and explain the reasoning behind any recommendations.

Always prioritize patient safety while providing practical, evidence-based guidance for clinicians."""

    @staticmethod
    def create_user_prompt(config: DrugDiseaseInput) -> str:
        """
        Create the user prompt for drug-disease interaction analysis.

        Args:
            config: Configuration containing medicine, condition, and analysis parameters

        Returns:
            str: User prompt with context and formatted according to the specified style
        """
        # Build context parts
        context_parts = [f"Analyzing interaction between {config.medicine_name} and {config.condition_name}"]
        
        if config.condition_severity:
            context_parts.append(f"Condition severity: {config.condition_severity}")
        if config.age is not None:
            context_parts.append(f"Patient age: {config.age} years")
        if config.other_medications:
            context_parts.append(f"Other medications: {config.other_medications}")

        context = ". ".join(context_parts) + "."
        base_query = f"Analyze the interaction between {config.medicine_name} and {config.condition_name}."

        if config.prompt_style == PromptStyle.CONCISE:
            return f"{base_query} {context} Provide a focused analysis of key safety concerns and essential management recommendations."

        elif config.prompt_style == PromptStyle.BALANCED:
            return f"{base_query} {context} Provide a balanced analysis covering mechanism, clinical significance, and practical management guidance."

        else:  # DETAILED
            return f"{base_query} {context} Provide a comprehensive analysis including detailed mechanism of interaction, complete efficacy and safety assessment, specific dosage recommendations, clinical management strategies, and patient counseling guidance."
