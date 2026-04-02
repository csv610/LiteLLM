from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SpecialityRoleInfo(BaseModel):
    """Information about a medical speciality's role."""
    speciality_name: str = Field(description="The name of the medical speciality.")
    primary_focus: str = Field(description="The body systems or conditions the speciality focuses on.")
    key_responsibilities: List[str] = Field(description="What the specialist generally does (diagnose, treat, manage).")
    common_procedures: List[str] = Field(description="Examples of procedures or tests they perform.")


class ComplianceReviewModel(BaseModel):
    """Compliance and regulatory review results."""
    is_compliant: bool = Field(description="Whether the content meets medical compliance standards")
    issues_found: List[str] = Field(description="List of compliance or safety issues identified")
    required_disclaimers: List[str] = Field(description="Mandatory disclaimers to include")
    suggested_edits: Optional[str] = Field(default=None, description="Suggested edits for compliance")


class MedicalSpecialityRolesModel(BaseModel):
    """Complete package for medical speciality roles."""
    speciality_name: str = Field(description="Medical speciality name")
    roles_info: SpecialityRoleInfo = Field(description="Roles and responsibilities info")
    compliance_review: Optional[ComplianceReviewModel] = Field(
        default=None, description="Final compliance and safety review"
    )


class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)
