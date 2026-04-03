"""
liteagents.py - Unified for med_history
"""
from app.MedKit.medical.med_history.shared.models import *
from lite.utils import save_model_response
from .patient_medical_history_prompts import MedicalHistoryInput, PromptBuilder
import logging
from lite.lite_client import LiteClient
from pathlib import Path
from .patient_medical_history_models import ModelOutput, PatientMedicalHistoryModel
import argparse
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
import sys

"""Patient Medical History Questions Generator CLI."""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))




try:
    from .patient_medical_history import PatientMedicalHistoryGenerator
except (ImportError, ValueError):
    from medical.med_history.agentic.patient_medical_history import (
        PatientMedicalHistoryGenerator,
    )
try:
    from .patient_medical_history_prompts import MedicalHistoryInput
except (ImportError, ValueError):
    from medical.med_history.agentic.patient_medical_history_prompts import MedicalHistoryInput

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate patient medical history questions."
    )
    parser.add_argument("-e", "--exam", required=True, help="Type of medical exam.")
    parser.add_argument("-a", "--age", type=int, required=True, help="Patient age.")
    parser.add_argument("-g", "--gender", required=True, help="Patient gender.")
    parser.add_argument(
        "-p", "--purpose", default="physical_exam", help="Purpose of medical history."
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
        log_file="patient_medical_history.log",
        verbosity=args.verbosity,
        enable_console=True,
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.3)
        generator = PatientMedicalHistoryGenerator(model_config)

        input_data = MedicalHistoryInput(
            exam=args.exam, age=args.age, gender=args.gender, purpose=args.purpose
        )

        logger.info(f"Generating questions for {args.exam} exam...")
        result = generator.generate_text(input_data, structured=args.structured)
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
Patient Medical History Analysis module.

This module provides the core PatientMedicalHistoryGenerator class for generating
patient medical history questions using LiteClient.
"""




logger = logging.getLogger(__name__)


class PatientMedicalHistoryGenerator:
    """Generates patient medical history questions using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.user_input = None  # Store the input for later use in save
        logger.debug("Initialized PatientMedicalHistoryGenerator")

    def generate_text(
        self, user_input: MedicalHistoryInput, structured: bool = False
    ) -> ModelOutput:
        """Generate 3-tier medical history questionnaire."""
        self.user_input = user_input
        logger.info(f"Starting 3-tier medical history generation for: {user_input.exam}")

        try:
            # 1. Specialist Stage (JSON)
            logger.debug("[Specialist] Generating questions...")
            system_prompt = PromptBuilder.create_system_prompt()
            user_prompt = PromptBuilder.create_user_prompt(user_input)
            
            spec_input = ModelInput(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_format=PatientMedicalHistoryModel if structured else None,
            )
            spec_res = self.ask_llm(spec_input)
            
            if structured:
                spec_json = spec_res.data.model_dump_json(indent=2)
            else:
                spec_json = spec_res.markdown

            # 2. Auditor Stage (JSON Audit)
            logger.debug("[Auditor] Auditing questions...")
            audit_sys, audit_usr = PromptBuilder.get_history_auditor_prompts(user_input, spec_json)
            audit_input = ModelInput(
                system_prompt=audit_sys,
                user_prompt=audit_usr,
                response_format=None # Audit result
            )
            audit_res = self.ask_llm(audit_input)
            audit_json = audit_res.markdown

            # 3. Final Synthesis Stage (Markdown Closer)
            logger.debug("[Output] Synthesizing final questionnaire...")
            out_sys, out_usr = PromptBuilder.get_output_synthesis_prompts(user_input, spec_json, audit_json)
            out_input = ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None,
            )
            final_res = self.ask_llm(out_input)

            logger.info("✓ Successfully generated 3-tier medical history questionnaire")
            return ModelOutput(
                data=spec_res.data if structured else None, 
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier History generation failed: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Internal helper to call the LLM client."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the patient medical history information to a file."""
        if self.user_input is None:
            raise ValueError(
                "No input information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = (
            f"{self.user_input.exam.lower().replace(' ', '_')}_medical_history"
        )

        return save_model_response(result, output_dir / base_filename)