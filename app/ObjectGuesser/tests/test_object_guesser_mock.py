import unittest
from unittest.mock import MagicMock
import json
from object_guesser_game import ObjectGuesserGame
from object_guessing_prompts import PromptBuilder

class TestPromptBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = PromptBuilder(max_questions=10)

    def test_extraction_prompt(self):
        prompt = self.builder.build_extraction_system_prompt()
        self.assertIn("Extraction Agent", prompt)
        self.assertIn("user_sentiment", prompt)

    def test_state_prompt(self):
        prompt = self.builder.build_state_system_prompt()
        self.assertIn("State Management Agent", prompt)
        self.assertIn("Blackboard", prompt)

    def test_strategy_prompt(self):
        prompt = self.builder.build_strategy_system_prompt()
        self.assertIn("Strategy Agent", prompt)
        self.assertIn("ASK_QUESTION", prompt)

class TestObjectGuesserGame(unittest.TestCase):
    def setUp(self):
        self.game = ObjectGuesserGame(max_questions=5)
        self.game.client = MagicMock()

    def test_add_to_history(self):
        self.game.add_to_history("user", "yes")
        self.assertEqual(len(self.game.conversation_history), 1)
        self.assertEqual(self.game.conversation_history[0], {"role": "user", "content": "yes"})

    def test_call_agent_parsing(self):
        # Mocking a JSON response
        self.game.client.generate_text.return_value = '{"test": "value"}'
        result = self.game._call_agent("system", "user")
        self.assertEqual(result, {"test": "value"})

    def test_call_agent_markdown_parsing(self):
        # Mocking a response with markdown blocks
        self.game.client.generate_text.return_value = 'Here is the JSON:\n```json\n{"test": "markdown"}\n```'
        result = self.game._call_agent("system", "user")
        self.assertEqual(result, {"test": "markdown"})

    def test_update_state(self):
        # Mocking state agent response
        self.game.client.generate_text.return_value = json.dumps({
            "properties": {"is_alive": "yes"},
            "category": "animal",
            "excluded_objects": []
        })
        self.game.update_state()
        self.assertEqual(self.game.blackboard["category"], "animal")
        self.assertEqual(self.game.blackboard["properties"]["is_alive"], "yes")

if __name__ == "__main__":
    unittest.main()
