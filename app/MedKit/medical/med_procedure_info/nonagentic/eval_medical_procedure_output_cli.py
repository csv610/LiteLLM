"""eval_medical_procedure_output - Critically review medical procedure documentation."""

import sys
from pathlib import Path

# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


import argparse
import logging
import sys

from tqdm import tqdm

# Ensure we can import from the current directory
sys.path.append(str(Path(__file__).parent))

from lite.config import ModelConfig
from lite.logging_config import configure_logging

try:
    from .eval_medical_procedure_output import MedicalProcedureEvaluator
except (ImportError, ValueError):
    from medical.med_procedure_info.nonagentic.eval_medical_procedure_output import (
        MedicalProcedureEvaluator,
    )

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Critically evaluate medical procedure information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "file",
        help="Path to the file containing the medical procedure information to evaluate, or a file path containing paths.",
    )
    parser.add_argument(
        "-d",
        "--output-dir",
        default="outputs",
        help="Directory for output files (default: outputs).",
    )
    parser.add_argument(
        "-m",
        "--model",
        default="ollama/gemma3:27b-cloud",
        help="Model to use (default: gemma3:27b-cloud)",
    )
    parser.add_argument(
        "-s",
        "--structured",
        action="store_true",
        default=True,
        help="Use structured output (Pydantic model) for the evaluation (default: True).",
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2).",
    )

    return parser.parse_args()


def evaluate_medical_procedure_report(args) -> int:

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "eval_medical_procedure.log"),
        verbosity=args.verbosity,
        enable_console=True,
    )

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Handle input - check if it's a file or direct term
    input_path = Path(args.file)
    if input_path.is_file():
        # Check if it's a markdown or text file which IS the target, OR a file list
        if input_path.suffix in [".md", ".txt", ".json"]:
            input_files = [str(input_path)]
        else:
            with open(input_path, "r", encoding="utf-8") as f:
                input_files = [line.strip() for line in f if line.strip()]
        logger.debug(f"Read {len(input_files)} files to evaluate from: {input_path}")
    else:
        input_files = [args.file]

    try:
        model_config = ModelConfig(
            model=args.model, temperature=0.1
        )  # Low temp for evaluation
        evaluator = MedicalProcedureEvaluator(model_config=model_config)

        for file_path in tqdm(input_files, desc="Evaluating procedure reports"):
            result = evaluator.generate_text(file_path=file_path)

            if result is None:
                logger.error(
                    f"✗ Failed to evaluate procedure information for: {file_path}"
                )
                continue

            # Save result to output directory
            saved_path = evaluator.save(result, output_dir)
            logger.info(f"Evaluation report saved to: {saved_path}")

        logger.debug("✓ Procedure evaluations completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Procedure evaluation failed: {e}")
        logger.exception("Full exception details:")
        return 1


def main():
    args = get_user_arguments()
    evaluate_medical_procedure_report(args)


if __name__ == "__main__":
    main()
