import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pytest
from unittest.mock import patch, MagicMock
from medical.med_procedure_info.medical_procedure_info import MedicalProcedureInfoGenerator
from lite.config import ModelConfig
from medical.med_procedure_info.medical_procedure_info_models import (
    MedicalProcedureInfoModel, ModelOutput, ProcedureMetadata,
    ProcedurePurpose, ProcedureIndications, PreparationRequirements,
    ProcedureDetails, DiscomfortAndRisks, RecoveryInformation,
    OutcomesAndEffectiveness, FollowUpCare, Alternatives,
    TechnicalDetails, ProcedureEvidence, ProcedureLimitations,
    CostAndInsurance, ProcedureEducation
)

@pytest.fixture
def mock_lite_client():
    with patch('medical.med_procedure_info.medical_procedure_info.LiteClient') as mock:
        yield mock

def test_generator_init():
    config = ModelConfig(model="test-model")
    generator = MedicalProcedureInfoGenerator(config)
    assert generator.model_config == config

def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalProcedureInfoGenerator(config)
    mock_output = ModelOutput(markdown="Appendedectomy info", data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    
    result = generator.generate_text("Appendectomy")
    assert result.markdown == "Appendedectomy info"
    assert generator.procedure_name == "Appendectomy"

def test_generate_text_empty():
    config = ModelConfig(model="test-model")
    generator = MedicalProcedureInfoGenerator(config)
    with pytest.raises(ValueError, match="Procedure name cannot be empty"):
        generator.generate_text("")

def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalProcedureInfoGenerator(config)
    
    # Minimal mock data for structured output
    mock_data = MedicalProcedureInfoModel(
        metadata=ProcedureMetadata(procedure_name="Appendectomy", alternative_names="Appy", procedure_category="Surgical", medical_specialty="General Surgery"),
        purpose=ProcedurePurpose(primary_purpose="Remove appendix", therapeutic_uses="Appendicitis", diagnostic_uses="None", preventive_uses="None"),
        indications=ProcedureIndications(when_recommended="Inflamed appendix", symptoms_requiring_procedure="Abdominal pain", conditions_treated="Appendicitis", contraindications="None"),
        preparation=PreparationRequirements(fasting_required="8 hours", medication_adjustments="None", dietary_restrictions="NPO", pre_procedure_tests="CBC, CT", items_to_bring="ID", lifestyle_modifications="None"),
        details=ProcedureDetails(procedure_type="Laparoscopic", anesthesia_type="General", step_by_step_process="1. Incision", duration="1 hour", location="Hospital", equipment_used="Laparoscope", hospital_stay="1 day"),
        risks=DiscomfortAndRisks(discomfort_level="Moderate", common_sensations="Grogginess", common_side_effects="Nausea", serious_risks="Infection", complication_rates="Low", mortality_risk="Very low"),
        recovery=RecoveryInformation(immediate_recovery="Waking up", recovery_timeline="2 weeks", pain_management="NSAIDs", activity_restrictions="No heavy lifting", return_to_work="1 week", return_to_normal_activities="2 weeks", warning_signs="Fever"),
        outcomes=OutcomesAndEffectiveness(success_rate="99%", expected_benefits="Cure", symptom_improvement="Immediate", long_term_outcomes="Good", factors_affecting_outcomes="Age"),
        follow_up=FollowUpCare(follow_up_schedule="2 weeks", monitoring_required="Incision check", lifestyle_changes="None", medications_after="Antibiotics", physical_therapy="No"),
        alternatives=Alternatives(alternative_procedures="Open surgery", non_surgical_alternatives="Antibiotics", advantages_over_alternatives="Faster recovery", when_alternatives_preferred="Rupture"),
        technical=TechnicalDetails(surgical_approach="Laparoscopic", technology_used="Robot", procedure_variations="Single port", surgeon_qualifications="Board certified", facility_requirements="OR"),
        evidence=ProcedureEvidence(evidence_summary="Standard of care", procedure_limitations=ProcedureLimitations(not_suitable_for="Unstable patients", age_limitations="None", medical_conditions_precluding="Coagulopathy", anatomical_limitations="Obesity")),
        cost_and_insurance=CostAndInsurance(
            typical_cost_range="$10k-20k", insurance_coverage="High",
            prior_authorization="Yes", medicare_coverage="Yes",
            medicaid_coverage="Yes", financial_assistance_programs="Available",
            cpt_codes="44950"
        ),
        education=ProcedureEducation(plain_language_explanation="Remove bad appendix", key_takeaways="Quick recovery", common_misconceptions="Can live without it")
    )
    
    mock_output = ModelOutput(data=mock_data, markdown=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    
    result = generator.generate_text("Appendectomy", structured=True)
    assert result.data.metadata.procedure_name == "Appendectomy"

@patch('medical.med_procedure_info.medical_procedure_info.save_model_response')
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalProcedureInfoGenerator(config)
    mock_output = ModelOutput(markdown="Info")
    mock_lite_client.return_value.generate_text.return_value = mock_output
    
    generator.generate_text("Appendectomy")
    generator.save(mock_output, Path("/tmp"))
    
    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("appendectomy")
