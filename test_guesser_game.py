#!/usr/bin/env python
"""
Test script for the object guesser game with pre-programmed answers.
"""

import sys
import io
from app.cli.object_guesser_game import ObjectGuessingGame

# Pre-programmed answers (think of a "lamp" as the object)
answers = [
    "yes",      # Is it a physical object?
    "no",       # Is it living?
    "no",       # Is it a person or animal?
    "yes",      # Do you use it indoors?
    "no",       # Is it furniture?
    "yes",      # Does it provide light?
    "no",       # Is it a flashlight?
    "yes",      # Does it need electricity?
    "yes",      # Correct, it's a lamp!
]

answer_iter = iter(answers)

def mock_input(prompt):
    """Mock input to return pre-programmed answers."""
    try:
        answer = next(answer_iter)
        print(f"User: {answer}")
        return answer
    except StopIteration:
        print("User: (no more answers)")
        sys.exit(0)

# Replace input with our mock
import builtins
builtins.input = mock_input

if __name__ == "__main__":
    game = ObjectGuessingGame(model="gemini/gemini-2.5-flash", temperature=0.7)
    try:
        game.play()
    except EOFError:
        print("\nTest completed!")
