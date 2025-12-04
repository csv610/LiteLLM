#!/usr/bin/env python
"""
Complete test for the object guesser game with more answers to reach a guess.
Test object: Dog
"""

import sys
import builtins
from app.cli.object_guesser_game import ObjectGuessingGame

# Pre-programmed answers for "dog"
answers = [
    "yes",      # Is it living?
    "yes",      # Is it an animal?
    "no",       # Is it a bird?
    "yes",      # Is it a mammal?
    "no",       # Is it a wild animal?
    "yes",      # Is it a pet/domestic animal?
    "yes",      # Is it a four-legged animal?
    "no",       # Is it a cat?
    "yes",      # Does it bark?
    "yes",      # Dog? Correct!
]

answer_iter = iter(answers)

def mock_input(prompt):
    """Mock input to return pre-programmed answers."""
    try:
        answer = next(answer_iter)
        print(f"User: {answer}")
        return answer
    except StopIteration:
        print("User: (out of answers)")
        sys.exit(0)

# Replace input with our mock
builtins.input = mock_input

if __name__ == "__main__":
    print("Testing with object: DOG\n")
    game = ObjectGuessingGame(model="gemini/gemini-2.5-flash", temperature=0.7)
    try:
        game.play()
    except EOFError:
        print("\nTest completed!")
