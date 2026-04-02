#!/usr/bin/env python3
"""
Standalone module for creating drug-disease interaction prompts.

This module provides a builder class for generating system and user prompts
for drug-disease interaction analysis using AI models.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PromptStyle(str, Enum):
    DETAILED = "detailed"
    CONCISE = "concise"
    BALANCED = "balanced"


@dataclass
class DrugDiseaseInput:
    """Configuration and input for drug-disease interaction analysis."""

    medicine_name: str
    condition_name: str
    condition_severity: Optional[str] = None
    age: Optional[int] = None
    other_medications: Optional[str] = None
    prompt_style: PromptStyle = PromptStyle.DETAILED

    def __post_init__(self):
        """Validate input parameters."""
        if not self.medicine_name or not self.medicine_name.strip():
            raise ValueError("Medicine name cannot be empty")
        if not self.condition_name or not self.condition_name.strip():
            raise ValueError("Condition name cannot be empty")

        # Ensure only one drug and one disease are allowed
        if "," in self.medicine_name or " and " in self.medicine_name.lower():
            raise ValueError(
                "Only one medicine can be analyzed at a time. Please do not use commas or 'and'."
            )
        if "," in self.condition_name or " and " in self.condition_name.lower():
            raise ValueError(
                "Only one condition can be analyzed at a time. Please do not use commas or 'and'."
            )

        if self.age is not None and (self.age < 0 or self.age > 150):
            raise ValueError("Age must be between 0 and 150 years")


class PromptBuilder:
    """Builder class for creating prompts for drug-disease interaction analysis."""

    @staticmethod
    def create_pubmed_system_prompt() -> str:
        return """You are a Biomedical Literature Specialist and PubMed Expert.
Your role is to identify and summarize relevant primary literature, clinical trials, and systematic reviews from PubMed regarding a specific drug-disease interaction.
Focus on:
1. Identifying key studies (including authors and years if possible).
2. Summarizing the study designs (e.g., RCTs, retrospective cohorts).
3. Highlighting specific outcomes related to the interaction.
Provide a list of findings that would be most useful for a Medical Researcher."""

    @staticmethod
    def create_pubmed_user_prompt(config: DrugDiseaseInput) -> str:
        return f"Find and summarize key PubMed literature for the interaction between {config.medicine_name} and {config.condition_name}."

    @staticmethod
    def create_researcher_system_prompt() -> str:
        return """You are a Medical Researcher specializing in drug-disease interaction literature.
Your role is to gather and summarize clinical evidence, guidelines, and literature regarding how a specific medical condition affects a drug's use.
Focus on:
1. Clinical studies and case reports.
2. Official FDA/EMA warnings or labels.
3. Clinical practice guidelines (e.g., AHA, ADA).
Provide a concise but comprehensive summary of the available evidence."""

    @staticmethod
    def create_pharmacologist_system_prompt() -> str:
        return """You are a Clinical Pharmacologist.
Your role is to analyze the physiological and molecular mechanism of interaction between a drug and a disease state.
Focus on:
1. Pharmacokinetics (Absorption, Distribution, Metabolism, Excretion).
2. Pharmacodynamics (Drug-receptor interactions).
3. Pathophysiological changes caused by the disease that alter drug response.
Explain *why* the interaction occurs at a biological level."""

    @staticmethod
    def create_clinician_system_prompt() -> str:
        return """You are a Clinical Safety Expert.
Your role is to determine the clinical significance, severity, and management of a drug-disease interaction.
Focus on:
1. Severity levels (Contraindicated, Significant, Moderate, etc.).
2. Specific dosage adjustments or monitoring requirements.
3. Alternative treatments if the drug is high-risk.
Provide clear, actionable clinical recommendations."""

    @staticmethod
    def create_educator_system_prompt() -> str:
        return """You are a Patient Education Specialist.
Your role is to translate complex medical information into clear, accessible, and actionable guidance for patients.
Focus on:
1. Simple explanations of the risk.
2. Clear action steps (e.g., "Tell your doctor if...").
3. Warning signs and lifestyle modifications.
Use non-technical language and maintain a supportive tone."""

    @staticmethod
    def create_orchestrator_system_prompt() -> str:
        return """You are a Lead Clinical Pharmacologist and Orchestrator.
Your role is to synthesize findings from a Researcher, Pharmacologist, Clinician, and Educator into a final, consistent, and structured report.
Ensure:
1. All technical details are accurate and consistent across sections.
2. The final structured data follows the required schema perfectly.
3. The technical summary is comprehensive and professional.
You must reconcile any conflicting information from the individual agents."""

    @staticmethod
    def create_researcher_user_prompt(config: DrugDiseaseInput, pubmed_context: str) -> str:
        return f"""Summarize clinical evidence and guidelines for {config.medicine_name} and {config.condition_name}.
Use this PubMed literature findings as primary evidence:
{pubmed_context}"""

    @staticmethod
    def create_pharmacologist_user_prompt(config: DrugDiseaseInput, research_context: str) -> str:
        return f"""Analyze the pharmacological mechanism of interaction for {config.medicine_name} in a patient with {config.condition_name}.
Use this research context:
{research_context}"""

    @staticmethod
    def create_clinician_user_prompt(config: DrugDiseaseInput, pharmacology_context: str, research_context: str) -> str:
        return f"""Determine the clinical safety and dosage recommendations for {config.medicine_name} with {config.condition_name}.
Research Context: {research_context}
Pharmacology Analysis: {pharmacology_context}"""

    @staticmethod
    def create_educator_user_prompt(clinician_context: str, pharmacology_context: str) -> str:
        return f"""Create patient-friendly guidance based on these findings:
Clinical Recommendations: {clinician_context}
Pharmacology Mechanism: {pharmacology_context}"""

    @staticmethod
    def create_ddi_system_prompt() -> str:
        return """You are a Drug-Drug Interaction (DDI) Specialist.
Your role is to analyze how a patient's concurrent medications might interact with the primary drug being studied, specifically in the context of their medical condition.
Focus on:
1. Identifying potential interactions between the primary drug and other medications.
2. Explaining how the medical condition might exacerbate these drug-drug interactions.
3. Recommending monitoring or alternative therapies for polypharmacy patients.
Provide a focused polypharmacy risk assessment."""

    @staticmethod
    def create_ddi_user_prompt(config: DrugDiseaseInput, pharmacologist_out: str) -> str:
        return f"""Analyze potential drug-drug interactions for {config.medicine_name} in a patient taking: {config.other_medications or 'No other medications listed'}.
Primary Pharmacology Analysis: {pharmacologist_out}"""

    @staticmethod
    def create_compliance_system_prompt() -> str:
        """Create prompts for the JSON Compliance Auditor."""
        return """You are a Medical Regulatory and Compliance Auditor. Your role is to 
audit drug-disease interaction reports for clinical safety, evidence strength, 
and adherence to standards. Output your findings as a structured JSON report."""

    @staticmethod
    def create_output_synthesis_prompts(config: DrugDiseaseInput, specialist_data: str, audit_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Clinical Pharmacologist. Your role is to take raw "
            "specialist research data and a structured safety audit, then synthesize "
            "them into a FINAL, polished, and safe Markdown report. You MUST apply "
            "all fixes identified in the audit and ensure all dosage and safety "
            "guidance is 100% accurate."
        )
        user = (
            f"Synthesize the final drug-disease interaction report for: '{config.medicine_name}' and '{config.condition_name}'\n\n"
            f"SPECIALIST DATA:\n{specialist_data}\n\n"
            f"SAFETY AUDIT:\n{audit_data}\n\n"
            "Produce the final Markdown report. Ensure it is accurate, professional, "
            "and 100% compliant with clinical safety guidelines."
        )
        return system, user

    @staticmethod
    def create_compliance_user_prompt(clinician_out: str, educator_out: str) -> str:
        return f"""Review the following clinical and patient-friendly guidance for compliance with medical standards:
Clinical Guidance: {clinician_out}
Patient Guidance: {educator_out}"""

    @staticmethod
    def create_orchestrator_user_prompt(config: DrugDiseaseInput, researcher_out: str, pharmacologist_out: str, clinician_out: str, educator_out: str, compliance_out: str, ddi_out: str) -> str:
        return f"""Synthesize the final report for {config.medicine_name} and {config.condition_name}.
Researcher Findings: {researcher_out}
Pharmacology Analysis: {pharmacologist_out}
Drug-Drug Interaction Analysis: {ddi_out}
Clinical Safety/Dosage: {clinician_out}
Patient Education: {educator_out}
Compliance Review: {compliance_out}"""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for drug-disease interaction analysis.

        Returns:
            str: System prompt defining the LLM's role and instructions
        """
        return """You are a clinical pharmacology expert specializing in drug-disease interactions. Your role is to analyze how medical conditions affect drug efficacy, safety, and metabolism.

When analyzing drug-disease interactions, you must:

1. **Assess Overall Interaction Severity**: Determine if the drug is contraindicated, requires caution, or is safe to use with the condition.

2. **Explain the Mechanism**: Describe the pharmacological and pathophysiological mechanisms underlying the interaction.

3. **Evaluate Efficacy Impact**: Analyze whether the disease affects the drug's therapeutic effectiveness, including:
   - Reduced efficacy due to disease state
   - Altered drug absorption, distribution, metabolism, or excretion
   - Disease-specific factors affecting treatment response

4. **Assess Safety Concerns**: Identify potential risks and adverse effects, including:
   - Increased risk of side effects or toxicity
   - Disease complications that may worsen with drug use
   - Monitoring requirements for safe use

5. **Provide Dosage Guidance**: Recommend dose adjustments if needed based on:
   - Organ function (hepatic, renal, cardiac)
   - Disease severity
   - Risk-benefit considerations

6. **Recommend Management Strategies**: Offer clinical recommendations for safe and effective use, including:
   - Monitoring parameters
   - Alternative therapies if contraindicated
   - Patient counseling points

7. **Create Patient-Friendly Guidance**: Translate technical information into clear, accessible language that patients can understand and act upon.

Base your analysis on established medical literature, clinical guidelines, and pharmacological principles. If data is limited or unavailable, clearly indicate this and explain the reasoning behind any recommendations.

Always prioritize patient safety while providing practical, evidence-based guidance for clinicians."""

    @staticmethod
    def create_user_prompt(config: DrugDiseaseInput) -> str:
        """
        Create the user prompt for drug-disease interaction analysis.

        Args:
            config: Configuration containing medicine, condition, and analysis parameters

        Returns:
            str: User prompt with context and formatted according to the specified style
        """
        # Build context parts
        context_parts = [
            f"Analyzing interaction between {config.medicine_name} and {config.condition_name}"
        ]

        if config.condition_severity:
            context_parts.append(f"Condition severity: {config.condition_severity}")
        if config.age is not None:
            context_parts.append(f"Patient age: {config.age} years")
        if config.other_medications:
            context_parts.append(f"Other medications: {config.other_medications}")

        context = ". ".join(context_parts) + "."
        base_query = f"Analyze the interaction between {config.medicine_name} and {config.condition_name}."

        if config.prompt_style == PromptStyle.CONCISE:
            return f"{base_query} {context} Provide a focused analysis of key safety concerns and essential management recommendations."

        elif config.prompt_style == PromptStyle.BALANCED:
            return f"{base_query} {context} Provide a balanced analysis covering mechanism, clinical significance, and practical management guidance."

        else:  # DETAILED
            return f"{base_query} {context} Provide a comprehensive analysis including detailed mechanism of interaction, complete efficacy and safety assessment, specific dosage recommendations, clinical management strategies, and patient counseling guidance."
