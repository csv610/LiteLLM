"""
liteagents.py - Unified for med_implant
"""
from lite.utils import save_model_response
from app.MedKit.medical.med_implant.shared.models import *
from tqdm import tqdm
import logging
from lite.lite_client import LiteClient
from pathlib import Path
import argparse
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
import sys

"""Medical Implant Information Generator CLI."""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))




try:
    try:
        from .medical_implant import MedicalImplantGenerator
    except (ImportError, ValueError):
        from medical.med_implant.agentic.medical_implant import MedicalImplantGenerator
except (ImportError, ValueError):

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate comprehensive medical implant information."
    )
    parser.add_argument(
        "-i",
        "--implant",
        required=True,
        help="Implant name or file path containing names.",
    )
    parser.add_argument(
        "-d", "--output-dir", default="outputs", help="Output directory."
    )
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use.")
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Verbosity level.",
    )
    parser.add_argument(
        "-s", "--structured", action="store_true", help="Use structured output."
    )
    return parser.parse_args()


def main():
    args = get_user_arguments()
    configure_logging(
        log_file="medical_implant.log", verbosity=args.verbosity, enable_console=True
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.implant)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.implant]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MedicalImplantGenerator(model_config)

        for item in tqdm(items, desc="Generating"):
            result = generator.generate_text(implant=item, structured=args.structured)
            if result:
                generator.save(result, output_dir)

        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())

#!/usr/bin/env python3
"""
Medical Implant module.

This module provides the core MedicalImplantGenerator class for generating
comprehensive medical implant information based on provided configuration.
"""



try:
    from .medical_implant_models import MedicalImplantInfoModel, ModelOutput
    from .medical_implant_prompts import PromptBuilder
except (ImportError, ValueError):
    from medical.med_implant.agentic.medical_implant_models import (
        MedicalImplantInfoModel,
        ModelOutput,
    )
    from medical.med_implant.agentic.medical_implant_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalImplantGenerator:
    """Generates comprehensive medical implant information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.implant = None  # Store the implant being analyzed
        logger.debug("Initialized MedicalImplantGenerator")

    def generate_text(self, implant: str, structured: bool = False) -> ModelOutput:
        """Generates 3-tier comprehensive medical implant information."""
        if not implant or not str(implant).strip():
            raise ValueError("Implant name cannot be empty")

        self.implant = implant
        logger.info(f"Starting 3-tier implant generation for: {implant}")

        try:
            # 1. Specialist Stage (JSON)
            logger.debug(f"[Specialist] Generating content for: {implant}")
            system_prompt = PromptBuilder.create_system_prompt()
            user_prompt = PromptBuilder.create_user_prompt(implant)
            
            spec_input = ModelInput(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_format=MedicalImplantInfoModel if structured else None,
            )
            spec_res = self.ask_llm(spec_input)
            
            if structured:
                spec_json = spec_res.data.model_dump_json(indent=2)
            else:
                spec_json = spec_res.markdown

            # 2. Auditor Stage (JSON Audit)
            logger.debug(f"[Auditor] Auditing content for: {implant}")
            audit_sys, audit_usr = PromptBuilder.get_implant_auditor_prompts(implant, spec_json)
            audit_input = ModelInput(
                system_prompt=audit_sys,
                user_prompt=audit_usr,
                response_format=None # Audit result
            )
            audit_res = self.ask_llm(audit_input)
            audit_json = audit_res.markdown

            # 3. Final Synthesis Stage (Markdown Closer)
            logger.debug(f"[Output] Synthesizing final report for: {implant}")
            out_sys, out_usr = PromptBuilder.get_output_synthesis_prompts(implant, spec_json, audit_json)
            out_input = ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None,
            )
            final_res = self.ask_llm(out_input)

            logger.info("✓ Successfully generated 3-tier implant information")
            return ModelOutput(
                data=spec_res.data if structured else None, 
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier implant generation failed: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the implant information to a file."""
        if self.implant is None:
            raise ValueError(
                "No implant information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.implant.lower().replace(' ', '_')}"

        return save_model_response(result, output_dir / base_filename)