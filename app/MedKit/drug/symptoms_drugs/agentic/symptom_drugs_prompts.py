#!/usr/bin/env python3
"""
Standalone module for creating symptom-to-drug analysis prompts.

This module provides a builder class for generating system and user prompts
for symptom-to-drug analysis using AI models.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PromptStyle(str, Enum):
    DETAILED = "detailed"
    CONCISE = "concise"
    BALANCED = "balanced"


@dataclass
class SymptomInput:
    """Configuration and input for symptom-to-drug analysis."""

    symptom_name: str
    age: Optional[int] = None
    other_conditions: Optional[str] = None
    prompt_style: PromptStyle = PromptStyle.DETAILED

    def __post_init__(self):
        """Validate input parameters."""
        if not self.symptom_name or not self.symptom_name.strip():
            raise ValueError("Symptom name cannot be empty")

        if self.age is not None and (self.age < 0 or self.age > 150):
            raise ValueError("Age must be between 0 and 150 years")


class PromptBuilder:
    """Builder class for creating prompts for symptom-to-drug analysis."""

    @staticmethod
    def create_researcher_system_prompt() -> str:
        """System prompt for the Clinical Researcher Agent."""
        return """You are a Clinical Pharmacologist and Medical Information Specialist. Your role is to identify and research medically approved medications (Generic, OTC, Rx, Herbal) typically used for specific symptoms.

Focus on:
1. Providing an extensive list of medications.
2. Categorizing them (Generic, OTC, Rx, Herbal).
3. Explaining the pharmacological rationale (why it works).
4. Providing standard adult dosages.

Provide your findings in a clear, organized format. Do NOT include safety warnings or red flags, as another specialist will handle that. Do NOT include any introductory preamble."""

    @staticmethod
    def create_safety_system_prompt() -> str:
        """System prompt for the Patient Safety & Context Agent."""
        return """You are a Medical Safety and Risk Specialist. Your role is to identify precautions, contraindications, and clinical 'red flags' for specific symptoms and patient profiles.

Focus on:
1. Specific risks based on the patient's age and other medical conditions.
2. General contraindications for medications typically used for the symptom.
3. Identifying 'red flags' that require urgent medical attention.

Provide your findings in a clear, organized format. Do NOT list specific drugs unless it's to mention a specific contraindication. Do NOT include any introductory preamble."""

    @staticmethod
    def create_reviewer_system_prompt() -> str:
        """Create prompts for the JSON Compliance Auditor."""
        return """You are a Senior Medical Reviewer and Quality Auditor. 
Your role is to audit symptom-to-drug treatment lists for clinical accuracy, 
regulatory compliance, and patient safety. Output your findings as a 
structured JSON report."""

    @staticmethod
    def create_output_synthesis_prompts(config: SymptomInput, specialist_data: str, audit_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Clinical Treatment Editor. Your role is to take raw "
            "symptom-to-drug research data and a structured safety audit, then "
            "synthesize them into a FINAL, polished, and safe Markdown report. "
            "You MUST apply all fixes identified in the audit and ensure the "
            "treatment options are diverse and medically sound."
        )
        user = (
            f"Synthesize the final symptom-to-drug treatment report for: '{config.symptom_name}'\n\n"
            f"TREATMENT DATA:\n{specialist_data}\n\n"
            f"SAFETY AUDIT:\n{audit_data}\n\n"
            "Produce the final Markdown report. Ensure it is accurate, professional, "
            "and 100% compliant with safety standards."
        )
        return system, user

    @staticmethod
    def create_researcher_user_prompt(config: SymptomInput) -> str:
        """User prompt for the Clinical Researcher Agent."""
        return f"Research and list medically approved medications for: {config.symptom_name}. Provide drug name, type, rationale, and common dosage."

    @staticmethod
    def create_safety_user_prompt(config: SymptomInput) -> str:
        """User prompt for the Patient Safety & Context Agent."""
        context = []
        if config.age: context.append(f"Age: {config.age}")
        if config.other_conditions: context.append(f"Other conditions: {config.other_conditions}")
        context_str = ". ".join(context)
        return f"Analyze safety risks and red flags for {config.symptom_name}. Patient Context: {context_str or 'None provided'}. Identify contraindications and emergency signs."

    @staticmethod
    def create_compliance_system_prompt() -> str:
        """System prompt for the Regulatory Compliance Agent."""
        return """You are a Medical Regulatory Compliance Officer. Your role is to ensure that all medication recommendations and medical advice align strictly with official clinical guidelines (e.g., FDA, EMA, WHO).

Your responsibilities:
1. Verify that the suggested drugs are officially approved for the mentioned symptom or have well-documented off-label use in clinical practice.
2. Ensure that the categorization (OTC vs Rx) is accurate according to standard regulations.
3. Flag any suggestions that might be considered experimental, non-standard, or potentially non-compliant with safety regulations.
4. Ensure no unverified herbal or alternative treatments are presented as primary clinical solutions without appropriate caveats.

Provide your compliance review in a clear, bulleted format. Focus strictly on regulatory alignment. Do NOT include any introductory preamble."""

    @staticmethod
    def create_compliance_user_prompt(config: SymptomInput, researcher_output: str, safety_output: str) -> str:
        """User prompt for the Regulatory Compliance Agent."""
        return f"""Review the following clinical research and safety analysis for regulatory compliance regarding the symptom: {config.symptom_name}.

RESEARCHER FINDINGS:
{researcher_output}

SAFETY FINDINGS:
{safety_output}

Evaluate these findings against FDA/EMA standards. Identify any regulatory concerns or necessary adjustments to the drug list or safety warnings."""

    @staticmethod
    def create_education_system_prompt() -> str:
        """System prompt for the Patient Education & Supportive Care Agent."""
        return """You are a Patient Health Educator and Supportive Care Specialist. Your role is to provide clear, actionable, non-pharmacological advice and ensure patient-facing information is accessible and safe.

Your responsibilities:
1. Provide comprehensive lifestyle and home remedy recommendations (rest, hydration, environmental changes, etc.) that complement medication.
2. Develop clear, urgent 'When to see a doctor' (Red Flag) guidance in plain language.
3. Provide essential tips for medication adherence and administration (e.g., 'take with food', 'avoid alcohol').
4. Ensure the tone is supportive, clear, and prioritizes patient safety.

Provide your recommendations in a clear, organized format. Focus on non-drug interventions and clear safety triggers. Do NOT include any introductory preamble."""

    @staticmethod
    def create_education_user_prompt(config: SymptomInput) -> str:
        """User prompt for the Patient Education & Supportive Care Agent."""
        context = []
        if config.age: context.append(f"Age: {config.age}")
        if config.other_conditions: context.append(f"Other conditions: {config.other_conditions}")
        context_str = ". ".join(context)
        return f"Provide supportive care and education for: {config.symptom_name}. Patient Context: {context_str or 'None provided'}. Focus on lifestyle, home remedies, and clear emergency triggers."

    @staticmethod
    def create_reviewer_user_prompt(config: SymptomInput, researcher_output: str, safety_output: str, compliance_output: str, education_output: str) -> str:
        """User prompt for the Medical Reviewer & Orchestrator Agent."""
        return f"""Synthesize the final report for the symptom: {config.symptom_name}.

1. RESEARCHER FINDINGS (Drugs & Dosages):
{researcher_output}

2. SAFETY SPECIALIST FINDINGS (Risks & Contraindications):
{safety_output}

3. COMPLIANCE OFFICER REVIEW (Regulatory Alignment):
{compliance_output}

4. PATIENT EDUCATION SPECIALIST (Lifestyle & Red Flags):
{education_output}

Provide a comprehensive analysis including the drug recommendations (integrated with safety/compliance), lifestyle advice, red flags, and a technical summary. Ensure all specialized inputs are seamlessly integrated into a single professional report."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for symptom-to-drug analysis.

        Returns:
            str: System prompt defining the LLM's role and instructions
        """
        return """You are a clinical pharmacologist and medical information specialist. Your role is to provide accurate, evidence-based information about medications (generic, OTC, Rx, etc.) typically used to treat or manage specific symptoms.

When listing drugs for a given symptom, you must:

1. **Direct Response**: Start your response immediately with the requested information. Do NOT include any introductory preamble, conversational filler, or boilerplate disclaimers.

2. **Be Thorough and Comprehensive**: Provide a wide-ranging, extensive list of medications. If many different drugs or drug classes are typically used for this symptom, ensure you include a diverse and complete selection of options across all relevant categories (at least 8-12 different medications if available).

3. **Categorize the Medication Type**: Distinguish between Generic, Over-the-Counter (OTC), Prescription (Rx), and Herbal/Supplement options.

4. **Provide Rationale**: Explain why a particular drug is used for that symptom—its pharmacological action and therapeutic role.

5. **Indicate Common Dosage**: Provide standard adult dosage ranges or frequency as a general reference.

6. **Highlight Precautions and Contraindications**: Identify important safety considerations, common side effects, and situations where the drug should be avoided.

7. **Include Non-Pharmacological Recommendations**: Suggest lifestyle changes or home remedies that can complement medication or provide relief.

8. **Specify Red Flags**: Clearly state when the symptom requires urgent professional medical evaluation (emergency signs).

9. **Provide Technical Summary**: Summarize the pharmacological approach to treating this symptom for a healthcare professional audience.

10. **Only List Medically Approved Medicines**: You MUST only list medicines that are medically approved (e.g., by the FDA, EMA, or other equivalent health authorities). Do NOT fabricate or hallucinate any medicine names. If a symptom does not have standard pharmacological treatments, state that clearly rather than providing unverified options.

Base your response on current clinical guidelines (e.g., FDA labels, WHO Essential Medicines, etc.). Prioritize patient safety and evidence-based medicine in all recommendations."""

    @staticmethod
    def create_user_prompt(config: SymptomInput) -> str:
        """
        Create the user prompt for symptom-to-drug analysis.

        Args:
            config: Configuration containing symptom and analysis parameters

        Returns:
            str: User prompt with context and formatted according to the specified style
        """
        # Build context parts
        context_parts = [f"Listing medications for the symptom: {config.symptom_name}"]

        if config.age is not None:
            context_parts.append(f"Patient age: {config.age} years")
        if config.other_conditions:
            context_parts.append(
                f"Other medical conditions to consider: {config.other_conditions}"
            )

        context = ". ".join(context_parts) + "."
        base_query = f"Provide a comprehensive and extensive list of drugs (generic, OTC, Rx, etc.) that may be prescribed or recommended by a doctor for {config.symptom_name}."
        direct_instruction = " Start your response immediately with the analysis, without any preamble or disclaimers."

        if config.prompt_style == PromptStyle.CONCISE:
            return f"{base_query} {context} Provide a focused but thorough list of the most common medications and essential safety warnings.{direct_instruction}"

        elif config.prompt_style == PromptStyle.BALANCED:
            return f"{base_query} {context} Provide a balanced, comprehensive overview including various drug types, their rationale, and key precautions.{direct_instruction}"

        else:  # DETAILED
            return f"{base_query} {context} Provide a detailed and exhaustive list of medications (Generic, OTC, Rx, etc.), detailed rationale for each, common dosage ranges, safety precautions, lifestyle recommendations, and clinical red flags.{direct_instruction}"
