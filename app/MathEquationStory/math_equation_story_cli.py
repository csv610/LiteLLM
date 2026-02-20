"""
Mathematical Equation Story Generator
Creates engaging, narrative-driven explanations of mathematical equations for absolute beginners.
Generates flowing, professional narratives like those found in popular science magazines.
Uses Gemini API to make complex mathematics intuitive and memorable through compelling storytelling.
"""

import argparse

from math_equation_story_models import MathematicalEquationStory
from math_equation_story_generator import MathEquationStoryGenerator


# ============================================================================
# STORY GENERATION FUNCTION
# ============================================================================

def generate_equation_story(equation_name: str, model_name: str) -> MathematicalEquationStory:
    """
    Generates a narrative-driven explanation of a mathematical equation.

    This function creates a detailed prompt that instructs the AI model to
    write a compelling story about the specified equation, in the style of a
    popular science magazine. The story is designed to be accessible to a
    general audience and to convey the beauty and importance of the mathematics.

    Args:
        equation_name (str): The name of the equation to be explained (e.g.,
                             "Pythagorean Theorem", "E=mc²").
        model_name (str): The name of the model to use (e.g., 'gemini-2.5-flash',
                         'claude-3-5-sonnet-20241022').

    Returns:
        MathematicalEquationStory: A Pydantic model containing the generated
                                   story and supporting materials.
    """
    # Initialize the generator with user-specified model
    generator = MathEquationStoryGenerator(model_name=model_name)
    
    # Generate the story
    return generator.generate_text(equation_name)


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_story(story: MathematicalEquationStory):
    """Display the story as a coherent, published article."""

    # Header with title and metadata
    print("\n" + "=" * 80)
    print(f"\n{story.title}")
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


def main():
    parser = argparse.ArgumentParser(
        prog="math_equation_story_cli.py",
        description="Generate engaging, narrative-driven explanations of mathematical equations in the style of science journalism.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Pythagorean Theorem"
  %(prog)s "E=mc²" --model gemini-2.5-flash
  %(prog)s "Newton's Law of Motion" -m claude-3-5-sonnet-20241022
  %(prog)s "Euler's Identity" -m gpt-4

Output:
  Generates a complete narrative article with title, story, vocabulary notes,
  and discussion questions suitable for high school students and general audiences.
        """
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
    print("Science Writing About Mathematics")
    print("=" * 80)

    print(f"\nGenerating story for: {args.equation_name}")
    print(f"Using model: {args.model_name}")
    print("(Crafting a compelling narrative...)\n")

    try:
        story = generate_equation_story(args.equation_name, args.model_name)
        display_story(story)

    except Exception as e:
        print(f"\nError generating story: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 80)
    print("\nStory generated successfully.")
    print("=" * 80)

if __name__ == "__main__":
   main()
