import unittest
from unittest.mock import patch, MagicMock
from socrates_tutor_prompts import PromptBuilder
from socrates_tutor import SocratesTutor

class TestPromptBuilder(unittest.TestCase):
    def test_get_system_prompt(self):
        prompt = PromptBuilder.get_system_prompt()
        self.assertIn("Socratic Method", prompt)
        self.assertNotIn("Hadamard", prompt)

    def test_get_initial_user_prompt(self):
        topic = "Justice"
        level = "student"
        prompt = PromptBuilder.get_initial_user_prompt(topic, level)
        self.assertIn(topic, prompt)
        self.assertIn(level, prompt)
        self.assertIn("initial definition", prompt)

class TestSocratesTutor(unittest.TestCase):
    def setUp(self):
        self.topic = "The Nature of Good"
        self.level = "curious"
        self.tutor = SocratesTutor(self.topic, self.level)

    @patch('socrates_tutor.completion')
    def test_begin_inquiry(self, mock_completion):
        # Mock the response from LiteLLM
        mock_response = {
            "choices": [{"message": {"content": "What is 'good'?"}}]
        }
        mock_completion.return_value = mock_response

        response = self.tutor.begin_inquiry()
        
        self.assertEqual(response, "What is 'good'?")
        self.assertEqual(len(self.tutor.history), 1)
        self.assertEqual(self.tutor.history[0]["question"], "What is 'good'?")
        self.assertEqual(self.tutor.history[0]["response"], None)

    @patch('socrates_tutor.completion')
    def test_provide_response(self, mock_completion):
        # We need to handle two calls: _ask_llm and _update_summary
        mock_completion.side_effect = [
            {"choices": [{"message": {"content": "Can you explain further?"}}]},
            {"choices": [{"message": {"content": "Summary content"}}]}
        ]

        # First, we need to begin inquiry to have a history item to respond to
        self.tutor.history = [{"question": "What is 'good'?", "response": None}]
        
        response = self.tutor.provide_response("Good is helping people.")
        
        self.assertEqual(response, "Can you explain further?")
        self.assertEqual(len(self.tutor.history), 2)
        self.assertEqual(self.tutor.history[0]["response"], "Good is helping people.")
        self.assertEqual(self.tutor.history[1]["question"], "Can you explain further?")
        self.assertEqual(self.tutor.summary, "Summary content")

if __name__ == '__main__':
    unittest.main()
