#!/usr/bin/env python3
"""
CLI for Medical Symptom Detection System.
Provides a structured consultation interface using LLM-based reasoning.
"""

import argparse
import sys
import traceback

from symptom_detection_qa import MedicalConsultation


def run_cli():
    """Run the medical consultation system."""
    parser = argparse.ArgumentParser(
        description="""Medical Symptom Checker CLI.
        A professional medical consultation interface that uses a structured decision tree
        to help identify potential conditions based on patient symptoms."""
    )

    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="ollama/gemma3",
        help="LLM model name to use for the consultation (default: ollama/gemma3)",
    )

    parser.add_argument(
        "-n",
        "--max-questions",
        type=int,
        default=15,
        help="Maximum number of follow-up questions to ask (default: 15)",
    )

    args = parser.parse_args()

    # Initialize and run the consultation
    app = MedicalConsultation(model=args.model)

    try:
        summary, summary_file, report_file = app.run(max_questions=args.max_questions)

        if summary:
            print("\n" + "=" * 80)
            print("CONSULTATION COMPLETED")
            print("=" * 80)
            print(f"✓ Medical Summary saved to: {summary_file}")
            print(f"✓ Medical Report saved to:  {report_file}")
            print("=" * 80 + "\n")
        else:
            # If summary is None, it means the consultation was stopped
            # (likely due to an emergency escalation handled within app.run())
            pass

    except KeyboardInterrupt:
        print("\n\nConsultation interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_cli()
