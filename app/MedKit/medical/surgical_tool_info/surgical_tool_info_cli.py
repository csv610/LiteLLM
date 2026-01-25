import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Union

from rich.console import Console
from rich.panel import Panel

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from utils.output_formatter import print_result
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from lite.utils import save_model_response

from surgical_tool_info_models import SurgicalToolInfo

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builder class for creating prompts for surgical tool information."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for surgical tool information generation."""
        return """You are an expert surgical instrument specialist with extensive knowledge of medical surgical tools and instruments.
Provide comprehensive, accurate, and clinically relevant information about surgical tools. Focus on practical applications,
safety considerations, and clinical usage."""

    @staticmethod
    def create_user_prompt(tool: str) -> str:
        """Create the user prompt for surgical tool information generation.

        Args:
            tool: The name of the surgical tool to generate information for.

        Returns:
            A comprehensive prompt asking for detailed surgical tool information.
        """
        return f"""Generate comprehensive information for the surgical tool: {tool}.
Include the following details:
- Description and purpose
- Key features and specifications
- Clinical applications
- Proper handling and sterilization
- Safety considerations
- Common variants or related instruments"""


class SurgicalToolInfoGenerator:
    """Generates comprehensive surgical tool information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        logger.debug(f"Initialized SurgicalToolInfoGenerator")

    def generate_text(self, tool: str, structured: bool = False) -> Union[SurgicalToolInfo, str]:
        """Generates comprehensive surgical tool information."""
        if not tool or not str(tool).strip():
            raise ValueError("Tool name cannot be empty")

        logger.debug(f"Starting surgical tool information generation for: {tool}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(tool)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = SurgicalToolInfo

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.info("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated surgical tool information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating surgical tool information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> Union[SurgicalToolInfo, str]:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, tool_info: Union[SurgicalToolInfo, str], output_path: Path) -> Path:
        """Saves the surgical tool information to a JSON or MD file."""
        if isinstance(tool_info, str) and output_path.suffix == ".json":
            output_path = output_path.with_suffix(".md")
        return save_model_response(tool_info, output_path)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive surgical tool information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python surgical_tool_info_cli.py -i scalpel
  python surgical_tool_info_cli.py -i "surgical forceps" -o output.json -v 3
  python surgical_tool_info_cli.py -i "retractor" -d outputs/tools
        """
    )
    parser.add_argument(
        "-i", "--tool",
        required=True,
        help="The name of the surgical tool to generate information for."
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to save the output JSON file."
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

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file="surgical_tool_info.log",
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Tool: {args.tool}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Output File: {args.output if args.output else 'Default'}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.7)
        generator = SurgicalToolInfoGenerator(model_config)
        tool_info = generator.generate_text(tool=args.tool, structured=args.structured)

        if tool_info is None:
            logger.error("✗ Failed to generate surgical tool information.")
            sys.exit(1)

        # Display formatted result
        print_result(tool_info, title="Surgical Tool Information")

        if args.output:
            generator.save(tool_info, Path(args.output))
        else:
            default_path = output_dir / f"{args.tool.lower().replace(' ', '_')}_info.json"
            generator.save(tool_info, default_path)

        logger.debug("✓ Surgical tool information generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Surgical tool information generation failed: {e}")
        logger.exception("Full exception details:")
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(app_cli())
