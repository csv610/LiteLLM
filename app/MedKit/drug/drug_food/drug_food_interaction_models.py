"""Pydantic models and enums for drug-food interaction analysis."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class FoodCategory(str, Enum):
    """Food and beverage categories for interaction analysis."""
    CITRUS_FRUITS = "Citrus Fruits"
    BERRIES_OTHER_FRUITS = "Berries & Other Fruits"
    DAIRY_CALCIUM = "Dairy & Calcium-rich Foods"
    HIGH_FAT_FOODS = "High-Fat Foods"
    LEAFY_GREENS = "Leafy Greens (Vitamin K)"
    ALCOHOL = "Alcohol"
    CAFFEINE = "Caffeine"
    HERBAL_SUPPLEMENTS = "Herbal Supplements & Teas"
    NUTS_SEEDS = "Nuts & Seeds"
    SPICES_SEASONINGS = "Spices & Seasonings"


class InteractionSeverity(str, Enum):
    """Severity levels for drug-food interactions."""
    NONE = "NONE"
    MINOR = "MINOR"
    MILD = "MILD"
    MODERATE = "MODERATE"
    SIGNIFICANT = "SIGNIFICANT"
    CONTRAINDICATED = "CONTRAINDICATED"


class ConfidenceLevel(str, Enum):
    """Confidence levels in interaction assessment."""
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"


class DataSourceType(str, Enum):
    """Types of data sources for interaction information."""
    CLINICAL_STUDIES = "Clinical Studies"
    PHARMACOKINETIC_ANALYSIS = "Pharmacokinetic Analysis"
    FDA_WARNINGS = "FDA Warnings"
    MANUFACTURER_DATA = "Manufacturer Data"
    AI_GENERATED = "AI-Generated"


class FoodCategoryInteractionModel(BaseModel):
    """Detailed interaction information for a specific food category."""
    category: FoodCategory = Field(description="Food category being analyzed")
    has_interaction: bool = Field(description="Whether an interaction exists with this food category")
    severity: InteractionSeverity = Field(
        description="Severity of interaction if present (NONE if no interaction)"
    )
    specific_foods: str = Field(
        description="Specific foods/beverages in this category that interact, comma-separated"
    )
    mechanism: Optional[str] = Field(
        default=None,
        description="How the food affects the medicine (absorption, metabolism, elimination)"
    )
    timing_recommendation: Optional[str] = Field(
        default=None,
        description="Recommended timing (e.g., 'take 2 hours before food', 'take with meals')"
    )


class DrugFoodInteractionDetailsModel(BaseModel):
    """Comprehensive drug-food interaction analysis."""
    medicine_name: str = Field(description="Name of the medicine")
    overall_severity: InteractionSeverity = Field(
        description="Overall severity considering all food interactions"
    )
    mechanism_of_interaction: str = Field(
        description="Detailed explanation of how food affects drug absorption, metabolism, or efficacy"
    )
    clinical_effects: str = Field(
        description="Observable clinical effects of food-drug interactions, comma-separated"
    )
    food_category_interactions: list[FoodCategoryInteraction] = Field(
        description="Detailed interactions for each food category"
    )
    management_recommendations: str = Field(
        description="Clinical recommendations for managing interactions (timing, food avoidance, monitoring), comma-separated"
    )
    foods_to_avoid: str = Field(
        description="Specific foods and beverages to avoid or limit, comma-separated"
    )
    foods_safe_to_consume: str = Field(
        description="Foods and beverages that are generally safe or beneficial, comma-separated"
    )
    confidence_level: ConfidenceLevel = Field(
        description="Confidence level in this interaction assessment (HIGH, MODERATE, LOW)"
    )
    data_source_type: DataSourceType = Field(
        description="Primary source of this interaction data"
    )
    references: Optional[str] = Field(
        default=None,
        description="Citations or references supporting this interaction data, comma-separated"
    )


class PatientFriendlySummaryModel(BaseModel):
    """Patient-friendly explanation of drug-food interactions."""
    simple_explanation: str = Field(
        description="Simple, non-technical explanation of how food affects this medicine"
    )
    what_patient_should_do: str = Field(
        description="Clear action steps for safe food and medicine use"
    )
    foods_to_avoid_simple: str = Field(
        description="Patient-friendly list of foods/drinks to avoid"
    )
    meal_timing_guidance: str = Field(
        description="Guidance on when to take medicine relative to meals"
    )
    warning_signs: str = Field(
        description="Symptoms indicating the interaction may be problematic, comma-separated"
    )


class DataAvailabilityInfoModel(BaseModel):
    """Information about data availability."""
    data_available: bool = Field(
        description="Whether food interaction data is available"
    )
    reason: Optional[str] = Field(
        default=None,
        description="Explanation if data is not available"
    )


class DrugFoodInteractionModel(BaseModel):
    """
    Comprehensive drug-food interaction analysis result.

    Combines clinical data, patient education, and detailed category information
    in a structured format for healthcare professionals and patients.
    """
    interaction_details: Optional[DrugFoodInteractionDetails] = Field(
        default=None,
        description="Detailed interaction information (None if data not available)"
    )
    technical_summary: str = Field(
        description="Technical summary of the interactions suitable for healthcare professionals"
    )
    patient_friendly_summary: Optional[PatientFriendlySummary] = Field(
        default=None,
        description="Patient-friendly explanation (None if no interactions)"
    )
    data_availability: DataAvailabilityInfo = Field(
        description="Status of data availability for this interaction check"
    )


class ModelOutput(BaseModel):
    data: Optional[DrugFoodInteractionModel] = None
    markdown: Optional[str] = None

