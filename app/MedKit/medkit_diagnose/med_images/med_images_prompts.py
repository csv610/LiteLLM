#!/usr/bin/env python3
"""
Standalone module for creating med image classification information prompts.

This module provides a builder class for generating system and user prompts
for med image classification information generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for med image classification information generation."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create a system prompt that defines the AI's role and guidelines.

        Returns:
            A system prompt string defining the AI's role as a medical information specialist.
        """
        system_prompt = """You are a medical information specialist with expertise in clinical laboratory testing and diagnostic procedures. Your role is to provide comprehensive, accurate, and evidence-based information about med image classifications.

When generating med image classification information, you must:

1. Provide scientifically accurate information based on current medical knowledge and standards
2. Use clear, professional medical terminology while remaining accessible
3. Include specific details about test procedures, methodologies, and interpretations
4. Cite appropriate reference ranges with units of measurement
5. Describe clinical significance and practical applications
6. Address patient preparation requirements and potential limitations
7. Maintain objectivity and avoid making diagnostic conclusions
8. Structure information logically and comprehensively
9. Do not include any preamble, disclaimer, and unnecessary information in the report.
"""
        return system_prompt

    @staticmethod
    def create_user_prompt(test_name: str) -> str:
        """
        Create a comprehensive prompt for generating med image classification information.

        Args:
            test_name: The name of the med image classification.

        Returns:
            A formatted prompt string for the AI model.
        """
        prompt = f"""Generate comprehensive med image classification information for: {test_name}

Include detailed information about:
1. Test name and alternative names
2. Purpose and clinical use
3. Test indications and when it is ordered
4. Sample requirements and collection procedures
5. Test methodology and technology
6. Normal reference ranges and result interpretation
7. Preparatory requirements and restrictions
8. Risks, benefits, and limitations
9. Cost and availability information
10. Results interpretation and follow-up actions

Provide accurate, evidence-based med image classification information."""
        return prompt

    @staticmethod
    def create_image_classification_system_prompt() -> str:
        """
        Create a system prompt for medical image classification.

        Returns:
            A system prompt string defining the AI's role as a medical radiologist and pathologist.
        """
        system_prompt = """You are an expert medical radiologist and pathologist specializing in multi-modal image analysis. 
Your task is to analyze the provided medical image and provide a detailed classification and clinical findings.

When analyzing the image, you must:
1. Identify the correct imaging modality (X-Ray, CT, MRI, Ultrasound, Mammography, Histopathology, Retinal Fundus, Dermoscopy, or SPECT)
2. Identify the anatomical site or organ being imaged
3. Describe detailed clinical findings and observations
4. Provide a primary classification or diagnosis (e.g., Pneumonia, Bone Fracture, Normal)
5. Provide a confidence score for your assessment (0.0 to 1.0)
6. Suggest appropriate next steps or follow-up recommendations
7. Maintain objectivity and use professional medical terminology
8. Do not include any preamble, disclaimer, and unnecessary information in the report.
"""
        return system_prompt

    @staticmethod
    def create_image_classification_user_prompt() -> str:
        """
        Create a prompt for medical image classification.

        Returns:
            A prompt string for the AI model.
        """
        return "Analyze this medical image and provide a detailed classification including modality, anatomical site, findings, and recommendations."
