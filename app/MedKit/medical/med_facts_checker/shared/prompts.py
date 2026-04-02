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
        """Create prompts for the JSON Compliance Auditor."""
        return f"""You are a Medical Compliance & Safety Auditor. 
Your role is to audit the fact-checking analysis for safety, ethical standards, 
and regulatory compliance. Output your findings as a structured JSON report.

ANALYSIS CONTENT:
{analysis_output}"""

    @staticmethod
    def create_output_synthesis_prompts(statement: str, specialist_data: str, audit_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Medical Fact-Checker. Your role is to take raw "
            "specialist research data and a structured safety audit, then "
            "synthesize them into a FINAL, authoritative, and safe Markdown report. "
            "You MUST apply all fixes identified in the audit and ensure the "
            "verdict is indisputable based on clinical evidence."
        )
        user = (
            f"Synthesize the final fact-checking report for: '{statement}'\n\n"
            f"RESEARCH DATA:\n{specialist_data}\n\n"
            f"SAFETY AUDIT:\n{audit_data}\n\n"
            "Produce the final Markdown report. Ensure it is accurate, professional, "
            "and 100% compliant with safety standards."
        )
        return system, user

    @staticmethod
    def create_user_prompt(statement: str) -> str:
        return f"Analyze the following medical statement: {statement}"
