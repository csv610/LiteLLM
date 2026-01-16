"""
similar_drugs_models.py - Pydantic Models for Similar Drugs Module

Defines data structures for similar medicine search and comparison results.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class SimilarityCategory(str, Enum):
    """Categories of similarity between medicines."""
    SAME_INGREDIENT = "Same Active Ingredient"
    SAME_THERAPEUTIC_CLASS = "Same Therapeutic Class"
    SIMILAR_MECHANISM = "Similar Mechanism of Action"


class EfficacyComparison(str, Enum):
    """Efficacy comparison relative to original drug."""
    LESS_EFFECTIVE = "Less Effective"
    SIMILAR_EFFICACY = "Similar Efficacy"
    MORE_EFFECTIVE = "More Effective"
    EFFICACY_VARIES = "Varies by Indication"


class SimilarMedicineDetail(BaseModel):
    """Detailed information about a similar medicine."""
    rank: int = Field(description="Ranking of similarity (1 being most similar)")
    medicine_name: str = Field(description="Name of the similar medicine")
    brand_names: Optional[str] = Field(
        default=None,
        description="Brand names or trade names, comma-separated"
    )
    active_ingredients: str = Field(
        description="Active pharmaceutical ingredients, comma-separated"
    )
    available_strengths: str = Field(
        description="Available dosage strengths, comma-separated"
    )
    available_forms: str = Field(
        description="Available pharmaceutical forms (tablet, capsule, liquid, etc.), comma-separated"
    )
    similarity_category: SimilarityCategory = Field(
        description="Category of similarity (same ingredient, class, or mechanism)"
    )
    similarity_score: float = Field(
        description="Similarity score (0-100) indicating how similar to original drug",
        ge=0,
        le=100
    )
    efficacy_comparison: EfficacyComparison = Field(
        description="How efficacy compares to original medicine"
    )
    onset_of_action: str = Field(
        description="How quickly the medicine starts working"
    )
    duration_of_effect: str = Field(
        description="How long the effects typically last"
    )
    common_side_effects: str = Field(
        description="Most commonly reported side effects, comma-separated"
    )
    typical_cost_range: str = Field(
        description="Typical cost range without insurance"
    )
    generic_available: bool = Field(
        description="Whether generic version is available"
    )
    key_advantages: str = Field(
        description="Key advantages compared to original drug, comma-separated"
    )
    key_disadvantages: str = Field(
        description="Key disadvantages compared to original drug, comma-separated"
    )
    when_to_prefer: str = Field(
        description="Clinical situations or patient types where this medicine might be preferred"
    )


class SimilarMedicinesCategory(BaseModel):
    """Grouped similar medicines by category."""
    category: SimilarityCategory = Field(description="Category of similarity")
    count: int = Field(description="Number of similar medicines in this category (from top 10-15)")
    medicines: list[SimilarMedicineDetail] = Field(
        description="List of similar medicines in this category (ranked by similarity)"
    )
    category_summary: str = Field(
        description="Summary of this category and its relevance"
    )


class SwitchingGuidance(BaseModel):
    """Guidance for switching from original medicine to alternative."""
    switching_considerations: str = Field(
        description="Important factors to consider when switching, comma-separated"
    )
    transition_recommendations: str = Field(
        description="How to transition from original to alternative medicine"
    )
    monitoring_during_switch: str = Field(
        description="What to monitor during transition, comma-separated"
    )
    contraindications_for_switch: str = Field(
        description="Situations where switching should be avoided or done carefully, comma-separated"
    )


class SimilarMedicinesResult(BaseModel):
    """
    Complete results of similar medicines search (top 10-15 alternatives).

    Provides alternatives organized by similarity category with detailed
    information for each alternative and switching guidance.
    """
    original_medicine: str = Field(description="Name of the original medicine being analyzed")
    original_active_ingredients: str = Field(
        description="Active ingredients in original medicine"
    )
    original_therapeutic_use: str = Field(
        description="Primary therapeutic indication of original medicine"
    )
    total_similar_medicines_found: int = Field(
        description="Total number of top similar medicines identified (10-15)"
    )
    categorized_results: list[SimilarMedicinesCategory] = Field(
        description="Similar medicines organized by similarity category, ranked by similarity score"
    )
    switching_guidance: SwitchingGuidance = Field(
        description="General guidance for switching medicines"
    )
    top_recommended: str = Field(
        description="Top 3 most recommended alternatives with brief rationale"
    )
    summary_analysis: str = Field(
        description="Overall analysis of top alternatives and key considerations"
    )
    clinical_notes: str = Field(
        description="Important clinical notes and evidence-based considerations for switching"
    )
