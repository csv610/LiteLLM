import unittest
from unittest.mock import MagicMock
import json
from .object_guesser_game import ObjectGuessingGame
from .object_guessing_prompts import PromptBuilder

class TestPromptBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = PromptBuilder(max_questions=10)

    def test_user_prompt(self):
        prompt = self.builder.build_user_prompt([])
        self.assertIn("think of an object", prompt)

class TestObjectGuessingGame(unittest.TestCase):
    def setUp(self):
        self.game = ObjectGuessingGame(max_questions=5)
        self.game.client = MagicMock()

    def test_add_to_history(self):
        self.game.add_to_history("user", "yes")
        self.assertEqual(len(self.game.conversation_history), 1)
        self.assertEqual(self.game.conversation_history[0], {"role": "user", "content": "yes"})

    def test_get_llm_question(self):
        # Mocking a response
        self.game.client.generate_text.return_value = "Is it a fruit?"
        result = self.game.get_llm_question()
        self.assertEqual(result, "Is it a fruit?")

    def test_extract_guess(self):
        # Test extraction from various patterns
        self.assertEqual(self.game.extract_guess("I guess it's a apple."), "apple")
        self.assertEqual(self.game.extract_guess("Is the object a banana?"), "banana")
        self.assertEqual(self.game.extract_guess("My guess is: orange!"), "orange")
        self.assertEqual(self.game.extract_guess("Just asking a question?"), None)

if __name__ == "__main__":
    unittest.main()
