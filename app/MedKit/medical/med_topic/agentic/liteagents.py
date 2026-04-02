"""
liteagents.py - Unified for med_topic
"""
from app.MedKit.medical.med_topic.shared.models import *\nfrom unittest.mock import patch\nfrom lite.utils import save_model_response\nfrom tqdm import tqdm\nfrom .medical_topic import MedicalTopicGenerator\nfrom .medical_topic_prompts import PromptBuilder\nfrom lite.lite_client import LiteClient\nimport logging\nimport pytest\nfrom pathlib import Path\nimport argparse\nfrom lite.config import ModelConfig\nfrom .medical_topic_models import MedicalTopicModel, ModelOutput\nfrom lite.config import ModelConfig, ModelInput\nfrom lite.logging_config import configure_logging\nimport sys\n\n#!/usr/bin/env python3
"""
Medical Topic module.

This module provides the core MedicalTopicGenerator class for generating
comprehensive medical topic information based on provided configuration.
"""




logger = logging.getLogger(__name__)


class MedicalTopicGenerator:
    """Generates comprehensive medical topic information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.topic = None  # Store the topic being analyzed
        logger.debug("Initialized MedicalTopicGenerator")

    def generate_text(self, topic: str, structured: bool = False) -> ModelOutput:
        """Generates 3-tier medical topic information: Specialist -> Auditor -> Output."""
        if not topic or not str(topic).strip():
            raise ValueError("Topic name cannot be empty")

        self.topic = topic
        logger.info(f"Starting 3-tier topic generation for: {topic}")

        try:
            # 1. Specialist Stage (JSON)
            logger.debug(f"[Specialist] Generating content for: {topic}")
            system_prompt = PromptBuilder.create_system_prompt()
            user_prompt = PromptBuilder.create_user_prompt(topic)

            spec_input = ModelInput(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_format=MedicalTopicModel if structured else None,
            )
            spec_res = self.ask_llm(spec_input)
            
            if structured:
                spec_json = spec_res.data.model_dump_json(indent=2)
            else:
                spec_json = spec_res.markdown

            # 2. Auditor Stage (JSON Audit)
            logger.debug(f"[Auditor] Auditing content for: {topic}")
            audit_sys, audit_usr = PromptBuilder.get_topic_auditor_prompts(topic, spec_json)
            audit_input = ModelInput(
                system_prompt=audit_sys,
                user_prompt=audit_usr,
                response_format=None # Audit is markdown/json
            )
            audit_res = self.ask_llm(audit_input)
            audit_json = audit_res.markdown

            # 3. Final Synthesis Stage (Markdown Closer)
            logger.debug(f"[Output] Synthesizing final report for: {topic}")
            out_sys, out_usr = PromptBuilder.get_output_synthesis_prompts(topic, spec_json, audit_json)
            out_input = ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None,
            )
            final_res = self.ask_llm(out_input)

            logger.info("✓ Successfully generated 3-tier medical topic information")
            return ModelOutput(
                data=spec_res.data, 
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier Topic generation failed: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical topic information to a file."""
        if self.topic is None:
            raise ValueError(
                "No topic information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.topic.lower().replace(' ', '_')}"

        return save_model_response(result, output_dir / base_filename)

"""Medical Topic Information Generator CLI."""



logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate comprehensive medical topic information."
    )
    parser.add_argument("topic", help="Medical topic or file path containing topics.")
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
        log_file="medical_topic.log", verbosity=args.verbosity, enable_console=True
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.topic)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.topic]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MedicalTopicGenerator(model_config)

        for item in tqdm(items, desc="Generating"):
            result = generator.generate_text(topic=item, structured=args.structured)
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


# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))



    ClinicalPresentationModel,
    ComplicationsModel,
    CostAndImpactModel,
    DefinitionModel,
    DiagnosisModel,
    EpidemiologyModel,
    EtiologyModel,
    MedicalTopicModel,
    ModelOutput,
    PathophysiologyModel,
    PreventionModel,
    PrognosisModel,
    PsychosocialImpactModel,
    ResearchAndEvidenceModel,
    SeeAlsoModel,
    SpecialPopulationsModel,
    TopicEducationModel,
    TopicMetadataModel,
    TopicOverviewModel,
    TreatmentModel,
)


@pytest.fixture
def mock_lite_client():
    with patch("medical.med_topic.agentic.medical_topic.LiteClient") as mock:
        yield mock


def test_generator_init():
    config = ModelConfig(model="test-model")
    generator = MedicalTopicGenerator(config)
    assert generator.model_config == config


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalTopicGenerator(config)
    mock_output = ModelOutput(markdown="Topic info", data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Diabetes")
    assert result.markdown == "Topic info"
    assert generator.topic == "Diabetes"


def test_generate_text_empty():
    config = ModelConfig(model="test-model")
    generator = MedicalTopicGenerator(config)
    with pytest.raises(ValueError, match="Topic name cannot be empty"):
        generator.generate_text("")


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalTopicGenerator(config)

    # Minimal mock data for structured output
    mock_data = MedicalTopicModel(
        overview=TopicOverviewModel(
            topic_name="Diabetes",
            alternative_names="DM",
            topic_category="Disease",
            medical_specialties="Endocrinology",
            prevalence="High",
        ),
        definition=DefinitionModel(
            plain_language_explanation="High sugar",
            medical_definition="Metabolic disorder",
            key_characteristics="Hyperglycemia",
            disease_classification="Chronic",
        ),
        epidemiology=EpidemiologyModel(
            incidence_rate="1M/yr",
            prevalence_rate="10%",
            age_of_onset="Variable",
            gender_differences="None",
            geographic_variation="Global",
            risk_groups="Obese",
        ),
        etiology=EtiologyModel(
            primary_causes="Insulin resistance",
            genetic_factors="Polygenic",
            environmental_factors="Diet",
            lifestyle_factors="Sedentary",
            infectious_agents="None",
            contributing_factors="Stress",
        ),
        pathophysiology=PathophysiologyModel(
            mechanism_of_disease="Beta cell failure",
            affected_systems="Multi-system",
            cellular_changes="Insulin signaling",
            progression_stages="Pre-diabetes to DM",
            inflammatory_response="Low grade",
            immune_involvement="Type 1 mainly",
        ),
        clinical_presentation=ClinicalPresentationModel(
            primary_symptoms="Thirst",
            secondary_symptoms="Blurry vision",
            symptom_onset="Gradual",
            severity_spectrum="Mild to severe",
            acute_vs_chronic="Chronic",
            symptom_triggers="Sugar",
            asymptomatic_presentation="Common early",
        ),
        diagnosis=DiagnosisModel(
            diagnostic_tests="A1C",
            imaging_studies="None",
            laboratory_findings="High glucose",
            diagnostic_criteria="A1C > 6.5",
            differential_diagnosis="Diabetes insipidus",
            diagnostic_challenges="Early detection",
            time_to_diagnosis="Years",
        ),
        complications=ComplicationsModel(
            acute_complications="DKA",
            chronic_complications="Neuropathy",
            complication_rates="High",
            organ_system_effects="Renal, Retinal",
            mortality_rate="Significant",
            disability_outcomes="Amputation",
        ),
        treatment=TreatmentModel(
            first_line_treatment="Metformin",
            medications="Insulin",
            surgical_interventions="Bariatric surgery",
            physical_therapy="Exercise",
            lifestyle_modifications="Diet",
            dietary_management="Low carb",
            complementary_approaches="None",
            treatment_duration="Lifelong",
        ),
        prognosis=PrognosisModel(
            overall_prognosis="Manageable",
            remission_possibility="Type 2 reversible",
            cure_potential="No",
            recovery_rates="N/A",
            factors_affecting_prognosis="Adherence",
            long_term_outlook="Good with control",
            quality_of_life_impact="Moderate",
        ),
        prevention=PreventionModel(
            primary_prevention="Healthy diet",
            secondary_prevention="Screening",
            screening_recommendations="Over 45",
            protective_factors="Active lifestyle",
            lifestyle_prevention="Weight control",
            vaccinations="None",
        ),
        research_and_evidence=ResearchAndEvidenceModel(
            evidence_quality="High",
            current_research_areas="Beta cell regeneration",
            emerging_treatments="SGLT2 inhibitors",
            clinical_trials="Many",
            guideline_sources="ADA",
        ),
        psychosocial_impact=PsychosocialImpactModel(
            mental_health_effects="Diabetes distress",
            emotional_burden="High",
            social_impact="Dietary restrictions",
            occupational_impact="None",
            coping_strategies="Support groups",
            support_resources="ADA website",
        ),
        special_populations=SpecialPopulationsModel(
            pediatric_considerations="Type 1 focus",
            geriatric_considerations="Hypoglycemia risk",
            pregnancy_considerations="Gestational DM",
            gender_specific_aspects="None",
            ethnic_variations="Higher in some groups",
        ),
        cost_and_impact=CostAndImpactModel(
            healthcare_costs="Very high",
            productivity_loss="Significant",
            burden_on_healthcare_system="High",
            insurance_considerations="Covered",
        ),
        education=TopicEducationModel(
            key_takeaways="Control sugar",
            common_misconceptions="No sugar ever",
            frequently_asked_questions="Can I eat fruit?",
            when_to_see_doctor="Blurred vision",
        ),
        see_also=SeeAlsoModel(
            related_topics="Obesity",
            connection_types="Risk factor",
            reason="Linked via insulin resistance",
        ),
        metadata=TopicMetadataModel(
            last_updated="2024",
            information_sources="Clinical guidelines",
            confidence_level="High",
            complexity_level="Intermediate",
        ),
    )

    mock_output = ModelOutput(data=mock_data, markdown=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Diabetes", structured=True)
    assert result.data.overview.topic_name == "Diabetes"


@patch("medical.med_topic.agentic.medical_topic.save_model_response")
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalTopicGenerator(config)
    mock_output = ModelOutput(markdown="Info")
    mock_lite_client.return_value.generate_text.return_value = mock_output

    generator.generate_text("Diabetes")
    generator.save(mock_output, Path("/tmp"))

    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("diabetes")

