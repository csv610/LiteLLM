#!/usr/bin/env python3
"""
Standalone module for creating medical test device prompts.

This module provides a builder class for generating system and user prompts
for medical device information generation using AI models.
"""


class PromptBuilder:
    """Builder class for constructing prompts for medical device information generation."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for the medical device information generator.

        Returns:
            The system prompt string.
        """
        return """You are a medical device information specialist with extensive knowledge of medical diagnostic and therapeutic equipment. Your role is to provide comprehensive, accurate, and evidence-based information about medical devices.

When generating medical device information, you must:

1. Provide technically accurate specifications and classifications based on FDA, CE, or other relevant regulatory standards
2. Include detailed information about device functionality, intended use, and clinical applications
3. Describe physical and operational specifications with precision
4. Address safety considerations, contraindications, and regulatory compliance
5. Include information about maintenance, servicing, and quality assurance requirements
6. Discuss cost considerations, availability, and market positioning where applicable
7. Present both advantages and limitations objectively
8. Use appropriate medical and technical terminology
9. Structure information in a clear, organized manner following the requested categories

Your responses should be comprehensive yet concise, suitable for healthcare professionals, biomedical engineers, and procurement specialists. Maintain a professional, objective tone and base all information on established medical device standards and clinical evidence."""

    @staticmethod
    def build_user_prompt(device_name: str) -> str:
        """
        Build the prompt for generating comprehensive medical device information.

        Args:
            device_name: Name of the medical device.

        Returns:
            The formatted prompt string.
        """
        return f"""Generate comprehensive medical device information for: {device_name}

Include detailed information about:
1. Device name and classification
2. Intended use and applications
3. Technical specifications and principles
4. Physical specifications
5. Operational requirements and specifications
6. Safety and regulatory information
7. Clinical applications and benefits
8. Maintenance and servicing requirements
9. Cost and availability information
10. Advantages and limitations

Provide accurate, evidence-based medical device information."""
