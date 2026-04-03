#!/usr/bin/env python3
"""
Standalone module for creating medical specialist referral prompts.

This module provides a builder class for generating system and user prompts
for medical specialist recommendation using AI models.
"""

from typing import List, Optional
from lite import ModelOutput
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
        description="Medical disclaimer",
    )


class PromptBuilder:
    """Builder class for creating prompts for medical specialist recommendation."""

    @staticmethod
    def get_symptom_analysis_prompts(question: str) -> tuple[str, str]:
        """Create prompts for the Symptom Analyst agent."""
        system_prompt = """You are a medical symptom analyst. Your task is to extract symptoms, assess severity, and identify affected body parts from the patient's description.
Be precise and professional. Categorize severity based on typical clinical urgency."""
        user_prompt = f'Analyze the following patient question: "{question}"'
        return system_prompt, user_prompt

    @staticmethod
    def get_specialist_matching_prompts(analysis: SymptomAnalysis) -> tuple[str, str]:
        """Create prompts for the Specialist Matcher agent (JSON Auditor)."""
        system_prompt = """You are a medical specialist matcher and compliance auditor. 
Based on a structured symptom analysis, recommend the most appropriate specialists and 
verify if the severity assessment is clinically sound. Output a structured JSON report."""
        user_prompt = f"Audit and match specialists for the following analysis: {analysis.model_dump_json()}"
        return system_prompt, user_prompt

    @staticmethod
    def get_output_synthesis_prompts(
        question: str, specialist_data: str, compliance_data: str
    ) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Medical Referral Editor and Triage Director. Your role is to "
            "take raw medical analysis from specialists and the specialist matcher's audit, "
            "then synthesize them into a FINAL, human-ready Markdown report. "
            "You MUST apply all fixes identified in the audit and ensure all mandatory "
            "medical disclaimers are prominently included."
        )
        user = (
            f'Synthesize the final medical referral report for: "{question}"\n\n'
            f"SYMPTOM ANALYSIS:\n{specialist_data}\n\n"
            f"SPECIALIST MATCHING AUDIT:\n{compliance_data}\n\n"
            "Produce the final Markdown report. Ensure it is accurate, professional, "
            "and 100% compliant with safety guidelines."
        )
        return system, user
