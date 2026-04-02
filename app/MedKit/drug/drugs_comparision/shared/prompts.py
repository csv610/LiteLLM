#!/usr/bin/env python3
"""
Standalone module for creating drugs comparison prompts.

This module provides a builder class for generating system and user prompts
for drugs comparison analysis using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medicines comparison analysis."""

    MEDICAL_GUARDRAILS = """
    MANDATORY CLINICAL STANDARDS:
    1. Cite sources (e.g., FDA label, NCT number, PubMed ID) for all efficacy and safety claims.
    2. Explicitly state 'No evidence found' if data is unavailable.
    3. Never provide definitive medical advice; use language like 'suggests' or 'indicated for'.
    4. If a drug has a Black Box Warning, it must be the first safety item mentioned.
    """

    @staticmethod
    def create_pharmacology_system_prompt() -> str:
        """System prompt for the Pharmacology Agent."""
        return f"""You are a clinical pharmacology expert. {PromptBuilder.MEDICAL_GUARDRAILS}
        Focus strictly on:
        1. Efficacy rates and clinical trial outcomes.
        2. Onset and duration of action.
        3. Common and serious side effects.
        4. Contraindications and black box warnings."""

    @staticmethod
    def create_regulatory_system_prompt() -> str:
        """System prompt for the Regulatory & Compliance Agent."""
        return f"""You are a pharmaceutical regulatory expert. {PromptBuilder.MEDICAL_GUARDRAILS}
        Focus strictly on:
        1. FDA approval status, dates, and types.
        2. Generic availability and patent expiration.
        3. Active FDA alerts and safety communications."""

    @staticmethod
    def create_market_access_system_prompt() -> str:
        """System prompt for the Market Access Agent."""
        return f"""You are a health economics and market access specialist. {PromptBuilder.MEDICAL_GUARDRAILS}
        Focus strictly on:
        1. Typical cost ranges and generic vs. brand pricing.
        2. Insurance coverage trends and tiering.
        3. Patient assistance programs and available formulations."""

    @staticmethod
    def create_clinical_context_system_prompt() -> str:
        """System prompt for the Clinical Context Agent."""
        return f"""You are a clinical practitioner. {PromptBuilder.MEDICAL_GUARDRAILS}
        Focus strictly on:
        1. Suitability for specific age groups (e.g., elderly).
        2. Performance in acute vs. chronic conditions.
        3. Considerations for patients with specific comorbidities."""

    @staticmethod
    def create_compliance_system_prompt() -> str:
        """System prompt for the Legal & Patient Compliance Agent."""
        return f"""You are a healthcare compliance and patient safety officer. {PromptBuilder.MEDICAL_GUARDRAILS}
        Focus strictly on:
        1. Controlled substance scheduling and legal prescribing constraints.
        2. Required clinical monitoring (e.g., regular blood work).
        3. Factors affecting patient adherence (e.g., dosing complexity, administration difficulty).
        4. Alignment with clinical guidelines and standard of care."""

    @staticmethod
    def create_safety_auditor_system_prompt() -> str:
        """System prompt for the Safety & Standards Auditor (JSON output)."""
        return """You are a Senior Medical Safety Auditor. Your role is to audit 
drug comparison reports for technical accuracy, safety standards, and clinical 
consistency. Output your findings as a structured JSON report."""

    @staticmethod
    def create_output_synthesis_prompts(medicine1: str, medicine2: str, specialist_data: str, audit_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Clinical Strategy Editor. Your role is to take raw "
            "comparative drug data and a structured safety audit, then synthesize "
            "them into a FINAL, polished, and safe Markdown comparison report. "
            "You MUST apply all fixes identified in the audit and ensure all "
            "Black Box warnings and safety alerts are prominently featured."
        )
        user = (
            f"Synthesize the final comparison report for: '{medicine1}' vs '{medicine2}'\n\n"
            f"COMPARATIVE DATA:\n{specialist_data}\n\n"
            f"SAFETY AUDIT:\n{audit_data}\n\n"
            "Produce the final Markdown report. Ensure it is accurate, professional, "
            "and 100% compliant with clinical safety standards."
        )
        return system, user

    @staticmethod
    def create_synthesis_system_prompt() -> str:
        """System prompt for the Synthesis & QA Orchestrator."""
        return f"""You are a senior medical editor and clinical strategist. {PromptBuilder.MEDICAL_GUARDRAILS}
        Your tasks:
        1. Synthesize reports from multiple experts into a cohesive comparison.
        2. Incorporate the Safety Auditor's findings to resolve conflicts.
        3. Summarize key differences clearly.
        4. Ensure the final narrative contains the mandatory medical disclaimer."""

    @staticmethod
    def create_user_prompt(medicine1: str, medicine2: str, context: str) -> str:
        """
        Create the user prompt for medicines comparison analysis.

        Args:
            medicine1: The name of the first medicine
            medicine2: The name of the second medicine
            context: Additional context for the comparison

        Returns:
            str: Formatted user prompt
        """
        return f"Detailed side-by-side comparison between {medicine1} and {medicine2}. {context}"
