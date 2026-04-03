from typing import Any

"""Pydantic models for patient legal rights information structure.

Defines all the data models used for representing comprehensive legal information
including patient rights, provider responsibilities, legal basis, and recourse.
"""

from typing import Optional

from lite import ModelOutput


class LegalOverviewModel(BaseModel):
    """Overview of the legal topic."""

    topic_name: str = Field(description="Official name of the legal right or topic")
    legal_basis: str = Field(
        description="Primary laws, regulations, or ethical standards (e.g., HIPAA, EMTALA, State Law)"
    )
    primary_stakeholders: str = Field(
        description="The groups most affected by or responsible for this right (e.g., patients, hospitals, physicians)"
    )


class LegalDefinitionModel(BaseModel):
    """Definition and scope of the legal right."""

    legal_scope: str = Field(description="The extent and coverage of this legal right")
    key_definitions: str = Field(
        description="Essential legal and healthcare definitions for this topic"
    )


class HistoricalRegulatoryModel(BaseModel):
    """Historical and regulatory context."""

    historical_context: str = Field(
        description="The evolution of this legal right over time"
    )
    key_laws_and_regulations: str = Field(
        description="Specific statutes, regulations, and case laws governing this topic"
    )


class CoreRightsModel(BaseModel):
    """Detailed patient rights."""

    specific_patient_rights: str = Field(
        description="A detailed list of specific rights guaranteed to patients"
    )
    legal_protections: str = Field(
        description="The protections offered by law to ensure these rights are upheld"
    )


class ProviderResponsibilitiesModel(BaseModel):
    """Responsibilities of healthcare providers."""

    obligations_of_providers: str = Field(
        description="What healthcare providers must do to comply with this legal right"
    )
    compliance_requirements: str = Field(
        description="Standard practices and administrative requirements for providers"
    )


class ImplementationModel(BaseModel):
    """Practical implementation."""

    how_to_exercise_rights: str = Field(
        description="Step-by-step guidance for patients to exercise this right"
    )
    required_documentation: str = Field(
        description="Forms or documentation typically needed to exercise or waive this right"
    )


class LimitationsModel(BaseModel):
    """Exceptions and limitations."""

    exceptions: str = Field(
        description="Situations where this right may not apply or is modified"
    )
    legal_limitations: str = Field(
        description="Constraints on the scope of the legal right"
    )


class RecourseModel(BaseModel):
    """Dispute resolution and recourse."""

    dispute_resolution_mechanisms: str = Field(
        description="Internal and external ways to resolve conflicts (e.g., hospital grievance committee, OCR complaint)"
    )
    legal_remedies: str = Field(
        description="Available legal actions or remedies if rights are violated"
    )


class TerminologyModel(BaseModel):
    """Key legal terminology."""

    key_legal_terms: str = Field(
        description="Glossary of essential legal terms for this topic"
    )


class RelatedConceptsModel(BaseModel):
    """Related legal concepts."""

    related_legal_concepts: str = Field(
        description="Other legal or ethical topics that overlap with this right"
    )


class FuturePerspectivesModel(BaseModel):
    """Current trends and future outlook."""

    current_legal_trends: str = Field(
        description="Ongoing changes or emerging issues related to this right"
    )
    future_perspectives: str = Field(
        description="Potential future developments in legislation or interpretation"
    )


class LegalRightsModel(BaseModel):
    """
    Comprehensive information on a patient's legal right.
    """

    overview: LegalOverviewModel
    definition: LegalDefinitionModel
    history: HistoricalRegulatoryModel
    core_rights: CoreRightsModel
    responsibilities: ProviderResponsibilitiesModel
    implementation: ImplementationModel
    limitations: LimitationsModel
    recourse: RecourseModel
    terminology: TerminologyModel
    related_concepts: RelatedConceptsModel
    future_perspectives: FuturePerspectivesModel
