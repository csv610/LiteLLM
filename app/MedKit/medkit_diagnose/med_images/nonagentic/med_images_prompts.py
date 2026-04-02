#!/usr/bin/env python3
"""
Standalone module for creating med image classification information prompts.

This module provides a builder class for generating system and user prompts
for med image classification information generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical image classification."""

    @staticmethod
    def create_image_classification_system_prompt() -> str:
        """
        Create a system prompt for medical image classification.

        Returns:
            A system prompt string defining the AI's role.
        """
        system_prompt = """You are an expert medical radiologist and pathologist. 
Your task is to analyze the provided medical image and provide a concise classification.

Provide:
1. Imaging modality
2. Anatomical site
3. Primary classification/finding
4. Confidence score (0.0 to 1.0)

Keep the output brief and professional. Do not include any preamble or extra text."""
        return system_prompt

    @staticmethod
    def create_image_classification_user_prompt() -> str:
        """
        Create a prompt for medical image classification.

        Returns:
            A prompt string for the AI model.
        """
        return "Classify this medical image concisely."
