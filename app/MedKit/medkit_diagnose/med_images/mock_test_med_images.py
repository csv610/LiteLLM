import unittest.mock as mock
from pathlib import Path

import pytest
from lite.config import ModelConfig

from medkit_diagnose.med_images.med_images import MedImageClassifier
from medkit_diagnose.med_images.med_images_models import (
    MedicalImageClassificationModel,
    ModelOutput,
)
from medkit_diagnose.med_images.med_images_prompts import PromptBuilder

# ============================================================================
# PYDANTIC MODEL TESTS
# ============================================================================


def test_model_output_validation():
    """Test the 'exactly one' validator in ModelOutput."""

    # Exactly one (data) - Should PASS
    mock_data = MedicalImageClassificationModel(
        modality="X-Ray",
        anatomical_site="Chest",
        classification="Normal",
        confidence_score=1.0,
    )
    output = ModelOutput(data=mock_data)
    assert output.data == mock_data
    assert output.markdown is None

    # Exactly one (markdown) - Should PASS
    output = ModelOutput(markdown="# Result\nNormal")
    assert output.markdown == "# Result\nNormal"
    assert output.data is None

    # Both set - Should FAIL
    with pytest.raises(
        ValueError, match="Exactly one of 'data' or 'markdown' must be set"
    ):
        ModelOutput(data=mock_data, markdown="# Result\nNormal")

    # Neither set - Should FAIL
    with pytest.raises(
        ValueError, match="Exactly one of 'data' or 'markdown' must be set"
    ):
        ModelOutput(data=None, markdown=None)


# ============================================================================
# PROMPT BUILDER TESTS
# ============================================================================


def test_prompt_builder():
    """Test that prompts are generated correctly."""

    # Image Classification System Prompt
    image_system = PromptBuilder.create_image_classification_system_prompt()
    assert isinstance(image_system, str)
    assert "radiologist" in image_system.lower()

    # Image Classification User Prompt
    image_user = PromptBuilder.create_image_classification_user_prompt()
    assert isinstance(image_user, str)
    assert "Classify" in image_user


# ============================================================================
# CLASSIFIER TESTS (Mocked)
# ============================================================================


@pytest.fixture
def classifier():
    with mock.patch(
        "medkit_diagnose.med_images.med_images.LiteClient"
    ) as mock_client_class:
        model_config = ModelConfig(model="ollama/gemma3", temperature=0.2)
        gen = MedImageClassifier(model_config)
        # Ensure the client is the mock instance
        gen.client = mock_client_class.return_value
        yield gen


@mock.patch("lite.image_utils.ImageUtils.encode_to_base64")
def test_classifier_classify_image(mock_encode, classifier):
    """Test image classification with mocked LiteClient."""
    mock_encode.return_value = "data:image/jpeg;base64,mock"
    mock_data = MedicalImageClassificationModel(
        modality="X-Ray",
        anatomical_site="Chest",
        classification="Normal",
        confidence_score=1.0,
    )
    mock_response = ModelOutput(data=mock_data)
    classifier.client.generate_text.return_value = mock_response

    # Use a dummy path
    result = classifier.classify_image("dummy/path/to/xray.jpg")

    assert result == mock_response
    assert classifier.test_name == "xray"  # Stem of the path
    classifier.client.generate_text.assert_called_once()


@mock.patch("medkit_diagnose.med_images.med_images.save_model_response")
def test_classifier_save(mock_save_model_response, classifier):
    """Test the save method."""
    mock_result = ModelOutput(markdown="Mock Content")
    mock_output_dir = Path("mock_outputs")

    # Should fail if test_name is not set
    classifier.test_name = None
    with pytest.raises(ValueError, match="No image information available"):
        classifier.save(mock_result, mock_output_dir)

    # Should call save_model_response if test_name IS set
    classifier.test_name = "xray"
    classifier.save(mock_result, mock_output_dir)

    expected_path = mock_output_dir / "xray"
    mock_save_model_response.assert_called_once_with(mock_result, expected_path)


# ============================================================================
# CLI LOGIC TESTS
# ============================================================================

from medkit_diagnose.med_images.med_images_cli import create_med_images_report


@mock.patch("medkit_diagnose.med_images.med_images_cli.MedImageClassifier")
@mock.patch("medkit_diagnose.med_images.med_images_cli.configure_logging")
def test_cli_report_generation(mock_configure_logging, mock_classifier_class):
    """Test the CLI's report generation loop."""
    mock_gen_instance = mock_classifier_class.return_value
    mock_data = MedicalImageClassificationModel(
        modality="X-Ray",
        anatomical_site="Chest",
        classification="Normal",
        confidence_score=1.0,
    )
    mock_gen_instance.classify_image.return_value = ModelOutput(data=mock_data)
    mock_gen_instance.save.return_value = Path("outputs/xray.json")

    # Mock arguments
    args = mock.Mock()
    args.input = "assets/xray.jpg"
    args.output_dir = "outputs"
    args.model = "ollama/gemma3"
    args.verbosity = 3
    args.structured = True

    exit_code = create_med_images_report(args)

    assert exit_code == 0
    mock_gen_instance.classify_image.assert_called_with(
        "assets/xray.jpg", structured=True
    )
    mock_gen_instance.save.assert_called()
