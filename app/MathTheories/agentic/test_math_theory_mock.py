import pytest
from unittest.mock import patch, MagicMock
import json

from app.MathTheories.agentic.math_theory_element import MathTheoryExplainer
from app.MathTheories.agentic.math_theory_models import (
    TheoryResponse, MathTheory, TheoryExplanation, 
    AudienceLevel, ResearchData, SolutionMethods, ReviewFeedback
)
from lite.config import ModelConfig

@pytest.fixture
def mock_lite_client():
    with patch('app.MathTheories.agentic.math_theory_element.LiteClient') as mock:
        yield mock

def test_explain_theory_agentic(mock_lite_client):
    instance = mock_lite_client.return_value
    
    # 1. Researcher: ResearchData
    research = ResearchData(
        theory_name="Group Theory",
        detailed_history="Abel and Galois...",
        core_axioms_and_rules=["Closure", "Associativity", "Identity", "Invertibility"],
        key_theorems=["Lagrange's Theorem", "Sylow Theorems"],
        modern_applications=["Cryptography", "Particle Physics"],
        connected_theories=["Field Theory", "Ring Theory"],
        current_research_frontiers="Classification of finite simple groups",
        technical_solution_details=SolutionMethods(analytical="Normal subgroups", numerical="GAP software")
    )
    
    # 2. Writer: TheoryExplanation
    explanation = TheoryExplanation(
        audience=AudienceLevel.UNDERGRAD,
        introduction="Intro to Groups",
        key_concepts=["Symmetry", "Permutations"],
        why_it_was_created="To solve polynomial equations",
        problems_solved_or_simplified="Quadratic vs Quintic",
        how_it_is_used_today="Encryption",
        foundation_for_other_theories="Modern Algebra",
        new_research="None",
        solution_methods=SolutionMethods(analytical="Paper", numerical="Computer")
    )
    
    # 3. Reviewer: ReviewFeedback
    feedback = ReviewFeedback(
        is_accurate=True,
        is_audience_appropriate=True,
        critique="Good job",
        required_corrections=None
    )
    
    instance.generate_text.side_effect = [research, explanation, feedback]
    
    explainer = MathTheoryExplainer(ModelConfig(model="mock"))
    result = explainer.fetch_theory_explanation("Group Theory", audience_levels=[AudienceLevel.UNDERGRAD])
    
    assert result.theory_name == "Group Theory"
    assert AudienceLevel.UNDERGRAD in result.explanations
    assert instance.generate_text.call_count == 3
