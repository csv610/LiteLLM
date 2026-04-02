"""
Scholar Major Work Generator
Creates engaging, narrative-driven explanations of major scientific work for absolute beginners.
Uses a 3-agent pipeline to ensure high narrative quality and historical accuracy.
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

from app.ScholarWork.agentic.scholar_work_generator import ScholarWorkGenerator


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================


def display_story(report_md: str):
    """Display the report as a polished Markdown document."""
    print("\n" + "=" * 80)
    print("FINAL SCHOLAR CONTRIBUTION REPORT")
    print("=" * 80 + "\n")
    print(report_md)
    print("\n" + "=" * 80)


def progress_callback(step: int, message: str):
    """Display progress during the multi-agent generation process."""
    print(f"[{step}/3] Agent: {message}")
    sys.stdout.flush()


def generate_scholar_story(
    scholar_name: str, major_contribution: str, model_name: str
) -> str:
    """
    Generates a comprehensive list of a scholar's major work and contributions.

    Args:
        scholar_name (str): The name of the scholar.
        major_contribution (str): (Optional) specific work, though all major works are now researched.
        model_name (str): The name of the model to use.

    Returns:
        str: A Markdown string containing the generated report.
    """
    generator = ScholarWorkGenerator(model_name=model_name)
    return generator.generate_text(
        scholar_name, major_contribution, progress_callback=progress_callback
    )


def main():
    parser = argparse.ArgumentParser(
        prog="scholar_work_cli.py",
        description="Generate a comprehensive list of major scientific work and contributions using multiple agents.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "scholar_name", type=str, help='Name of the scholar (e.g., "Albert Einstein")'
    )

    parser.add_argument(
        "major_contribution",
        type=str,
        nargs="?",
        default="their major works",
        help='Specific contribution to emphasize (optional)',
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
    print("SCHOLAR MAJOR WORK & CONTRIBUTIONS GENERATOR")
    print("Multi-Agent Science Synthesis Engine")
    print("=" * 80)

    print(f"\nGenerating contribution report for: {args.scholar_name}")
    print(f"Using model: {args.model_name}")
    print("-" * 40)

    try:
        report_md = generate_scholar_story(
            args.scholar_name, args.major_contribution, args.model_name
        )

        print("-" * 40)
        print("[Done] Contribution report fully crafted and edited.")
        print("-" * 40 + "\n")

        display_story(report_md)

        print("\n" + "=" * 80)
        print("\nReport generated successfully.")
        print("=" * 80)

    except Exception as e:
        print(f"\nError generating story: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
