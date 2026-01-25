"""
Pydantic models for medical anatomy information.

This module contains all the structured data models used to represent
anatomical information in a standardized format.
"""

from pydantic import BaseModel, Field
from typing import Optional


class AnatomyOverviewModel(BaseModel):
    """Basic information about the anatomical structure."""
    structure_name: str = Field(description="Official anatomical name of the structure")
    common_names: str = Field(description="Common or alternative names, comma-separated")
    anatomical_classification: str = Field(description="Classification (bone, muscle, organ, vessel, nerve, etc)")
    body_system: str = Field(description="Primary body system this structure belongs to")
    embryological_origin: str = Field(description="Germ layer or embryological origin")
    prevalence_variation: str = Field(description="How common this structure is (universal, variable, or rare)")


class AnatomicalPositionModel(BaseModel):
    """Location and orientation of the structure."""
    anatomical_location: str = Field(description="Specific location in the body")
    body_regions: str = Field(description="Body regions or quadrants, comma-separated")
    surface_landmarks: str = Field(description="Palpable surface landmarks for identification")
    anatomical_planes: str = Field(description="Position relative to anatomical planes (anterior, posterior, medial, lateral, etc)")
    depth: str = Field(description="Depth in relation to skin surface (superficial, deep, etc)")
    relationships_to_other_structures: str = Field(description="How this structure relates to nearby structures, comma-separated")


class GrossMorphologyModel(BaseModel):
    """Structural form and external appearance."""
    shape_description: str = Field(description="Overall shape and form of the structure")
    dimensions: str = Field(description="Typical size measurements (length, width, diameter, volume)")
    color_and_appearance: str = Field(description="Gross appearance including color and texture")
    surface_features: str = Field(description="Notable surface features or markings")
    attachment_points: str = Field(description="Where structure attaches to other structures, comma-separated")
    borders_and_margins: str = Field(description="Description of borders and anatomical margins")


class MicroscopicStructureModel(BaseModel):
    """Histological and cellular composition."""
    tissue_type: str = Field(description="Primary tissue types present, comma-separated")
    cellular_components: str = Field(description="Types of cells found in structure, comma-separated")
    histological_layers: str = Field(description="Distinct histological layers if applicable")
    special_structures: str = Field(description="Special microscopic features or organelles, comma-separated")
    staining_characteristics: str = Field(description="Appearance under different histological stains")


class AnatomicalFunctionModel(BaseModel):
    """Functions and roles of the structure."""
    primary_functions: str = Field(description="Main functions of this structure, comma-separated")
    secondary_functions: str = Field(description="Secondary or supporting functions, comma-separated")
    mechanism_of_action: str = Field(description="How the structure performs its functions")
    functional_relationships: str = Field(description="Relationships with other structures for function, comma-separated")
    functional_significance: str = Field(description="Clinical importance of this structure's function")


class VascularInnervationModel(BaseModel):
    """Blood supply and nerve supply."""
    arterial_supply: str = Field(description="Major arteries supplying this structure")
    venous_drainage: str = Field(description="Major veins draining this structure")
    lymphatic_drainage: str = Field(description="Lymphatic drainage pathways if applicable")
    nerve_supply: str = Field(description="Cranial or spinal nerves innervating structure")
    nerve_types: str = Field(description="Types of innervation (somatic, autonomic, sensory, motor, etc)")
    dermatome_or_myotome: str = Field(description="Associated dermatome or myotome if applicable")


class VariationsAndAnomaliesModel(BaseModel):
    """Normal variations and developmental anomalies."""
    anatomical_variations: str = Field(description="Normal anatomical variations, comma-separated")
    variation_frequency: str = Field(description="How common variations are in population")
    congenital_anomalies: str = Field(description="Congenital anomalies if applicable, comma-separated")
    age_related_changes: str = Field(description="How structure changes with age")
    sex_differences: str = Field(description="Differences between males and females if applicable")
    ethnic_or_genetic_variants: str = Field(description="Variations across populations if applicable")


class ClinicalSignificanceModel(BaseModel):
    """Medical and clinical relevance."""
    clinical_importance: str = Field(description="Why this structure is clinically important")
    common_pathologies: str = Field(description="Common diseases affecting this structure, comma-separated")
    injury_vulnerability: str = Field(description="Susceptibility to injury and trauma")
    pain_and_referred_pain: str = Field(description="Pain patterns and referred pain associated with structure")
    diagnostic_palpation: str = Field(description="How structure is examined clinically")
    surgical_considerations: str = Field(description="Important considerations during surgery or procedures")


class ImagingCharacteristicsModel(BaseModel):
    """How structure appears on imaging studies."""
    radiographic_appearance: str = Field(description="Appearance on X-ray")
    ultrasound_appearance: str = Field(description="Appearance on ultrasound")
    ct_appearance: str = Field(description="Appearance on CT scan")
    mri_appearance: str = Field(description="Appearance on MRI")
    imaging_techniques: str = Field(description="Best imaging modalities for visualization, comma-separated")
    radiodensity_or_signal: str = Field(description="Radiodensity, signal intensity, or echogenicity")


class DevelopmentalAnatomyModel(BaseModel):
    """Growth and development of the structure."""
    embryological_development: str = Field(description="How structure develops embryologically")
    fetal_development: str = Field(description="Development stages during fetal period")
    postnatal_growth: str = Field(description="Growth and development after birth")
    maturation_timeline: str = Field(description="Timeline of when structure reaches maturity")
    growth_patterns: str = Field(description="Growth patterns or growth spurts if applicable")


class AnatomicalLandmarksAndApproachesModel(BaseModel):
    """Clinical landmarks and surgical approaches."""
    surface_landmarks: str = Field(description="Palpable landmarks for identification")
    surface_anatomy_techniques: str = Field(description="Techniques for identifying structure clinically")
    surgical_approaches: str = Field(description="Common surgical approaches to access structure, comma-separated")
    anatomical_borders: str = Field(description="Important anatomical borders for surgical approach")
    risk_structures: str = Field(description="Nearby structures at risk during surgical access, comma-separated")


class SeeAlsoModel(BaseModel):
    """Cross-references to related anatomical structures."""
    related_structures: str = Field(description="Related anatomical structures, comma-separated")
    connection_types: str = Field(description="Types of connections (adjacent, continuous, functionally related, innervated by, supplied by, etc), comma-separated")
    reason: str = Field(description="Brief explanation of how these structures relate to main structure")


class AnatomyMetadataModel(BaseModel):
    """Metadata and information structure."""
    last_updated: str = Field(description="When this information was last reviewed")
    information_sources: str = Field(description="Primary sources of information (anatomical textbooks, databases), comma-separated")
    confidence_level: str = Field(description="Confidence in provided information (high, medium, low)")
    complexity_level: str = Field(description="Complexity of topic (basic, intermediate, advanced)")


class MedicalAnatomyModel(BaseModel):
    """
    Comprehensive anatomical structure information.
    """
    # Basic identification
    overview: AnatomyOverviewModel

    # Location and positioning
    anatomical_position: AnatomicalPositionModel

    # Structure and form
    gross_morphology: GrossMorphologyModel
    microscopic_structure: MicroscopicStructureModel

    # Function and relationships
    anatomical_function: AnatomicalFunctionModel
    vascular_innervation: VascularInnervationModel

    # Variations and development
    variations_and_anomalies: VariationsAndAnomaliesModel
    developmental_anatomy: DevelopmentalAnatomyModel

    # Clinical aspects
    clinical_significance: ClinicalSignificanceModel
    imaging_characteristics: ImagingCharacteristicsModel
    anatomical_landmarks_and_approaches: AnatomicalLandmarksAndApproachesModel

    # Cross-references
    see_also: SeeAlsoModel

    # Metadata
    metadata: AnatomyMetadataModel


class ModelOutput(BaseModel):
    data: Optional[MedicalAnatomyModel] = None
    markdown: Optional[str] = None
