"""
Scholar Major Work Generator
Creates engaging, narrative-driven explanations of major scientific work for absolute beginners.
Generates flowing, professional narratives like those found in popular science magazines.
Uses AI to make complex scientific contributions intuitive and memorable through compelling storytelling.
"""

import argparse
import sys
from pathlib import Path

# Add the project root to sys.path
path = Path(__file__).parent
while path.name != "app" and path.parent != path:
    path = path.parent
if path.name == "app":
    root = path.parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

from app.ScholarWork.nonagentic.scholar_work_models import ScholarMajorWork
from app.ScholarWork.nonagentic.scholar_work_generator import ScholarWorkGenerator


# ============================================================================
# STORY GENERATION FUNCTION
# ============================================================================


def generate_scholar_story(
    scholar_name: str, major_contribution: str, model_name: str
) -> ScholarMajorWork:
    """
    Generates a narrative-driven explanation of a scholar's major work.

    Args:
        scholar_name (str): The name of the scholar (e.g., "Albert Einstein", "Marie Curie").
        major_contribution (str): The specific work (e.g., "General Relativity", "Radioactivity").
        model_name (str): The name of the model to use.

    Returns:
        ScholarMajorWork: A Pydantic model containing the generated story and materials.
    """
    # Initialize the generator with user-specified model
    generator = ScholarWorkGenerator(model_name=model_name)

    # Generate the story
    return generator.generate_text(scholar_name, major_contribution)


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================


def display_story(story: ScholarMajorWork):
    """Display the story as a coherent, published article."""

    # Header with title and metadata
    print("\n" + "=" * 80)
    print(f"\n{story.title.upper()}")
    print(f"\n{story.subtitle}")
    print(f"\n{'—' * 80}")
    print(f"Scholar: {story.scholar_name}")
    print(f"Contribution: {story.major_contribution}")
    print("\n" + "=" * 80 + "\n")

    # The main narrative - displayed as continuous prose
    print(story.story)

    # Supporting materials
    print("\n" + "=" * 80)
    print("\nKEY TERMS & CONCEPTS")
    print("=" * 80 + "\n")
    print(story.key_terms)

    print("\n" + "=" * 80)
    print("\nIMPACT SUMMARY")
    print("=" * 80 + "\n")
    print(story.impact_summary)

    print("\n" + "=" * 80)
    print("\nDISCUSSION QUESTIONS")
    print("=" * 80 + "\n")
    for i, question in enumerate(story.discussion_questions, 1):
        print(f"{i}. {question}\n")


def main():
    parser = argparse.ArgumentParser(
        prog="scholar_work_cli.py",
        description="Generate engaging, narrative-driven explanations of major scientific work in the style of science journalism.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Albert Einstein" "General Relativity"
  %(prog)s "Marie Curie" "Radioactivity" --model gemini-2.5-flash
  %(prog)s "Charles Darwin" "Natural Selection" -m claude-3-5-sonnet-20241022
  %(prog)s "Ada Lovelace" "First Computer Algorithm" -m gpt-4

Output:
  Generates a complete narrative article with title, story, key terms,
  impact summary, and discussion questions suitable for a general audience.
        """,
    )

    parser.add_argument(
        "scholar_name", type=str, help='Name of the scholar (e.g., "Albert Einstein")'
    )

    parser.add_argument(
        "major_contribution",
        type=str,
        nargs="?",
        default="their most significant work",
        help='Specific contribution to explain (e.g., "General Relativity")',
    )

    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="ollama/gemma3",
        dest="model_name",
        help="Model name to use for generation (default: ollama/gemma3)",
    )

    args = parser.parse_args()

    print("=" * 80)
    print("SCHOLAR MAJOR WORK GENERATOR")
    print("Science Writing About Great Scholars")
    print("=" * 80)

    print(f"\nGenerating story for: {args.scholar_name}")
    print(f"Focusing on: {args.major_contribution}")
    print(f"Using model: {args.model_name}")
    print("(Crafting a compelling narrative...)\n")

    try:
        story = generate_scholar_story(
            args.scholar_name, args.major_contribution, args.model_name
        )
        display_story(story)

        print("\n" + "=" * 80)
        print("\nStory generated successfully.")
        print("=" * 80)

    except Exception as e:
        print(f"\nError generating story: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
