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
        with patch('socrates_tutor.LiteClient') as mock_client:
            self.mock_client = mock_client.return_value
            self.tutor = SocratesTutor(self.topic, self.level)

    def test_begin_inquiry(self):
        # Mock the response from LiteClient
        mock_response = {
            "choices": [{"message": {"content": "What is 'good'?"}}]
        }
        self.mock_client.completion.return_value = mock_response

        response = self.tutor.begin_inquiry()
        
        self.assertEqual(response, "What is 'good'?")
        self.assertEqual(len(self.tutor.history), 1)
        self.assertEqual(self.tutor.history[0]["question"], "What is 'good'?")
        self.assertEqual(self.tutor.history[0]["response"], None)

    def test_provide_response(self):
        # We need to handle two calls: _ask_llm and _update_summary
        self.mock_client.completion.side_effect = [
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
