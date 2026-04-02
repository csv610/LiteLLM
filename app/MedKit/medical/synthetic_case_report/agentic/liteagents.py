"""
liteagents.py - Unified for synthetic_case_report
"""
from lite.utils import save_model_response\nfrom tqdm import tqdm\nfrom app.MedKit.medical.synthetic_case_report.shared.models import *\nimport pytest\nimport logging\nfrom lite.lite_client import LiteClient\nfrom pathlib import Path\nfrom unittest.mock import patch, MagicMock\nimport argparse\nfrom lite.config import ModelConfig\nimport json\nfrom lite.config import ModelConfig, ModelInput\nfrom lite.logging_config import configure_logging\nimport sys\n\n
# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))



    SyntheticCaseReportGenerator,
)
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



    DiagnosticTherapeuticOutput,
    ModelOutput,
    PatientPresentationOutput,
    ReviewSynthesisOutput,
    SyntheticCaseReportModel,
)

logger = logging.getLogger(__name__)


class SyntheticCaseReportGenerator:
    """Generates synthetic medical case reports based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.condition = None
        logger.debug("Initialized SyntheticCaseReportGenerator")

    def generate_text(self, condition: str, structured: bool = False) -> ModelOutput:
        if not condition or not str(condition).strip():
            raise ValueError("Condition name cannot be empty")

        self.condition = condition
        logger.debug(f"Starting synthetic case report generation for: {condition}")

        if not structured:
            return self._generate_single_agent(condition)

        return self._generate_multi_agent(condition)

    def _generate_single_agent(self, condition: str) -> ModelOutput:
        """Original single-agent generation for unstructured output."""
        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(condition),
            response_format=None,
        )

        try:
            result = self.client.generate_text(model_input=model_input)
            logger.debug("✓ Successfully generated synthetic case report (single agent)")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating synthetic case report: {e}")
            raise

    def _generate_multi_agent(self, condition: str) -> ModelOutput:
        """Multi-agent sequential generation: Specialist (JSON) -> Compliance (JSON) -> Output (Markdown)."""
        logger.info(f"🚀 Starting 3-tier multi-agent generation for: {condition}")

        # Step 1: Patient & Presentation Agent (Specialist - JSON)
        logger.debug("Step 1: Patient & Presentation Agent")
        step1_input = ModelInput(
            system_prompt=PromptBuilder.create_patient_presentation_agent_prompt(),
            user_prompt=PromptBuilder.create_patient_presentation_user_prompt(condition),
            response_format=PatientPresentationOutput,
        )
        step1_result = self.client.generate_text(model_input=step1_input)
        step1_data: PatientPresentationOutput = step1_result.data

        # Step 2: Diagnostic & Therapeutic Agent (Specialist - JSON)
        logger.debug("Step 2: Diagnostic & Therapeutic Agent")
        step2_input = ModelInput(
            system_prompt=PromptBuilder.create_diagnostic_therapeutic_agent_prompt(),
            user_prompt=PromptBuilder.create_diagnostic_therapeutic_user_prompt(
                condition, json.dumps(step1_data.model_dump(), indent=2)
            ),
            response_format=DiagnosticTherapeuticOutput,
        )
        step2_result = self.client.generate_text(model_input=step2_input)
        step2_data: DiagnosticTherapeuticOutput = step2_result.data

        # Step 3: Review & Compliance Agent (Auditor - JSON)
        logger.debug("Step 3: Review & Compliance Agent")
        full_context = {
            "presentation": step1_data.model_dump(),
            "diagnostic_therapeutic": step2_data.model_dump(),
        }
        specialist_json = json.dumps(full_context, indent=2)
        
        step3_input = ModelInput(
            system_prompt=PromptBuilder.create_review_synthesis_agent_prompt(),
            user_prompt=PromptBuilder.create_review_synthesis_user_prompt(
                condition, specialist_json
            ),
            response_format=ReviewSynthesisOutput,
        )
        step3_result = self.client.generate_text(model_input=step3_input)
        step3_data: ReviewSynthesisOutput = step3_result.data
        compliance_json = json.dumps(step3_data.model_dump(), indent=2)

        # Step 4: Output Synthesis Agent (Closer - Markdown)
        logger.debug("Step 4: Output Synthesis Agent")
        output_sys, output_user = PromptBuilder.create_output_synthesis_prompts(
            condition, specialist_json, compliance_json
        )
        
        output_input = ModelInput(
            system_prompt=output_sys,
            user_prompt=output_user,
            response_format=None,
        )
        
        final_markdown = self.client.generate_text(model_input=output_input)

        # Assemble Final Model (Optional - for backward compatibility if needed)
        # Note: step3_data now contains audit findings rather than synthesis, 
        # so final_report assembly might need adjustment if still used.
        final_report = None 

        logger.info("✓ Successfully generated 3-tier multi-agent synthetic case report")
        return ModelOutput(data=final_report, markdown=final_markdown)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        if self.condition is None:
            raise ValueError(
                "No condition information available. Call generate_text first."
            )
        base_filename = f"{self.condition.lower().replace(' ', '_')}_casereport"
        return save_model_response(result, output_dir / base_filename)

"""Synthetic Medical Case Report Generator CLI."""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))




try:
    from .synthetic_case_report import SyntheticCaseReportGenerator
except (ImportError, ValueError):
    from medical.synthetic_case_report.agentic.synthetic_case_report import (
        SyntheticCaseReportGenerator,
    )

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate synthetic medical case reports."
    )
    parser.add_argument(
        "condition", help="Condition name or file path containing names."
    )
    parser.add_argument(
        "-d", "--output-dir", default="outputs", help="Output directory."
    )
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use.")
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Verbosity level.",
    )
    parser.add_argument(
        "-s", "--structured", action="store_true", help="Use structured output."
    )
    return parser.parse_args()


def main():
    args = get_user_arguments()
    configure_logging(
        log_file="synthetic_case_report.log",
        verbosity=args.verbosity,
        enable_console=True,
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.condition)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.condition]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = SyntheticCaseReportGenerator(model_config)

        for item in tqdm(items, desc="Generating"):
            result = generator.generate_text(condition=item, structured=args.structured)
            if result:
                generator.save(result, output_dir)

        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())

