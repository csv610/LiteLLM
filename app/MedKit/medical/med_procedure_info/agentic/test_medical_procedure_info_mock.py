import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import patch

import pytest
from lite.config import ModelConfig

try:
    from medical.med_procedure_info.agentic.medical_procedure_info import (
        MedicalProcedureInfoGenerator,
    )
    from medical.med_procedure_info.agentic.medical_procedure_info_models import (
        AdminAgentOutput,
        Alternatives,
        ClinicalAgentOutput,
        ComplianceReport,
        CostAndInsurance,
        DiscomfortAndRisks,
        FollowUpCare,
        MedicalProcedureInfoModel,
        ModelOutput,
        OutcomesAndEffectiveness,
        PreparationRequirements,
        ProcedureDetails,
        ProcedureEducation,
        ProcedureEvidence,
        ProcedureIndications,
        ProcedureLimitations,
        ProcedureMetadata,
        ProcedurePurpose,
        RecoveryAgentOutput,
        RecoveryInformation,
        RiskAgentOutput,
        TechnicalAgentOutput,
        TechnicalDetails,
    )
except ImportError:
    from medical_procedure_info import MedicalProcedureInfoGenerator
    from medical_procedure_info_models import (
        AdminAgentOutput,
        Alternatives,
        ClinicalAgentOutput,
        ComplianceReport,
        CostAndInsurance,
        DiscomfortAndRisks,
        FollowUpCare,
        MedicalProcedureInfoModel,
        ModelOutput,
        OutcomesAndEffectiveness,
        PreparationRequirements,
        ProcedureDetails,
        ProcedureEducation,
        ProcedureEvidence,
        ProcedureIndications,
        ProcedureLimitations,
        ProcedureMetadata,
        ProcedurePurpose,
        RecoveryAgentOutput,
        RecoveryInformation,
        RiskAgentOutput,
        TechnicalAgentOutput,
        TechnicalDetails,
    )


@pytest.fixture
def mock_lite_client():
    # Use absolute path for mocking to be safe
    mock_path = "medical.med_procedure_info.agentic.medical_procedure_info.LiteClient"
    with patch(mock_path) as mock:
        yield mock


def test_generator_init():
    config = ModelConfig(model="test-model")
    generator = MedicalProcedureInfoGenerator(config)
    assert generator.model_config == config


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalProcedureInfoGenerator(config)
    mock_output = ModelOutput(markdown="Appendectomy info", data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Appendectomy")
    assert "Appendectomy info" in result.markdown
    assert generator.procedure_name == "Appendectomy"


def test_generate_text_empty():
    config = ModelConfig(model="test-model")
    generator = MedicalProcedureInfoGenerator(config)
    with pytest.raises(ValueError, match="Procedure name cannot be empty"):
        generator.generate_text("")


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalProcedureInfoGenerator(config)

    # Mock side_effect to handle multiple agent calls
    def side_effect(model_input):
        sys_prompt = str(model_input.system_prompt).lower()
        if "compliance" in sys_prompt:
            return ModelOutput(data=ComplianceReport(is_compliant=True, safety_concerns=[], readability_issues=[], tone_violations=[], suggestions=[]))
        elif "clinical diagnostician" in sys_prompt:
            return ModelOutput(data=ClinicalAgentOutput(
                metadata=ProcedureMetadata(procedure_name="Appendectomy", alternative_names="", procedure_category="", medical_specialty=""),
                purpose=ProcedurePurpose(primary_purpose="", therapeutic_uses="", diagnostic_uses="", preventive_uses=""),
                indications=ProcedureIndications(when_recommended="", symptoms_requiring_procedure="", conditions_treated="", contraindications=""),
                alternatives=Alternatives(alternative_procedures="", non_surgical_alternatives="", advantages_over_alternatives="", when_alternatives_preferred="")
            ))
        elif "procedure specialist" in sys_prompt:
            return ModelOutput(data=TechnicalAgentOutput(
                details=ProcedureDetails(procedure_type="", anesthesia_type="", step_by_step_process="", duration="", location="", equipment_used="", hospital_stay=""),
                technical=TechnicalDetails(surgical_approach="", technology_used="", procedure_variations="", surgeon_qualifications="", facility_requirements=""),
                evidence=ProcedureEvidence(evidence_summary="", procedure_limitations=ProcedureLimitations(not_suitable_for="", age_limitations="", medical_conditions_precluding="", anatomical_limitations=""))
            ))
        elif "risk analyst" in sys_prompt:
            return ModelOutput(data=RiskAgentOutput(
                risks=DiscomfortAndRisks(discomfort_level="", common_sensations="", common_side_effects="", serious_risks="", complication_rates="", mortality_risk="")
            ))
        elif "care coordinator" in sys_prompt:
            return ModelOutput(data=RecoveryAgentOutput(
                preparation=PreparationRequirements(fasting_required="", medication_adjustments="", dietary_restrictions="", pre_procedure_tests="", items_to_bring="", lifestyle_modifications=""),
                recovery=RecoveryInformation(immediate_recovery="", recovery_timeline="", pain_management="", activity_restrictions="", return_to_work="", return_to_normal_activities="", warning_signs=""),
                outcomes=OutcomesAndEffectiveness(success_rate="", expected_benefits="", symptom_improvement="", long_term_outcomes="", factors_affecting_outcomes=""),
                follow_up=FollowUpCare(follow_up_schedule="", monitoring_required="", lifestyle_changes="", medications_after="", physical_therapy="")
            ))
        elif "patient liaison" in sys_prompt:
            return ModelOutput(data=AdminAgentOutput(
                cost_and_insurance=CostAndInsurance(typical_cost_range="", insurance_coverage="", prior_authorization="", medicare_coverage="", medicaid_coverage="", financial_assistance_programs="", cpt_codes=""),
                education=ProcedureEducation(plain_language_explanation="", key_takeaways="", common_misconceptions="")
            ))
        return ModelOutput()

    mock_lite_client.return_value.generate_text.side_effect = side_effect

    result = generator.generate_text("Appendectomy", structured=True)
    assert result.data.metadata.procedure_name == "Appendectomy"
    assert result.compliance_report.is_compliant is True


@patch("medical.med_procedure_info.agentic.medical_procedure_info.save_model_response")
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
