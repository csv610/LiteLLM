"""patient_medical_history_cli.py - Generate exam-specific medical history questions."""

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.config import ModelConfig
from lite.logging_config import configure_logging

from patient_medical_history_prompts import PromptBuilder, MedicalHistoryInput
from patient_medical_history import PatientMedicalHistoryGenerator

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Generate comprehensive patient medical history questions.")
    parser.add_argument("-e", "--exam", required=True, help="Type of medical exam (e.g., cardiac, respiratory)")
    parser.add_argument("-a", "--age", type=int, required=True, help="Patient age in years")
    parser.add_argument("-g", "--gender", required=True, help="Patient gender")
    parser.add_argument("-p", "--purpose", default="physical_exam", help="Purpose of medical history (default: physical_exam)")
    parser.add_argument("-d", "--output-dir", default="outputs", help="Directory for output files (default: outputs).")
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use (default: ollama/gemma3).")
    parser.add_argument("-v", "--verbosity", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2).")
    parser.add_argument("-s", "--structured", action="store_true", default=False, help="Use structured output (Pydantic model) for the response.")

    return parser.parse_args()


def create_patient_medical_history_report(args) -> int:
    """Generate patient medical history report."""
    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "patient_medical_history.log"),
        verbosity=args.verbosity,
        enable_console=True
    )
    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Exam: {args.exam}")
    logger.debug(f"  Age: {args.age}")
    logger.debug(f"  Gender: {args.gender}")
    logger.debug(f"  Purpose: {args.purpose}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.3)
        generator = PatientMedicalHistoryGenerator(model_config)
        
        medical_history_input = MedicalHistoryInput(
            exam=args.exam,
            age=args.age,
            gender=args.gender,
            purpose=args.purpose
        )
        
        history_info = generator.generate_text(medical_history_input, structured=args.structured)

        if history_info is None:
            logger.error("✗ Failed to generate patient medical history information.")
            return 1

        # Save result to output directory
        generator.save(history_info, output_dir)

        logger.debug("✓ Patient medical history generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Patient medical history generation failed: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == "__main__":
    args = get_user_arguments()
    create_patient_medical_history_report(args)
