"""
Advanced examples of using the MultipleChoiceSolver with context and multiple images.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from multiple_choice_solver import (
    MultipleChoiceSolver,
    MultipleChoiceQuestion,
)


def example_1_with_context():
    """Example 1: Question with context."""
    print("\n" + "="*60)
    print("Example 1: Question with context")
    print("="*60)

    solver = MultipleChoiceSolver()

    context = """
    The Eiffel Tower was built for the 1889 World's Fair in Paris.
    It was designed by Gustave Eiffel and initially intended to be temporary.
    However, due to its popularity and cultural significance, it was made permanent.
    """

    question = MultipleChoiceQuestion(
        question="Who designed the Eiffel Tower?",
        options=["André Breton", "Gustave Eiffel", "Le Corbusier", "Henri Labrouste"],
        context=context
    )

    answer = solver.solve(question)
    if answer:
        print(f"Question: {answer.question}")
        print(f"Correct Answer(s): {', '.join([f'{o.key}: {o.value}' for o in answer.correct_options])}")
        print(f"Confidence: {answer.confidence:.1%}")
        print(f"Reasoning: {answer.reasoning}")


def example_2_with_multiple_images():
    """Example 2: Question with multiple images."""
    print("\n" + "="*60)
    print("Example 2: Question with multiple images (conceptual)")
    print("="*60)

    solver = MultipleChoiceSolver()

    # This is a conceptual example - provide real image paths to test
    question = MultipleChoiceQuestion(
        question="Which image contains a tiger?",
        options=["Image 1", "Image 2", "Image 3", "Image 4"],
        image_paths=[
            "/path/to/lion.jpg",
            "/path/to/tiger.jpg",
            "/path/to/leopard.jpg",
            "/path/to/jaguar.jpg"
        ]
    )

    print("(Skipping - provide real image paths to test)")
    print("Usage: question with image_paths = [img1, img2, img3, img4]")


def example_3_context_and_images():
    """Example 3: Question with both context and multiple images."""
    print("\n" + "="*60)
    print("Example 3: Context + Multiple images (conceptual)")
    print("="*60)

    solver = MultipleChoiceSolver()

    context = """
    You are shown 4 images of different countries' flag designs.
    Flags were created in different time periods.
    """

    question = MultipleChoiceQuestion(
        question="Which image shows the flag of Japan?",
        options=["Image A", "Image B", "Image C", "Image D"],
        context=context,
        image_paths=[
            "/path/to/flag_japan.jpg",
            "/path/to/flag_south_korea.jpg",
            "/path/to/flag_vietnam.jpg",
            "/path/to/flag_thailand.jpg"
        ]
    )

    print("(Skipping - provide real image paths to test)")
    print("Usage: MultipleChoiceQuestion with both context and image_paths")


def example_4_dict_with_all_fields():
    """Example 4: Dictionary input with context and images."""
    print("\n" + "="*60)
    print("Example 4: Dictionary input with all fields")
    print("="*60)

    solver = MultipleChoiceSolver()

    question_dict = {
        "question": "What is the primary language of Brazil?",
        "options": ["Spanish", "Portuguese", "French", "English"],
        "context": "Brazil is the largest country in South America by both area and population.",
        "image_paths": []  # Can include image paths here
    }

    answer = solver.solve(question_dict)
    if answer:
        print(f"Question: {answer.question}")
        print(f"Correct Answer(s): {', '.join([f'{o.key}: {o.value}' for o in answer.correct_options])}")
        print(f"Confidence: {answer.confidence:.1%}")


def example_5_json_file_format():
    """Example 5: JSON file format with context and images."""
    print("\n" + "="*60)
    print("Example 5: JSON file format example")
    print("="*60)

    example_json = {
        "question": "Which animal is shown in the first image?",
        "options": ["Cat", "Dog", "Bird", "Rabbit"],
        "context": "These are domesticated pets commonly found in households.",
        "image_paths": ["pet1.jpg", "pet2.jpg", "pet3.jpg", "pet4.jpg"]
    }

    print("Example JSON structure for questions.json:")
    print(str(example_json).replace("'", '"'))
    print("\nYou can also have a list of such objects for batch processing.")


def example_6_using_string_interface():
    """Example 6: Simple string interface with context and images."""
    print("\n" + "="*60)
    print("Example 6: String interface with context and images")
    print("="*60)

    solver = MultipleChoiceSolver()

    # Using the string interface
    question_text = "Which is a programming language?"
    options = ["Python", "Hammer", "Wrench", "JavaScript"]
    context = "Programming languages are tools for writing software."
    image_paths = None  # Optional

    answer = solver.solve(
        question=question_text,
        options=options,
        context=context,
        image_paths=image_paths
    )

    if answer:
        print(f"Question: {answer.question}")
        print(f"Correct Answer(s): {', '.join([f'{o.key}: {o.value}' for o in answer.correct_options])}")


if __name__ == "__main__":
    example_1_with_context()
    example_2_with_multiple_images()
    example_3_context_and_images()
    example_4_dict_with_all_fields()
    example_5_json_file_format()
    example_6_using_string_interface()
