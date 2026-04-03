from app.MedKit.medical.base.models import ModelOutput

"""
med_ethics_models.py - Pydantic Models for Medical Ethics Analysis

This module contains all Pydantic data models for organizing and validating
medical ethics analysis across multiple dimensions.
"""

from typing import List, Optional, Union

from pydantic import BaseModel, Field


class EthicalPrincipleModel(BaseModel):
    """
    Analysis of a core ethical principle.
    """

    principle: str = Field(
        description="The name of the principle (e.g., Autonomy, Beneficence)."
    )
    application: str = Field(
        description="How this principle applies to the specific case."
    )
    implications: List[str] = Field(
        description="Implications of following or violating this principle."
    )


class StakeholderModel(BaseModel):
    """
    An individual or group affected by the ethical decision.
    """

    name: str = Field(description="The stakeholder (e.g., Patient, Family, Physician).")
    interests: List[str] = Field(
        description="The interests or concerns of this stakeholder."
    )
    rights: List[str] = Field(description="Relevant rights of this stakeholder.")


class SourceCitation(BaseModel):
    """
    A specific citation for a legal or professional guideline.
    """

    source_name: str = Field(description="Name of the source (e.g., HIPAA, AMA Code).")
    section: Optional[str] = Field(description="Specific section or article.")
    url: Optional[str] = Field(description="URL to the source if available.")


class LegalFrameworkModel(BaseModel):
    """
    Relevant legal and professional guidelines.
    """

    regulations: List[str] = Field(description="Relevant laws or regulations.")
    professional_guidelines: List[str] = Field(
        description="Guidelines from professional bodies (e.g., AMA, GMC)."
    )
    citations: List[SourceCitation] = Field(
        default_factory=list, description="Specific citations for the guidelines."
    )


class AnalystOutput(BaseModel):
    """
    Output from the Ethical Analyst agent.
    """

    principles: List[EthicalPrincipleModel] = Field(
        description="Application of core ethical principles."
    )
    stakeholders: List[StakeholderModel] = Field(
        description="Analysis of key stakeholders."
    )
    ethical_issues: List[str] = Field(
        description="The primary ethical questions or dilemmas identified."
    )


class ComplianceOutput(BaseModel):
    """
    Output from the Compliance agent.
    """

    legal_considerations: LegalFrameworkModel = Field(
        description="Relevant legal and professional context."
    )


class SafetyCheckModel(BaseModel):
    """
    Output from the Safety Critic agent.
    """

    passed: bool = Field(description="Whether the report passed the safety check.")
    critical_omissions: List[str] = Field(
        description="Any critical ethical or legal points missed."
    )
    hallucination_warnings: List[str] = Field(
        description="Any suspicious or unverified claims identified."
    )
    recommendations_for_improvement: List[str] = Field(
        description="Suggestions to make the report safer or more accurate."
    )


class EthicalAnalysisModel(BaseModel):
    """
    Comprehensive medical ethics analysis.
    """

    case_title: str = Field(
        description="A concise, descriptive 3-5 word title for the case."
    )
    summary: str = Field(description="A brief summary of the ethical dilemma.")
    facts: List[str] = Field(description="Key medical and social facts of the case.")
    ethical_issues: List[str] = Field(
        description="The primary ethical questions or dilemmas identified."
    )
    stakeholders: List[StakeholderModel] = Field(
        description="Analysis of key stakeholders."
    )
    principles: List[EthicalPrincipleModel] = Field(
        description="Application of core ethical principles."
    )
    legal_considerations: LegalFrameworkModel = Field(
        description="Relevant legal and professional context."
    )
    recommendations: List[str] = Field(
        description="Proposed actions or considerations for resolution."
    )
    conclusion: str = Field(description="Final summary of the ethical analysis.")
