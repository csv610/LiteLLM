"""
Standalone module for creating medical procedure identification prompts.

This module provides a builder class for generating system and user prompts
for identifying if a medical procedure is well-known in the healthcare community.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MedicalProcedureIdentifierInput:
    """Configuration and input for medical procedure identification."""
    procedure_name: str

    def __post_init__(self):
        """Validate input parameters."""
        if not self.procedure_name or not self.procedure_name.strip():
            raise ValueError("Procedure name cannot be empty")


class PromptBuilder:
    """Builder class for creating prompts for medical procedure identification."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for medical procedure identification.

        Returns:
            str: System prompt defining the LLM's role and instructions
        """
        return """You are a senior clinical coordinator and surgical specialist with deep expertise in medical procedures, interventions, and clinical protocols. Your task is to identify if a given "medical procedure" name is "well-known" in the healthcare field.

A medical procedure (e.g., appendectomy, colonoscopy, angioplasty, hemodialysis) is considered "well-known" if it:
1. Is a standard intervention or diagnostic action performed in clinical practice.
2. Has established protocols, codes (like CPT or ICD-10-PCS), and safety standards.
3. Is frequently taught in medical and nursing curricula.
4. Is part of standard clinical pathways for treating or diagnosing specific conditions.

When identifying a procedure, you must:
1. Determine its recognition status.
2. Identify its type (e.g., surgical, interventional, diagnostic, conservative).
3. List its primary indications (when it is performed).
4. Provide a brief explanation of its clinical significance.

If a procedure is experimental, highly specialized, obsolete, or not well-known, clearly state that and explain why.

Always provide accurate, evidence-based information."""

    @staticmethod
    def create_user_prompt(config: MedicalProcedureIdentifierInput) -> str:
        """
        Create the user prompt for medical procedure identification.

        Args:
            config: Configuration containing the procedure name

        Returns:
            str: User prompt
        """
        return f"Identify the medical procedure '{config.procedure_name}' and determine if it is well-known in the healthcare community. Provide details on its type, indications, and clinical significance."
