"""
liteagents.py - Unified for med_myths_checker
"""
from .medical_myth_checker_models import MedicalMythAnalysisModel, ModelOutput\nfrom lite.utils import save_model_response\nfrom typing import Optional\nfrom tqdm import tqdm\nfrom app.MedKit.medical.med_myths_checker.shared.models import *\nimport logging\nfrom lite.lite_client import LiteClient\nfrom pathlib import Path\nimport argparse\nfrom lite.config import ModelConfig\nfrom lite.config import ModelConfig, ModelInput\nfrom lite.logging_config import configure_logging\nimport sys\nfrom .medical_myth_checker_prompts import PromptBuilder\n\n"""Medical Myth Checker CLI."""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))




try:
    from .medical_myth_checker import MedicalMythsChecker
except (ImportError, ValueError):
    from medical.med_myths_checker.agentic.medical_myth_checker import MedicalMythsChecker

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze medical myths and provide evidence-based assessments."
    )
    parser.add_argument("myth", help="Medical myth or file path containing myths.")
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
        log_file="medical_myth_checker.log",
        verbosity=args.verbosity,
        enable_console=True,
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.myth)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.myth]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        checker = MedicalMythsChecker(model_config)

        for item in tqdm(items, desc="Analyzing"):
            result = checker.generate_text(myth=item, structured=args.structured)
            if result:
                checker.save(result, output_dir)

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
Medical Myths Checker module.

This module provides the core MedicalMythsChecker class for analyzing
medical myths for factual accuracy based on peer-reviewed evidence.
"""




logger = logging.getLogger(__name__)


class MedicalMythsChecker:
    """Analyzes medical myths for factual accuracy based on peer-reviewed evidence."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the myths checker."""
        self.client = LiteClient(model_config=model_config)
        self.myth: Optional[str] = None

    def generate_text(self, myth: str, structured: bool = False) -> ModelOutput:
        """Analyze a medical myth using a 3-tier agent system."""
        if not myth or not myth.strip():
            raise ValueError("Myth statement cannot be empty")

        self.myth = myth
        logger.info(f"Starting 3-tier myth analysis for: {myth}")

        try:
            # 1. Specialist Stage (JSON)
            logger.debug("[Specialist] Analyzing myth evidence...")
            spec_input = ModelInput(
                system_prompt=PromptBuilder.system_prompt(),
                user_prompt=PromptBuilder.user_prompt(myth),
                response_format=MedicalMythAnalysisModel if structured else None,
            )
            spec_res = self._ask_llm(spec_input)
            
            if structured:
                spec_json = spec_res.data.model_dump_json(indent=2)
            else:
                spec_json = spec_res.markdown

            # 2. Auditor Stage (JSON Audit)
            logger.debug("[Auditor] Auditing evidence...")
            audit_sys, audit_usr = PromptBuilder.get_evidence_auditor_prompts(myth, spec_json)
            audit_input = ModelInput(
                system_prompt=audit_sys,
                user_prompt=audit_usr,
                response_format=None # Audit result
            )
            audit_res = self._ask_llm(audit_input)
            audit_json = audit_res.markdown

            # 3. Final Synthesis Stage (Markdown Closer)
            logger.debug("[Output] Synthesizing final report...")
            out_sys, out_usr = PromptBuilder.get_output_synthesis_prompts(myth, spec_json, audit_json)
            out_input = ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None,
            )
            final_res = self._ask_llm(out_input)

            logger.info("✓ Successfully generated 3-tier myth analysis")
            return ModelOutput(
                data=spec_res.data, 
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier Myth generation failed: {e}")
            raise

    def _ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """
        Internal helper to call the LLM client.
        """
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical myth analysis to a file."""
        if self.myth is None:
            raise ValueError("No myth information available. Call generate_text first.")

        # Generate base filename - save_model_response will add appropriate extension
        # Create a safe filename from the myth statement
        safe_myth = (
            self.myth.lower()[:50].replace(" ", "_").replace('"', "").replace("'", "")
        )
        base_filename = f"myth_analysis_{safe_myth}"

        return save_model_response(result, output_dir / base_filename)

