"""Module docstring - Evaluate Physical Exam Questions.

This module assesses the quality and compliance of medical exam questions using LLM-powered
evaluation. It analyzes question clarity, clinical relevance, medical standards compliance,
cultural sensitivity, and trauma-informed design. Generates detailed evaluation reports with
scored criteria, section-specific feedback, strengths, improvement areas, and recommendations.
"""

# ==============================================================================
# STANDARD LIBRARY IMPORTS
# ==============================================================================
import argparse
import json
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# ==============================================================================
# THIRD-PARTY IMPORTS
# ==============================================================================
from rich.console import Console
from rich.panel import Panel

# ==============================================================================
# LOCAL IMPORTS (LiteClient setup)
# ==============================================================================
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

# ==============================================================================
# LOCAL IMPORTS (Module models)
# ==============================================================================
from eval_physical_exam_questions_models import QualityEvaluation

# ==============================================================================
# LOGGING CONFIGURATION
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==============================================================================
# CONSTANTS
# ==============================================================================
console = Console()

# ==============================================================================
# CONFIGURATION CLASS
# ==============================================================================

@dataclass
class EvalPhysicalExamConfig:
    """Configuration for evaluating physical exam questions."""
    output_path: Optional[Path] = None
    output_dir: Path = Path("outputs")
    verbosity: bool = False


# ==============================================================================
# MAIN CLASS
# ==============================================================================

class PhysicalExamEvaluator:
    """Evaluates quality of generated physical exam questions."""

    def __init__(self, config: EvalPhysicalExamConfig):
        self.config = config
        self.client = LiteClient(
            ModelConfig(model="ollama/gemma3", temperature=0.7)
        )
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

        if self.config.verbosity:
            logger.setLevel("DEBUG")
        else:
            logger.setLevel("INFO")

        logger.info(f"Initialized PhysicalExamEvaluator")

    def evaluate(self, input_file: str) -> QualityEvaluation:
        """
        Evaluate the quality of generated exam questions using LLM assessment.

        Args:
            input_file: Path to JSON file with exam questions

        Returns:
            QualityEvaluation: Validated evaluation results
        """
        logger.info("-" * 80)
        logger.info(f"Starting exam question evaluation")
        logger.info(f"Input file: {input_file}")

        try:
            # Load the generated questions
            with open(input_file, 'r') as f:
                exam_data = json.load(f)

            # Count questions
            pmh = exam_data.get('past_medical_history', {})
            fh = exam_data.get('family_history', {})
            drug = exam_data.get('drug_information', {})
            vacc = exam_data.get('vaccination', {})
            lifestyle = exam_data.get('lifestyle_and_social', {})

            total_questions = (
                len(pmh.get('condition_questions', [])) + len(pmh.get('hospitalization_questions', [])) + len(pmh.get('surgery_questions', [])) +
                len(fh.get('maternal_history_questions', [])) + len(fh.get('paternal_history_questions', [])) + len(fh.get('genetic_risk_questions', [])) +
                len(drug.get('medication_questions', [])) + len(drug.get('allergy_questions', [])) + len(drug.get('adverse_reaction_questions', [])) +
                len(vacc.get('vaccination_status_questions', [])) + len(vacc.get('vaccine_specific_questions', [])) + len(vacc.get('booster_questions', [])) +
                len(lifestyle.get('lifestyle_questions', [])) + len(lifestyle.get('personal_social_questions', []))
            )

            exam_name = exam_data.get('exam', 'Unknown Exam').title()

            # Create comprehensive evaluation prompt
            prompt = f"""
You are a medical education expert and quality assurance specialist. Evaluate the following medical history questions for quality and compliance with medical standards.

EXAM: {exam_name}
PATIENT AGE: {exam_data.get('age', 'N/A')}
PATIENT GENDER: {exam_data.get('gender', 'N/A')}
PURPOSE: {exam_data.get('purpose', 'physical_exam')}

QUESTIONS DATA:
- Past Medical History Questions: {len(pmh.get('condition_questions', [])) + len(pmh.get('hospitalization_questions', [])) + len(pmh.get('surgery_questions', []))} questions
- Family History Questions: {len(fh.get('maternal_history_questions', [])) + len(fh.get('paternal_history_questions', [])) + len(fh.get('genetic_risk_questions', []))} questions
- Drug Information Questions: {len(drug.get('medication_questions', [])) + len(drug.get('allergy_questions', [])) + len(drug.get('adverse_reaction_questions', []))} questions
- Vaccination Questions: {len(vacc.get('vaccination_status_questions', [])) + len(vacc.get('vaccine_specific_questions', [])) + len(vacc.get('booster_questions', []))} questions
- Lifestyle & Social Questions: {len(lifestyle.get('lifestyle_questions', [])) + len(lifestyle.get('personal_social_questions', []))} questions
- TOTAL QUESTIONS: {total_questions} questions

Provide comprehensive quality evaluation of the exam questions."""

            logger.info("Calling LiteClient.generate_text()...")
            result = self.client.generate_text(
                model_input=ModelInput(
                    user_prompt=prompt,
                    response_format=QualityEvaluation,
                )
            )

            logger.info(f"✓ Successfully evaluated exam questions")
            logger.info(f"Overall Quality Score: {result.overall_quality_score}/100")
            logger.info("-" * 80)
            return result
        except Exception as e:
            logger.error(f"✗ Error evaluating exam questions: {e}")
            logger.exception("Full exception details:")
            logger.info("-" * 80)
            raise


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def print_result(result: QualityEvaluation, verbose: bool = False) -> None:
    """Print result in a formatted manner using rich."""
    console = Console()

    # Extract main fields from the result model
    result_dict = result.model_dump()

    # Create a formatted panel showing the result
    # Use semantic formatting: green for success/positive, yellow for warnings, blue for info
    # Display the data in organized sections

    for section_name, section_value in result_dict.items():
        if section_value is not None:
            if isinstance(section_value, dict):
                formatted_text = "\n".join([f"  [bold]{k}:[/bold] {v}" for k, v in section_value.items()])
            else:
                formatted_text = str(section_value)

            console.print(Panel(
                formatted_text,
                title=section_name.replace('_', ' ').title(),
                border_style="cyan",
            ))


def generate_evaluation_report(evaluation: QualityEvaluation, output_file: Optional[str] = None) -> str:
    """
    Generate a detailed evaluation report.

    Args:
        evaluation: QualityEvaluation object with results
        output_file: Optional path to save report

    Returns:
        str: Formatted report text
    """
    report = f"""
╔══════════════════════════════════════════════════════════════════════╗
║          MEDICAL EXAM QUESTIONS - QUALITY EVALUATION REPORT           ║
╚══════════════════════════════════════════════════════════════════════╝

EVALUATION DATE: {Path.cwd()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 OVERALL QUALITY SCORE: {evaluation.overall_quality_score:.1f}/100
Status: {'✓ PASS' if evaluation.pass_fail == 'pass' else '⚠ CONDITIONAL PASS' if evaluation.pass_fail == 'conditional_pass' else '✗ FAIL'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 DETAILED SCORES:

  Medical Standards Compliance:    {evaluation.medical_standards_compliance:.1f}/100
  Question Sufficiency:             {evaluation.question_sufficiency:.1f}/100
  Relevancy to Exam Type:          {evaluation.relevancy_score:.1f}/100
  Clinical Accuracy:                {evaluation.accuracy_score:.1f}/100
  Cultural Sensitivity:             {evaluation.cultural_sensitivity_score:.1f}/100
  Trauma-Informed Approach:         {evaluation.trauma_informed_score:.1f}/100

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💪 STRENGTHS:
"""
    for i, strength in enumerate(evaluation.strengths, 1):
        report += f"\n  {i}. {strength}"

    report += f"\n\n⚠ AREAS FOR IMPROVEMENT:\n"
    for i, improvement in enumerate(evaluation.areas_for_improvement, 1):
        report += f"\n  {i}. {improvement}"

    report += f"\n\n💡 RECOMMENDATIONS:\n"
    for i, rec in enumerate(evaluation.recommendations, 1):
        report += f"\n  {i}. {rec}"

    report += f"\n\n╔══════════════════════════════════════════════════════════════════════╗\n"
    report += f"║ FINAL VERDICT: {evaluation.pass_fail.upper()}\n"
    report += f"╚══════════════════════════════════════════════════════════════════════╝\n"

    # Save report if output file specified
    if output_file:
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(report)
        logger.info(f"✓ Report saved to {output_file}")

    return report


# ==============================================================================
# ARGUMENT PARSER
# ==============================================================================


# ==============================================================================
# MAIN FUNCTION
# ==============================================================================

def main() -> int:
    """
    CLI entry point for evaluating physical exam questions.
    """
    logger.info("="*80)
    logger.info("EVAL PHYSICAL EXAM QUESTIONS CLI - Starting")
    logger.info("="*80)

    parser = argparse.ArgumentParser(
        description="Evaluate quality of generated physical exam questions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python eval_physical_exam_questions_cli.py -i exam_questions.json
  python eval_physical_exam_questions_cli.py -i exam_questions.json -o report.txt
  python eval_physical_exam_questions_cli.py -i exam_questions.json -j results.json -v
        """
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Input JSON file from medical exam generator"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output evaluation report file"
    )
    parser.add_argument(
        "-j", "--json-output",
        help="Output evaluation results as JSON"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose/debug logging output."
    )

    args = parser.parse_args()

    logger.info(f"CLI Arguments:")
    logger.info(f"  Input file: {args.input}")
    logger.info(f"  Report output: {args.output if args.output else 'None'}")
    logger.info(f"  JSON output: {args.json_output if args.json_output else 'None'}")
    logger.info(f"  Verbose: {args.verbose}")

    # Create configuration
    config = EvalPhysicalExamConfig(verbosity=args.verbose)

    try:
        # Evaluate questions
        logger.info(f"Evaluating: {args.input}")
        evaluator = PhysicalExamEvaluator(config)
        evaluation = evaluator.evaluate(args.input)

        # Display formatted result
        print_result(evaluation, args.verbose)

        # Generate and display report
        report = generate_evaluation_report(evaluation, args.output)
        console.print(report)

        # Save JSON results if requested
        if args.json_output:
            Path(args.json_output).parent.mkdir(parents=True, exist_ok=True)
            with open(args.json_output, 'w') as f:
                json.dump(evaluation.model_dump(), f, indent=2)
            logger.info(f"✓ JSON evaluation saved to {args.json_output}")

        logger.info("="*80)
        logger.info("✓ Evaluation completed successfully")
        logger.info("="*80)
        return 0

    except Exception as e:
        logger.error("="*80)
        logger.error(f"✗ Evaluation failed: {e}")
        logger.exception("Full exception details:")
        logger.error("="*80)
        sys.exit(1)


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    sys.exit(main())
