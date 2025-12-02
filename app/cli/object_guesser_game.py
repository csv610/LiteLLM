"""
Object Guessing Game using LiteClient

The LLM plays a guessing game where the user thinks of an object,
and the LLM asks yes/no questions to identify it.

The LLM keeps track of answers and asks smart questions to minimize
the number of questions needed to identify the object.
"""

import json
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput


class ObjectGuessingGame:
    """
    A guessing game where the LLM tries to identify an object
    thought of by the user through yes/no questions.
    """

    def __init__(self, model: str = "gemini/gemini-2.5-flash", temperature: float = 0.7):
        """
        Initialize the guessing game.

        Args:
            model: The model to use for generating questions
            temperature: Temperature for model responses (0.7 for more varied questions)
        """
        self.model_config = ModelConfig(model=model, temperature=temperature)
        self.client = LiteClient(model_config=self.model_config)
        self.conversation_history = []
        self.question_count = 0
        self.max_questions = 20

    def add_to_history(self, role: str, content: str):
        """Add a message to conversation history."""
        self.conversation_history.append({"role": role, "content": content})

    def build_system_prompt(self) -> str:
        """Build the system prompt for the LLM."""
        return """You are playing a guessing game. The user has thought of an object,
and your job is to identify it by asking yes/no questions.

RULES:
1. Ask strategic yes/no questions to narrow down what the object is
2. Keep track of all previous answers to avoid contradictions
3. Ask questions that help you eliminate as many possibilities as possible
4. After you have enough information, make a guess
5. If you identify the object correctly, the game ends

STRATEGY:
- Start with broad categories (Is it a person? Is it an animal? Is it living?)
- Then narrow down (Is it a common object? Is it made of metal?)
- Use previous answers to inform follow-up questions
- Once you're confident, make your guess in the format: "I guess it's a [OBJECT_NAME]"
- Keep your responses concise - ask ONE question per turn (except for your guess)

Remember: You have 20 questions to identify the object. Make them count!"""

    def get_llm_question(self) -> str:
        """Get the next question from the LLM."""
        # Build conversation context
        conversation_context = "\n".join(
            [f"{msg['role'].upper()}: {msg['content']}" for msg in self.conversation_history]
        )

        system_prompt = self.build_system_prompt()

        if not self.conversation_history:
            # First question
            prompt = f"{system_prompt}\n\nStart the game by asking your first yes/no question to identify the object."
        else:
            # Follow-up questions
            prompt = f"""{system_prompt}

Previous conversation:
{conversation_context}

Based on the answers so far, ask your next yes/no question to identify the object.
Remember to keep track of all previous answers and avoid asking contradictory questions.
Only ask yes/no questions (or make a guess when you're confident)."""

        model_input = ModelInput(user_prompt=prompt)
        response = self.client.generate_text(model_input=model_input)

        if isinstance(response, dict) and "error" in response:
            raise Exception(f"Error from LLM: {response['error']}")

        return response

    def extract_guess(self, text: str) -> str | None:
        """Extract a guess from the LLM response if it made one."""
        lower_text = text.lower()

        # Check for explicit guess patterns first
        explicit_patterns = [
            "i guess it's a ",
            "i guess it's ",
            "i guess: ",
            "my guess is a ",
            "my guess is ",
        ]

        for pattern in explicit_patterns:
            if pattern in lower_text:
                # Find the position after the pattern
                start = lower_text.find(pattern) + len(pattern)
                # Extract until punctuation or newline
                remaining = text[start:].split('\n')[0]
                guess = remaining.split('!')[0].split('?')[0].split('.')[0].strip()

                # Validate that the guess looks like an actual object name
                # Should be relatively short (1-4 words) and not contain analysis language
                if guess and len(guess) > 0:
                    words = guess.split()
                    # Reject if too many words or contains analysis keywords
                    if len(words) <= 4 and not any(keyword in lower_text[lower_text.find(pattern):lower_text.find(pattern)+len(pattern)+len(guess)+20] for keyword in ["is ", "are ", "have ", "contains ", "made of "]):
                        return guess

        # Check for identification questions like "Is the object a [thing]?"
        import re
        question_pattern = r'is the object(?:\s+something)?\s+a\s+([a-z\s]+)\?'
        match = re.search(question_pattern, lower_text)
        if match:
            guess = match.group(1).strip()
            if guess and len(guess) > 0:
                words = guess.split()
                if len(words) <= 4:
                    return guess

        return None

    def play(self):
        """Main game loop."""
        print("\n" + "=" * 60)
        print("OBJECT GUESSING GAME")
        print("=" * 60)
        print("\nThink of an object and keep it in mind.")
        print("The LLM will ask yes/no questions to identify it.")
        print("Answer with 'yes', 'no', or 'somewhat' (for partial matches).\n")

        while self.question_count < self.max_questions:
            try:
                # Get question from LLM
                question = self.get_llm_question()
                self.add_to_history("assistant", question)
                self.question_count += 1

                print(f"\n[Question {self.question_count}] LLM: {question}")

                # Check if LLM made a guess
                guess = self.extract_guess(question)
                if guess:
                    print(f"\nLLM's Guess: Is it a {guess}?")
                    user_answer = input("User: ").strip().lower()

                    if user_answer in ["yes", "y", "correct", "that's right"]:
                        print(f"\n🎉 Correct! The object was a {guess}!")
                        print(f"The LLM identified it in {self.question_count} questions.")
                        return True
                    else:
                        print(f"\nLLM's guess was wrong. Let me ask more questions...")
                        self.add_to_history("user", f"No, it's not a {guess}. Keep trying.")
                        continue

                # Get user's answer
                user_answer = input("User (yes/no/somewhat): ").strip().lower()

                # Validate input
                if user_answer not in ["yes", "y", "no", "n", "somewhat", "kind of", "sort of"]:
                    print("Please answer with 'yes', 'no', or 'somewhat'.")
                    continue

                # Normalize answer
                if user_answer in ["y"]:
                    user_answer = "yes"
                elif user_answer in ["n"]:
                    user_answer = "no"

                self.add_to_history("user", user_answer)

            except KeyboardInterrupt:
                print("\n\nGame interrupted by user.")
                return False
            except Exception as e:
                print(f"\nError: {e}")
                print("Retrying...")
                continue

        print(f"\nGame Over! The LLM couldn't identify the object in {self.max_questions} questions.")
        print("Better luck next time!")
        return False


def main():
    """Main entry point for the game."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Play an object guessing game with an LLM"
    )
    parser.add_argument(
        "--model",
        default="gemini/gemini-2.5-flash",
        help="Model to use (default: gemini/gemini-2.5-flash)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Temperature for model responses (default: 0.7)",
    )

    args = parser.parse_args()

    game = ObjectGuessingGame(model=args.model, temperature=args.temperature)
    game.play()


if __name__ == "__main__":
    main()
