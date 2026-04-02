import pytest
from unittest.mock import patch, MagicMock
import json
import os

from HilbertProblems.agentic.hilbert_problems import HilbertProblemsGuide
from HilbertProblems.agentic.hilbert_problems_models import HilbertProblemModel, ProblemStatus

@pytest.fixture
def mock_lite_client():
    with patch('HilbertProblems.agentic.hilbert_problems.LiteClient') as mock:
        yield mock

@pytest.fixture
def sample_problem():
    return HilbertProblemModel(
        number=1,
        title="The Continuum Hypothesis",
        description="The problem of the power of the continuum.",
        status=ProblemStatus.PARTIALLY_SOLVED,
        solved_by="Kurt Gödel, Paul Cohen",
        solution_year=1963,
        solution_method="Forcing and inner models",
        related_fields=["Set Theory", "Logic"],
        notes="Independence from ZFC."
    )

def test_generate_text_agentic(mock_lite_client, sample_problem):
    # Setup mock for both research and review clients
    instance = mock_lite_client.return_value
    # 1. Researcher draft
    # 2. Reviewer result
    instance.generate_text.side_effect = [sample_problem, sample_problem]
    
    guide = HilbertProblemsGuide()
    result = guide.generate_text(1)
    
    assert result.number == 1
    assert result.title == "The Continuum Hypothesis"
    # researcher + reviewer = 2 calls
    assert instance.generate_text.call_count == 2

def test_generate_text_reviewer_fallback_agentic(mock_lite_client, sample_problem):
    instance = mock_lite_client.return_value
    # Researcher succeeds, Reviewer returns non-structured
    instance.generate_text.side_effect = [sample_problem, "not-structured"]

    guide = HilbertProblemsGuide()
    result = guide.generate_text(1)

    assert result == sample_problem
    assert instance.generate_text.call_count == 2

def test_generate_text_invalid_problem_number_agentic():
    guide = HilbertProblemsGuide()

    with pytest.raises(ValueError, match="between 1 and 23"):
        guide.generate_text(24)

def test_display_summary_agentic(mock_lite_client, capsys):
    instance = mock_lite_client.return_value
    # Researcher draft, Reviewer refined
    instance.generate_text.side_effect = [
        "Researcher summary draft...",
        "Reviewer refined summary..."
    ]
    
    guide = HilbertProblemsGuide()
    guide.display_summary()
    
    captured = capsys.readouterr()
    assert "SUMMARY OF HILBERT'S 23 PROBLEMS" in captured.out
    assert "Reviewer refined summary..." in captured.out
    assert instance.generate_text.call_count == 2
