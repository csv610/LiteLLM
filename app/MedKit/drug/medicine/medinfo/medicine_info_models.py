"""
medicine_info_models.py - Pydantic Models for Medicine Information

Defines all data models used for generating and validating comprehensive
pharmaceutical medicine information.
"""

from pydantic import BaseModel, Field
from typing import Optional


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class MedicineGeneralInformation(BaseModel):
    """Basic information about the medicine."""
    generic_name: str = Field(description="Generic name of the medicine")
    brand_names: str = Field(description="Brand names or trade names, comma-separated")
    active_ingredients: str = Field(description="Active pharmaceutical ingredients, comma-separated")
    common_strengths: str = Field(description="Available dosage strengths, comma-separated")
    forms_available: str = Field(description="Available pharmaceutical forms (tablet, capsule, liquid, injection, topical, etc.), comma-separated")


class TherapeuticClassification(BaseModel):
    """Classification of the medicine."""
    therapeutic_class: str = Field(description="Primary therapeutic class (e.g., Antivirals, Antihypertensives, Beta-blockers)")
    pharmacological_class: str = Field(description="Pharmacological class based on mechanism (e.g., ACE inhibitors, SSRIs, NSAIDs)")
    chemical_class: str = Field(description="Chemical classification based on structure (e.g., Benzimidazoles, Penicillins, Quinolones)")


class MedicineBackground(BaseModel):
    """Historical and mechanistic information."""
    mechanism_of_action: str = Field(description="How the medicine works at cellular/molecular level")
    history_of_medicine: str = Field(description="Historical development and approval of the medicine")


class Dosage(BaseModel):
    """Age-specific dosing recommendations."""
    pediatric_dosage: str = Field(description="Dosage for children/infants, often age or weight-based, comma-separated")
    adult_dosage: str = Field(description="Standard dosage for adult patients, comma-separated")
    geriatric_dosage: str = Field(description="Dosage for elderly patients, often requiring adjustments, comma-separated")


class AdministrationGuidance(BaseModel):
    """Instructions for different forms of administration."""
    liquid_oral_suspension: Optional[str] = Field(description="Instructions for liquid forms: shaking, measuring, storage after opening")
    tablet_capsule: Optional[str] = Field(description="Instructions for solid forms: swallowing, crushing, timing with food")
    injectable: Optional[str] = Field(description="Instructions for injections: preparation, route, handling")
    topical: Optional[str] = Field(description="Instructions for topical application: technique, coverage, frequency")


class UsageAndAdministration(BaseModel):
    """Dosing and administration information."""
    patient_suitability: str = Field(description="Appropriate patient types and conditions for which this medicine is suitable")
    dosage_and_administration: str = Field(description="General dosing guidelines and administration frequency")
    age_specific_dosage: Dosage
    administration_guidance: AdministrationGuidance
    storage_instruction: str = Field(description="Storage requirements, temperature ranges, and shelf life")


class DrugInteractions(BaseModel):
    """Drug and substance interactions."""
    drug_interactions: str = Field(description="Clinically significant interactions with other medicines, comma-separated")
    supplement_interactions: str = Field(description="Interactions with herbal supplements and remedies, comma-separated")
    food_interactions: str = Field(description="Known interactions with specific foods or beverages, comma-separated")
    alcohol_interactions: str = Field(description="Effects of alcohol consumption with this medicine")


class SafetyInformation(BaseModel):
    """Safety, side effects, and warnings."""
    boxed_warning: Optional[str] = Field(description="FDA black box warning if applicable")
    common_side_effects: str = Field(description="Temporary side effects commonly experienced, comma-separated")
    serious_side_effects: str = Field(description="Rare but serious adverse effects requiring immediate medical attention, comma-separated")
    interactions: DrugInteractions
    contraindications: str = Field(description="Conditions or situations where medicine should not be used, comma-separated")
    precautions: str = Field(description="Special precautions and warnings for specific patient groups, comma-separated")


class SpecialInstructions(BaseModel):
    """Special situation guidance."""
    missing_dose: str = Field(description="What to do if a dose is missed")
    overdose: str = Field(description="Symptoms and management of overdose")
    expired_medicine: str = Field(description="Effects and risks of using expired medicine")


class SpecialPopulations(BaseModel):
    """Considerations for special populations."""
    pregnancy: str = Field(description="Safety and effects during pregnancy, including FDA pregnancy category")
    breastfeeding: str = Field(description="Transfer to breast milk and safety while breastfeeding")
    renal_impairment: Optional[str] = Field(description="Dosage adjustments needed for patients with kidney disease")
    hepatic_impairment: Optional[str] = Field(description="Dosage adjustments needed for patients with liver disease")


class Efficacy(BaseModel):
    """Effectiveness and clinical outcomes."""
    efficacy_rates: str = Field(description="Clinical effectiveness or success rates from studies")
    onset_of_action: str = Field(description="How long it takes for the medicine to start working")
    duration_of_effect: str = Field(description="How long the effects typically last")
    therapeutic_outcomes: str = Field(description="Expected health improvements and symptom relief, comma-separated")


class Alternatives(BaseModel):
    """Alternative treatment options."""
    alternative_medicines: str = Field(description="Other medicines used for similar conditions, comma-separated")
    non_pharmacological_options: str = Field(description="Non-medication treatment alternatives, comma-separated")
    advantages_over_alternatives: str = Field(description="Why this medicine may be preferred, comma-separated")
    better_alternatives: Optional[str] = Field(description="Superior or more effective replacement medicines with reasons why they are better, comma-separated")


class MedicineEducation(BaseModel):
    """Patient education content."""
    plain_language_explanation: str = Field(description="Simple explanation of what this medicine does")
    key_takeaways: str = Field(description="3-5 most important points about the medicine, comma-separated")
    common_misconceptions: str = Field(description="Common myths or misunderstandings about this medicine, comma-separated")


class CostAndAvailability(BaseModel):
    """Financial and availability information."""
    typical_cost_range: str = Field(description="General cost range without insurance")
    insurance_coverage: str = Field(description="How typically covered by insurance")
    availability: str = Field(description="Prescription status (OTC, Rx, controlled substance) and availability by region")
    generic_availability: str = Field(description="Whether generic versions are available and relative costs")
    patient_assistance_programs: str = Field(description="Manufacturer assistance programs or discounts available, comma-separated")
    ban_status: Optional[str] = Field(description="Countries or regions where the medicine is banned or restricted, if applicable")


class MedicineEvidence(BaseModel):
    """Evidence-based information."""
    evidence_level: str = Field(description="Quality of evidence supporting this medicine (high, moderate, low)")
    clinical_studies: str = Field(description="Summary of major clinical trials and research findings")
    fda_approval_status: str = Field(description="FDA approval status and indication approved")
    approval_dates: Optional[str] = Field(description="FDA and other regulatory approval dates (e.g., FDA approval date, EMA approval date, WHO approval date), comma-separated")


class MedicineResearch(BaseModel):
    """Current research and innovations."""
    recent_advancements: str = Field(description="Recent developments in formulation or delivery, comma-separated")
    ongoing_research: str = Field(description="Current clinical trials or research areas, comma-separated")
    future_developments: str = Field(description="Potential future improvements or new formulations, comma-separated")


class MedicineInfoModel(BaseModel):
    """
    Comprehensive pharmaceutical medicine information.

    Organized as a collection of BaseModel sections, each representing
    a distinct aspect of medicine documentation.
    """
    # Core identification
    general_information: MedicineGeneralInformation

    # Classification and background
    classification: TherapeuticClassification
    background: MedicineBackground

    # Usage and administration
    usage_and_administration: UsageAndAdministration

    # Safety and interactions
    safety: SafetyInformation
    special_instructions: SpecialInstructions

    # Specific populations
    special_populations: SpecialPopulations

    # Efficacy and alternatives
    efficacy: Efficacy
    alternatives: Alternatives

    # Patient communication
    education: MedicineEducation

    # Financial and availability
    cost_and_availability: CostAndAvailability

    # Evidence-based information
    evidence: MedicineEvidence

    # Research and innovation
    research: MedicineResearch


class ModelOutput(BaseModel):
    data: Optional[MedicineInfoModel] = None
    markdown: Optional[str] = None

