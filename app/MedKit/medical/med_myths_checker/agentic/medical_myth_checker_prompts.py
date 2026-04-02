#!/usr/bin/env python3
"""
Standalone module for creating medical myths checker prompts.

This module provides a builder class for generating system and user prompts
for medical myth analysis using AI models.
"""


class PromptBuilder:
    """Builder for constructing prompts for medical myth analysis."""

    @staticmethod
    def system_prompt() -> str:
        """Generate the system prompt for myth analysis."""
        return """You are a medical fact-checker with expertise in evidence-based medicine. Your task is to analyze medical claims/myths and provide an assessment grounded EXCLUSIVELY in peer-reviewed scientific evidence.

CRITICAL REQUIREMENTS:
1. ALL claims must be verified against peer-reviewed medical literature, clinical trials, and established medical guidelines
2. Only cite evidence from peer-reviewed journals, systematic reviews, meta-analyses, or official medical organizations (WHO, NIH, CDC, etc.)
3. If a claim cannot be supported by peer-reviewed evidence, mark it as FALSE or UNCERTAIN and explain what peer-reviewed research contradicts or is lacking
4. Include specific journal names, publication years, and authors when possible
5. Do NOT use general knowledge or anecdotal evidence - only evidence-based medicine"""

    @staticmethod
    def user_prompt(myth: str) -> str:
        """Generate the user prompt for myth analysis."""
        return f"Analyze the following medical myth grounded in peer-reviewed evidence: {myth}"

    @staticmethod
    def get_evidence_auditor_prompts(myth: str, analysis_content: str) -> tuple[str, str]:
        """Create prompts for the Evidence Compliance Auditor (JSON output)."""
        system = (
            "You are a Senior Medical Evidence Auditor. Your role is to audit medical "
            "myth assessments for factual accuracy and strength of evidence. Output "
            "a structured JSON report identifying any weak citations or incorrect "
            "conclusions based on current medical literature."
        )
        user = (
            f"Audit the following medical myth analysis for '{myth}' and output a "
            f"structured JSON report:\n\n{analysis_content}"
        )
        return system, user

    @staticmethod
    def get_output_synthesis_prompts(myth: str, specialist_data: str, audit_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Medical Myth-Busting Editor. Your role is to take raw "
            "evidence analysis and a structured quality audit, then synthesize them "
            "into a FINAL, high-impact, and safe Markdown report. You MUST apply "
            "all fixes identified in the audit and ensure the debunking is "
            "clear, authoritative, and medically sound."
        )
        user = (
            f"Synthesize the final myth-busting report for: '{myth}'\n\n"
            f"EVIDENCE DATA:\n{specialist_data}\n\n"
            f"QUALITY AUDIT:\n{audit_data}\n\n"
            "Produce the final Markdown report. Ensure it is accurate, professional, "
            "and effectively communicates the truth based on medical evidence."
        )
        return system, user
