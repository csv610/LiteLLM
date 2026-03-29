#!/usr/bin/env python3
"""
Standalone module for creating medical speciality prompts.

This module provides a builder class for generating system and user prompts
for medical speciality generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical speciality generation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Generate the system prompt for the medical specialties generator."""
        return "You are an expert in medical education and healthcare systems. Generate a complete and accurate database of medical specialties."

    @staticmethod
    def create_user_prompt() -> str:
        """Generate the user prompt for the medical specialties generator."""
        return """Generate a comprehensive list of medical specialists covering all major fields of medicine.
Organize them by logical categories (body system, type of care, patient population).

For each specialist, provide:
1. Formal specialty name
2. Category name and description
3. Role description
4. Conditions/diseases treated
5. Common referral reasons
6. Subspecialties
7. Surgical vs non-surgical
8. Patient population focus

Include both common (cardiology, dermatology) and specialized (physiatry, interventional radiology) fields."""
