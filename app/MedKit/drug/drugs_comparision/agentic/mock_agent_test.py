import logging
from unittest.mock import MagicMock, patch
from drugs_comparison import DrugsComparison, DrugsComparisonInput
from drugs_comparison_models import (
    MedicinesComparisonResult, ClinicalMetrics, RegulatoryMetrics, 
    PracticalMetrics, ComplianceMetrics, ComparisonSummary, RecommendationContext,
    SafetyAudit, EffectivenessRating, SafetyRating, AvailabilityStatus
)
from lite.config import ModelConfig

# Configure logging to see the agent flow
logging.basicConfig(level=logging.DEBUG)

def mock_ask_llm(model_input):
    system_prompt = model_input.system_prompt
    
    if "pharmacology expert" in system_prompt:
        return "PHARMACOLOGY REPORT: Ibuprofen is an NSAID. Acetaminophen is an antipyretic/analgesic. Ibuprofen has higher GI risk."
    
    elif "regulatory expert" in system_prompt:
        return "REGULATORY REPORT: Both are FDA approved and available OTC. Patents expired decades ago."
    
    elif "market access specialist" in system_prompt:
        return "MARKET ACCESS REPORT: Both are very affordable (<$10 for bottle). Widely available in pharmacies and grocery stores."
    
    elif "clinical practitioner" in system_prompt:
        return "CLINICAL CONTEXT REPORT: Ibuprofen better for inflammation. Acetaminophen safer for elderly and those with kidney issues."
    
    elif "compliance and patient safety" in system_prompt:
        return "COMPLIANCE REPORT: Both are non-controlled. No major prescribing restrictions. High adherence for both as they are OTC."
    
    elif "Senior Medical Safety Auditor" in system_prompt:
        return "SAFETY AUDIT: Black box warnings verified for both. Pharmacology cites FDA Label 2023. Regulatory cites FDA approval database. Evidence quality: High."
    
    elif "senior medical editor" in system_prompt:
        # Return a structured result for the synthesis agent
        return MedicinesComparisonResult(
            medicine1_clinical=ClinicalMetrics(
                medicine_name="Ibuprofen",
                effectiveness_rating=EffectivenessRating.HIGH,
                efficacy_rate="85%",
                onset_of_action="30-60 mins",
                duration_of_effect="4-6 hours",
                safety_rating=SafetyRating.MODERATE_RISK,
                common_side_effects="Stomach upset",
                serious_side_effects="GI bleeding",
                contraindications="NSAID allergy, ulcers"
            ),
            medicine2_clinical=ClinicalMetrics(
                medicine_name="Acetaminophen",
                effectiveness_rating=EffectivenessRating.HIGH,
                efficacy_rate="80%",
                onset_of_action="30-60 mins",
                duration_of_effect="4-6 hours",
                safety_rating=SafetyRating.LOW_RISK,
                common_side_effects="Nausea",
                serious_side_effects="Liver toxicity",
                contraindications="Severe liver disease"
            ),
            medicine1_regulatory=RegulatoryMetrics(
                medicine_name="Ibuprofen",
                fda_approval_status="Approved",
                approval_date="1974",
                approval_type="Standard",
                has_black_box_warning=True,
                fda_alerts="CV risk",
                generic_available=True
            ),
            medicine2_regulatory=RegulatoryMetrics(
                medicine_name="Acetaminophen",
                fda_approval_status="Approved",
                approval_date="1955",
                approval_type="Standard",
                has_black_box_warning=False,
                fda_alerts="Liver warning",
                generic_available=True
            ),
            medicine1_practical=PracticalMetrics(
                medicine_name="Ibuprofen",
                availability_status=AvailabilityStatus.OVER_THE_COUNTER,
                typical_cost_range="$5-15",
                insurance_coverage="Standard",
                available_formulations="Tablet, Gel, Liquid",
                dosage_strengths="200mg, 400mg",
                patient_assistance_programs="N/A"
            ),
            medicine2_practical=PracticalMetrics(
                medicine_name="Acetaminophen",
                availability_status=AvailabilityStatus.OVER_THE_COUNTER,
                typical_cost_range="$5-15",
                insurance_coverage="Standard",
                available_formulations="Tablet, Liquid",
                dosage_strengths="325mg, 500mg",
                patient_assistance_programs="N/A"
            ),
            medicine1_compliance=ComplianceMetrics(
                medicine_name="Ibuprofen",
                controlled_substance_schedule="Non-controlled",
                prescribing_restrictions="None (OTC)",
                monitoring_requirements="Renal function for long-term use",
                patient_adherence_risk="Low",
                guideline_alignment="First-line for inflammatory pain"
            ),
            medicine2_compliance=ComplianceMetrics(
                medicine_name="Acetaminophen",
                controlled_substance_schedule="Non-controlled",
                prescribing_restrictions="None (OTC)",
                monitoring_requirements="None (Routine)",
                patient_adherence_risk="Low",
                guideline_alignment="First-line for mild-to-moderate pain"
            ),
            comparison_summary=ComparisonSummary(
                more_effective="Context dependent",
                safer_option="Acetaminophen (lower GI risk)",
                more_affordable="Equivalent",
                easier_access="Equivalent",
                key_differences="Anti-inflammatory properties, GI vs Liver risk profile"
            ),
            recommendations=RecommendationContext(
                for_acute_conditions="Both effective",
                for_elderly_patients="Acetaminophen preferred",
                overall_recommendation="Use Ibuprofen for inflammation, Acetaminophen for simple pain/fever."
            ),
            safety_audit=SafetyAudit(
                black_box_warning_verified=True,
                evidence_citations="FDA Label 2023, DailyMed Ibuprofen, FDA Acetaminophen Consumer Guide",
                recommendation_safety_level="Conservative"
            ),
            narrative_analysis="Synthesized analysis of 6 specialist reports audited for safety...",
            evidence_quality="High",
            limitations="General OTC guidance only"
        )
    
    return "Unknown agent"

def run_mock_test():
    print("\n--- Starting Mock Multi-Agent Test ---\n")
    
    model_config = ModelConfig(model="mock-model")
    analyzer = DrugsComparison(model_config)
    
    # Patch the internal _ask_llm method
    with patch.object(DrugsComparison, '_ask_llm', side_effect=mock_ask_llm):
        config = DrugsComparisonInput(
            medicine1="Ibuprofen",
            medicine2="Acetaminophen",
            use_case="General Pain",
            patient_age=65
        )
        
        result = analyzer.generate_text(config, structured=True)
        
        print("\n--- Final Synthesized Result ---")
        print(f"Medicine 1: {result.medicine1_clinical.medicine_name}")
        print(f"Medicine 2: {result.medicine2_clinical.medicine_name}")
        print(f"Summary: {result.comparison_summary.key_differences}")
        print(f"Recommendation for Elderly: {result.recommendations.for_elderly_patients}")
        print("\nTest completed successfully!")

if __name__ == "__main__":
    run_mock_test()
