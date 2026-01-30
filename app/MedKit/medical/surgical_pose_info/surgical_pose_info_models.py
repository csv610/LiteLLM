"""
Pydantic models for surgical position information structure.

This module defines the data models used to represent comprehensive surgical patient
positioning information with validation and structured schema generation.
"""

from pydantic import BaseModel, Field
from typing import Optional


class PoseBasicsModel(BaseModel):
    position_name: str = Field(description="Official name of the surgical position (e.g., Supine, Prone, Lithotomy)")
    alternative_names: str = Field(description="Other names or variations, comma-separated")
    category: str = Field(description="General category (e.g., Dorsal, Ventral, Lateral)")
    common_uses: str = Field(description="General types of surgery this position is used for, comma-separated")


class PoseIndicationsModel(BaseModel):
    primary_procedures: str = Field(description="Specific surgical procedures requiring this position, comma-separated")
    anatomical_access: str = Field(description="Anatomical areas exposed or accessible in this position")
    specialty_usage: str = Field(description="Medical specialties that frequently use this position (e.g., Urology, Gyn, Gen Surg)")


class PatientSetupModel(BaseModel):
    equipment_needed: str = Field(description="Required table attachments, supports, and positioning aids, comma-separated")
    step_by_step_placement: str = Field(description="Brief sequential steps to place the patient in this position")
    head_and_neck: str = Field(description="Positioning and protection of the head and neck (e.g., neutral alignment, eyes taped)")
    upper_extremities: str = Field(description="Positioning of arms (e.g., on armboards, tucked at sides) and constraints")
    lower_extremities: str = Field(description="Positioning of legs (e.g., in stirrups, straight, flexed)")
    padding_requirements: str = Field(description="Specific areas requiring padding to prevent pressure injuries")


class SafetyConsiderationsModel(BaseModel):
    pressure_points: str = Field(description="Key anatomical areas at risk for pressure ulcers (e.g., sacrum, heels, occiput)")
    nerve_risks: str = Field(description="Nerves at risk of injury due to stretch or compression (e.g., Brachial plexus, Ulnar, Peroneal)")
    prevention_strategies: str = Field(description="Specific actions to mitigate nerve and pressure injuries")
    check_points: str = Field(description="Critical safety checks to perform after positioning")


class PhysiologicalEffectsModel(BaseModel):
    respiratory_effects: str = Field(description="Impact on lung volume, diaphragm movement, and ventilation")
    cardiovascular_effects: str = Field(description="Impact on venous return, cardiac output, and blood pressure")
    other_physiological_changes: str = Field(description="Other systemic effects (e.g., intraocular pressure, intracranial pressure)")


class ContraindicationsAndModificationsModel(BaseModel):
    absolute_contraindications: str = Field(description="Conditions under which this position must NOT be used")
    relative_contraindications: str = Field(description="Conditions requiring caution or modification")
    modifications_for_obesity: str = Field(description="Adjustments needed for morbidly obese patients")
    modifications_for_pediatrics: str = Field(description="Adjustments needed for pediatric patients")
    modifications_for_elderly: str = Field(description="Adjustments needed for geriatric patients with limited mobility/fragile skin")


class PostOperativeCareModel(BaseModel):
    repositioning_care: str = Field(description="Care required when returning patient to neutral/supine position")
    monitoring_requirements: str = Field(description="Specific signs to monitor immediately after repositioning")


class SurgicalPoseInfoModel(BaseModel):
    pose_basics: PoseBasicsModel
    indications: PoseIndicationsModel
    patient_setup: PatientSetupModel
    safety_considerations: SafetyConsiderationsModel
    physiological_effects: PhysiologicalEffectsModel
    contraindications_and_modifications: ContraindicationsAndModificationsModel
    post_operative_care: PostOperativeCareModel


class ModelOutput(BaseModel):
    data: Optional[SurgicalPoseInfoModel] = None
    markdown: Optional[str] = None