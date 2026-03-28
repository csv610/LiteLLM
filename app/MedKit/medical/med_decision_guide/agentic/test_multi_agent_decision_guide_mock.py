import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from lite.config import ModelConfig

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from medical.med_decision_guide.agentic.multi_agent_decision_guide import (
    MultiAgentMedicalDecisionGuideGenerator,
)
from medical.med_decision_guide.agentic.medical_decision_guide_models import (
    SymptomMetadataModel,
    EmergencyTriageModel,
    DecisionLogicModel,
    OutcomeListModel,
    DecisionNode,
    Outcome,
    ModelOutput
)

@pytest.fixture
def mock_lite_client():
    with patch("medical.med_decision_guide.agentic.multi_agent_decision_guide.LiteClient") as mock:
        yield mock

def test_multi_agent_generator_init():
    config = ModelConfig(model="test-model")
    generator = MultiAgentMedicalDecisionGuideGenerator(config)
    assert generator.model_config == config
    assert generator.analyzer.name == "SymptomAnalyzer"

def test_multi_agent_generate(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MultiAgentMedicalDecisionGuideGenerator(config)
    
    # Mock return values for each agent call
    mock_metadata = SymptomMetadataModel(
        guide_name="Test Guide",
        primary_symptom="Test Symptom",
        secondary_symptoms="s1, s2",
        age_groups_covered="All",
        scope="Test Scope"
    )
    
    mock_triage = EmergencyTriageModel(
        warning_signs="w1, w2",
        emergency_indicators="e1, e2"
    )
    
    mock_logic = DecisionLogicModel(
        start_node_id="q1",
        decision_nodes=[
            DecisionNode(node_id="q1", question="Q1?", yes_node_id="o1", no_node_id="o2")
        ]
    )
    
    mock_outcomes = OutcomeListModel(
        outcomes=[
            Outcome(
                outcome_id="o1", severity_level="s", urgency="u", 
                recommendation="r", possible_diagnoses="d", 
                home_care_advice="h", warning_signs="w"
            ),
            Outcome(
                outcome_id="o2", severity_level="s", urgency="u", 
                recommendation="r", possible_diagnoses="d", 
                home_care_advice="h", warning_signs="w"
            )
        ]
    )

    # Configure the mock to return these in order
    mock_lite_client.return_value.generate_text.side_effect = [
        ModelOutput(data=mock_metadata),
        ModelOutput(data=mock_triage),
        ModelOutput(data=mock_logic),
        ModelOutput(data=mock_outcomes)
    ]

    result = generator.generate("Test Symptom")
    
    assert result.guide_name == "Test Guide"
    assert result.primary_symptom == "Test Symptom"
    assert len(result.decision_nodes) == 1
    assert len(result.outcomes) == 2
    assert result.warning_signs == "w1, w2"
    assert result.emergency_indicators == "e1, e2"
    assert mock_lite_client.return_value.generate_text.call_count == 4
