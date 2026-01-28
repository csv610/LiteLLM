#!/usr/bin/env python3
"""
Standalone module for creating drug-food interaction prompts.

This module provides a builder class and input model for generating system and user prompts
for drug-food interaction analysis using AI models.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DrugFoodInput:
    """Configuration and input for drug-food interaction analysis."""
    medicine_name: str
    diet_type: Optional[str] = None
    medical_conditions: Optional[str] = None
    age: Optional[int] = None
    specific_food: Optional[str] = None
    prompt_style: str = "detailed"
    
    def validate(self) -> None:
        """Validate the input parameters.
        
        Raises:
            ValueError: If any parameter is invalid
        """
        if not self.medicine_name or not self.medicine_name.strip():
            raise ValueError("Medicine name cannot be empty or just whitespace")
        
        if self.age is not None and (self.age < 0 or self.age > 150):
            raise ValueError("Age must be between 0 and 150 years")


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
        return f"{config.medicine_name} food and beverage interactions analysis. {context}"
    
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
