import logging
import sys
from pathlib import Path
from typing import Union

from lite.config import ModelConfig, ModelInput

# Ensure repository root is in path for imports
# Use .resolve() to get absolute paths to avoid issues with relative CWDs
_repo_root = Path(__file__).resolve().parent.parent.parent.parent.parent
_medkit_root = _repo_root / "app" / "MedKit"
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))
if str(_medkit_root) not in sys.path:
    sys.path.insert(0, str(_medkit_root))

from utils.cli_base import BaseCLI, BaseGenerator
from disease_info_models import DiseaseInfoModel, ModelOutput
from disease_info_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class DiseaseInfoGenerator(BaseGenerator):
    """Generates comprehensive disease information.

    Inherits from BaseGenerator and provides domain-specific generation logic
    for generating evidence-based disease information.
    """

    def generate_text( self, disease: str, structured: bool = False) -> ModelOutput:
        """Generate comprehensive disease information.

        Args:
            disease: Name of the disease
            structured: Whether to use structured output (Pydantic model)

        Returns:
            Union[DiseaseInfoModel, str]: Structured or plain text result
        """
        # Validate input
        if not disease or not str(disease).strip():
            raise ValueError("Disease name cannot be empty")

        self.logger.debug(f"Starting disease information generation for: {disease}")

        # Create model input with prompts
        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(disease),
            response_format=DiseaseInfoModel if structured else None,
        )

        result = self._ask_llm(model_input)

        if isinstance(result, DiseaseInfoModel):
            self.logger.debug(f"Disease: {result.identity.name}")

        return result


class DiseaseInfoCLI(BaseCLI):
    """CLI for disease information generation.

    Refactored to inherit from BaseCLI, demonstrating the pattern of:
    - Using BaseCLI for standardized argument parsing and orchestration
    - Implementing domain-specific add_arguments() and run() methods
    - Automatic handling of logging, model config, and output formatting

    This reduces boilerplate from ~210 to ~110 lines (48% reduction).
    """

    description = "Generate comprehensive disease information"
    epilog = """
Examples:
  python disease_info_cli.py -i diabetes
  python disease_info_cli.py -i "heart disease" -o output.json -v 3
  python disease_info_cli.py -i pneumonia -d outputs/diseases
    """

    def add_arguments(self, parser) -> None:
        """Add domain-specific arguments.

        Args:
            parser: ArgumentParser instance
        """
        parser.add_argument(
            "-i", "--disease",
            required=True,
            help="The name of the disease to generate information for"
        )

    def validate_args(self) -> None:
        """Validate parsed arguments.

        Raises:
            ValueError: If required arguments are invalid
        """
        if not self.args.disease.strip():
            raise ValueError("Disease name cannot be empty")

    def run(self) -> ModelOutput:
        """Run the disease information generation.

        Returns:
            Union[DiseaseInfoModel, str]: Disease information result
        """
        # Create generator
        generator = DiseaseInfoGenerator(self.model_config, self.logger)

        # Generate disease information
        result = generator.generate_text(
            disease=self.args.disease,
            structured=self.args.structured
        )

        # Save result if output path is specified
        if result is not None:
            output_path = self._get_output_path(
                self.args.disease,
                suffix="info"
            )
            generator.save(result, output_path)

        return result


def main() -> int:
    """Main entry point for the CLI."""
    cli = DiseaseInfoCLI(logger_name=__name__)
    return cli.execute()


if __name__ == "__main__":
    sys.exit(main())
