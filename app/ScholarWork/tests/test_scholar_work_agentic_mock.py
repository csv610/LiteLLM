import unittest
from unittest.mock import MagicMock, patch
from pydantic import ValidationError
import io
import contextlib

from ScholarWork.agentic.scholar_work_models import ScholarMajorWork, ResearchBrief
from ScholarWork.agentic.scholar_work_generator import ScholarWorkGenerator
from ScholarWork.agentic.scholar_work_cli import display_story, generate_scholar_story

class TestScholarMajorWorkModel(unittest.TestCase):
    def test_valid_model(self):
        data = {
            "scholar_name": "Albert Einstein",
            "major_contribution": "General Relativity",
            "title": "Bending Space and Time",
            "subtitle": "How Einstein reimagined gravity",
            "story": "Once upon a time in Bern...",
            "key_terms": "Spacetime: the four-dimensional manifold...",
            "impact_summary": "Changed our understanding of the universe.",
            "discussion_questions": ["What is spacetime?", "Why is it curved?"]
        }
        model = ScholarMajorWork(**data)
        self.assertEqual(model.scholar_name, "Albert Einstein")
        self.assertEqual(len(model.discussion_questions), 2)

class TestResearchBriefModel(unittest.TestCase):
    def test_valid_brief(self):
        data = {
            "scholar_name": "Marie Curie",
            "major_contribution": "Radioactivity",
            "historical_context": "Late 19th century physics...",
            "scientific_core": "Spontaneous emission of radiation...",
            "revolutionary_impact": "Challenged the indivisibility of atoms.",
            "modern_legacy": ["Cancer treatment", "Nuclear power"],
            "key_anecdotes": ["Mobile X-ray units in WWI"]
        }
        model = ResearchBrief(**data)
        self.assertEqual(model.scholar_name, "Marie Curie")
        self.assertEqual(len(model.modern_legacy), 2)

class TestScholarWorkGenerator(unittest.TestCase):
    @patch('ScholarWork.agentic.scholar_work_generator.LiteClient')
    def test_generate_text(self, mock_lite_client):
        # Setup mock
        mock_instance = mock_lite_client.return_value
        
        # Mock researcher output
        mock_brief = ResearchBrief(
            scholar_name="Albert Einstein",
            major_contribution="General Relativity",
            historical_context="...",
            scientific_core="...",
            revolutionary_impact="...",
            modern_legacy=["..."],
            key_anecdotes=["..."]
        )
        
        # Mock journalist output
        mock_story_text = "Once upon a time..."
        
        # Mock editor output
        mock_final_story = ScholarMajorWork(
            scholar_name="Albert Einstein",
            major_contribution="General Relativity",
            title="Bending Space and Time",
            subtitle="...",
            story=mock_story_text,
            key_terms="...",
            impact_summary="...",
            discussion_questions=["..."]
        )
        
        # Configure the mock to return different values for each call
        mock_instance.generate_text.side_effect = [mock_brief, mock_story_text, mock_final_story]

        generator = ScholarWorkGenerator(model_name="test-model")
        
        # Use a dummy callback
        callback = MagicMock()
        
        result = generator.generate_text("Albert Einstein", "General Relativity", progress_callback=callback)

        self.assertEqual(result.scholar_name, "Albert Einstein")
        self.assertEqual(result.story, "Once upon a time...")
        self.assertEqual(mock_instance.generate_text.call_count, 3)
        self.assertEqual(callback.call_count, 3)

    def test_get_model_info(self):
        generator = ScholarWorkGenerator(model_name="test-model", temperature=0.5)
        info = generator.get_model_info()
        self.assertEqual(info["model_name"], "test-model")
        self.assertEqual(info["temperature"], 0.5)

class TestCLI(unittest.TestCase):
    def test_display_story(self):
        story = ScholarMajorWork(
            scholar_name="Albert Einstein",
            major_contribution="General Relativity",
            title="Bending Space and Time",
            subtitle="How Einstein reimagined gravity",
            story="Once upon a time there was space and time...",
            key_terms="Spacetime: matter",
            impact_summary="Impact on science",
            discussion_questions=["Q1", "Q2"]
        )
        
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            display_story(story)
        
        output = f.getvalue()
        self.assertIn("BENDING SPACE AND TIME", output)
        self.assertIn("Albert Einstein", output)

    @patch('ScholarWork.agentic.scholar_work_cli.ScholarWorkGenerator')
    def test_generate_scholar_story(self, mock_generator_class):
        mock_generator = mock_generator_class.return_value
        expected_story = MagicMock(spec=ScholarMajorWork)
        mock_generator.generate_text.return_value = expected_story
        
        result = generate_scholar_story("Albert Einstein", "General Relativity", "test-model")
        
        self.assertEqual(result, expected_story)
        mock_generator_class.assert_called_with(model_name="test-model")
        mock_generator.generate_text.assert_called()

if __name__ == "__main__":
    unittest.main()
