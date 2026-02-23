"""
med_ethics_models.py - Pydantic Models for Medical Ethics Analysis

This module contains all Pydantic data models for organizing and validating
medical ethics analysis across multiple dimensions.
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class EthicalPrincipleModel(BaseModel):
    """
    Analysis of a core ethical principle.
    """
    principle: str = Field(description="The name of the principle (e.g., Autonomy, Beneficence).")
    application: str = Field(description="How this principle applies to the specific case.")
    implications: List[str] = Field(description="Implications of following or violating this principle.")


class StakeholderModel(BaseModel):
    """
    An individual or group affected by the ethical decision.
    """
    name: str = Field(description="The stakeholder (e.g., Patient, Family, Physician).")
    interests: List[str] = Field(description="The interests or concerns of this stakeholder.")
    rights: List[str] = Field(description="Relevant rights of this stakeholder.")


class LegalFrameworkModel(BaseModel):
    """
    Relevant legal and professional guidelines.
    """
    regulations: List[str] = Field(description="Relevant laws or regulations.")
    professional_guidelines: List[str] = Field(description="Guidelines from professional bodies (e.g., AMA, GMC).")


class EthicalAnalysisModel(BaseModel):
    """
    Comprehensive medical ethics analysis.
    """
    summary: str = Field(description="A brief summary of the ethical dilemma.")
    facts: List[str] = Field(description="Key medical and social facts of the case.")
    ethical_issues: List[str] = Field(description="The primary ethical questions or dilemmas identified.")
    stakeholders: List[StakeholderModel] = Field(description="Analysis of key stakeholders.")
    principles: List[EthicalPrincipleModel] = Field(description="Application of core ethical principles.")
    legal_considerations: LegalFrameworkModel = Field(description="Relevant legal and professional context.")
    recommendations: List[str] = Field(description="Proposed actions or considerations for resolution.")
    conclusion: str = Field(description="Final summary of the ethical analysis.")


class ModelOutput(BaseModel):
    data: Optional[EthicalAnalysisModel] = None
    markdown: Optional[str] = None
