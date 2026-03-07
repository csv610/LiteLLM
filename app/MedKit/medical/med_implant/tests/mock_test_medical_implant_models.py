import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from medical.med_implant.medical_implant_models import (
    ImplantMetadataModel,
    ImplantPurposeModel,
    MedicalImplantInfoModel,
)


def test_implant_metadata_model():
    data = {
        "implant_name": "Pacemaker",
        "alternative_names": "Cardiac Pacemaker, Pulse Generator",
        "implant_type": "cardiovascular",
        "medical_specialty": "Cardiology",
        "common_manufacturers": "Medtronic, Abbott, Boston Scientific",
    }
    model = ImplantMetadataModel(**data)
    assert model.implant_name == "Pacemaker"
    assert "Medtronic" in model.common_manufacturers


def test_implant_purpose_model():
    data = {
        "primary_purpose": "Regulate heart rhythm",
        "therapeutic_uses": "Bradycardia, Heart block",
        "functional_benefits": "Heart rate stabilization",
        "quality_of_life_improvements": "Increased energy, reduced dizziness",
    }
    model = ImplantPurposeModel(**data)
    assert model.primary_purpose == "Regulate heart rhythm"


def test_medical_implant_info_model():
    # Test complex nesting
    metadata = {
        "implant_name": "Pacemaker",
        "alternative_names": "test",
        "implant_type": "test",
        "medical_specialty": "test",
        "common_manufacturers": "test",
    }
    purpose = {
        "primary_purpose": "test",
        "therapeutic_uses": "test",
        "functional_benefits": "test",
        "quality_of_life_improvements": "test",
    }
    indications = {
        "when_recommended": "test",
        "conditions_treated": "test",
        "symptom_relief": "test",
        "contraindications": "test",
        "age_considerations": "test",
    }
    materials = {
        "primary_materials": "test",
        "material_properties": "test",
        "biocompatibility": "test",
        "allergic_considerations": "test",
        "corrosion_resistance": "test",
    }
    installation = {
        "surgical_approach": "test",
        "surgical_steps": "test",
        "anesthesia_type": "test",
        "procedure_duration": "test",
        "hospital_requirements": "test",
        "recovery_location": "test",
        "hospitalization_duration": "test",
    }
    functionality = {
        "how_it_works": "test",
        "expected_performance": "test",
        "adjustment_requirements": "test",
        "lifespan": "test",
        "failure_modes": "test",
    }
    recovery = {
        "immediate_recovery": "test",
        "healing_timeline": "test",
        "pain_management": "test",
        "activity_restrictions": "test",
        "return_to_normal_activities": "test",
        "wound_care": "test",
        "warning_signs": "test",
    }
    outcomes = {
        "success_rate": "test",
        "functional_outcomes": "test",
        "pain_relief": "test",
        "mobility_improvement": "test",
        "longevity_data": "test",
        "patient_satisfaction": "test",
        "factors_affecting_outcomes": "test",
    }
    complications = {
        "infection_risk": "test",
        "rejection_risk": "test",
        "mechanical_failure": "test",
        "common_complications": "test",
        "serious_complications": "test",
        "revision_rates": "test",
        "mortality_risk": "test",
    }
    imaging = {
        "mri_compatibility": "test",
        "ct_imaging": "test",
        "x_ray_considerations": "test",
        "monitoring_frequency": "test",
        "diagnostic_tests": "test",
        "remote_monitoring": "test",
    }
    activity_restrictions = {
        "permanent_restrictions": "test",
        "temporary_restrictions": "test",
        "sports_and_exercise": "test",
        "lifting_and_weight_bearing": "test",
        "occupational_considerations": "test",
        "travel_considerations": "test",
    }
    maintenance = {
        "daily_care": "test",
        "periodic_inspections": "test",
        "battery_replacement": "test",
        "component_replacement": "test",
        "maintenance_costs": "test",
        "long_term_management": "test",
    }
    follow_up = {
        "follow_up_schedule": "test",
        "post_operative_visits": "test",
        "long_term_monitoring": "test",
        "provider_specialists": "test",
        "medications_after": "test",
        "complications_monitoring": "test",
    }
    alternatives = {
        "alternative_implants": "test",
        "non_implant_alternatives": "test",
        "advantages_over_alternatives": "test",
        "when_alternatives_preferred": "test",
    }
    limitations = {
        "not_suitable_for": "test",
        "anatomical_limitations": "test",
        "health_condition_limitations": "test",
        "age_limitations": "test",
    }
    evidence = {
        "evidence_summary": "test",
        "clinical_trials": "test",
        "implant_limitations": limitations,
    }
    cost_and_insurance = {
        "implant_cost": "test",
        "surgical_costs": "test",
        "total_cost_range": "test",
        "insurance_coverage": "test",
        "prior_authorization": "test",
        "medicare_coverage": "test",
        "medicaid_coverage": "test",
        "financial_assistance_programs": "test",
        "cpt_codes": "test",
    }
    education = {
        "plain_language_explanation": "test",
        "daily_living_tips": "test",
        "common_misconceptions": "test",
        "key_takeaways": "test",
    }

    info_data = {
        "metadata": metadata,
        "purpose": purpose,
        "indications": indications,
        "materials": materials,
        "installation": installation,
        "functionality": functionality,
        "recovery": recovery,
        "outcomes": outcomes,
        "complications": complications,
        "imaging": imaging,
        "activity_restrictions": activity_restrictions,
        "maintenance": maintenance,
        "follow_up": follow_up,
        "alternatives": alternatives,
        "evidence": evidence,
        "cost_and_insurance": cost_and_insurance,
        "education": education,
    }

    model = MedicalImplantInfoModel(**info_data)
    assert model.metadata.implant_name == "Pacemaker"
    assert model.evidence.implant_limitations.not_suitable_for == "test"
