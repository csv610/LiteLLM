#!/usr/bin/env python3
"""
Prompts for multi-agent medical decision guide generation.
"""

class MultiAgentPrompts:
    """Prompts for specialized medical agents."""

    @staticmethod
    def get_analyzer_system_prompt() -> str:
        return """You are a Medical Research Analyst. 
Your task is to analyze a given symptom and provide high-level metadata:
- Secondary symptoms often associated with it.
- Typical age groups covered in a general assessment.
- The clinical scope (what is covered and what is not).
Focus only on these aspects."""

    @staticmethod
    def get_analyzer_user_prompt(symptom: str) -> str:
        return f"Provide clinical metadata for the symptom: {symptom}."

    @staticmethod
    def get_triage_system_prompt() -> str:
        return """You are an Emergency Medicine Specialist.
Your task is to identify critical warning signs and emergency indicators for a given symptom.
- Warning signs: Red flags requiring immediate attention but not necessarily an ER visit.
- Emergency indicators: Life-threatening signs requiring immediate 911/ER.
Be concise and focus on patient safety."""

    @staticmethod
    def get_triage_user_prompt(symptom: str) -> str:
        return f"Identify red flags and emergency indicators for: {symptom}."

    @staticmethod
    def get_logic_architect_system_prompt() -> str:
        return """You are a Clinical Logic Architect.
Your task is to design a decision tree for symptom assessment.
You must provide a series of questions (DecisionNodes) that lead to either another question or a terminal Outcome ID.
Focus on logical flow and diagnostic reasoning.
Ensure every path leads to an Outcome ID."""

    @staticmethod
    def get_logic_architect_user_prompt(symptom: str, context: str) -> str:
        return f"Design a decision tree logic for {symptom}. Context: {context}"

    @staticmethod
    def get_outcome_specialist_system_prompt() -> str:
        return """You are a Clinical Outcome Specialist.
Your task is to define the specific clinical outcomes, recommendations, and home care advice for the terminal nodes of a decision tree.
For each outcome ID provided, define severity, urgency, recommendations, possible diagnoses, and home care advice."""

    @staticmethod
    def get_outcome_specialist_user_prompt(symptom: str, tree_logic: str) -> str:
        return f"Define outcomes for the following decision tree logic for {symptom}: {tree_logic}"

    @staticmethod
    def get_synthesis_system_prompt() -> str:
        return """You are a Senior Medical Coordinator.
Your task is to synthesize information from various specialists into a cohesive Medical Decision Guide.
Ensure clinical consistency, logical flow, and that all IDs match correctly between nodes and outcomes."""

    @staticmethod
    def get_compliance_system_prompt() -> str:
        return """You are a Clinical Safety & Compliance Auditor. 
Your task is to audit a completed medical decision guide for safety, adherence 
to standards, and clinical logic. Output your findings as a structured JSON report."""

    @staticmethod
    def get_compliance_user_prompt(guide_data: str) -> str:
        return f"Audit the following medical decision guide for clinical safety and compliance and output a structured JSON report: {guide_data}"

    @staticmethod
    def get_output_synthesis_prompts(symptom: str, specialist_data: str, audit_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Medical Content Director. Your role is to take a "
            "structured medical decision tree and its safety audit, then synthesize "
            "them into a FINAL, polished, and safe Markdown decision guide. "
            "You MUST apply all safety fixes identified in the audit and ensure the "
            "guide is easy for clinicians or patients to follow."
        )
        user = (
            f"Synthesize the final medical decision guide for: '{symptom}'\n\n"
            f"DECISION GUIDE DATA:\n{specialist_data}\n\n"
            f"SAFETY AUDIT:\n{audit_data}\n\n"
            "Produce the final Markdown decision guide. Ensure it is accurate, "
            "logically sound, and 100% compliant with safety standards."
        )
        return system, user
