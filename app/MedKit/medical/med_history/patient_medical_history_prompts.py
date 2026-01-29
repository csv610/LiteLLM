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
        """Create the user prompt for medical history question generation.
        
        Args:
            medical_history_input: Input parameters for medical history generation
            
        Returns:
            str: Formatted user prompt
        """
        return f"""Generate comprehensive medical history questions for a {medical_history_input.age}-year-old {medical_history_input.gender} patient undergoing a {medical_history_input.exam} exam for the purpose of {medical_history_input.purpose}.

The questions should be:
1. Trauma-informed: Respectful, non-judgmental, and culturally sensitive.
2. Purpose-specific: 
   - 'surgery': Focus on anesthesia risk, bleeding, and recovery.
   - 'medication': Focus on allergies, interactions, and adherence.
   - 'physical_exam': Focus on current status and systematic review.
3. Clinically relevant: Explain why each question matters for the {medical_history_input.exam} exam.
4. Comprehensive: Include past history, family history, drug info, vaccinations, and lifestyle/social factors.

Provide follow-up questions for positive responses to key clinical indicators."""
