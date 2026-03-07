import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import patch

import pytest
from lite.config import ModelConfig

from medical.surgical_info.surgery_info_models import (
    AlternativesModel,
    CostAndInsuranceModel,
    FollowUpModel,
    ModelOutput,
    OperativePhaseModel,
    OperativeRisksModel,
    PostoperativePhaseModel,
    PreoperativePhaseModel,
    RecoveryAndOutcomesModel,
    SpecialPopulationsModel,
    SurgeryBackgroundModel,
    SurgeryEducationModel,
    SurgeryEvidenceModel,
    SurgeryIndicationsModel,
    SurgeryInfoModel,
    SurgeryMetadataModel,
    SurgeryResearchModel,
    TechnicalDetailsModel,
)
from medical.surgical_info.surgical_info import SurgeryInfoGenerator


@pytest.fixture
def mock_lite_client():
    with patch("medical.surgical_info.surgical_info.LiteClient") as mock:
        yield mock


def test_generator_init():
    config = ModelConfig(model="test-model")
    generator = SurgeryInfoGenerator(config)
    assert generator.model_config == config


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SurgeryInfoGenerator(config)
    mock_output = ModelOutput(markdown="Surgery info", data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Appendectomy")
    assert result.markdown == "Surgery info"
    assert generator.surgery == "Appendectomy"


def test_generate_text_empty():
    config = ModelConfig(model="test-model")
    generator = SurgeryInfoGenerator(config)
    with pytest.raises(ValueError, match="Surgery name cannot be empty"):
        generator.generate_text("")


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SurgeryInfoGenerator(config)

    # Minimal mock data for structured output
    mock_data = SurgeryInfoModel(
        metadata=SurgeryMetadataModel(
            surgery_name="Appendectomy",
            alternative_names="Appy",
            procedure_code="44950",
            surgery_category="GI",
            body_systems_involved="Digestive",
        ),
        background=SurgeryBackgroundModel(
            definition="Remove appendix",
            surgical_anatomy="RLQ",
            historical_background="Ancient",
            epidemiology="Common",
        ),
        indications=SurgeryIndicationsModel(
            absolute_indications="Appendicitis",
            relative_indications="None",
            emergency_indications="Rupture",
            absolute_contraindications="None",
            relative_contraindications="None",
        ),
        preoperative=PreoperativePhaseModel(
            patient_evaluation="Physical",
            laboratory_tests="CBC",
            imaging_studies="CT",
            specialist_consultations="None",
            risk_stratification="ASA",
            preoperative_preparation="NPO",
            patient_counseling_points="Risks",
        ),
        operative=OperativePhaseModel(
            surgical_approaches="Laparoscopic",
            anesthesia_type="General",
            patient_positioning="Supine",
            surgical_steps="1. Cut",
            instruments_equipment="Trocar",
            duration="1 hour",
        ),
        operative_risks=OperativeRisksModel(
            intraoperative_complications="Bleeding",
            early_postoperative_complications="Infection",
            late_postoperative_complications="Adhesions",
            complication_rates="Low",
        ),
        postoperative=PostoperativePhaseModel(
            immediate_care="Recovery room",
            pain_management="NSAIDs",
            monitoring_parameters="Vitals",
            diet_progression="Clear liquids",
            mobilization_protocol="Early",
            drain_management="None",
            hospital_stay="1 day",
            discharge_criteria="Stable",
        ),
        recovery_outcomes=RecoveryAndOutcomesModel(
            recovery_timeline="2 weeks",
            rehabilitation_protocol="None",
            return_to_work="1 week",
            return_to_normal_activities="2 weeks",
            success_rates="99%",
            functional_outcomes="Good",
            recurrence_rates="None",
            long_term_outcomes="Excellent",
        ),
        follow_up=FollowUpModel(
            follow_up_schedule="2 weeks",
            monitoring_required="Wound check",
            lifestyle_modifications="None",
            warning_signs="Fever",
        ),
        alternatives=AlternativesModel(
            medical_management="Antibiotics",
            minimally_invasive_procedures="Laparoscopic",
            conservative_approaches="None",
            advantages_over_alternatives="Cure",
        ),
        special_populations=SpecialPopulationsModel(
            pediatric_considerations="Common in kids",
            geriatric_considerations="Subtle presentation",
            pregnancy_considerations="Emergency surgery",
        ),
        technical=TechnicalDetailsModel(
            surgical_approach_variations="Open vs Lap",
            surgeon_qualifications="Board certified",
            facility_requirements="OR",
            technology_used="Robot",
        ),
        research=SurgeryResearchModel(
            recent_innovations="NOTES",
            robotic_ai_applications="None",
            emerging_technologies="None",
            clinical_trials="None",
            future_directions="None",
            quality_improvement_initiatives="ERAS",
        ),
        evidence=SurgeryEvidenceModel(
            evidence_level="High",
            evidence_summary="Standard of care",
            comparative_effectiveness="Laparoscopic preferred",
        ),
        education=SurgeryEducationModel(
            plain_language_explanation="Remove bad appendix",
            key_takeaways="Fast recovery",
            common_misconceptions="Can live without it",
        ),
        cost_and_insurance=CostAndInsuranceModel(
            typical_cost_range="$10k-20k",
            insurance_coverage="High",
            medicare_coverage="Yes",
            medicaid_coverage="Yes",
            prior_authorization="Yes",
            financial_assistance_programs="Available",
        ),
    )

    mock_output = ModelOutput(data=mock_data, markdown=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Appendectomy", structured=True)
    assert result.data.metadata.surgery_name == "Appendectomy"


@patch("medical.surgical_info.surgical_info.save_model_response")
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SurgeryInfoGenerator(config)
    mock_output = ModelOutput(markdown="Info")
    mock_lite_client.return_value.generate_text.return_value = mock_output

    generator.generate_text("Appendectomy")
    generator.save(mock_output, Path("/tmp"))

    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("appendectomy")
