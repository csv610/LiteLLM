import unittest
from unittest.mock import MagicMock
from object_guesser_game import ObjectGuessingGame
from object_guessing_prompts import PromptBuilder

class TestPromptBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = PromptBuilder(max_questions=10)

    def test_system_prompt_contains_max_questions(self):
        prompt = self.builder.build_system_prompt()
        self.assertIn("10 questions", prompt)

    def test_first_user_prompt(self):
        prompt = self.builder.build_user_prompt([])
        self.assertIn("Start the game", prompt)

    def test_follow_up_user_prompt(self):
        history = [{"role": "assistant", "content": "Is it alive?"}, {"role": "user", "content": "yes"}]
        prompt = self.builder.build_user_prompt(history)
        self.assertIn("ASSISTANT: Is it alive?", prompt)
        self.assertIn("USER: yes", prompt)

class TestObjectGuessingGame(unittest.TestCase):
    def setUp(self):
        # Mocking LiteClient to avoid real API calls
        self.game = ObjectGuessingGame(max_questions=5)
        self.game.client = MagicMock()

    def test_add_to_history(self):
        self.game.add_to_history("user", "yes")
        self.assertEqual(len(self.game.conversation_history), 1)
        self.assertEqual(self.game.conversation_history[0], {"role": "user", "content": "yes"})

    def test_extract_guess_explicit(self):
        guess = self.game.extract_guess("I guess it's a toaster")
        self.assertEqual(guess, "toaster")

        guess = self.game.extract_guess("My guess is: a blue whale!")
        self.assertEqual(guess, "blue whale")

    def test_extract_guess_question_format(self):
        guess = self.game.extract_guess("Is the object a microwave?")
        self.assertEqual(guess, "microwave")

    def test_extract_guess_no_guess(self):
        guess = self.game.extract_guess("Is it larger than a breadbox?")
        self.assertIsNone(guess)

if __name__ == "__main__":
    unittest.main()
