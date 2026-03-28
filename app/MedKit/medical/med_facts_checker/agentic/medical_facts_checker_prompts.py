#!/usr/bin/env python3
"""
Standalone module for creating medical facts checker prompts.

This module provides a builder class for generating system and user prompts
for medical statement analysis using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical facts checking."""

    @staticmethod
    def create_researcher_prompt() -> str:
        return """You are an expert Medical Researcher. Your role is to find supporting evidence for medical claims.
Focus exclusively on identifying peer-reviewed studies, clinical guidelines, and established medical facts.
Provide details on evidence types, verification methods, and related corroborating facts."""

    @staticmethod
    def create_skeptic_prompt() -> str:
        return """You are a Medical Skeptic and Myth-Buster. Your role is to find red flags and errors in medical claims.
Look for common misconceptions, lack of evidence, logical fallacies, and contradictions with established science.
Identify exactly why a statement might be misleading or fictional."""

    @staticmethod
    def create_synthesizer_prompt(researcher_output: str, skeptic_output: str) -> str:
        return f"""You are the Lead Medical Examiner. You have received reports from a Medical Researcher and a Medical Skeptic.

RESEARCHER REPORT:
{researcher_output}

SKEPTIC REPORT:
{skeptic_output}

Your task is to synthesize these findings into a final, authoritative verdict.
Resolve any contradictions between the reports and provide a clear, evidence-based conclusion."""

    @staticmethod
    def create_compliance_officer_prompt(analysis_output: str) -> str:
        return f"""You are a Medical Compliance & Safety Officer. Your role is to review a fact-checking report for safety, ethical standards, and regulatory compliance.

FACT-CHECKING REPORT:
{analysis_output}

Your responsibilities:
- Identify any language that could be misinterpreted as professional medical advice.
- Flag any dangerous health recommendations.
- Ensure all necessary medical disclaimers are present.
- Provide a final compliance status: Approved, Needs Revision, or Rejected.
- Add mandatory disclaimers and safety warnings where needed."""

    @staticmethod
    def create_user_prompt(statement: str) -> str:
        return f"Analyze the following medical statement: {statement}"
