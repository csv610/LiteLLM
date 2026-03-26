"""
Mathematical Equation Story Generator
Creates engaging, narrative-driven explanations of mathematical equations for absolute beginners.
Uses a 3-agent pipeline to ensure high narrative quality and technical accuracy.
"""

import argparse
import sys

from math_equation_story_models import MathematicalEquationStory
from math_equation_story_generator import MathEquationStoryGenerator


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_story(story: MathematicalEquationStory):
    """Display the story as a coherent, published article."""

    # Header with title and metadata
    print("\n" + "=" * 80)
    print(f"\n{story.title.upper()}")
    print(f"\n{story.subtitle}")
    print(f"\n{'—' * 80}")
    print(f"Equation: {story.equation_name}")
    print(f"Formula: {story.latex_formula}")
    print("\n" + "=" * 80 + "\n")

    # The main narrative - displayed as continuous prose
    print(story.story)

    # Supporting materials
    print("\n" + "=" * 80)
    print("\nVOCABULARY & CONCEPTS")
    print("=" * 80 + "\n")
    print(story.vocabulary_notes)

    print("\n" + "=" * 80)
    print("\nDISCUSSION QUESTIONS")
    print("=" * 80 + "\n")
    for i, question in enumerate(story.discussion_questions, 1):
        print(f"{i}. {question}\n")


def progress_callback(step: int, message: str):
    """Display progress during the multi-agent generation process."""
    print(f"[{step}/3] Agent: {message}")
    sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser(
        prog="math_equation_story_cli.py",
        description="Generate engaging, narrative-driven explanations of mathematical equations in the style of science journalism.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'equation_name',
        type=str,
        help='Name of the equation to explain (e.g., "Pythagorean Theorem", "E=mc²")'
    )

    parser.add_argument(
        '-m', '--model',
        type=str,
        default='ollama/gemma3',
        dest='model_name',
        help='Model name to use for generation (default: ollama/gemma3)'
    )

    args = parser.parse_args()

    print("=" * 80)
    print("MATHEMATICAL EQUATION STORY GENERATOR")
    print("Multi-Agent Science Writing Engine")
    print("=" * 80)

    print(f"\nGenerating story for: {args.equation_name}")
    print(f"Using model: {args.model_name}")
    print("-" * 40)
    
    try:
        generator = MathEquationStoryGenerator(model_name=args.model_name)
        story = generator.generate_text(args.equation_name, progress_callback=progress_callback)
        
        print("-" * 40)
        print("[Done] Story fully crafted and edited.")
        print("-" * 40 + "\n")
        
        display_story(story)

    except Exception as e:
        print(f"\nError generating story: {e}")
        # import traceback
        # traceback.print_exc()

    print("\n" + "=" * 80)
    print("\nStory generated successfully.")
    print("=" * 80)

if __name__ == "__main__":
   main()
