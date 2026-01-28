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
        return f"""Medical Myth/Claim to Analyze: {myth}

Respond ONLY with valid JSON in this exact format:
{{
    "myths": [
        {{
            "statement": "exact claim from the input",
            "status": "TRUE or FALSE or UNCERTAIN",
            "explanation": "detailed medical explanation grounded in peer-reviewed evidence",
            "peer_reviewed_sources": "Specific citations: Journal names, publication years, and research findings. Or: 'No peer-reviewed evidence found' with explanation of research gaps",
            "risk_level": "LOW or MODERATE or HIGH"
        }}
    ]
}}"""
