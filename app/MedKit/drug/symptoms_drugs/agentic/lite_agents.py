"""
liteagents.py - Unified for symptoms_drugs
"""
from .symptom_drugs_models import ModelOutput, SymptomDrugAnalysisModel\nfrom .symptom_drugs import SymptomDrugs\nfrom lite.utils import save_model_response\nfrom app.MedKit.drug.symptoms_drugs.shared.models import *\nimport logging\nfrom lite.lite_client import LiteClient\nfrom pathlib import Path\nfrom .symptom_drugs_prompts import PromptBuilder, SymptomInput\nimport argparse\nfrom lite.config import ModelConfig\nfrom lite.config import ModelConfig, ModelInput\nfrom lite.logging_config import configure_logging\nfrom .symptom_drugs_prompts import PromptStyle, SymptomInput\n\n#!/usr/bin/env python3
"""Symptom-to-Drug Analysis CLI."""



logger = logging.getLogger(__name__)


def parse_prompt_style(style_str: str) -> PromptStyle:
    """Parse prompt style string to PromptStyle enum."""
    style_mapping = {
        "detailed": PromptStyle.DETAILED,
        "concise": PromptStyle.CONCISE,
        "balanced": PromptStyle.BALANCED,
    }

    if style_str.lower() not in style_mapping:
        raise ValueError(
            f"Invalid prompt style: {style_str}. "
            f"Choose from: {', '.join(style_mapping.keys())}"
        )
    return style_mapping[style_str.lower()]


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Symptom-to-Drug Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "symptom_name",
        type=str,
        help="The symptom for which to list medications",
    )

    parser.add_argument(
        "--age",
        "-a",
        type=int,
        default=None,
        help="Patient's age in years (0-150)",
    )

    parser.add_argument(
        "--conditions",
        "-c",
        type=str,
        default=None,
        help="Other medical conditions to consider (comma-separated)",
    )

    parser.add_argument(
        "--style",
        "-s",
        type=str,
        choices=["detailed", "concise", "balanced"],
        default="detailed",
        help="Prompt style for analysis (default: detailed)",
    )

    parser.add_argument(
        "--output-dir",
        "-od",
        default="outputs",
        help="Directory for output files (default: outputs).",
    )

    parser.add_argument(
        "--verbosity",
        "-v",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2).",
    )

    parser.add_argument(
        "--structured",
        "-t",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response",
    )

    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="ollama/gemma3",
        help="LLM model to use for analysis (default: ollama/gemma3)",
    )

    return parser.parse_args()


def create_symptom_drug_report(args) -> int:

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "symptom_drugs.log"),
        verbosity=args.verbosity,
        enable_console=True,
    )

    logger.info("=" * 80)
    logger.info("SYMPTOM-TO-DRUG CLI - Starting")
    logger.info("=" * 80)

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        config = SymptomInput(
            symptom_name=args.symptom_name,
            age=args.age,
            other_conditions=args.conditions,
            prompt_style=parse_prompt_style(args.style),
        )

        logger.info("Configuration created successfully")

        model_config = ModelConfig(model=args.model, temperature=0.2)
        analyzer = SymptomDrugs(model_config)
        result = analyzer.generate_text(config, structured=args.structured)

        if result is None:
            logger.error("✗ Failed to analyze symptom and list medications.")
            return 1

        # Save result to output directory
        analyzer.save(result, output_dir)

        logger.debug("✓ Symptom-to-drug analysis completed successfully")
        return 0

    except ValueError as e:
        logger.error(f"✗ Invalid input: {e}")
        return 1
    except Exception as e:
        logger.error(f"✗ Symptom-to-drug analysis failed: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == "__main__":
    args = get_user_arguments()
    create_symptom_drug_report(args)

#!/usr/bin/env python3
"""
Symptom-to-Drug Analysis module.

This module provides the core SymptomDrugs class for listing medications
prescribed for specific symptoms based on clinical guidance.
"""



logger = logging.getLogger(__name__)


class SymptomDrugs:
    """Analyzes symptoms to list medications typically used for treatment."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.config = None  # Store the configuration for later use in save
        logger.debug("Initialized SymptomDrugs")

    def generate_text(
        self, config: SymptomInput, structured: bool = False
    ) -> ModelOutput:
        """Analyzes symptoms using a 3-tier agent system."""
        self.config = config
        logger.info(f"Starting 3-tier analysis for: {config.symptom_name}")

        try:
            # --- Tier 1: Specialists (JSON Sequential) ---
            logger.debug("Tier 1: Specialists running...")
            # 1. Researcher
            res_out = self._ask_llm(ModelInput(
                system_prompt=PromptBuilder.create_researcher_system_prompt(),
                user_prompt=PromptBuilder.create_researcher_user_prompt(config)
            )).markdown

            # 2. Safety
            saf_out = self._ask_llm(ModelInput(
                system_prompt=PromptBuilder.create_safety_system_prompt(),
                user_prompt=PromptBuilder.create_safety_user_prompt(config)
            )).markdown

            # 3. Compliance
            com_out = self._ask_llm(ModelInput(
                system_prompt=PromptBuilder.create_compliance_system_prompt(),
                user_prompt=PromptBuilder.create_compliance_user_prompt(config, res_out, saf_out)
            )).markdown

            # 4. Educator
            edu_out = self._ask_llm(ModelInput(
                system_prompt=PromptBuilder.create_education_system_prompt(),
                user_prompt=PromptBuilder.create_education_user_prompt(config)
            )).markdown

            spec_data_json = f"RESEARCH:\n{res_out}\n\nSAFETY:\n{saf_out}\n\nCOMPLIANCE:\n{com_out}\n\nEDUCATION:\n{edu_out}"

            # --- Tier 2: Compliance Auditor (JSON Audit) ---
            logger.debug("Tier 2: Auditor performing quality check...")
            audit_res = self._ask_llm(ModelInput(
                system_prompt=PromptBuilder.create_reviewer_system_prompt(),
                user_prompt=PromptBuilder.create_reviewer_user_prompt(config, res_out, saf_out, com_out, edu_out),
                response_format=SymptomDrugAnalysisModel if structured else None
            ))
            
            if structured:
                audit_json = audit_res.data.model_dump_json(indent=2)
            else:
                audit_json = audit_res.markdown

            # --- Tier 3: Final Output Synthesis (Markdown Closer) ---
            logger.debug("Tier 3: Output Agent synthesizing final report...")
            out_sys, out_usr = PromptBuilder.create_output_synthesis_prompts(config, spec_data_json, audit_json)
            final_res = self._ask_llm(ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None
            ))

            logger.info(f"✓ Successfully generated 3-tier treatment report for: {config.symptom_name}")
            return ModelOutput(
                data=audit_res.data if structured else None, 
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier Symptom-Drug generation failed: {e}")
            raise

    def _ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Helper to call LiteClient with error handling and ensure ModelOutput return."""
        logger.debug("Calling LiteClient...")
        try:
            response = self.client.generate_text(model_input=model_input)
            
            # If the response is already a ModelOutput, return it
            if isinstance(response, ModelOutput):
                return response
            
            # If it's a Pydantic model (structured output from LiteClient)
            if hasattr(response, "model_dump"):
                return ModelOutput(data=response)
                
            # If it's a string, wrap it in ModelOutput as markdown
            if isinstance(response, str):
                return ModelOutput(markdown=response)
            
            # Fallback for other types
            return ModelOutput(markdown=str(response))
            
        except Exception as e:
            logger.error(f"✗ Error during LLM analysis: {e}")
            logger.exception("Full exception details:")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the symptom-to-drug analysis to a file."""
        if self.config is None:
            raise ValueError(
                "No configuration information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        symptom_safe = self.config.symptom_name.lower().replace(" ", "_")
        base_filename = f"{symptom_safe}_drug_recommendations"

        return save_model_response(result, output_dir / base_filename)

