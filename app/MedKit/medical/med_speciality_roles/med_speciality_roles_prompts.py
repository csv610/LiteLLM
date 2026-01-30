#!/usr/bin/env python3
"""
Standalone module for creating medical specialist referral prompts.

This module provides a builder class for generating system and user prompts
for medical specialist recommendation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical specialist recommendation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for speciality role description.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are a medical knowledge assistant. Your task is to provide detailed information about the roles and responsibilities of a specific medical specialist.
For a given medical speciality, you should list:
1.  **Primary Focus:** What body systems or conditions they focus on.
2.  **Key Responsibilities:** What they generally do (diagnose, treat, manage).
3.  **Common Procedures:** Examples of procedures or tests they perform.

Example format:
- Speciality: "Cardiologist"
  Roles:
  - **Primary Focus:** Heart and cardiovascular system.
  - **Key Responsibilities:** Diagnosing and treating heart defects, coronary artery disease, heart failure, and valvular heart disease.
  - **Common Procedures:** EKG, Echocardiogram, Cardiac Catheterization."""

    @staticmethod
    def create_user_prompt(speciality: str) -> str:
        """Create the user prompt for speciality role description.

        Args:
            speciality: The medical speciality to describe

        Returns:
            str: Formatted user prompt
        """
        return f"""Please describe the key roles and responsibilities of a: "{speciality}"
"""
