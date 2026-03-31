import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import patch

import pytest
from lite.config import ModelConfig

from medical.med_facts_checker.agentic.medical_facts_checker import MedicalFactsChecker
from medical.med_facts_checker.agentic.medical_facts_checker_models import (
    AnalyzerMetadata,
    ContextInformation,
    DetailedAnalysis,
    FictionIndicators,
    MedicalFactFictionAnalysisModel,
    ModelOutput,
    StatementAnalysis,
)


@pytest.fixture
def mock_lite_client():
    with patch("medical.med_facts_checker.agentic.medical_facts_checker.LiteClient") as mock:
        yield mock


def test_medical_facts_checker_init():
    config = ModelConfig(model="test-model")
    checker = MedicalFactsChecker(config)
    assert checker.client is not None


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    checker = MedicalFactsChecker(config)
    
    # Mock four responses: Researcher, Skeptic, Synthesizer, Compliance
    mock_responses = [
        ModelOutput(markdown="R", data=None),
        ModelOutput(markdown="S", data=None),
        ModelOutput(markdown="Synthesized Report", data=None),
        ModelOutput(markdown="Final Approved Report", data=None)
    ]
    mock_lite_client.return_value.generate_text.side_effect = mock_responses

    result = checker.generate_text("Water is wet")
    assert result.markdown == "Final Approved Report"
    assert result.researcher_report == "R"
    assert result.skeptic_report == "S"
    assert mock_lite_client.return_value.generate_text.call_count == 4


def test_generate_text_empty_statement():
    config = ModelConfig(model="test-model")
    checker = MedicalFactsChecker(config)
    with pytest.raises(ValueError, match="Statement cannot be empty"):
        checker.generate_text("")


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    checker = MedicalFactsChecker(config)

    mock_data = MedicalFactFictionAnalysisModel(
        detailed_analysis=DetailedAnalysis(
            statement_analysis=StatementAnalysis(
                statement="Vitamin C cures cancer",
                classification="Fiction",
                confidence_level="High",
                confidence_percentage=99,
            ),
            factual_support=None,
            fiction_indicators=FictionIndicators(
                red_flags="No clinical evidence",
                factual_errors="Vitamin C is an antioxidant, not a cure",
                lack_of_evidence="Large trials failed",
                fictional_elements="Alternative medicine myth",
            ),
            context=ContextInformation(
                subject_area="Oncology",
                key_terms="Vitamin C, Cancer",
                assumptions="High dose is effective",
                scope_clarity="Clear",
            ),
            explanation="No evidence supports this.",
            potential_confusion="Early lab studies were misinterpreted.",
        ),
        metadata=AnalyzerMetadata(
            analysis_date="2024-05-20",
            knowledge_cutoff="2023-12",
            analysis_method="Evidence review",
            limitations="Based on current clinical data",
        ),
    )

    # Mock four responses: Researcher, Skeptic, Synthesizer, Compliance (with data)
    mock_responses = [
        ModelOutput(markdown="R", data=None),
        ModelOutput(markdown="S", data=None),
        ModelOutput(markdown="Synthesized Report", data=None),
        ModelOutput(data=mock_data, markdown=None)
    ]
    mock_lite_client.return_value.generate_text.side_effect = mock_responses

    result = checker.generate_text("Vitamin C cures cancer", structured=True)
    assert result.data.detailed_analysis.statement_analysis.classification == "Fiction"
    assert result.researcher_report == "R"
    assert result.skeptic_report == "S"
    assert mock_lite_client.return_value.generate_text.call_count == 4


def test_save_error():
    config = ModelConfig(model="test-model")
    checker = MedicalFactsChecker(config)
    with pytest.raises(ValueError, match="No statement information available"):
        checker.save(ModelOutput(), Path("/tmp"))


@patch("medical.med_facts_checker.agentic.medical_facts_checker.save_model_response")
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    checker = MedicalFactsChecker(config)
    
    mock_responses = [
        ModelOutput(markdown="R"),
        ModelOutput(markdown="S"),
        ModelOutput(markdown="Synth"),
        ModelOutput(markdown="Final")
    ]
    mock_lite_client.return_value.generate_text.side_effect = mock_responses

    checker.generate_text("Water is wet")
    mock_output = mock_responses[-1]
    checker.save(mock_output, Path("/tmp"))

    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("water_is_wet_facts_analysis")
