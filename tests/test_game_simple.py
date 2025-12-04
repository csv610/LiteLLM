#!/usr/bin/env python
"""
Simple test for the object guesser game.
Test object: Apple
"""

import sys
import builtins
from app.cli.object_guesser_game import ObjectGuessingGame

# Pre-programmed answers for "apple"
answers = [
    "yes",      # Is it a living thing? (was once)
    "no",       # Is it an animal?
    "yes",      # Is it a plant (or plant-based)?
    "no",       # Is it still growing in nature?
    "yes",      # Is it food?
    "yes",      # Is it a fruit?
    "no",       # Is it a citrus fruit?
    "yes",      # Does it grow on trees?
    "yes",      # Apple! Correct?
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
    print("Testing with object: APPLE\n")
    game = ObjectGuessingGame(model="gemini/gemini-2.5-flash", temperature=0.7)
    try:
        game.play()
    except EOFError:
        print("\nTest completed!")
