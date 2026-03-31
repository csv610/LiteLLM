import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import patch

import pytest
from lite.config import ModelConfig

from medical.med_myths_checker.agentic.medical_myth_checker import MedicalMythsChecker
from medical.med_myths_checker.agentic.medical_myth_checker_models import (
    MedicalMythAnalysisModel,
    ModelOutput,
    MythAnalysisModel,
)


@pytest.fixture
def mock_lite_client():
    with patch("medical.med_myths_checker.agentic.medical_myth_checker.LiteClient") as mock:
        yield mock


def test_checker_init():
    config = ModelConfig(model="test-model")
    checker = MedicalMythsChecker(config)
    assert checker.client is not None


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    checker = MedicalMythsChecker(config)
    mock_output = ModelOutput(markdown="Myth analysis", data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = checker.generate_text("Carrots improve eyesight")
    assert result.markdown == "Myth analysis"
    assert checker.myth == "Carrots improve eyesight"


def test_generate_text_empty():
    config = ModelConfig(model="test-model")
    checker = MedicalMythsChecker(config)
    with pytest.raises(ValueError, match="Myth statement cannot be empty"):
        checker.generate_text("")


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    checker = MedicalMythsChecker(config)

    mock_data = MedicalMythAnalysisModel(
        myths=[
            MythAnalysisModel(
                statement="Carrots improve eyesight",
                status="FALSE",
                explanation="They help maintain but don't improve it.",
                peer_reviewed_sources="Journal of Nutrition (2010)",
                risk_level="LOW",
            )
        ]
    )

    mock_output = ModelOutput(data=mock_data, markdown=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = checker.generate_text("Carrots improve eyesight", structured=True)
    assert result.data.myths[0].status == "FALSE"


@patch("medical.med_myths_checker.agentic.medical_myth_checker.save_model_response")
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    checker = MedicalMythsChecker(config)
    mock_output = ModelOutput(markdown="Analysis")
    mock_lite_client.return_value.generate_text.return_value = mock_output

    checker.generate_text("Carrots improve eyesight")
    checker.save(mock_output, Path("/tmp"))

    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert "carrots_improve_eyesight" in str(args[1])


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
