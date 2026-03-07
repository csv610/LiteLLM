import unittest
from unittest.mock import patch, MagicMock
from hadamard_tutor_prompts import PromptBuilder
from hadamard_tutor import HadamardTutorQuestionGenerator

class TestPromptBuilder(unittest.TestCase):
    def test_get_system_prompt(self):
        prompt = PromptBuilder.get_system_prompt()
        self.assertIn("Hadamard", prompt)
        self.assertIn("discovery process", prompt)

    def test_get_instructions(self):
        prompt = PromptBuilder.get_instructions()
        self.assertIn("YOUR ROLE IS EXCLUSIVELY TO GENERATE QUESTIONS", prompt)
        self.assertIn("DO NOT PROVIDE EXPLANATIONS, ANSWERS, OR DIRECT TEACHING", prompt)
        self.assertIn("LEAVE ALL THE DISCOVERY AND EXPLANATION TO THE STUDENT", prompt)

    def test_get_initial_user_prompt(self):
        topic = "Fractals"
        level = "researcher"
        prompt = PromptBuilder.get_initial_user_prompt(topic, level)
        self.assertIn(topic, prompt)
        self.assertIn(level, prompt)
        self.assertIn("Preparation", prompt)
        self.assertIn("Ask me a question", prompt)

class TestHadamardTutorQuestionGenerator(unittest.TestCase):
    def setUp(self):
        self.topic = "Number Theory"
        self.level = "advanced"
        with patch('hadamard_tutor.LiteClient') as mock_client:
            self.mock_client = mock_client.return_value
            self.tutor = HadamardTutorQuestionGenerator(self.topic, self.level)

    def test_get_preparation_phase(self):
        # Mock the response from LiteClient
        self.mock_client.completion.side_effect = [{"choices": [{"message": {"content": "Preparation content"}}]}]

        response = self.tutor.get_preparation_phase()
        
        self.assertEqual(response, "Preparation content")
        self.assertEqual(len(self.tutor.history), 1)
        self.assertEqual(self.tutor.history[0]["question"], "Preparation content")

    def test_get_incubation_phase(self):
        self.mock_client.completion.side_effect = [
            {"choices": [{"message": {"content": "Incubation content"}}]},
            {"choices": [{"message": {"content": "Summary content"}}]}
        ]

        # First, we need to begin inquiry to have a history item to respond to
        self.tutor.history = [{"question": "Preparation content", "response": None}]
        
        response = self.tutor.get_incubation_phase("I'm stuck.")
        
        self.assertEqual(response, "Incubation content")
        self.assertEqual(len(self.tutor.history), 2)
        self.assertEqual(self.tutor.history[0]["response"], "I'm stuck.")
        self.assertEqual(self.tutor.summary, "Summary content")

if __name__ == '__main__':
    unittest.main()
