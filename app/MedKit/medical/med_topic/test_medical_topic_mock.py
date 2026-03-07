import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import patch

import pytest
from lite.config import ModelConfig

from medical.med_topic.medical_topic import MedicalTopicGenerator
from medical.med_topic.medical_topic_models import (
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
    with patch("medical.med_topic.medical_topic.LiteClient") as mock:
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


@patch("medical.med_topic.medical_topic.save_model_response")
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
