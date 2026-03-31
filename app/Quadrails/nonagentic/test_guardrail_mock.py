import pytest
import asyncio
from unittest.mock import patch
from pathlib import Path

from .guardrail import GuardrailAnalyzer
from .guardrail_models import (
    GuardrailResponse,
    GuardrailResult,
    SafetyCategory,
    PreprocessingError,
    ImageGuardrailResponse,
)


# Manual async runner since pytest-asyncio is missing
def run_async(coro):
    return asyncio.run(coro)


@pytest.fixture
def mock_lite_client():
    with patch("lite.lite_client.LiteClient") as mock:
        yield mock


@pytest.fixture
def safe_response():
    return GuardrailResponse(
        text="Hello, how are you today?",
        is_safe=True,
        flagged_categories=[],
        summary="The text is safe and contains no safety violations.",
    )


@pytest.fixture
def flagged_response():
    return GuardrailResponse(
        text="I hate everyone and want to hurt them.",
        is_safe=False,
        flagged_categories=[
            GuardrailResult(
                category=SafetyCategory.HATE_SPEECH,
                is_flagged=True,
                score=0.95,
                reasoning="Contains hateful language directed at a broad group.",
            )
        ],
        summary="The text contains hate speech.",
    )


def test_analyze_text_safe(mock_lite_client, safe_response):
    instance = mock_lite_client.return_value
    instance.generate_text.return_value = safe_response

    analyzer = GuardrailAnalyzer()
    result = run_async(analyzer.analyze_text("Hello, how are you today?"))

    assert result.is_safe is True
    assert instance.generate.called


def test_analyze_text_caching(mock_lite_client, safe_response):
    instance = mock_lite_client.return_value
    instance.generate_text.return_value = safe_response

    analyzer = GuardrailAnalyzer()
    text = "Is this cached?"

    # First call
    run_async(analyzer.analyze_text(text))
    assert instance.generate.call_count == 1

    # Second call
    run_async(analyzer.analyze_text(text))
    assert instance.generate.call_count == 1


def test_analyze_text_preprocessing_error():
    analyzer = GuardrailAnalyzer()
    with pytest.raises(PreprocessingError):
        run_async(analyzer.analyze_text("   "))


def test_analyze_text_preprocessing(mock_lite_client, safe_response):
    instance = mock_lite_client.return_value
    instance.generate_text.return_value = safe_response

    analyzer = GuardrailAnalyzer(max_length=10)
    input_text = "Hello \x00 World   "
    result = run_async(analyzer.analyze_text(input_text))

    assert result.text == "Hello Worl"


def test_analyze_text_flagged(mock_lite_client, flagged_response):
    instance = mock_lite_client.return_value
    instance.generate_text.return_value = flagged_response

    analyzer = GuardrailAnalyzer()
    result = run_async(analyzer.analyze_text("I hate everyone and want to hurt them."))

    assert result.is_safe is False
    assert result.flagged_categories[0].category == SafetyCategory.HATE_SPEECH


def test_display_results(safe_response, capsys):
    GuardrailAnalyzer.display_results(safe_response)
    captured = capsys.readouterr()
    assert "GUARDRAIL ANALYSIS RESULTS" in captured.out
    assert "OVERALL SAFETY: ✅ SAFE" in captured.out


@pytest.fixture
def nudity_violence_image_response():
    return ImageGuardrailResponse(
        image_path="/path/to/unsafe.jpg",
        is_safe=False,
        flagged_categories=[
            GuardrailResult(
                category=SafetyCategory.NUDITY,
                is_flagged=True,
                score=0.98,
                reasoning="Image contains explicit nudity.",
            ),
            GuardrailResult(
                category=SafetyCategory.VIOLENCE,
                is_flagged=True,
                score=0.95,
                reasoning="Image depicts extreme physical violence.",
            ),
        ],
        summary="Image flagged for nudity and violence.",
    )


def test_analyze_image_unsafe(mock_lite_client, nudity_violence_image_response):
    instance = mock_lite_client.return_value
    instance.generate_text.return_value = nudity_violence_image_response

    analyzer = GuardrailAnalyzer()

    with patch("guardrail.Path.exists", return_value=True):
        with patch("guardrail.Path.absolute", return_value=Path("/path/to/unsafe.jpg")):
            result = run_async(analyzer.analyze_image("/path/to/unsafe.jpg"))

            assert result.is_safe is False
            categories = [res.category for res in result.flagged_categories]
            assert SafetyCategory.NUDITY in categories
            assert SafetyCategory.VIOLENCE in categories
            assert instance.generate.called


def test_analyze_image_file_not_found():
    analyzer = GuardrailAnalyzer()
    with pytest.raises(PreprocessingError):
        run_async(analyzer.analyze_image("non_existent.jpg"))
