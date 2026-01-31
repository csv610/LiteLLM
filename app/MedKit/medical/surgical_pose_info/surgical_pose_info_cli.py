import argparse
import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.logging_config import configure_logging

from .surgical_pose_info import SurgicalPoseInfoGenerator, COMMON_SURGICAL_POSITIONS

logger = logging.getLogger(__name__)

def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive surgical position information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-i", "--pose",
        help="The name of the surgical position to generate information for."
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List common surgical positions."
    )
    parser.add_argument(
        "-d", "--output-dir",
        default="outputs",
        help="Directory for output files (default: outputs)."
    )
    parser.add_argument(
        "-m", "--model",
        default="ollama/gemma3",
        help="Model to use for generation (default: ollama/gemma3)."
    )
    parser.add_argument(
        "-v", "--verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2)."
    )
    parser.add_argument(
        "-s", "--structured",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response."
    )

    return parser.parse_args()


def app_cli() -> int:
    """CLI entry point."""
    args = get_user_arguments()

    if args.list:
        print("Common Surgical Positions:")
        for pos in COMMON_SURGICAL_POSITIONS:
            print(f"  - {pos}")
        return 0

    if not args.pose:
        print("Error: The -i/--pose argument is required unless -l/--list is used.")
        return 1

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "surgical_pose_info.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Pose: {args.pose}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = SurgicalPoseInfoGenerator(model_config)
        pose_info = generator.generate_text(pose=args.pose, structured=args.structured)

        if pose_info is None:
            logger.error("✗ Failed to generate surgical position information.")
            return 1

        # Save result to output directory
        generator.save(pose_info, output_dir)

        logger.debug("✓ Surgical position information generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Surgical position information generation failed: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == "__main__":
    app_cli()
