"""eval_physical_exam_questions - Evaluate quality of generated physical exam questions.

This module assesses the quality and compliance of medical exam questions using LLM-powered
evaluation. It analyzes question clarity, clinical relevance, medical standards compliance,
cultural sensitivity, and trauma-informed design. Generates detailed evaluation reports with
scored criteria, section-specific feedback, strengths, improvement areas, and recommendations.

QUICK START:
    Evaluate exam questions from a JSON file:

    >>> from eval_physical_exam_questions import evaluate_exam_questions
    >>> evaluation = evaluate_exam_questions("exam_questions.json")
    >>> print(f"Overall Score: {evaluation.overall_quality_score}/100")

    Or use the CLI:

    $ python eval_physical_exam_questions.py -i exam_questions.json
    $ python eval_physical_exam_questions.py -i exam_questions.json -o report.txt -j results.json

COMMON USES:
    1. Question quality assurance - validating exam question sets before deployment
    2. Curriculum development - ensuring questions meet medical education standards
    3. Compliance verification - checking cultural sensitivity and trauma-informed design
    4. Performance improvement - identifying specific areas needing revision
    5. Standards compliance - confirming adherence to medical examination guidelines

KEY FEATURES AND COVERAGE AREAS:
    - Medical Standards Compliance: validates against current medical guidelines
    - Question Sufficiency: checks adequate coverage across exam sections
    - Relevancy Scoring: measures alignment with specific exam types
    - Clinical Accuracy: verifies evidence-based medical information
    - Clarity Assessment: evaluates patient comprehensibility
    - Cultural Sensitivity: ensures respectful language and inclusive design
    - Trauma-Informed Evaluation: assesses sensitivity to patient safety and autonomy
    - Detailed Section Evaluations: feedback for each exam section
    - Pass/Fail Verdict: overall quality determination
"""

import json
import argparse
from pathlib import Path
from medkit.core.medkit_client import MedKitClient
from eval_physical_exam_questions_models import QualityEvaluation


def evaluate_exam_questions(input_file: str) -> QualityEvaluation:
    """Evaluate the quality of generated exam questions using LLM assessment."""

    # Load the generated questions
    with open(input_file, 'r') as f:
        exam_data = json.load(f)

    # Load model name from ModuleConfig


    model_name = "ollama/gemma3:12b"  # Default model for this module


    


    client = MedKitClient(model_name=model_name)

    # Count questions from new format
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

    SAMPLE QUESTIONS:
    {json.dumps([pmh.get('condition_questions', [{}])[0]], indent=2)[:500]}...

    EVALUATION CRITERIA:
    1. Medical Standards Compliance (0-100): Do questions follow current medical guidelines and best practices?
    2. Question Sufficiency (0-100): Are there enough questions in each section? (Medical exams typically need 15-20+ questions)
    3. Relevancy (0-100): Are questions relevant and specific to the {exam_name} exam?
    4. Clinical Accuracy (0-100): Is clinical information accurate and evidence-based?
    5. Clarity (0-100): Are questions clear, concise, and understandable to patients?
    6. Cultural Sensitivity (0-100): Does language respect diverse cultural backgrounds?
    7. Trauma-Informed Approach (0-100): Does content follow trauma-informed care principles?
    8. Patient Safety (0-100): Does content prioritize patient safety, consent, and autonomy?

    Provide evaluation as JSON with these fields:
    {{
        "overall_quality_score": (0-100),
        "medical_standards_compliance": (0-100),
        "question_sufficiency": (0-100),
        "relevancy_score": (0-100),
        "accuracy_score": (0-100),
        "clarity_score": (0-100),
        "cultural_sensitivity_score": (0-100),
        "trauma_informed_score": (0-100),
        "strengths": ["list of 3-5 strengths"],
        "areas_for_improvement": ["list of 3-5 areas"],
        "recommendations": ["list of 3-5 recommendations"],
        "section_feedback": {{
            "exam_questions": {{"sufficiency": "adequate/insufficient/excessive", "feedback": "..."}},
            "family_history_questions": {{"sufficiency": "adequate/insufficient/excessive", "feedback": "..."}},
            "medical_drug_history_questions": {{"sufficiency": "adequate/insufficient/excessive", "feedback": "..."}},
            "lifestyle_social_history_questions": {{"sufficiency": "adequate/insufficient/excessive", "feedback": "..."}},
            "psychological_comfort_questions": {{"sufficiency": "adequate/insufficient/excessive", "feedback": "..."}},
            "trauma_history_questions": {{"sufficiency": "adequate/insufficient/excessive", "feedback": "..."}},
            "introduction": {{"feedback": "..."}}
        }},
        "pass_fail": "pass/conditional_pass/fail"
    }}
    """

    # Get LLM evaluation
    evaluation_result = client.generate_text(prompt, schema=QualityEvaluation, sys_prompt=prompt)

    # Set exam_name if not already set
    if not hasattr(evaluation_result, 'exam_name') or evaluation_result.exam_name is None:
        evaluation_result.exam_name = exam_name

    return evaluation_result


def generate_evaluation_report(evaluation: QualityEvaluation, output_file: str = None):
    """Generate a detailed evaluation report."""

    report = f"""
╔══════════════════════════════════════════════════════════════════════╗
║          MEDICAL EXAM QUESTIONS - QUALITY EVALUATION REPORT           ║
╚══════════════════════════════════════════════════════════════════════╝

EXAM: {evaluation.exam_name}
EVALUATION DATE: {Path.cwd()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 OVERALL QUALITY SCORE: {evaluation.overall_quality_score:.1f}/100
Status: {'✅ PASS' if evaluation.pass_fail == 'pass' else '⚠️ CONDITIONAL PASS' if evaluation.pass_fail == 'conditional_pass' else '❌ FAIL'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 DETAILED SCORES:

  🏥 Medical Standards Compliance:    {evaluation.medical_standards_compliance:.1f}/100
  ✅ Question Sufficiency:             {evaluation.question_sufficiency:.1f}/100
  🎯 Relevancy to Exam Type:          {evaluation.relevancy_score:.1f}/100
  🔬 Clinical Accuracy:                {evaluation.accuracy_score:.1f}/100
  🌍 Cultural Sensitivity:             {evaluation.cultural_sensitivity_score:.1f}/100
  💙 Trauma-Informed Approach:         {evaluation.trauma_informed_score:.1f}/100

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💪 STRENGTHS:
"""
    for i, strength in enumerate(evaluation.strengths, 1):
        report += f"\n  {i}. {strength}"

    report += f"\n\n⚠️ AREAS FOR IMPROVEMENT:\n"
    for i, improvement in enumerate(evaluation.areas_for_improvement, 1):
        report += f"\n  {i}. {improvement}"

    report += f"\n\n💡 RECOMMENDATIONS:\n"
    for i, rec in enumerate(evaluation.recommendations, 1):
        report += f"\n  {i}. {rec}"

    report += f"\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    report += f"\nSECTION EVALUATIONS:\n"

    for section in evaluation.section_evaluations:
        status_icon = "✅" if section.sufficiency_status == "adequate" else "⚠️" if section.sufficiency_status == "insufficient" else "❌"
        report += f"\n  {status_icon} {section.section_name}"
        report += f"\n     Questions: {section.question_count} ({section.expected_count})"
        report += f"\n     Quality Score: {section.average_quality_score:.1f}/100"
        report += f"\n     Status: {section.sufficiency_status}"
        report += f"\n     Feedback: {section.feedback}\n"

    report += f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    report += f"\nCRITERIA EVALUATION SUMMARY:\n"

    for criteria in evaluation.criteria_evaluations:
        status_icon = "✅" if criteria.status == "pass" else "⚠️" if criteria.status == "warning" else "❌"
        report += f"\n  {status_icon} {criteria.criterion}"
        report += f"\n     Score: {criteria.score:.1f}/{criteria.max_score:.1f}"
        report += f"\n     Status: {criteria.status}"
        report += f"\n     Feedback: {criteria.feedback}\n"

    report += f"\n╔══════════════════════════════════════════════════════════════════════╗\n"
    report += f"║ FINAL VERDICT: {evaluation.pass_fail.upper()}\n"
    report += f"╚══════════════════════════════════════════════════════════════════════╝\n"

    # Save report
    if output_file:
        with open(output_file, 'w') as f:
            f.write(report)
        print(f"✓ Report saved to {output_file}")

    return report


def cli():
    """CLI for evaluating physical exam questions."""
    parser = argparse.ArgumentParser(description="Evaluate quality of generated physical exam questions")
    parser.add_argument("-i", "--input", required=True, help="Input JSON file from medical_physical_exams_questions.py")
    parser.add_argument("-o", "--output", help="Output evaluation report file")
    parser.add_argument("-j", "--json-output", help="Output evaluation results as JSON")

    args = parser.parse_args()

    # Evaluate questions
    print(f"Evaluating: {args.input}")
    evaluation = evaluate_exam_questions(args.input)

    # Generate report
    report = generate_evaluation_report(evaluation, args.output)
    print(report)

    # Save JSON results if requested
    if args.json_output:
        Path("outputs").mkdir(exist_ok=True)
        with open(args.json_output, 'w') as f:
            json.dump(evaluation.model_dump(), f, indent=2)
        print(f"✓ JSON evaluation saved to {args.json_output}")


if __name__ == "__main__":
    cli()
