import unittest
from unittest.mock import MagicMock, patch
from pydantic import ValidationError
import io
import contextlib

from ScholarWork.nonagentic.scholar_work_models import ScholarMajorWork
from ScholarWork.nonagentic.scholar_work_prompts import PromptBuilder
from ScholarWork.nonagentic.scholar_work_generator import ScholarWorkGenerator
from ScholarWork.nonagentic.scholar_work_cli import display_story, generate_scholar_story

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

    def test_invalid_model_missing_field(self):
        data = {
            "scholar_name": "Albert Einstein",
            # missing major_contribution
            "title": "Bending Space and Time",
            "subtitle": "How Einstein reimagined gravity",
            "story": "Once upon a time in Bern...",
            "key_terms": "Spacetime",
            "impact_summary": "Impact",
            "discussion_questions": ["Q1"]
        }
        with self.assertRaises(ValidationError):
            ScholarMajorWork(**data)

class TestPromptBuilder(unittest.TestCase):
    def test_create_user_prompt(self):
        prompt = PromptBuilder.create_user_prompt("Marie Curie", "Radioactivity")
        self.assertIn("Marie Curie", prompt)
        self.assertIn("Radioactivity", prompt)
        self.assertIn("Scientific American", prompt)

    def test_create_system_prompt(self):
        prompt = PromptBuilder.create_system_prompt()
        self.assertIn("science historian", prompt)
        self.assertIn("science journalism", prompt)

    def test_create_model_input(self):
        model_input = PromptBuilder.create_model_input("Ada Lovelace")
        self.assertIn("user_prompt", model_input)
        self.assertIn("system_prompt", model_input)
        self.assertEqual(model_input["response_format"], ScholarMajorWork)

class TestScholarWorkGenerator(unittest.TestCase):
    @patch('ScholarWork.nonagentic.scholar_work_generator.LiteClient')
    def test_generate_text(self, mock_lite_client):
        # Setup mock
        mock_instance = mock_lite_client.return_value
        expected_story = ScholarMajorWork(
            scholar_name="Albert Einstein",
            major_contribution="General Relativity",
            title="Bending Space and Time",
            subtitle="How Einstein reimagined gravity",
            story="Mocked story content",
            key_terms="Mocked terms",
            impact_summary="Mocked impact",
            discussion_questions=["Q1", "Q2"]
        )
        mock_instance.generate_text.return_value = expected_story

        generator = ScholarWorkGenerator(model_name="test-model")
        result = generator.generate_text("Albert Einstein", "General Relativity")

        self.assertEqual(result.scholar_name, "Albert Einstein")
        self.assertEqual(result.story, "Mocked story content")
        mock_instance.generate_text.assert_called_once()

    def test_get_model_info(self):
        generator = ScholarWorkGenerator(model_name="test-model", temperature=0.5)
        info = generator.get_model_info()
        self.assertEqual(info["model_name"], "test-model")
        self.assertEqual(info["temperature"], 0.5)

    def test_update_model(self):
        generator = ScholarWorkGenerator(model_name="old-model")
        generator.update_model("new-model", temperature=0.8)
        self.assertEqual(generator.model_name, "new-model")
        self.assertEqual(generator.model_config.temperature, 0.8)

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
        self.assertIn("BENDING SPACE AND TIME", output.upper())
        self.assertIn("Albert Einstein", output)
        self.assertIn("KEY TERMS & CONCEPTS", output)
        self.assertIn("IMPACT SUMMARY", output)
        self.assertIn("DISCUSSION QUESTIONS", output)

    @patch('ScholarWork.nonagentic.scholar_work_cli.ScholarWorkGenerator')
    def test_generate_scholar_story(self, mock_generator_class):
        mock_generator = mock_generator_class.return_value
        expected_story = MagicMock(spec=ScholarMajorWork)
        mock_generator.generate_text.return_value = expected_story
        
        result = generate_scholar_story("Albert Einstein", "General Relativity", "test-model")
        
        self.assertEqual(result, expected_story)
        mock_generator_class.assert_called_with(model_name="test-model")
        mock_generator.generate_text.assert_called_with("Albert Einstein", "General Relativity")

if __name__ == "__main__":
    unittest.main()
