import pytest
from pydantic import ValidationError
from paradox_models import (
    AudienceLevel, ParadoxResolution, ParadoxExplanation, Paradox, ParadoxResponse, ParadoxStatus
)

def test_audience_level_enum():
    assert AudienceLevel.GENERAL == "general"
    assert AudienceLevel.RESEARCHER == "researcher"

def test_paradox_status_enum():
    assert ParadoxStatus.SOLVED == "Solved"
    assert ParadoxStatus.UNSOLVED == "Unsolved"

def test_paradox_resolution_model():
    res = ParadoxResolution(
        who_solved="Someone", 
        how_it_was_solved="By doing something", 
        logical="Logic here", 
        mathematical="Math here"
    )
    assert res.who_solved == "Someone"
    assert res.how_it_was_solved == "By doing something"
    assert res.logical == "Logic here"
    assert res.mathematical == "Math here"

def test_paradox_explanation_model():
    exp_data = {
        "introduction": "Intro",
        "status": ParadoxStatus.SOLVED,
        "root_cause": "Hidden assumptions",
        "key_concepts": ["Concept 1"],
        "historical_context": "History",
        "the_contradiction": "Contradiction",
        "modern_relevance": "Modern",
        "impact_on_thought": "Impact",
        "current_debates": "Debates",
        "resolutions": {
            "who_solved": "Mathematicians",
            "how_it_was_solved": "Calculus",
            "logical": "L",
            "mathematical": "M"
        }
    }
    exp = ParadoxExplanation(**exp_data)
    assert exp.introduction == "Intro"
    assert exp.status == ParadoxStatus.SOLVED
    assert exp.resolutions.who_solved == "Mathematicians"
    assert exp.resolutions.how_it_was_solved == "Calculus"

def test_paradox_model():
    paradox_data = {
        "paradox_name": "Test Paradox",
        "explanations": {
            AudienceLevel.UNDERGRAD: {
                "introduction": "Intro",
                "status": ParadoxStatus.UNSOLVED,
                "root_cause": "Hidden assumptions",
                "key_concepts": ["Concept 1"],
                "historical_context": "History",
                "the_contradiction": "Contradiction",
                "modern_relevance": "Modern",
                "impact_on_thought": "Impact",
                "current_debates": "Debates",
                "resolutions": {
                    "who_solved": "Nobody",
                    "how_it_was_solved": "Not yet",
                    "logical": "L",
                    "mathematical": "M"
                }
            }
        }
    }
    p = Paradox(**paradox_data)
    assert p.paradox_name == "Test Paradox"
    assert p.explanations[AudienceLevel.UNDERGRAD].status == ParadoxStatus.UNSOLVED
    assert AudienceLevel.UNDERGRAD in p.explanations

def test_invalid_paradox_model():
    with pytest.raises(ValidationError):
        # Missing required fields
        Paradox(paradox_name="Incomplete")
