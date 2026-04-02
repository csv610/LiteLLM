"""
Scholar Major Work Generator
Creates a complete list of major scientific work and contributions for absolute beginners.
Generates a detailed, authoritative collection of scientific breakthroughs and discoveries.
Uses AI to make complex scientific contributions intuitive and memorable.
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
# WORK GENERATION FUNCTION
# ============================================================================


def generate_scholar_work(
    scholar_name: str, focus_area: str, model_name: str
) -> ScholarMajorWork:
    """
    Generates a complete list of a scholar's major work and contributions.

    Args:
        scholar_name (str): The name of the scholar (e.g., "Albert Einstein", "Marie Curie").
        focus_area (str): The specific focus area (e.g., "General Relativity", "Radioactivity").
        model_name (str): The name of the model to use.

    Returns:
        ScholarMajorWork: A Pydantic model containing the generated list and materials.
    """
    # Initialize the generator with user-specified model
    generator = ScholarWorkGenerator(model_name=model_name)

    # Generate the work
    return generator.generate_text(scholar_name, focus_area)


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================


def display_work(work: ScholarMajorWork):
    """Display the major work and contributions as a comprehensive list."""

    # Header with title and metadata
    print("\n" + "=" * 80)
    print(f"\n{work.title.upper()}")
    print(f"\n{work.subtitle}")
    print(f"\n{'—' * 80}")
    print(f"Scholar: {work.scholar_name}")
    print("\n" + "=" * 80 + "\n")

    # The main contributions - displayed as a list
    print("MAJOR WORK AND CONTRIBUTIONS")
    print("-" * 30 + "\n")
    for i, contribution in enumerate(work.major_contributions, 1):
        print(f"{i}. {contribution}\n")

    # Supporting materials
    print("\n" + "=" * 80)
    print("\nKEY TERMS & CONCEPTS")
    print("=" * 80 + "\n")
    print(work.key_terms)

    print("\n" + "=" * 80)
    print("\nIMPACT SUMMARY")
    print("=" * 80 + "\n")
    print(work.impact_summary)

    print("\n" + "=" * 80)
    print("\nDISCUSSION QUESTIONS")
    print("=" * 80 + "\n")
    for i, question in enumerate(work.discussion_questions, 1):
        print(f"{i}. {question}\n")


def generate_scholar_story(
    scholar_name: str, focus_area: str, model_name: str
) -> ScholarMajorWork:
    """Backward-compatible alias for older tests and callers."""
    return generate_scholar_work(scholar_name, focus_area, model_name)


def display_story(work: ScholarMajorWork):
    """Backward-compatible alias for older tests and callers."""
    display_work(work)


def main():
    parser = argparse.ArgumentParser(
        prog="scholar_work_cli.py",
        description="Generate a complete list of major scientific work and contributions in an authoritative style.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Albert Einstein" "General Relativity"
  %(prog)s "Marie Curie" "Radioactivity" --model gemini-2.5-flash
  %(prog)s "Charles Darwin" "Natural Selection" -m claude-3-5-sonnet-20241022
  %(prog)s "Ada Lovelace" "First Computer Algorithm" -m gpt-4

Output:
  Generates a complete list of major works with title, contributions, key terms,
  impact summary, and discussion questions suitable for a general audience.
        """,
    )

    parser.add_argument(
        "scholar_name", type=str, help='Name of the scholar (e.g., "Albert Einstein")'
    )

    parser.add_argument(
        "focus_area",
        type=str,
        nargs="?",
        default="their most significant work",
        help='Specific focus area (e.g., "General Relativity")',
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
    print("Documenting the Contributions of Great Scholars")
    print("=" * 80)

    print(f"\nGenerating work list for: {args.scholar_name}")
    print(f"Focusing on: {args.focus_area}")
    print(f"Using model: {args.model_name}")
    print("(Compiling a comprehensive list...)\n")

    try:
        work = generate_scholar_work(
            args.scholar_name, args.focus_area, args.model_name
        )
        display_work(work)

        print("\n" + "=" * 80)
        print("\nMajor work list generated successfully.")
        print("=" * 80)

    except Exception as e:
        print(f"\nError generating work list: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
