#!/usr/bin/env python3
"""
Orchestrator for the Medical Anatomy Generator-Evaluator (Maker-Checker) workflow.

This script coordinates the MedicalAnatomyGenerator (Maker) and the
AnatomyReportEvaluator (Checker) to produce high-quality, verified anatomical reports.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional

from tqdm import tqdm

# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from lite.lite_client import LiteClient

try:
    from .medical_anatomy import MedicalAnatomyGenerator
    from .evaluate_anatomy_report import AnatomyReportEvaluator, AnatomyEvaluationResult
    from .medical_anatomy_models import FactCheckModel
    from .medical_anatomy_prompts import PromptBuilder
except (ImportError, ValueError):
    from medical.anatomy.agentic.medical_anatomy import MedicalAnatomyGenerator
    from medical.anatomy.agentic.evaluate_anatomy_report import AnatomyReportEvaluator, AnatomyEvaluationResult
    from medical.anatomy.agentic.medical_anatomy_models import FactCheckModel
    from medical.anatomy.agentic.medical_anatomy_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class AgenticAnatomyWorkflow:
    """Orchestrates the Generator-Evaluator workflow."""

    def __init__(
        self,
        generator_model: str,
        evaluator_model: str,
        output_dir: Path,
        structured: bool = False,
    ):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.structured = structured

        # Initialize Generator Agent
        gen_config = ModelConfig(model=generator_model, temperature=0.2)
        self.generator = MedicalAnatomyGenerator(gen_config)

        # Initialize Evaluator Agent
        # If evaluator_model is the same as generator_model, we still create a separate instance
        # although they might share the same underlying LiteClient logic if needed.
        self.evaluator = AnatomyReportEvaluator(model=evaluator_model)

        # Initialize Fact-Checker Auditor
        self.auditor_client = LiteClient(ModelConfig(model=evaluator_model, temperature=0.0))

        logger.info(f"Workflow initialized: Generator={generator_model}, Evaluator={evaluator_model}")

    def run_workflow(self, body_part: str) -> Optional[AnatomyEvaluationResult]:
        """Runs the generation then evaluation for a single body part."""
        logger.info(f"--- Processing: {body_part} ---")

        # 1. Generation Phase (Maker)
        print(f"  [Maker] Generating anatomical report for {body_part}...")
        try:
            gen_result = self.generator.generate_text(body_part, structured=self.structured)
            report_path = self.generator.save(gen_result, self.output_dir)
            print(f"  ✓ [Maker] Report saved to {report_path}")
        except Exception as e:
            logger.error(f"  ❌ [Maker] Generation failed: {e}")
            return None

        # Extract technical section for fact-checking
        report_md = gen_result.markdown
        if "SECTION 1" in report_md:
            technical_content = report_md.split("SECTION 1:")[1].split("---")[0].strip()
        else:
            technical_content = report_md

        # 2. Fact-Checking Phase (Auditor)
        print(f"  [Auditor] Verifying anatomical claims for {body_part}...")
        try:
            fact_check = self._run_fact_checker(technical_content)
            self._print_fact_check_summary(fact_check)
        except Exception as e:
            logger.error(f"  ❌ [Auditor] Fact-check failed: {e}")
            fact_check = None

        # 3. Evaluation Phase (Checker)
        print(f"  [Checker] Evaluating report for {body_part}...")
        try:
            eval_result = self.evaluator.evaluate_file(report_path)
            self._print_evaluation_summary(eval_result)
            return eval_result
        except Exception as e:
            logger.error(f"  ❌ [Checker] Evaluation failed: {e}")
            return None

    def _run_fact_checker(self, technical_report: str) -> FactCheckModel:
        """Run the Fact-Checker agent."""
        system_prompt = PromptBuilder.create_fact_checker_system_prompt()
        user_prompt = PromptBuilder.create_fact_checker_user_prompt(technical_report)

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=FactCheckModel,
        )

        return self.auditor_client.generate_text(model_input=model_input)

    def _print_fact_check_summary(self, result: FactCheckModel):
        """Prints a summary of the fact-check results."""
        print(f"\n  🔍 Fact-Check Summary (Accuracy: {result.accuracy_score}%)")
        
        incorrect_claims = [c for c in result.claims if c.status.lower() == 'incorrect']
        if incorrect_claims:
            print(f"  🔴 Found {len(incorrect_claims)} incorrect claims:")
            for c in incorrect_claims:
                print(f"    - Claim: {c.claim}")
                print(f"      Correction: {c.correction}")
        else:
            print("  ✅ All anatomical claims verified successfully.")
        
        print(f"  Summary: {result.summary}")
        print("-" * 50)

    def _print_evaluation_summary(self, result: AnatomyEvaluationResult):
        """Prints a concise summary of the evaluation."""
        status_color = {
            "PASS": "✅",
            "CONDITIONAL_PASS": "⚠️",
            "FAIL": "❌"
        }.get(result.pass_fail_status, "❓")

        print(f"\n  {status_color} Evaluation Result: {result.pass_fail_status}")
        print(f"  Quality Score: {result.overall_quality_score}/100")
        
        # Display key ratings
        print(f"  Accuracy:      {result.anatomical_accuracy[0].value}")
        print(f"  Clinical:      {result.clinical_reliability[0].value}")
        print(f"  Accessibility: {result.general_accessibility[0].value}")
        
        if result.critical_issues:
            print(f"  🔴 Critical Issues ({len(result.critical_issues)}):")
            for issue in result.critical_issues[:3]:
                print(f"    - {issue}")
        
        if result.pass_fail_status == "FAIL":
            print("  ❌ Report failed clinical safety, accuracy, or simplification checks.")
        elif result.pass_fail_status == "CONDITIONAL_PASS":
            print("  ⚠️ Report has minor issues that should be addressed.")
        else:
            print("  ✅ Report passed all strict anatomical and accessibility standards.")
        print("-" * 50)


def get_args():
    parser = argparse.ArgumentParser(
        description="Agentic Medical Anatomy Workflow (Maker-Checker)"
    )
    parser.add_argument(
        "body_part", help="Anatomical part to analyze (or file with list of parts)."
    )
    parser.add_argument(
        "-d", "--output-dir", default="agentic_outputs", help="Output directory."
    )
    parser.add_argument(
        "-gm", "--gen-model", default="ollama/gemma3", help="Model for Generator Agent."
    )
    parser.add_argument(
        "-em", "--eval-model", default="ollama/gemma3", help="Model for Evaluator Agent."
    )
    parser.add_argument(
        "-s", "--structured", action="store_true", help="Use structured output for generation."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging."
    )
    return parser.parse_args()


def main():
    args = get_args()
    configure_logging(
        log_file="anatomy_workflow.log", 
        verbosity=4 if args.verbose else 3, 
        enable_console=args.verbose
    )

    input_path = Path(args.body_part)
    if input_path.is_file():
        with open(input_path, "r") as f:
            items = [line.strip() for line in f if line.strip()]
    else:
        items = [args.body_part]

    workflow = AgenticAnatomyWorkflow(
        generator_model=args.gen_model,
        evaluator_model=args.eval_model,
        output_dir=Path(args.output_dir),
        structured=args.structured
    )

    print(f"\n🚀 Starting Agentic Anatomy Workflow on {len(items)} item(s)\n")
    
    results = []
    for item in items:
        res = workflow.run_workflow(item)
        if res:
            results.append(res)

    # Final summary
    if len(items) > 1:
        print("\n" + "=" * 50)
        print("WORKFLOW BATCH SUMMARY")
        print("=" * 50)
        passed = sum(1 for r in results if r.pass_fail_status == "PASS")
        failed = sum(1 for r in results if r.pass_fail_status == "FAIL")
        conditional = sum(1 for r in results if r.pass_fail_status == "CONDITIONAL_PASS")
        
        print(f"Total processed: {len(results)}")
        print(f"✅ PASSED: {passed}")
        print(f"⚠️  CONDITIONAL: {conditional}")
        print(f"❌ FAILED: {failed}")
        print("=" * 50)


if __name__ == "__main__":
    main()
