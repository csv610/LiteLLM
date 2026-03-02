import unittest
from unittest.mock import patch, MagicMock
from feymann_tutor_prompts import PromptBuilder
from feymann_tutor import FeynmanTutor

class TestPromptBuilder(unittest.TestCase):
    def test_get_system_prompt(self):
        prompt = PromptBuilder.get_system_prompt()
        self.assertIn("Feynman", prompt)
        self.assertIn("master explainer", prompt)

    def test_get_initial_user_prompt(self):
        topic = "Quantum Mechanics"
        level = "beginner"
        prompt = PromptBuilder.get_initial_user_prompt(topic, level)
        self.assertIn(topic, prompt)
        self.assertIn(level, prompt)

class TestFeynmanTutor(unittest.TestCase):
    def setUp(self):
        self.topic = "Relativity"
        self.level = "intermediate"
        self.tutor = FeynmanTutor(self.topic, self.level)

    @patch('feymann_tutor.completion')
    def test_get_initial_explanation(self, mock_completion):
        # Mock the response from LiteLLM
        mock_completion.side_effect = [{"choices": [{"message": {"content": "Initial explanation"}}]}]

        response = self.tutor.get_initial_explanation()
        
        self.assertEqual(response, "Initial explanation")
        self.assertEqual(len(self.tutor.history), 1)
        self.assertEqual(self.tutor.history[0]["question"], "Initial explanation")

    @patch('feymann_tutor.completion')
    def test_refine_explanation(self, mock_completion):
        mock_completion.side_effect = [
            {"choices": [{"message": {"content": "Refined explanation"}}]},
            {"choices": [{"message": {"content": "Summary content"}}]}
        ]

        # First, we need to begin inquiry to have a history item to respond to
        self.tutor.history = [{"question": "Initial explanation", "response": None}]
        
        response = self.tutor.refine_explanation("I don't understand.")
        
        self.assertEqual(response, "Refined explanation")
        self.assertEqual(len(self.tutor.history), 2)
        self.assertEqual(self.tutor.history[0]["response"], "I don't understand.")
        self.assertEqual(self.tutor.summary, "Summary content")

if __name__ == '__main__':
    unittest.main()
