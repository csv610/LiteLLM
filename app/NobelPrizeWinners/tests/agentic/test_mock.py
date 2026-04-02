import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

# Add project root to sys.path
root = Path(__file__).parent.parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from NobelPrizeWinners.agentic.nobel_prize_explorer import NobelPrizeWinnerInfo
from NobelPrizeWinners.agentic.nobel_prize_models import (
    PrizeWinner, PrizeResponse, PersonalBackground, BroaderRecognition, FAQItem, GlossaryItem
)
from lite.config import ModelConfig


@pytest.fixture
def mock_lite_client():
    with patch("NobelPrizeWinners.agentic.nobel_prize_explorer.LiteClient") as mock:
        yield mock


def test_fetch_nobel_agentic(mock_lite_client):
    # Create a minimal PrizeWinner instance
    winner = PrizeWinner(
        name="Pierre Agostini",
        year=2023,
        category="Physics",
        contribution="For experimental methods that generate attosecond pulses of light for the study of electron dynamics in matter.",
        personal_background=PersonalBackground(
            birth_date="1941-07-23",
            birth_place="Tunis, Tunisia",
            nationality="French-American",
            family_background="Grew up in Tunisia.",
            education=["Ph.D., Aix-Marseille University (1968)"],
            early_influences="Influenced by the development of laser physics."
        ),
        career_timeline=[{
            "title": "Professor",
            "institution": "Ohio State University",
            "location": "Columbus, USA",
            "start_year": 2005,
            "description": "Professor of Physics."
        }],
        broader_recognition=BroaderRecognition(
            honors_and_awards=["Nobel Prize in Physics"],
            academy_memberships=["Member of NAS"],
            editorial_roles=[],
            mentorship_contributions="Mentored many students.",
            leadership_roles=[],
            public_engagement="Public speaker."
        ),
        history="Chronological history of discovery that contains more than fifty characters to pass validation requirements correctly.",
        impact="Measurable scientific impact that contains more than fifty characters to pass validation requirements correctly.",
        foundation="Specific ways this discovery influenced that contains more than fifty characters to pass validation requirements.",
        applications=["Attosecond spectroscopy"],
        relevancy="How the idea is still valid that contains more than fifty characters to pass validation requirements correctly.",
        advancements=["New laser techniques"],
        refinements=["Better resolution"],
        gaps=["Even shorter pulses"],
        keywords=["attosecond", "physics"],
        learning_objectives=["Understanding electron dynamics"],
        faq=[FAQItem(question="What is an attosecond?", answer="10^-18 seconds")],
        glossary=[GlossaryItem(term="Attosecond", definition="A very short time.")]
    )
    
    response = PrizeResponse(winners=[winner])
    
    # Mock LiteClient instance
    mock_instance = mock_lite_client.return_value
    # Two agent passes: generation and validation
    mock_instance.generate_text.side_effect = [response, response]

    mock_config = ModelConfig(model="test-model", temperature=0.2)
    agent = NobelPrizeWinnerInfo(mock_config)
    agent.logger = MagicMock()
    
    # Call the correct method with correct arguments
    result = agent.fetch_winners("Physics", "2023", "test-model")

    assert len(result) == 1
    assert result[0].name == "Pierre Agostini"
    assert result[0].year == 2023
    assert mock_instance.generate_text.call_count == 2
