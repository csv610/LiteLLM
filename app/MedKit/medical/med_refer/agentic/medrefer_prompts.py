#!/usr/bin/env python3
"""
Standalone module for creating medical specialist referral prompts.

This module provides a builder class for generating system and user prompts
for medical specialist recommendation using AI models.
"""


from typing import List, Optional
from pydantic import BaseModel, Field


class SymptomAnalysis(BaseModel):
    """Structured analysis of patient symptoms."""
    symptoms: List[str] = Field(description="List of identified symptoms")
    severity: str = Field(description="Overall severity: Low, Medium, High, or Urgent")
    affected_body_parts: List[str] = Field(description="Body parts or systems affected")


class SpecialistList(BaseModel):
    """List of recommended medical specialists."""
    specialists: List[str] = Field(description="List of recommended specialists")
    reasoning: str = Field(description="Brief explanation for the recommendations")


class Recommendation(BaseModel):
    """Final medical referral recommendation."""
    analysis: SymptomAnalysis
    referrals: SpecialistList
    disclaimer: str = Field(
        default="This is an AI-generated recommendation and should not replace professional medical advice. Please consult a healthcare professional immediately for urgent symptoms.",
        description="Medical disclaimer"
    )


class PromptBuilder:
    """Builder class for creating prompts for medical specialist recommendation."""

    @staticmethod
    def get_symptom_analysis_prompts(question: str) -> tuple[str, str]:
        """Create prompts for the Symptom Analyst agent."""
        system_prompt = """You are a medical symptom analyst. Your task is to extract symptoms, assess severity, and identify affected body parts from the patient's description.
Be precise and professional. Categorize severity based on typical clinical urgency."""
        user_prompt = f"Analyze the following patient question: \"{question}\""
        return system_prompt, user_prompt

    @staticmethod
    def get_specialist_matching_prompts(analysis: SymptomAnalysis) -> tuple[str, str]:
        """Create prompts for the Specialist Matcher agent."""
        system_prompt = """You are a medical specialist matcher. Based on a structured symptom analysis, recommend the most appropriate specialists.
Provide a clear reasoning for each recommendation."""
        user_prompt = f"Recommend specialists for the following analysis: {analysis.model_dump_json()}"
        return system_prompt, user_prompt

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for specialist recommendation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are a medical assistant. Based on the given medical question, recommend the most suitable specialist doctors.
Some symptoms may require consultation with multiple specialists.

Example format:
- Question: "I have chest pain and shortness of breath."
  Specialists: Cardiologist, Pulmonologist

- Question: "I have severe joint pain and swelling."
  Specialists: Rheumatologist, Orthopedic Surgeon

- Question: "I have blurry vision and headaches."
  Specialists: Ophthalmologist, Neurologist"""

    @staticmethod
    def create_user_prompt(question: str) -> str:
        """Create the user prompt for specialist recommendation.

        Args:
            question: The patient's medical question or symptoms

        Returns:
            str: Formatted user prompt
        """
        return f"""Now, analyze the following question and recommend the best specialists:

Question: "{question}"
Specialists:"""
