import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from lite.utils import save_model_response

from surgical_pose_info_models import SurgicalPoseInfoModel, ModelOutput
from surgical_pose_info_prompts import PromptBuilder

logger = logging.getLogger(__name__)

COMMON_SURGICAL_POSITIONS = [
    "Supine (Dorsal Decubitus)",
    "Prone (Ventral Decubitus)",
    "Lithotomy",
    "Trendelenburg",
    "Reverse Trendelenburg",
    "Lateral Decubitus (Right/Left)",
    "Fowler's Position",
    "Semi-Fowler's Position",
    "Jackknife (Kraske)",
    "Kidney Position",
    "Sims' Position",
    "Sitting (Beach Chair)"
]


class SurgicalPoseInfoGenerator:
    """Generates comprehensive surgical position information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.pose = None  # Store the position being analyzed
        logger.debug(f"Initialized SurgicalPoseInfoGenerator")

    def generate_text(self, pose: str, structured: bool = False) -> ModelOutput:
        """Generates comprehensive surgical position information."""
        if not pose or not str(pose).strip():
            raise ValueError("Position name cannot be empty")

        # Store the pose for later use in save
        self.pose = pose
        logger.debug(f"Starting surgical position information generation for: {pose}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(pose)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = SurgicalPoseInfoModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.info("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated surgical position information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating surgical position information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the surgical position information to a file."""
        if self.pose is None:
            raise ValueError("No position information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.pose.lower().replace(' ', '_')}"
        
        return save_model_response(result, output_dir / base_filename)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive surgical position information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python surgical_pose_info_cli.py -i supine
  python surgical_pose_info_cli.py -i "lithotomy position" -v 3
  python surgical_pose_info_cli.py -i "prone" -d outputs/positions
  python surgical_pose_info_cli.py -l
        """
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
