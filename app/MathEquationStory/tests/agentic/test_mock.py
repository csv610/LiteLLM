import pytest
from unittest.mock import patch, MagicMock
import json

from app.MathEquationStory.agentic.math_equation_story_generator import MathEquationStoryGenerator
from app.MathEquationStory.agentic.math_equation_story_models import (
    MathematicalEquationStory, ResearchBrief
)
from lite.config import ModelConfig

@pytest.fixture
def mock_lite_client():
    with patch('app.MathEquationStory.agentic.math_equation_story_generator.LiteClient') as mock:
        yield mock

def test_generate_story_agentic(mock_lite_client):
    instance = mock_lite_client.return_value
    
    # 1. Researcher: ResearchBrief
    brief = ResearchBrief(
        equation_name="e=mc^2",
        historical_context="Einstein 1905",
        mathematical_core="Mass-energy equivalence",
        real_world_applications=["Nuclear power"],
        key_metaphors=["Energy as frozen mass"],
        common_misconceptions=["Mass is created"]
    )
    
    # 2. Journalist/Editor: MathematicalEquationStory
    story = MathematicalEquationStory(
        equation_name="e=mc^2",
        latex_formula="e=mc^2",
        title="The Energy of Light",
        subtitle="Mass and Energy",
        story="Long ago...",
        vocabulary_notes="Mass, Energy",
        discussion_questions=["What is light?"]
    )
    
    # The pipeline is Researcher -> Journalist -> Editor. 
    # Let's check the generator to see how many calls it makes.
    instance.generate_text.side_effect = [brief, story, story]
    
    generator = MathEquationStoryGenerator()
    result = generator.generate_text("e=mc^2")
    
    assert result.equation_name == "e=mc^2"
    assert instance.generate_text.call_count == 3
