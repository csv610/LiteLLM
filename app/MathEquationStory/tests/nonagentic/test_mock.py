import unittest
from unittest.mock import MagicMock, patch
from pydantic import ValidationError
import io
import contextlib

from MathEquationStory.nonagentic.math_equation_story_models import MathematicalEquationStory
from MathEquationStory.nonagentic.math_equation_story_prompts import PromptBuilder
from MathEquationStory.nonagentic.math_equation_story_generator import MathEquationStoryGenerator
from MathEquationStory.assets.well_known_equations import (
    get_equation_by_name, 
    get_equations_by_category, 
    EquationCategory,
    ALL_EQUATIONS
)
from MathEquationStory.nonagentic.math_equation_story_cli import display_story, generate_equation_story

class TestMathematicalEquationStoryModel(unittest.TestCase):
    def test_valid_model(self):
        data = {
            "equation_name": "E=mc²",
            "latex_formula": "E = mc^2",
            "title": "Energy and Mass",
            "subtitle": "The most famous equation",
            "story": "Once upon a time...",
            "vocabulary_notes": "Mass: amount of matter",
            "discussion_questions": ["What is E?", "What is m?", "What is c?"]
        }
        model = MathematicalEquationStory(**data)
        self.assertEqual(model.equation_name, "E=mc²")
        self.assertEqual(len(model.discussion_questions), 3)

    def test_invalid_model_missing_field(self):
        data = {
            "equation_name": "E=mc²",
            # missing latex_formula
            "title": "Energy and Mass",
            "subtitle": "The most famous equation",
            "story": "Once upon a time...",
            "vocabulary_notes": "Mass: amount of matter",
            "discussion_questions": ["What is E?"]
        }
        with self.assertRaises(ValidationError):
            MathematicalEquationStory(**data)

class TestPromptBuilder(unittest.TestCase):
    def test_create_user_prompt(self):
        prompt = PromptBuilder.create_user_prompt("Pythagorean Theorem")
        self.assertIn("Pythagorean Theorem", prompt)
        self.assertIn("Scientific American", prompt)

    def test_create_system_prompt(self):
        prompt = PromptBuilder.create_system_prompt()
        self.assertIn("science writer", prompt)
        self.assertIn("Scientific American", prompt)

    def test_create_model_input(self):
        model_input = PromptBuilder.create_model_input("E=mc²")
        self.assertIn("user_prompt", model_input)
        self.assertIn("system_prompt", model_input)
        self.assertEqual(model_input["response_format"], MathematicalEquationStory)

class TestMathEquationStoryGenerator(unittest.TestCase):
    @patch('MathEquationStory.nonagentic.math_equation_story_generator.LiteClient')
    def test_generate_text(self, mock_lite_client):
        # Setup mock
        mock_instance = mock_lite_client.return_value
        expected_story = MathematicalEquationStory(
            equation_name="E=mc²",
            latex_formula="E = mc^2",
            title="Energy and Mass",
            subtitle="The most famous equation",
            story="Mocked story content",
            vocabulary_notes="Mocked notes",
            discussion_questions=["Q1", "Q2"]
        )
        mock_instance.generate_text.return_value = expected_story

        generator = MathEquationStoryGenerator(model_name="test-model")
        result = generator.generate_text("E=mc²")

        self.assertEqual(result.equation_name, "E=mc²")
        self.assertEqual(result.story, "Mocked story content")
        mock_instance.generate_text.assert_called_once()

    def test_get_model_info(self):
        generator = MathEquationStoryGenerator(model_name="test-model", temperature=0.5)
        info = generator.get_model_info()
        self.assertEqual(info["model_name"], "test-model")
        self.assertEqual(info["temperature"], 0.5)

    def test_update_model(self):
        generator = MathEquationStoryGenerator(model_name="old-model")
        generator.update_model("new-model", temperature=0.8)
        self.assertEqual(generator.model_name, "new-model")
        self.assertEqual(generator.model_config.temperature, 0.8)

class TestWellKnownEquations(unittest.TestCase):
    def test_get_equation_by_name(self):
        eq = get_equation_by_name("Pythagorean Theorem")
        self.assertEqual(eq.name, "Pythagorean Theorem")
        self.assertEqual(eq.latex, "a^2 + b^2 = c^2")

    def test_get_equation_by_name_not_found(self):
        with self.assertRaises(ValueError):
            get_equation_by_name("Non-existent Equation")

    def test_get_equations_by_category(self):
        physics_eqs = get_equations_by_category(EquationCategory.PHYSICS)
        self.assertTrue(len(physics_eqs) > 0)
        for eq in physics_eqs:
            self.assertEqual(eq.category, EquationCategory.PHYSICS)

    def test_all_equations_not_empty(self):
        self.assertTrue(len(ALL_EQUATIONS) > 0)

class TestCLI(unittest.TestCase):
    def test_display_story(self):
        story = MathematicalEquationStory(
            equation_name="E=mc²",
            latex_formula="E = mc^2",
            title="Energy and Mass",
            subtitle="The most famous equation",
            story="Once upon a time there was energy...",
            vocabulary_notes="Mass: matter",
            discussion_questions=["Q1", "Q2"]
        )
        
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            display_story(story)
        
        output = f.getvalue()
        self.assertIn("Energy and Mass", output)
        self.assertIn("E=mc²", output)
        self.assertIn("VOCABULARY & CONCEPTS", output)
        self.assertIn("DISCUSSION QUESTIONS", output)

    @patch('MathEquationStory.nonagentic.math_equation_story_cli.MathEquationStoryGenerator')
    def test_generate_equation_story(self, mock_generator_class):
        mock_generator = mock_generator_class.return_value
        expected_story = MagicMock(spec=MathematicalEquationStory)
        mock_generator.generate_text.return_value = expected_story
        
        result = generate_equation_story("E=mc²", "test-model")
        
        self.assertEqual(result, expected_story)
        mock_generator_class.assert_called_with(model_name="test-model")
        mock_generator.generate_text.assert_called_with("E=mc²")

if __name__ == "__main__":
    unittest.main()
