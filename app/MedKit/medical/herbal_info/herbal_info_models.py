"""
Pydantic models for herbal information structure.
"""

from pydantic import BaseModel, Field
from typing import Optional


class HerbalMetadataModel(BaseModel):
    """Basic information about the herbal remedy."""
    common_name: str = Field(description="Common name of the herb")
    botanical_name: str = Field(description="Scientific/botanical name (Latin nomenclature)")
    other_names: str = Field(description="Alternative common names and local names, comma-separated")
    plant_family: str = Field(description="Plant family classification (e.g., Asteraceae, Lamiaceae)")
    active_constituents: str = Field(description="Primary active compounds and phytochemicals, comma-separated")
    forms_available: str = Field(description="Available herbal forms (dried leaf, extract, tincture, essential oil, capsule, tea, etc.), comma-separated")


class HerbalClassificationModel(BaseModel):
    """Classification and traditional use categories."""
    traditional_system: str = Field(description="Traditional medicine systems (Ayurveda, Traditional Chinese Medicine, Western Herbalism, etc.), comma-separated")
    primary_uses: str = Field(description="Primary traditional and contemporary uses, comma-separated")
    energetics: str = Field(description="Traditional energetic properties (warming, cooling, drying, moistening, etc.)")
    taste_profile: str = Field(description="Traditional taste attributes (bitter, sweet, pungent, etc.)")


class HerbalBackgroundModel(BaseModel):
    """Historical and botanical information."""
    origin_and_habitat: str = Field(description="Geographic origin and natural growing regions")
    history_and_traditional_use: str = Field(description="Historical use patterns and cultural significance across different traditions")
    botanical_description: str = Field(description="Physical characteristics of the plant including appearance, growth patterns, and harvesting information")


class HerbalMechanismModel(BaseModel):
    """How the herb works in the body."""
    mechanism_of_action: str = Field(description="Proposed biochemical mechanisms of how the herb exerts therapeutic effects")
    active_constituents_effects: str = Field(description="Specific effects of identified active compounds, comma-separated")
    body_systems_affected: str = Field(description="Primary body systems and organs targeted (nervous, digestive, immune, etc.), comma-separated")


class DosageModel(BaseModel):
    """Age-specific dosing recommendations."""
    children_dosage: str = Field(description="Dosage for children, often adjusted by age or weight, comma-separated")
    adult_dosage: str = Field(description="Standard dosage for adult use, comma-separated")
    elderly_dosage: str = Field(description="Dosage considerations for elderly or sensitive individuals, comma-separated")


class AdministrationGuidanceModel(BaseModel):
    """Instructions for different forms of administration."""
    tea_infusion: Optional[str] = Field(default=None, description="Instructions for preparing tea: steeping time, water temperature, frequency")
    tincture: Optional[str] = Field(default=None, description="Instructions for tincture use: dilution, dosing, frequency")
    extract: Optional[str] = Field(default=None, description="Instructions for extract or concentrated forms: measuring, mixing, timing")
    topical: Optional[str] = Field(default=None, description="Instructions for external application: preparation, application method, frequency")
    culinary_use: Optional[str] = Field(default=None, description="Instructions for culinary applications and food preparation")


class UsageAndAdministrationModel(BaseModel):
    """Dosing and administration information."""
    suitable_conditions: str = Field(description="Health conditions and situations where this herb is traditionally used")
    preparation_methods: str = Field(description="Common preparation techniques and which forms work best")
    age_specific_dosage: DosageModel
    administration_guidance: AdministrationGuidanceModel
    storage_instruction: str = Field(description="Storage requirements, temperature ranges, shelf life, and preservation methods")
    quality_indicators: str = Field(description="What to look for in high-quality herbal products, comma-separated")


class HerbalInteractionsModel(BaseModel):
    """Herb and substance interactions."""
    drug_interactions: str = Field(description="Known interactions with pharmaceutical medications, comma-separated")
    herb_interactions: str = Field(description="Interactions with other herbs and supplements, comma-separated")
    food_interactions: str = Field(description="Known interactions with specific foods, comma-separated")
    caffeine_interactions: str = Field(description="Effects of combining with caffeine or stimulants")
    alcohol_interactions: str = Field(description="Effects of combining with alcohol")


class SafetyInformationModel(BaseModel):
    """Safety, side effects, and warnings."""
    common_side_effects: str = Field(description="Mild, temporary effects sometimes experienced, comma-separated")
    serious_adverse_effects: str = Field(description="Rare but serious adverse effects to be aware of, comma-separated")
    interactions: HerbalInteractionsModel
    contraindications: str = Field(description="Conditions or situations where herb should be avoided, comma-separated")
    precautions: str = Field(description="Special precautions for specific populations or conditions, comma-separated")
    toxicity_concerns: Optional[str] = Field(default=None, description="Any known toxicity issues or overdose concerns")


class SpecialInstructionsModel(BaseModel):
    """Special situation guidance."""
    discontinuation_guidance: str = Field(description="How to safely stop using the herb and any withdrawal considerations")
    overdose_information: str = Field(description="Symptoms and management if excessive amounts are consumed")
    quality_concerns: str = Field(description="Potential adulterants, contamination risks, and how to verify authenticity")


class SpecialPopulationsModel(BaseModel):
    """Considerations for special populations."""
    pregnancy_use: str = Field(description="Safety and traditional use during pregnancy")
    breastfeeding_use: str = Field(description="Safety and traditional use while breastfeeding")
    pediatric_use: str = Field(description="Age-appropriate use and special considerations for pediatric use")
    kidney_disease_considerations: Optional[str] = Field(default=None, description="Considerations for patients with kidney dysfunction")
    liver_disease_considerations: Optional[str] = Field(default=None, description="Considerations for patients with liver dysfunction")


class EfficacyModel(BaseModel):
    """Effectiveness and clinical outcomes."""
    traditional_efficacy_claims: str = Field(description="Traditional effectiveness claims and cultural evidence")
    clinical_evidence: str = Field(description="Summary of scientific studies and clinical trial findings")
    onset_of_action: str = Field(description="Expected timeframe for noticing effects")
    duration_of_effect: str = Field(description="How long effects typically last")
    expected_outcomes: str = Field(description="Expected health improvements and benefits, comma-separated")


class AlternativesModel(BaseModel):
    """Alternative treatment options."""
    similar_herbs: str = Field(description="Other herbs with similar uses and properties, comma-separated")
    complementary_herbs: str = Field(description="Herbs commonly combined with this one, comma-separated")
    non_herbal_alternatives: str = Field(description="Non-herbal treatment alternatives, comma-separated")
    when_to_seek_conventional_care: str = Field(description="Situations where conventional medical care should be prioritized")


class HerbalEducationModel(BaseModel):
    """Patient education content."""
    plain_language_explanation: str = Field(description="Simple explanation of what this herb does and how it works")
    key_takeaways: str = Field(description="3-5 most important points about using this herb safely and effectively, comma-separated")
    common_misconceptions: str = Field(description="Common myths or misunderstandings about this herb, comma-separated")
    sustainability_notes: str = Field(description="Information about sustainable harvesting and conservation status if relevant")


class CostAndAvailabilityModel(BaseModel):
    """Financial and availability information."""
    typical_cost_range: str = Field(description="General cost range for quality products")
    availability: str = Field(description="Regulatory status and availability by region (OTC, dietary supplement, etc.)")
    quality_considerations: str = Field(description="How to identify quality products and reputable sources")
    organic_availability: str = Field(description="Whether organic versions are available and cost differences")
    sourcing_information: str = Field(description="Information about ethical sourcing and fair trade options")


class HerbalEvidenceModel(BaseModel):
    """Evidence-based information."""
    evidence_level: str = Field(description="Quality of scientific evidence (well-established, traditional use only, emerging research, etc.)")
    clinical_studies: str = Field(description="Summary of major scientific studies and research findings")
    regulatory_status: str = Field(description="Regulatory approval status in different countries and FDA classification if applicable")


class HerbalResearchModel(BaseModel):
    """Current research and innovations."""
    recent_research: str = Field(description="Recent scientific studies and findings, comma-separated")
    ongoing_studies: str = Field(description="Current clinical trials and research areas, comma-separated")
    future_applications: str = Field(description="Potential future uses and research directions, comma-separated")


class HerbalInfoModel(BaseModel):
    """
    Comprehensive herbal remedy information.
    """
    # Core identification
    metadata: HerbalMetadataModel

    # Classification and background
    classification: HerbalClassificationModel
    background: HerbalBackgroundModel

    # Mechanism and chemistry
    mechanism: HerbalMechanismModel

    # Usage and administration
    usage_and_administration: UsageAndAdministrationModel

    # Safety and interactions
    safety: SafetyInformationModel
    special_instructions: SpecialInstructionsModel

    # Specific populations
    special_populations: SpecialPopulationsModel

    # Efficacy and alternatives
    efficacy: EfficacyModel
    alternatives: AlternativesModel

    # Patient communication
    education: HerbalEducationModel

    # Financial and availability
    cost_and_availability: CostAndAvailabilityModel

    # Evidence-based information
    evidence: HerbalEvidenceModel

    # Research and innovation
    research: HerbalResearchModel


class ModelOutput(BaseModel):
    data: Optional[HerbalInfoModel] = None
    markdown: Optional[str] = None
