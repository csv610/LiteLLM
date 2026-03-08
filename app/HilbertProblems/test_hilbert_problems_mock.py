import pytest
from unittest.mock import patch
import json
import os

from hilbert_problems import HilbertProblemsGuide
from hilbert_problems_models import HilbertProblemModel, ProblemStatus

@pytest.fixture
def mock_lite_client():
    with patch('hilbert_problems.LiteClient') as mock:
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

def test_generate_text(mock_lite_client, sample_problem):
    # Setup mock
    instance = mock_lite_client.return_value
    instance.generate_text.return_value = sample_problem
    
    guide = HilbertProblemsGuide()
    result = guide.generate_text(1)
    
    assert result.number == 1
    assert result.title == "The Continuum Hypothesis"
    instance.generate_text.assert_called_once()

def test_save_to_file(sample_problem, tmp_path):
    guide = HilbertProblemsGuide()
    output_dir = tmp_path / "outputs"
    
    file_path = guide.save_to_file(sample_problem, str(output_dir))
    
    assert os.path.exists(file_path)
    with open(file_path, 'r') as f:
        data = json.load(f)
        assert data['number'] == 1
        assert data['title'] == "The Continuum Hypothesis"

def test_display_problem(sample_problem, capsys):
    HilbertProblemsGuide.display_problem(sample_problem)
    captured = capsys.readouterr()
    assert "HILBERT'S PROBLEM #1" in captured.out
    assert "The Continuum Hypothesis" in captured.out
    assert "STATUS: PARTIALLY_SOLVED" in captured.out

def test_display_summary(mock_lite_client, capsys):
    instance = mock_lite_client.return_value
    instance.generate_text.return_value = "Summary of all problems..."
    
    guide = HilbertProblemsGuide()
    guide.display_summary()
    
    captured = capsys.readouterr()
    assert "SUMMARY OF HILBERT'S 23 PROBLEMS" in captured.out
    assert "Summary of all problems..." in captured.out
    instance.generate_text.assert_called_once()
