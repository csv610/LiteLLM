"""
Standalone module for creating medical device identification prompts.

This module provides a builder class for generating system and user prompts
for identifying if a medical device is well-known in the healthcare community.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MedicalDeviceIdentifierInput:
    """Configuration and input for medical device identification."""
    device_name: str

    def __post_init__(self):
        """Validate input parameters."""
        if not self.device_name or not self.device_name.strip():
            raise ValueError("Device name cannot be empty")


class PromptBuilder:
    """Builder class for creating prompts for medical device identification."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for medical device identification.

        Returns:
            str: System prompt defining the LLM's role and instructions
        """
        return """You are a senior biomedical engineer and clinical technology specialist with extensive knowledge of medical instrumentation, implants, and diagnostic hardware. Your task is to identify if a given "medical device" name is "well-known" in the healthcare field.

A medical device (e.g., pacemaker, MRI scanner, scalpel, insulin pump) is considered "well-known" if it:
1. Is a standard tool or piece of equipment used in clinical or surgical settings.
2. Is approved by major regulatory bodies for medical use (like FDA Class I, II, or III).
3. Has established protocols for use, maintenance, and safety.
4. Is frequently mentioned in medical literature, hospital procurement, or clinical guidelines.

When identifying a device, you must:
1. Determine its recognition status.
2. Identify its category (e.g., therapeutic, diagnostic, life-support, monitoring).
3. Describe its primary function (what it does).
4. Provide a brief explanation of its clinical significance.

If a device is experimental, obsolete, or not well-known, clearly state that and explain why.

Always provide accurate, evidence-based information."""

    @staticmethod
    def create_user_prompt(config: MedicalDeviceIdentifierInput) -> str:
        """
        Create the user prompt for medical device identification.

        Args:
            config: Configuration containing the device name

        Returns:
            str: User prompt
        """
        return f"Identify the medical device '{config.device_name}' and determine if it is well-known in the healthcare community. Provide details on its category, primary function, and clinical significance."
