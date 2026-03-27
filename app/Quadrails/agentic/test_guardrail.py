import asyncio
from pathlib import Path
from unittest.mock import patch

import pytest

from guardrail import GuardrailAnalyzer, TextGuardrailAgent, ImageGuardrailAgent
from guardrail_models import (
    AnalysisError,
    GuardrailResponse,
    GuardrailResult,
    ImageGuardrailResponse,
    PreprocessingError,
    SafetyCategory,
)


def run_async(coro):
    return asyncio.run(coro)


@pytest.fixture
def mock_lite_client():
    with patch("guardrail.LiteClient") as mock:
        yield mock


@pytest.fixture
def safe_text_response():
    return GuardrailResponse(
        text="Hello, how are you today?",
        is_safe=True,
        flagged_categories=[],
        summary="The text is safe and contains no safety violations.",
    )


@pytest.fixture
def unsafe_image_response():
    return ImageGuardrailResponse(
        image_path="/tmp/unsafe.jpg",
        is_safe=False,
        flagged_categories=[
            GuardrailResult(
                category=SafetyCategory.NUDITY,
                is_flagged=True,
                score=0.98,
                reasoning="Image contains explicit nudity.",
            )
        ],
        summary="Image flagged for nudity.",
    )


def test_text_analysis_uses_cache(mock_lite_client, safe_text_response):
    instance = mock_lite_client.return_value
    instance.generate.return_value = safe_text_response

    agent = TextGuardrailAgent()
    text = "Is this cached?"

    first = run_async(agent.analyze_text(text))
    second = run_async(agent.analyze_text(text))

    assert first.is_safe is True
    assert second.is_safe is True
    assert instance.generate.call_count == 1


def test_text_preprocessing_enforced(mock_lite_client, safe_text_response):
    instance = mock_lite_client.return_value
    instance.generate.return_value = safe_text_response

    agent = TextGuardrailAgent(max_length=10)
    result = run_async(agent.analyze_text("Hello \x00 World   "))

    assert result.text == "Hello Worl"


def test_text_empty_after_preprocessing_raises():
    agent = TextGuardrailAgent()
    with pytest.raises(PreprocessingError):
        run_async(agent.analyze_text("   "))


def test_text_preserves_analysis_error(mock_lite_client):
    instance = mock_lite_client.return_value
    instance.generate.side_effect = AnalysisError("structured failure")

    agent = TextGuardrailAgent()

    with pytest.raises(AnalysisError, match="structured failure"):
        run_async(agent.analyze_text("hello"))


def test_image_cache_invalidates_when_file_changes(mock_lite_client, unsafe_image_response, tmp_path):
    instance = mock_lite_client.return_value
    instance.generate.return_value = unsafe_image_response

    image_path = tmp_path / "sample.jpg"
    image_path.write_bytes(b"first")

    agent = ImageGuardrailAgent()
    run_async(agent.analyze_image(str(image_path)))
    assert instance.generate.call_count == 1

    image_path.write_bytes(b"second version")
    run_async(agent.analyze_image(str(image_path)))

    assert instance.generate.call_count == 2


def test_image_missing_file_raises():
    agent = ImageGuardrailAgent()
    with pytest.raises(PreprocessingError):
        run_async(agent.analyze_image("non_existent.jpg"))


def test_display_results_for_text(safe_text_response, capsys):
    GuardrailAnalyzer.display_results(safe_text_response)
    captured = capsys.readouterr()
    assert "GUARDRAIL ANALYSIS RESULTS" in captured.out
    assert "OVERALL SAFETY: ✅ SAFE" in captured.out

