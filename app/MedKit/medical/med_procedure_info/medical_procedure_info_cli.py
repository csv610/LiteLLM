"""medical_procedure_info - Generate comprehensive medical procedure documentation."""

import json
import sys
import argparse
from pathlib import Path
from typing import Optional, Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response
from utils.output_formatter import print_result

from medical_procedure_info_models import ProcedureInfo


class PromptBuilder:
    """Builder class for creating prompts for medical procedure documentation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for medical procedure documentation."""
        return "You are an expert medical documentation specialist. Generate comprehensive, evidence-based procedure information."

    @staticmethod
    def create_user_prompt(procedure: str) -> str:
        """Create the user prompt for procedure information."""
        return f"Generate complete, evidence-based information for the medical procedure: {procedure}"


class MedicalProcedureInfoGenerator:
    """Generate comprehensive information for medical procedures using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.client = LiteClient(model_config=model_config)
        self.procedure_name: Optional[str] = None

    def generate_text(self, procedure: str, structured: bool = False) -> Union[ProcedureInfo, str]:
        """Generate and retrieve comprehensive medical procedure information."""
        if not procedure or not procedure.strip():
            raise ValueError("Procedure name cannot be empty")

        self.procedure_name = procedure

        response_format = None
        if structured:
            response_format = ProcedureInfo

        model_input = ModelInput(
            user_prompt=PromptBuilder.create_user_prompt(procedure),
            response_format=response_format,
            system_prompt=PromptBuilder.create_system_prompt()
        )

        result = self._ask_llm(model_input)
        return result

    def _ask_llm(self, model_input: ModelInput) -> Union[ProcedureInfo, str]:
        """Internal helper to call the LLM client."""
        return self.client.generate_text(model_input=model_input)


def main():
    parser = argparse.ArgumentParser(description="Generate comprehensive information for a medical procedure.")
    parser.add_argument("-i", "--procedure", required=True, help="Name of the medical procedure")
    parser.add_argument("-o", "--output", type=Path, help="Path to save JSON output.")
    parser.add_argument("-m", "--model", default="gemini-1.5-pro", help="Model to use (default: gemini-1.5-pro)")
    parser.add_argument("-s", "--structured", action="store_true", default=False, help="Use structured output (Pydantic model) for the response.")

    args = parser.parse_args()

    try:
        model_config = ModelConfig(model=args.model, temperature=0.3)
        generator = MedicalProcedureInfoGenerator(model_config=model_config)
        print(f"Generating procedure documentation for: {args.procedure}...")
        result = generator.generate_text(procedure=args.procedure, structured=args.structured)
        
        print_result(result, title="Medical Procedure Documentation")
        
        if args.output:
            output_path = args.output
            if isinstance(result, str) and output_path.suffix == ".json":
                output_path = output_path.with_suffix(".md")
            save_model_response(result, output_path)
            print(f"✓ Results saved to {output_path}")

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
