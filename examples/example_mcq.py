"""Example usage of LiteMCQClient for solving multiple-choice questions."""

import sys
sys.path.insert(0, '/Users/csv610/Projects/LiteLLM')

from lite.litellm_mcq_client import LiteMCQClient, print_answer
from lite.config import MCQInput, ModelConfig

model = "ollama/gemma3"


def example_simple_question():
    """Example 1: Simple multiple-choice question."""
    print("\n" + "="*60)
    print("Example 1: Simple Multiple-Choice Question")
    print("="*60)

    client = LiteMCQClient(model=model)

    question = MCQInput(
        question="What is 15 + 23?",
        options=[
            "35",
            "37",
            "38",
            "40"
        ]
    )

    answer = client.solve(question)
    print_answer(answer)


def example_with_context():
    """Example 2: Question with context."""
    print("\n" + "="*60)
    print("Example 2: Question with Context")
    print("="*60)

    client = LiteMCQClient(model=model)

    question = MCQInput(
        question="Based on the context, what year did the American Revolution end?",
        context="""The American Revolutionary War began in 1775 and ended in 1783 with the
Treaty of Paris, which formally recognized American independence. The Declaration of
Independence was signed in 1776, marking the official declaration of independence.""",
        options=[
            "1775",
            "1776",
            "1783",
            "1789"
        ]
    )

    answer = client.solve(question)
    print_answer(answer)


def example_with_dict_options():
    """Example 3: Question with dictionary-style options."""
    print("\n" + "="*60)
    print("Example 3: Question with Dictionary Options")
    print("="*60)

    client = LiteMCQClient(model=model)

    question = MCQInput(
        question="What is the chemical formula for water?",
        options={
            "A": "CO2",
            "B": "H2O",
            "C": "NaCl",
            "D": "O2"
        }
    )

    answer = client.solve(question)
    print_answer(answer)


def example_scientific_question():
    """Example 4: Scientific knowledge question."""
    print("\n" + "="*60)
    print("Example 4: Scientific Knowledge Question")
    print("="*60)

    client = LiteMCQClient(model=model)

    question = MCQInput(
        question="What is the boiling point of water at standard atmospheric pressure?",
        options=[
            "50°C",
            "80°C",
            "100°C",
            "120°C"
        ]
    )

    answer = client.solve(question)
    print_answer(answer)


def example_with_custom_model():
    """Example 5: Using a custom model configuration."""
    print("\n" + "="*60)
    print("Example 5: Custom Model Configuration")
    print("="*60)

    # Initialize client with one model
    client = LiteMCQClient(model=model)

    question = MCQInput(
        question="What is 2 + 2?",
        options=["3", "4", "5", "6"]
    )

    # Solve with a custom model config (different temperature)
    custom_config = ModelConfig(model="gemini/gemini-2.5-flash", temperature=0.1)
    answer = client.solve(question, model_config=custom_config)
    print_answer(answer)


def example_batch_questions():
    """Example 6: Solving multiple questions."""
    print("\n" + "="*60)
    print("Example 6: Batch Processing Multiple Questions")
    print("="*60)

    client = LiteMCQClient(model=model)

    questions = [
        MCQInput(
            question="What is 5 × 6?",
            options=["25", "30", "35", "40"]
        ),
        MCQInput(
            question="How many sides does a hexagon have?",
            options=["4", "5", "6", "8"]
        ),
        MCQInput(
            question="What is the freezing point of water in Celsius?",
            options=["0°C", "-10°C", "10°C", "32°C"]
        ),
    ]

    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i}:")
        answer = client.solve(question)
        print_answer(answer)


def example_multiple_correct_answers():
    """Example 7: Question with multiple correct answers."""
    print("\n" + "="*60)
    print("Example 7: Multiple Correct Answers")
    print("="*60)

    client = LiteMCQClient(model=model)

    question = MCQInput(
        question="Which of the following are even numbers? (Select all that apply)",
        options={
            "A": "2",
            "B": "4",
            "C": "7",
            "D": "8"
        }
    )

    answer = client.solve(question)
    print_answer(answer)


if __name__ == "__main__":
    # Run examples
    example_simple_question()
    example_with_context()
    example_with_dict_options()
    example_scientific_question()
    example_with_custom_model()
    example_batch_questions()
    example_multiple_correct_answers()
