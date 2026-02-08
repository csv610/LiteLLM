#!/usr/bin/env python3
"""
Standalone module for creating drug addiction analysis prompts.

This module provides a builder class and input model for generating system and user prompts
for drug addiction analysis using AI models.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DrugAddictionInput:
    """Configuration and input for drug addiction analysis."""
    medicine_name: str
    usage_duration: Optional[str] = None
    prompt_style: str = "detailed"
    
    def validate(self) -> None:
        """Validate the input parameters.
        
        Raises:
            ValueError: If any parameter is invalid
        """
        if not self.medicine_name or not self.medicine_name.strip():
            raise ValueError("Medicine name cannot be empty or just whitespace")


class PromptBuilder:
    """Builder class for creating prompts for drug addiction analysis."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for drug addiction analysis.

        Returns:
            str: System prompt defining the AI's role and instructions
        """
        return """You are an expert in addiction medicine and clinical pharmacology. Your role is to analyze the addictive potential of drugs, their mechanisms of dependence, withdrawal profiles, and treatment strategies.

When analyzing drug addiction risks, you must:

1. Identify other names for the substance, including brand names, generic names, and common street names.
2. Evaluate the addictive potential based on pharmacological properties and clinical evidence.
3. Identify the DEA Controlled Substance Schedule (Schedule I to V) if applicable.
4. Explain the neurological and psychological mechanisms that lead to dependence.
5. Detail the withdrawal symptoms, their severity, and management.
6. Identify long-term physical and mental health consequences of prolonged use.
7. List risk factors that may predispose an individual to addiction for this specific substance.
8. Provide evidence-based treatment and recovery recommendations.
9. Always include a patient-friendly summary that helps individuals understand the risks and where to seek help.

Base your analysis on current medical literature, DSM-5 criteria (if applicable), and clinical guidelines. Prioritize accuracy and harm reduction."""

    @classmethod
    def create_user_prompt(cls, config: DrugAddictionInput) -> str:
        """
        Create the user prompt for drug addiction analysis.

        Args:
            config: Configuration containing the medicine and patient information

        Returns:
            str: Formatted user prompt with context
        """
        context = cls._build_context(config)
        return f"Analyze the addiction potential and risks for {config.medicine_name}. {context}"
    
    @staticmethod
    def _build_context(config: DrugAddictionInput) -> str:
        """Build the analysis context string from input parameters.
        
        Args:
            config: Configuration containing the medicine and patient information
            
        Returns:
            str: Formatted context string
        """
        context_parts = [f"Substance: {config.medicine_name}"]
        if config.usage_duration:
            context_parts.append(f"Reported usage duration: {config.usage_duration}")
        return ". ".join(context_parts) + "."