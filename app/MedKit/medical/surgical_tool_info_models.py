"""
Pydantic models for surgical tool information structure.

This module defines the data models used to represent comprehensive surgical tool
and instrument information with validation and structured schema generation.
"""

from pydantic import BaseModel, Field
from typing import Optional


class ToolBasics(BaseModel):
    tool_name: str = Field(description="Official name of the surgical tool")
    alternative_names: str = Field(description="Other names or abbreviations for this tool, comma-separated")
    tool_category: str = Field(description="Category (cutting, grasping, retracting, cautery, etc)")
    surgical_specialties: str = Field(description="Medical specialties that use this tool, comma-separated")
    instrument_family: str = Field(description="Family or group this tool belongs to (e.g., scissor family, clamp family)")


class ToolPurpose(BaseModel):
    primary_purpose: str = Field(description="Main function of this surgical tool")
    surgical_applications: str = Field(description="Specific surgical procedures where this tool is used, comma-separated")
    anatomical_targets: str = Field(description="Anatomical structures this tool is typically used on, comma-separated")
    tissue_types: str = Field(description="Types of tissue this tool is designed to work with (soft tissue, bone, vascular), comma-separated")
    unique_advantages: str = Field(description="What makes this tool superior to alternatives for its intended use, comma-separated")


class PhysicalSpecifications(BaseModel):
    dimensions: str = Field(description="Overall length and dimensions with specific measurements in cm or inches")
    weight: str = Field(description="Tool weight if relevant with specific values in grams or ounces")
    material_composition: str = Field(description="Materials used (stainless steel grades, titanium, tungsten carbide), comma-separated")
    finish_type: str = Field(description="Surface finish (polished, electropolished, serrated, textured)")
    blade_or_tip_specifications: str = Field(description="Specific details about working edge (blade angle, tip curvature, point geometry) with measurements")
    handle_design: str = Field(description="Handle characteristics (ergonomic curve, textured grip, material, weight distribution)")
    sterility_type: str = Field(description="Single-use or reusable, and sterilization method (autoclavable, ETO gas, etc)")


class OperationalCharacteristics(BaseModel):
    cutting_or_grasping_force: str = Field(description="Force specifications with numerical values if applicable")
    actuation_mechanism: str = Field(description="How the tool is activated (manual, mechanical, powered, articulated)")
    degrees_of_freedom: str = Field(description="Range of motion or articulation (fixed, single axis, multi-axis with specific angles)")
    precision_level: str = Field(description="Precision capability (gross, fine, micro-level) with specific measurements")
    engagement_depth: str = Field(description="Depth of cut, grasp, or working depth with specific values")
    working_distance: str = Field(description="Distance from tool tip to handle/body, optimal working distance from patient")


class SafetyFeatures(BaseModel):
    safety_mechanisms: str = Field(description="Built-in safety features (locks, guards, quick-release), comma-separated")
    slip_resistance: str = Field(description="Grip and handling safety features to prevent slipping")
    wear_considerations: str = Field(description="Signs of tool wear that indicate replacement need")
    maximum_safe_force: str = Field(description="Specifications on maximum force that should be applied without damage")
    emergency_protocols: str = Field(description="What to do if tool becomes stuck or breaks during use, comma-separated")
    tissue_damage_prevention: str = Field(description="Design features to minimize inadvertent tissue damage, comma-separated")


class PreOperativePreperation(BaseModel):
    inspection_requirements: str = Field(description="Pre-use inspection checklist (sharp test, functional test, damage check), comma-separated")
    cleaning_protocols: str = Field(description="How to properly clean before surgery with specific cleaning agents and duration")
    sterilization_requirements: str = Field(description="Sterilization method (autoclave temperature/time, chemical), specific parameters")
    quality_assurance_tests: str = Field(description="Tests to verify tool functionality before use, comma-separated")
    storage_requirements: str = Field(description="Proper storage conditions (temperature, humidity, protective cases)")
    preparation_time: str = Field(description="Time required for complete preparation and sterilization")


class IntraOperativeUse(BaseModel):
    positioning_in_field: str = Field(description="How tool is positioned relative to surgical field and anatomy")
    handling_technique: str = Field(description="Proper handling and technique for effective use")
    hand_position_requirements: str = Field(description="Specific hand grip and positioning for optimal control and visibility")
    coordination_with_other_tools: str = Field(description="How this tool is coordinated with other instruments, comma-separated")
    common_movements: str = Field(description="Typical motions performed with this tool during surgery (cutting angle, retraction direction, etc)")
    visibility_requirements: str = Field(description="Visual field needed to safely use this tool")
    ergonomic_considerations: str = Field(description="Ergonomic aspects of prolonged use (fatigue risk, repetitive strain prevention)")


class DiscomfortRisksAndComplications(BaseModel):
    surgeon_fatigue_factors: str = Field(description="Design aspects that might cause surgeon fatigue or strain with prolonged use")
    common_handling_errors: str = Field(description="Frequent mistakes surgeons make with this tool, comma-separated")
    tissue_damage_risks: str = Field(description="Potential unintended tissue damage (perforation, crushing, charring), comma-separated")
    instrument_complications: str = Field(description="Breakage, dulling, or malfunction risks, comma-separated")
    cross_contamination_risks: str = Field(description="Infection control concerns if not properly handled or sterilized")
    material_reactions: str = Field(description="Potential reactions with specific implants or materials in patient")
    electrical_safety: str = Field(description="For powered tools: electrical hazards, grounding, safety interlocks")


class MaintenanceAndCare(BaseModel):
    post_operative_cleaning: str = Field(description="Cleaning protocol after surgery with specific solutions and duration")
    lubrication_schedule: str = Field(description="When and with what lubricant to maintain tool function")
    inspection_frequency: str = Field(description="How often tool should be inspected with specific timeframes")
    wear_indicators: str = Field(description="Signs that tool needs replacement or sharpening, comma-separated")
    sharpening_protocol: str = Field(description="For cutting tools: sharpening method, frequency, specifications when sharp")
    repair_guidelines: str = Field(description="When tool can be repaired vs must be replaced")
    expected_lifespan: str = Field(description="Typical lifespan in number of uses or years with specific parameters")


class SterilizationAndDisinfection(BaseModel):
    approved_sterilization_methods: str = Field(description="Approved methods with temperature/pressure/time specifications, comma-separated")
    incompatible_sterilization: str = Field(description="Methods that should NOT be used and why, comma-separated")
    disinfection_alternatives: str = Field(description="If high-level disinfection acceptable, methods and conditions")
    packaging_requirements: str = Field(description="Packaging standards for sterilization (wrap type, labeling)")
    validation_standards: str = Field(description="Standards for validating sterilization (biological indicators, etc)")
    reprocessing_manufacturer_protocols: str = Field(description="Manufacturer-specific reprocessing guidelines to follow")


class AlternativesAndComparisons(BaseModel):
    similar_alternative_tools: str = Field(description="Other tools that serve similar function, comma-separated")
    advantages_over_alternatives: str = Field(description="Specific advantages of this tool compared to alternatives, comma-separated")
    disadvantages_vs_alternatives: str = Field(description="When alternatives might be preferred, comma-separated reasons")
    cost_comparison: str = Field(description="Relative cost compared to alternatives (if single-use, cost per use)")
    when_to_use_this_tool: str = Field(description="Specific clinical/anatomical scenarios where this tool is optimal")
    complementary_tools: str = Field(description="Tools often used alongside this one, comma-separated")


class HistoricalContext(BaseModel):
    invention_history: str = Field(description="History of tool development and key innovators")
    evolution_timeline: str = Field(description="Major design improvements over time with dates if applicable")
    clinical_evidence: str = Field(description="Key studies demonstrating effectiveness or safety")
    widespread_adoption: str = Field(description="When and why this tool became standard in practice")
    current_status: str = Field(description="Current role in modern surgery (standard, transitioning out, emerging)")


class SpecialtySpecificConsiderations(BaseModel):
    general_surgery_specific: str = Field(description="Specific uses and considerations in general surgery")
    orthopedic_specific: str = Field(description="Specific uses and considerations in orthopedic surgery")
    cardiac_specific: str = Field(description="Specific uses and considerations in cardiac surgery")
    neurosurgery_specific: str = Field(description="Specific uses and considerations in neurosurgery")
    vascular_specific: str = Field(description="Specific uses and considerations in vascular surgery")
    laparoscopic_considerations: str = Field(description="Modifications or special considerations for minimally invasive use")
    robotic_integration: str = Field(description="If applicable: use with robotic surgical systems")


class TrainingAndCertification(BaseModel):
    training_requirements: str = Field(description="Training needed to safely use this tool")
    proficiency_indicators: str = Field(description="Signs of mastery and competency with tool use, comma-separated")
    common_learning_mistakes: str = Field(description="Typical errors made during training period, comma-separated")
    skill_development_timeline: str = Field(description="Typical time to proficiency for experienced vs novice surgeons")
    formal_education_resources: str = Field(description="Textbooks, courses, or programs that teach this tool, comma-separated")
    mentoring_best_practices: str = Field(description="Best practices for teaching others to use this tool")


class RegulatoryAndStandards(BaseModel):
    fda_classification: str = Field(description="FDA classification (Class I, II, III) if applicable")
    fda_status: str = Field(description="FDA approval/clearance status with approval date if applicable")
    iso_standards: str = Field(description="Relevant ISO standards the tool must meet, comma-separated")
    country_approvals: str = Field(description="Countries where tool is approved for use")
    quality_certifications: str = Field(description="Quality and manufacturing certifications (ISO 13485, CE mark, etc)")
    traceability_requirements: str = Field(description="Labeling and tracking requirements for patient safety and recalls")


class CostAndProcurement(BaseModel):
    single_use_cost: Optional[str] = Field(description="Cost per use for single-use instruments")
    reusable_initial_cost: Optional[str] = Field(description="Initial purchase cost for reusable instruments")
    lifecycle_cost: str = Field(description="Total cost of ownership including maintenance, sterilization, replacement")
    vendor_options: str = Field(description="Major manufacturers and suppliers, comma-separated")
    procurement_lead_time: str = Field(description="Typical ordering and delivery timeframe")
    inventory_recommendations: str = Field(description="How many should be stocked based on usage")
    insurance_coverage: str = Field(description="Typical insurance/hospital coverage for this tool")


class EducationalContent(BaseModel):
    plain_language_explanation: str = Field(description="Simple explanation of what this tool does and why")
    key_takeaways: str = Field(description="3-5 most important points about this tool, comma-separated")
    common_misconceptions: str = Field(description="Common myths or misunderstandings about this tool, comma-separated")
    patient_communication: str = Field(description="How to explain use of this tool to patients seeking informed consent")
    video_demonstration_topics: str = Field(description="Key aspects that should be covered in training videos, comma-separated")


class SurgicalToolInfo(BaseModel):
    tool_basics: ToolBasics
    tool_purpose: ToolPurpose
    physical_specifications: PhysicalSpecifications
    operational_characteristics: OperationalCharacteristics
    safety_features: SafetyFeatures
    preparation: PreOperativePreperation
    intraoperative_use: IntraOperativeUse
    discomfort_risks_and_complications: DiscomfortRisksAndComplications
    maintenance_and_care: MaintenanceAndCare
    sterilization_and_disinfection: SterilizationAndDisinfection
    alternatives_and_comparisons: AlternativesAndComparisons
    historical_context: HistoricalContext
    specialty_specific_considerations: SpecialtySpecificConsiderations
    training_and_certification: TrainingAndCertification
    regulatory_and_standards: RegulatoryAndStandards
    cost_and_procurement: CostAndProcurement
    educational_content: EducationalContent
