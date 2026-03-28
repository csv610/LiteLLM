#!/usr/bin/env python3
"""
Standalone module for creating surgical tool information prompts.

This module provides a builder class for generating system and user prompts
for surgical tool information generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for surgical tool information."""

    @staticmethod
    def create_technical_expert_system_prompt() -> str:
        """Create the system prompt for the Technical Expert agent."""
        return """You are a Technical Surgical Instrument Engineer. Your expertise lies in the physical design, 
specifications, operational mechanics, and regulatory standards of surgical tools.
Provide precise, technical information focusing on dimensions, materials, mechanics, and compliance."""

    @staticmethod
    def create_clinical_specialist_system_prompt() -> str:
        """Create the system prompt for the Clinical Specialist agent."""
        return """You are a Senior Surgical Consultant. Your expertise lies in the clinical application, 
surgical purpose, intraoperative use, and comparative analysis of surgical tools across various specialties.
Provide clinically focused information on how the tool is used in the OR and its role in patient care."""

    @staticmethod
    def create_safety_maintenance_specialist_system_prompt() -> str:
        """Create the system prompt for the Safety & Maintenance Specialist agent."""
        return """You are a Surgical Safety and Sterile Processing Expert. Your expertise lies in safety features, 
pre-operative preparation, sterilization protocols, maintenance, and risk mitigation.
Provide detailed information on ensuring the tool is safe, clean, and well-maintained."""

    @staticmethod
    def create_medical_historian_educator_system_prompt() -> str:
        """Create the system prompt for the Medical Historian and Educator agent."""
        return """You are a Medical Historian and Surgical Educator. Your expertise lies in the historical context, 
training requirements, cost analysis, and patient education aspects of surgical tools.
Provide context on where the tool came from, how surgeons learn to use it, and how to communicate its use."""

    @staticmethod
    def create_orchestrator_system_prompt() -> str:
        """Create the system prompt for the Orchestrator agent."""
        return """You are the Chief Medical Information Officer. Your role is to synthesize specialized reports 
from multiple surgical experts into a single, cohesive, and comprehensive surgical tool profile.
Ensure consistency, remove redundancies, and ensure the final report meets the highest medical standards."""

    @staticmethod
    def create_technical_expert_user_prompt(tool: str) -> str:
        return f"""Provide technical specifications for the surgical tool: {tool}.
Focus on:
- Tool basics (category, names, specialties)
- Physical specifications (dimensions, materials, finish)
- Operational characteristics (actuation, precision, force)
- Regulatory standards (FDA, ISO, certifications)"""

    @staticmethod
    def create_clinical_specialist_user_prompt(tool: str) -> str:
        return f"""Provide clinical insights for the surgical tool: {tool}.
Focus on:
- Tool purpose and applications
- Intraoperative use and handling techniques
- Specialty-specific considerations
- Alternatives and comparisons"""

    @staticmethod
    def create_safety_maintenance_user_prompt(tool: str) -> str:
        return f"""Provide safety and maintenance protocols for the surgical tool: {tool}.
Focus on:
- Safety features and risk mitigation
- Pre-operative preparation and inspection
- Discomfort, risks, and complications
- Maintenance, care, and sterilization protocols"""

    @staticmethod
    def create_medical_historian_educator_user_prompt(tool: str) -> str:
        return f"""Provide historical and educational context for the surgical tool: {tool}.
Focus on:
- Historical context and evolution
- Training and certification requirements
- Cost and procurement information
- Educational content for patients and staff"""

    @staticmethod
    def create_orchestrator_user_prompt(tool: str, expert_reports: str) -> str:
        return f"""Synthesize the following expert reports for the surgical tool: {tool}.
Expert Reports:
{expert_reports}

Combine these into a single comprehensive profile following the standard surgical tool information model."""
