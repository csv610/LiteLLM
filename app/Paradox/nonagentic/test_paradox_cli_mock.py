import sys
from unittest.mock import patch
from .paradox_cli import paradox_to_markdown, arguments_parser
from .paradox_models import Paradox, AudienceLevel, ParadoxStatus

def test_arguments_parser_default():
    with patch.object(sys, 'argv', ['paradox_cli.py']):
        args = arguments_parser()
        assert args.paradox == "Zeno's paradox"
        assert args.level == "undergrad"

def test_arguments_parser_custom():
    with patch.object(sys, 'argv', ['paradox_cli.py', '-p', 'Fermi paradox', '-l', 'phd']):
        args = arguments_parser()
        assert args.paradox == "Fermi paradox"
        assert args.level == "phd"

def test_paradox_to_markdown():
    mock_paradox = Paradox(
        paradox_name="Test Paradox",
        explanations={
            AudienceLevel.UNDERGRAD: {
                "introduction": "Intro content",
                "status": ParadoxStatus.SOLVED,
                "root_cause": "Hidden assumptions content",
                "key_concepts": ["Concept 1", "Concept 2"],
                "historical_context": "History content",
                "the_contradiction": "Contradiction content",
                "modern_relevance": "Modern content",
                "impact_on_thought": "Impact content",
                "current_debates": "Debates content",
                "resolutions": {
                    "who_solved": "Person X",
                    "how_it_was_solved": "Method Y",
                    "logical": "L content",
                    "mathematical": "M content"
                }
            }
        }
    )
    
    md = paradox_to_markdown(mock_paradox)
    assert "# Test Paradox" in md
    assert "**Who Solved It:** Person X" in md
    assert "**How It Was Solved:** Method Y" in md
    assert "### Root Cause" in md
    assert "Hidden assumptions content" in md
    assert "## Audience Level: Undergrad" in md
    assert "### Introduction\nIntro content" in md
    assert "- Concept 1" in md
    assert "**Logical Details:** L content" in md
