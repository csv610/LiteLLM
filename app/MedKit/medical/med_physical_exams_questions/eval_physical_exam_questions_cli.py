import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Optional, Union



sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.utils import save_model_response
from lite.config import ModelConfig, ModelInput
from utils.output_formatter import print_result
from lite.logging_config import configure_logging

from eval_physical_exam_questions_models import QualityEvaluation

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builder class for creating prompts for physical exam question evaluation."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for physical exam question evaluation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are a medical education expert and quality assurance specialist with expertise in evaluating medical history questionnaires and physical examination protocols.

Your responsibilities include:
- Evaluating the quality, clarity, and appropriateness of medical history questions
- Assessing compliance with medical standards and best practices
- Identifying gaps in coverage or areas for improvement
- Ensuring questions are age-appropriate, gender-appropriate, and culturally sensitive
- Verifying that questions follow proper medical interview techniques
- Checking for completeness across all relevant medical history domains

Guidelines:
- Evaluate questions for clinical relevance and accuracy
- Assess the comprehensiveness of coverage across medical history categories
- Check for appropriate depth and breadth of questioning
- Ensure questions are clear, unambiguous, and patient-friendly
- Identify any redundant, inappropriate, or poorly worded questions
- Base evaluation on established medical education and clinical practice standards
- Provide constructive feedback for improvement"""

    @staticmethod
    def create_user_prompt(exam_data: dict) -> str:
        """
        Create the user prompt for evaluating physical exam questions.

        Args:
            exam_data: Dictionary containing exam question data

        Returns:
            str: Formatted user prompt
        """
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

        return f"""Evaluate the following medical history questions for quality and compliance with medical standards.

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


class PhysicalExamEvaluator:
    """Evaluates quality of generated physical exam questions."""

    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)
        logger.debug(f"Initialized PhysicalExamEvaluator")

    def generate_text(self, input_file: str, structured: bool = False) -> Union[QualityEvaluation, str]:
        """
        Evaluate the quality of generated exam questions using LLM assessment.

        Args:
            input_file: Path to JSON file with exam questions
            structured: Whether to use structured output mode (default: False)

        Returns:
            QualityEvaluation: Validated evaluation results (if structured=True, else raw response if applicable)
        """
        logger.debug(f"Starting exam question evaluation")
        logger.debug(f"Input file: {input_file}")

        try:
            with open(input_file, 'r') as f:
                exam_data = json.load(f)

            user_prompt = PromptBuilder.create_user_prompt(exam_data)
            logger.debug(f"Prompt: {user_prompt}")

            response_format = None
            if structured:
                response_format = QualityEvaluation

            model_input = ModelInput(
                system_prompt=PromptBuilder.create_system_prompt(),
                user_prompt=user_prompt,
                response_format=response_format,
            )

            result = self.client.generate_text(model_input=model_input)

            logger.debug(f"✓ Successfully evaluated exam questions")
            return result
        except Exception as e:
            raise
    def _ask_llm(self, model_input: ModelInput) -> Union[QualityEvaluation, str]:
        """Internal helper to call the LLM client."""
        return self.client.generate_text(model_input=model_input)


def generate_evaluation_report(evaluation: Union[QualityEvaluation, str], output_file: Optional[str] = None) -> str:
    """
    Generate a detailed evaluation report.

    Args:
        evaluation: QualityEvaluation object with results
        output_file: Optional path to save report

    Returns:
        str: Formatted report text
    """
    if isinstance(evaluation, str):
        report = evaluation
    else:
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

def main() -> int:
    """
    CLI entry point for evaluating physical exam questions.
    """
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
        "-m", "--model",
        default="gemini-1.5-pro",
        help="LLM model to use (default: gemini-1.5-pro)"
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

    args = parser.parse_args()

    configure_logging(
        log_file="eval_physical_exam_questions.log",
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.info("="*80)
    logger.info("EVAL PHYSICAL EXAM QUESTIONS CLI - Starting")
    logger.info("="*80)

    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Input file: {args.input}")
    logger.debug(f"  Report output: {args.output if args.output else 'None'}")
    logger.debug(f"  JSON output: {args.json_output if args.json_output else 'None'}")
    logger.debug(f"  Verbosity: {args.verbosity}")
    logger.debug(f"  Structured output: {args.structured}")

    # Ensure output directory exists (default outputs dir)
    Path("outputs").mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.7)
        evaluator = PhysicalExamEvaluator(model_config)
        evaluation = evaluator.generate_text(args.input, structured=args.structured)

        print_result(evaluation, title="Physical Exam Questions Evaluation")

        report = generate_evaluation_report(evaluation, args.output)
        print(report)

        if args.json_output:
            Path(args.json_output).parent.mkdir(parents=True, exist_ok=True)
            output_json_path = args.json_output
            if isinstance(evaluation, str) and output_json_path.endswith(".json"):
                 output_json_path = output_json_path.replace(".json", ".md")
            
            with open(output_json_path, 'w') as f:
                if isinstance(evaluation, str):
                    f.write(evaluation)
                else:
                    json.dump(evaluation.model_dump(), f, indent=2)
            logger.info(f"✓ Results saved to {output_json_path}")

        logger.debug("✓ Evaluation completed successfully")
        return 0

    except Exception as e:
        logger.error(f"✗ Evaluation failed: {e}")
        logger.exception("Full exception details:")
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
