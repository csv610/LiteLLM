import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import patch

import pytest
from lite.config import ModelConfig

from medical.med_decision_guide.agentic.medical_decision_guide import (
    MedicalDecisionGuideGenerator,
)
from medical.med_decision_guide.agentic.medical_decision_guide_models import (
    DecisionNode,
    MedicalDecisionGuideModel,
    ModelOutput,
    Outcome,
)


@pytest.fixture
def mock_lite_client():
    with patch("medical.med_decision_guide.agentic.medical_decision_guide.LiteClient") as mock:
        yield mock


def test_medical_decision_guide_generator_init():
    config = ModelConfig(model="test-model")
    generator = MedicalDecisionGuideGenerator(config)
    assert generator.model_config == config


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalDecisionGuideGenerator(config)
    mock_output = ModelOutput(markdown="Chest pain guide", data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Chest pain")
    assert result.markdown == "Chest pain guide"
    assert generator.symptom == "Chest pain"


def test_generate_text_empty_symptom():
    config = ModelConfig(model="test-model")
    generator = MedicalDecisionGuideGenerator(config)
    with pytest.raises(ValueError, match="Symptom name cannot be empty"):
        generator.generate_text("")


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalDecisionGuideGenerator(config)

    mock_data = MedicalDecisionGuideModel(
        guide_name="Chest Pain Assessment",
        primary_symptom="Chest Pain",
        secondary_symptoms="Shortness of breath, sweating",
        age_groups_covered="Adults, Elderly",
        scope="Emergency assessment of chest pain",
        start_node_id="q1",
        decision_nodes=[
            DecisionNode(
                node_id="q1",
                question="Is it crushing pain?",
                yes_node_id="out_emergency",
                no_node_id="q2",
            ),
            DecisionNode(
                node_id="q2",
                question="Is it sharp?",
                yes_node_id="out_mild",
                no_node_id="out_moderate",
            ),
        ],
        outcomes=[
            Outcome(
                outcome_id="out_emergency",
                severity_level="Emergency",
                urgency="Emergency",
                recommendation="Call 911",
                possible_diagnoses="MI",
                home_care_advice="None",
                warning_signs="Crushing pain",
            ),
            Outcome(
                outcome_id="out_mild",
                severity_level="Mild",
                urgency="Self-care",
                recommendation="Rest",
                possible_diagnoses="Pleurisy",
                home_care_advice="OTC pain relief",
                warning_signs="Worsening pain",
            ),
            Outcome(
                outcome_id="out_moderate",
                severity_level="Moderate",
                urgency="Urgent-care",
                recommendation="See doctor",
                possible_diagnoses="GERD",
                home_care_advice="Antacids",
                warning_signs="Pain after eating",
            ),
        ],
        warning_signs="Shortness of breath",
        emergency_indicators="Crushing pain",
    )

    mock_output = ModelOutput(data=mock_data, markdown=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Chest pain", structured=True)
    assert result.data.guide_name == "Chest Pain Assessment"


def test_save_error():
    config = ModelConfig(model="test-model")
    generator = MedicalDecisionGuideGenerator(config)
    with pytest.raises(ValueError, match="No symptom information available"):
        generator.save(ModelOutput(), Path("/tmp"))


@patch("medical.med_decision_guide.agentic.medical_decision_guide.save_model_response")
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalDecisionGuideGenerator(config)
    mock_output = ModelOutput(markdown="Chest pain guide")
    mock_lite_client.return_value.generate_text.return_value = mock_output

    generator.generate_text("Chest pain")
    generator.save(mock_output, Path("/tmp"))

    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("chest_pain_decision_guide")

