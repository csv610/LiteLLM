import argparse
import json
import logging
import sys
from pathlib import Path
from typing import final, Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from lite.utils import save_model_response

from medical_implant_models import MedicalImplantInfoModel, ModelOutput

logger = logging.getLogger(__name__)

class PromptBuilder:
    """Builder class for creating prompts for medical implant information."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for medical implant information generation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are a medical device and implant specialist with expertise in biomedical engineering and clinical applications of medical implants.

Your responsibilities include:
- Providing comprehensive, evidence-based information about medical implants and devices
- Explaining device design, materials, and mechanisms of action
- Describing indications, contraindications, and patient selection criteria
- Detailing implantation procedures and technical considerations
- Outlining potential complications, device lifespan, and follow-up requirements
- Discussing regulatory status and clinical outcomes

Guidelines:
- Base all information on current medical device literature and regulatory standards
- Include both technical specifications and clinical perspectives
- Emphasize patient safety, biocompatibility, and long-term outcomes
- Address maintenance, monitoring, and replacement considerations
- Provide balanced information about risks and benefits
- Reference current evidence and clinical guidelines where applicable"""

    @staticmethod
    def create_user_prompt(implant: str) -> str:
        """
        Create the user prompt for medical implant information.

        Args:
            implant: The name of the medical implant

        Returns:
            str: Formatted user prompt
        """
        return f"Generate comprehensive information for the medical implant: {implant}."


@final
class MedicalImplantGenerator:
    """Generates comprehensive medical implant information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.implant = None  # Store the implant being analyzed
        logger.debug(f"Initialized MedicalImplantGenerator")

    def generate_text(self, implant: str, structured: bool = False) -> ModelOutput:
        """Generates comprehensive medical implant information."""
        if not implant or not str(implant).strip():
            raise ValueError("Implant name cannot be empty")

        # Store the implant for later use in save
        self.implant = implant
        logger.debug(f"Starting medical implant information generation for: {implant}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(implant)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
           response_format = MedicalImplantInfoModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated implant information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating implant information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the implant information to a file."""
        if self.implant is None:
            raise ValueError("No implant information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.implant.lower().replace(' ', '_')}"
        
        return save_model_response(result, output_dir / base_filename)

def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive medical implant information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python medical_implant_cli.py -i "cardiac pacemaker"
  python medical_implant_cli.py -i "hip prosthesis" -o output.json -v 3
  python medical_implant_cli.py -i "cochlear implant" -d outputs/implants
        """
    )
    parser.add_argument(
        "-i", "--implant",
        required=True,
        help="The name of the medical implant to generate information for."
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
        "--quick",
        action="store_true",
        help="Use quick mode (no Pydantic model for response formatting)."
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
    args = get_user_arguments()

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "medical_implant.log"),
        verbosity=args.verbosity,
        enable_console=True
    )
    logger.debug(f"  Implant: {args.implant}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MedicalImplantGenerator(model_config)
        
        # Determine if structured output should be used
        use_structured = args.structured and not args.quick
        
        implant_info = generator.generate_text(implant=args.implant, structured=use_structured)

        if implant_info is None:
            logger.error("✗ Failed to generate implant information.")
            return 1

        # Save result to output directory
        generator.save(implant_info, output_dir)

        logger.debug("Implant information generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Implant information generation failed: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == "__main__":
    app_cli()
