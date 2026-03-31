import pytest
from unittest.mock import patch, MagicMock
import json
import os

from app.Riemann.nonagentic.riemann_problems import RiemannTheoryGuide
from app.Riemann.nonagentic.riemann_problems_models import RiemannTheoryModel

@pytest.fixture
def mock_lite_client():
    with patch('app.Riemann.nonagentic.riemann_problems.LiteClient') as mock:
        yield mock

@pytest.fixture
def sample_theory():
    return RiemannTheoryModel(
        name="The Riemann Hypothesis",
        definition="The real part of every non-trivial zero of the Riemann zeta function is 1/2.",
        layperson_explanation="A mystery about the distribution of prime numbers.",
        intuition="The zeroes of the zeta function are perfectly aligned.",
        motivation="To understand the distribution of prime numbers.",
        misconceptions=["It has been proven."],
        historical_context="Proposed by Bernhard Riemann in 1859.",
        limitations="Only applies to the zeta function.",
        modern_developments="Many partial results have been achieved.",
        counterfactual_impact="Number theory would be much less developed.",
        key_properties=["Critical line at Re(s) = 1/2"],
        applications=["Cryptography", "Number Theory"],
        related_concepts=["Zeta Function"],
        significance="One of the most important unsolved problems in mathematics."
    )

def test_generate_text_nonagentic(mock_lite_client, sample_theory):
    instance = mock_lite_client.return_value
    instance.generate_text.return_value = sample_theory
    
    guide = RiemannTheoryGuide()
    result = guide.generate_text("The Riemann Hypothesis")
    
    assert result.name == "The Riemann Hypothesis"
    assert instance.generate_text.call_count == 1

def test_display_summary_nonagentic(mock_lite_client, capsys):
    instance = mock_lite_client.return_value
    instance.generate_text.return_value = "Summary of Riemann theories..."
    
    guide = RiemannTheoryGuide()
    # Mocking available_theories for the test
    guide.available_theories = ["Riemann Hypothesis"]
    guide.display_summary()
    
    captured = capsys.readouterr()
    assert "SUMMARY OF RIEMANN THEORIES" in captured.out
    assert "Summary of Riemann theories..." in captured.out
