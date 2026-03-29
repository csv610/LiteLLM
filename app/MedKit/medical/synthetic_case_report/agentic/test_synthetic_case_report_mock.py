import sys
import json
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import patch, MagicMock

import pytest
from lite.config import ModelConfig

from medical.synthetic_case_report.agentic.synthetic_case_report import (
    SyntheticCaseReportGenerator,
)
from medical.synthetic_case_report.agentic.synthetic_case_report_models import (
    CaseReportMetadataModel,
    ClinicalFindingsModel,
    DiagnosticAssessmentModel,
    DiagnosticTherapeuticOutput,
    DiscussionModel,
    FollowUpAndOutcomesModel,
    InformedConsentModel,
    ModelOutput,
    PatientInformationModel,
    PatientPerspectiveModel,
    PatientPresentationOutput,
    ReviewSynthesisOutput,
    SyntheticCaseReportModel,
    TherapeuticInterventionsModel,
    TimelineModel,
)


@pytest.fixture
def mock_lite_client():
    with patch(
        "medical.synthetic_case_report.agentic.synthetic_case_report.LiteClient"
    ) as mock:
        yield mock


def test_generator_init():
    config = ModelConfig(model="test-model")
    generator = SyntheticCaseReportGenerator(config)
    assert generator.model_config == config


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SyntheticCaseReportGenerator(config)
    mock_output = ModelOutput(markdown="Case report info", data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Diabetes")
    assert result.markdown == "Case report info"
    assert generator.condition == "Diabetes"


def test_generate_text_empty():
    config = ModelConfig(model="test-model")
    generator = SyntheticCaseReportGenerator(config)
    with pytest.raises(ValueError, match="Condition name cannot be empty"):
        generator.generate_text("")


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SyntheticCaseReportGenerator(config)

    # Step 1 Mock Output
    step1_data = PatientPresentationOutput(
        patient_information=PatientInformationModel(
            age=45, gender="Male", ethnicity="E1", occupation="O1",
            relevant_family_history="F1", past_medical_history="P1",
            surgical_history="S1", medication_history="M1",
            allergy_history="A1", social_history="S2"
        ),
        clinical_findings=ClinicalFindingsModel(
            chief_complaint="C1", history_of_present_illness="H1",
            symptom_onset="O1", symptom_progression="P1",
            associated_symptoms="A1", alleviating_factors="A2",
            aggravating_factors="A3", impact_on_activities="I1",
            physical_exam_findings="P2", abnormal_findings="A4"
        ),
        timeline=TimelineModel(
            initial_presentation_date="D1", key_clinical_events="E1",
            diagnostic_workup_timeline="T1", treatment_initiation_date="D2",
            significant_changes="S1", duration_of_illness="D3"
        )
    )

    # Step 2 Mock Output
    step2_data = DiagnosticTherapeuticOutput(
        diagnostic_assessment=DiagnosticAssessmentModel(
            laboratory_tests_performed="L1", laboratory_values="V1",
            imaging_studies="I1", imaging_findings="F1",
            pathology_results="P1", specialized_testing="S1",
            diagnostic_criteria_assessment="D1", diagnostic_challenges="C1",
            noteworthy_findings_pattern="P1"
        ),
        therapeutic_interventions=TherapeuticInterventionsModel(
            initial_management="M1", medications_prescribed="M2",
            dosage_adjustments="D1", surgical_interventions="S1",
            procedural_interventions="P1", supportive_care="S2",
            lifestyle_modifications="L1", rehabilitation_therapy="R1",
            adverse_events="A1", treatment_response="R2"
        ),
        follow_up_and_outcomes=FollowUpAndOutcomesModel(
            clinical_response_to_treatment="R1", symptom_resolution="S1",
            functional_status="S2", final_clinical_status="S3",
            complications_during_course="C1", length_of_hospital_stay="D1",
            duration_of_followup="D2", discharge_medications="M1",
            followup_schedule="S4", current_status="S5"
        )
    )

    # Step 3 Mock Output
    step3_data = ReviewSynthesisOutput(
        metadata=CaseReportMetadataModel(
            case_report_title="Multi-Agent Title",
            keywords="k1, k2", medical_specialty="Med",
            date_case_compiled="2024", case_authors="A1",
            institution="H1", information_sources="S1",
            confidence_level="High", clinical_accuracy="Accurate",
            bias_mitigation_note="None"
        ),
        discussion=DiscussionModel(
            case_significance="S1", findings_interpretation="I1",
            diagnostic_approach_discussion="D1", treatment_rationale="R1",
            treatment_effectiveness="E1", learning_points="L1",
            pathophysiological_insights="P1", clinical_pearls="P2",
            implications_for_practice="I2", recommendations="R2"
        ),
        patient_perspective=PatientPerspectiveModel(
            patient_experience="E1", understanding_of_diagnosis="U1",
            treatment_satisfaction="S1", quality_of_life_impact="I1",
            adherence_to_treatment="A1", psychosocial_factors="P1"
        ),
        informed_consent=InformedConsentModel(
            consent_statement="C1", patient_anonymity="A1",
            institutional_approval="I1", ethical_considerations="E1"
        )
    )

    # Configure side_effect for three calls
    mock_lite_client.return_value.generate_text.side_effect = [
        ModelOutput(data=step1_data),
        ModelOutput(data=step2_data),
        ModelOutput(data=step3_data)
    ]

    result = generator.generate_text("Diabetes", structured=True)
    
    assert result.data.metadata.case_report_title == "Multi-Agent Title"
    assert result.data.patient_information.age == 45
    assert result.data.diagnostic_assessment.laboratory_tests_performed == "L1"
    assert result.data.discussion.case_significance == "S1"
    assert mock_lite_client.return_value.generate_text.call_count == 3


@patch("medical.synthetic_case_report.agentic.synthetic_case_report.save_model_response")
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SyntheticCaseReportGenerator(config)
    mock_output = ModelOutput(markdown="Info")
    mock_lite_client.return_value.generate_text.return_value = mock_output

    generator.generate_text("Diabetes")
    generator.save(mock_output, Path("/tmp"))

    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("diabetes_casereport")
