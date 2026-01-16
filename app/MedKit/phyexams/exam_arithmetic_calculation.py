"""
Arithmetic Calculation Assessment

Evaluate patient arithmetic calculation capabilities through mental math
exercises without paper and pencil using BaseModel definitions and the
MedKit AI client with schema-aware prompting.
"""

import sys
import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional

# Fix import path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.pydantic_prompt_generator import PromptStyle


class SimpleAddition(BaseModel):
    """Patient's ability to perform simple addition mentally."""
    single_digit_addition: str = Field(description="Ability to add single-digit numbers (e.g., 3 + 5, 7 + 8). Provide patient's answers and accuracy")
    two_digit_addition: str = Field(description="Ability to add two-digit numbers (e.g., 23 + 14, 45 + 27). Provide patient's answers and accuracy")
    three_digit_addition: str = Field(description="Ability to add three-digit numbers (e.g., 125 + 234, 456 + 312). Provide patient's answers and accuracy")
    multiple_additions: str = Field(description="Ability to add multiple numbers in sequence (e.g., 5 + 3 + 7, 12 + 8 + 15). Provide patient's answers and accuracy")
    addition_speed: str = Field(description="Speed of response for addition problems - immediate/hesitant/delayed")
    addition_errors: str = Field(description="Types of errors made in addition - none/occasional/frequent/systematic")


class SimpleSubtraction(BaseModel):
    """Patient's ability to perform simple subtraction mentally."""
    single_digit_subtraction: str = Field(description="Ability to subtract single-digit numbers (e.g., 8 - 3, 9 - 5). Provide patient's answers and accuracy")
    two_digit_subtraction: str = Field(description="Ability to subtract two-digit numbers (e.g., 45 - 12, 78 - 34). Provide patient's answers and accuracy")
    three_digit_subtraction: str = Field(description="Ability to subtract three-digit numbers (e.g., 456 - 123, 789 - 234). Provide patient's answers and accuracy")
    subtraction_with_borrowing: str = Field(description="Ability to subtract when borrowing is required (e.g., 25 - 18, 100 - 45). Provide patient's answers and accuracy")
    subtraction_speed: str = Field(description="Speed of response for subtraction problems - immediate/hesitant/delayed")
    subtraction_errors: str = Field(description="Types of errors made in subtraction - none/occasional/frequent/systematic")


class SimpleMultiplication(BaseModel):
    """Patient's ability to perform simple multiplication mentally."""
    single_digit_multiplication: str = Field(description="Ability to multiply single-digit numbers (e.g., 3 × 4, 6 × 7, 8 × 9). Provide patient's answers and accuracy")
    multiplication_by_ten: str = Field(description="Ability to multiply by 10, 100 (e.g., 7 × 10, 12 × 100). Provide patient's answers and accuracy")
    two_digit_multiplication: str = Field(description="Ability to multiply two-digit numbers (e.g., 12 × 5, 15 × 3). Provide patient's answers and accuracy")
    times_tables_recall: str = Field(description="Recall of basic times tables (2x, 5x, 10x tables). Describe fluency and accuracy")
    multiplication_speed: str = Field(description="Speed of response for multiplication problems - immediate/hesitant/delayed")
    multiplication_errors: str = Field(description="Types of errors made in multiplication - none/occasional/frequent/systematic")


class SimpleDivision(BaseModel):
    """Patient's ability to perform simple division mentally."""
    single_digit_division: str = Field(description="Ability to divide single-digit results (e.g., 8 ÷ 2, 15 ÷ 3, 20 ÷ 4). Provide patient's answers and accuracy")
    division_by_ten: str = Field(description="Ability to divide by 10, 100 (e.g., 50 ÷ 10, 200 ÷ 100). Provide patient's answers and accuracy")
    division_with_remainder: str = Field(description="Ability to divide with remainders (e.g., 17 ÷ 5, 23 ÷ 4). Provide patient's answers and accuracy")
    simple_fractions: str = Field(description="Understanding of simple fractions (e.g., half of 10, quarter of 20). Provide patient's answers and accuracy")
    division_speed: str = Field(description="Speed of response for division problems - immediate/hesitant/delayed")
    division_errors: str = Field(description="Types of errors made in division - none/occasional/frequent/systematic")


class MixedOperations(BaseModel):
    """Patient's ability to perform calculations mixing different operations."""
    order_of_operations: str = Field(description="Understanding of order of operations (e.g., 2 + 3 × 4, 10 - 2 × 3). Provide patient's answers and accuracy")
    two_step_problems: str = Field(description="Ability to solve two-step problems (e.g., 'add 5 and 3, then multiply by 2'). Provide patient's answers and accuracy")
    word_problems_simple: str = Field(description="Ability to solve simple word problems mentally (e.g., 'If you have 10 apples and eat 3, how many remain?'). Provide patient's answers and accuracy")
    percentage_simple: str = Field(description="Ability to calculate simple percentages (e.g., 50% of 20, 10% of 100). Provide patient's answers and accuracy")
    mixed_operations_speed: str = Field(description="Speed of response for mixed operation problems - immediate/hesitant/delayed")
    mixed_operations_errors: str = Field(description="Types of errors made in mixed operations - none/occasional/frequent/systematic")


class CalculationStrategies(BaseModel):
    """Patient's mental calculation strategies and approaches."""
    counting_on_fingers: str = Field(description="Whether patient uses fingers for counting - not at all/occasionally/frequently/always")
    counting_aloud: str = Field(description="Whether patient counts aloud or subvocalizes - not at all/occasionally/frequently/always")
    calculation_strategies: str = Field(description="Observed strategies used (e.g., rounding, breaking into parts, starting from larger number, etc.)")
    strategy_efficiency: str = Field(description="Effectiveness of strategies used - efficient/moderately efficient/inefficient/disorganized")
    self_correction: str = Field(description="Ability to recognize and correct errors - excellent/good/fair/poor")
    confidence_level: str = Field(description="Patient's confidence in their answers - high/moderate/low/varies by difficulty")


class CognitiveLimitations(BaseModel):
    """Assessment of cognitive limitations in arithmetic processing."""
    dyscalculia_indicators: str = Field(description="Indicators of dyscalculia or arithmetic disorder - present/absent/possible")
    working_memory_limitations: str = Field(description="Evidence of working memory difficulties affecting calculation - yes/no/unclear")
    attention_difficulties: str = Field(description="Difficulties maintaining attention during calculations - yes/no/minimal")
    anxiety_during_calculation: str = Field(description="Math anxiety or performance anxiety observed - yes/no/mild/severe")
    specific_operation_deficits: str = Field(description="Specific operations that are particularly difficult - none/addition/subtraction/multiplication/division/mixed")
    processing_speed: str = Field(description="Overall processing speed for arithmetic - normal/slow/very slow/fast")


class ContextualFactors(BaseModel):
    """Consideration of contextual factors affecting calculation performance."""
    educational_background: str = Field(description="Patient's educational level and math instruction background")
    language_barriers: str = Field(description="Any language barriers affecting understanding of problems - yes/no/possible")
    cultural_numeracy_practices: str = Field(description="Cultural background and typical numeracy practices relevant to assessment")
    fatigue_or_stress_impact: str = Field(description="Observable impact of fatigue, stress, or emotion on performance")
    medication_or_health_effects: str = Field(description="Potential impact of medications, sleep deprivation, or health conditions")
    motivation_level: str = Field(description="Patient's effort and motivation during assessment - high/moderate/low")


class AssessmentSummary(BaseModel):
    """Overall assessment findings and clinical recommendations."""
    calculation_ability_level: str = Field(description="Overall arithmetic calculation ability level (normal/mildly impaired/moderately impaired/severely impaired)")
    arithmetic_strengths: str = Field(description="Identified arithmetic strengths by operation type, comma-separated")
    arithmetic_weaknesses: str = Field(description="Identified arithmetic weaknesses by operation type, comma-separated")
    processing_capabilities: str = Field(description="Assessment of mental processing speed and working memory for arithmetic")
    clinical_significance: str = Field(description="Clinical significance of findings and relationship to diagnosis or condition")
    recommendations: str = Field(description="Recommendations for cognitive support, remediation, or accommodations, comma-separated")
    neuropsychological_referral: str = Field(description="Whether neuropsychological or educational evaluation is recommended and rationale")


class ArithmeticCalculationAssessment(BaseModel):
    """
    Comprehensive arithmetic calculation assessment.

    Organized as a collection of BaseModel sections, each representing
    a distinct aspect of arithmetic and mental calculation evaluation.
    Includes assessment through simple addition, subtraction, multiplication,
    division, and mixed operations without paper and pencil.
    """
    # Addition capabilities
    simple_addition: SimpleAddition

    # Subtraction capabilities
    simple_subtraction: SimpleSubtraction

    # Multiplication capabilities
    simple_multiplication: SimpleMultiplication

    # Division capabilities
    simple_division: SimpleDivision

    # Mixed operations
    mixed_operations: MixedOperations

    # Calculation strategies and approaches
    calculation_strategies: CalculationStrategies

    # Identified limitations
    cognitive_limitations: CognitiveLimitations

    # Contextual factors
    contextual_factors: ContextualFactors

    # Final assessment
    assessment_summary: AssessmentSummary


def ask_arithmetic_questions() -> dict:
    """
    Ask patient arithmetic calculation questions interactively.
    Returns a dictionary of patient responses to be used in assessment.
    """
    print("\n" + "="*60)
    print("ARITHMETIC CALCULATION ASSESSMENT")
    print("="*60)
    print("\nMEASURES: Evaluates patient's mental arithmetic capabilities across:")
    print("  • Single, two, and three-digit addition")
    print("  • Subtraction (with and without borrowing)")
    print("  • Multiplication (single-digit, tables, two-digit)")
    print("  • Division (with remainder, fractions)")
    print("  • Mixed operations and word problems")
    print("  • Mental calculation strategies and efficiency")
    print("  • Processing speed and error patterns")

    print("\nTOP 10 KEY ASSESSMENT QUESTIONS:")
    print("  1. Can you perform single-digit addition accurately (e.g., 3+5, 7+8)?")
    print("  2. Can you add multi-digit numbers mentally (e.g., 45+27, 125+234)?")
    print("  3. Can you subtract with borrowing (e.g., 25-18, 100-45)?")
    print("  4. Do you know multiplication facts fluently (e.g., times tables)?")
    print("  5. Can you multiply multi-digit numbers mentally (e.g., 12×5, 15×3)?")
    print("  6. Can you divide and handle remainders (e.g., 17÷5)?")
    print("  7. Do you understand order of operations (e.g., 2+3×4)?")
    print("  8. Can you solve simple word problems mentally (e.g., apples, percentages)?")
    print("  9. What strategies do you use for mental math (counting, rounding, breaking down)?")
    print(" 10. Do you experience math anxiety, and how confident are you in your answers?")

    print("\n" + "="*60)
    print("MENTAL ARITHMETIC ASSESSMENT QUESTIONNAIRE")
    print("="*60)
    print("Please answer these math problems mentally (no paper/pencil).")

    responses = {}

    # ADDITION
    print("\n--- ADDITION ---")
    responses['add_1'] = input("What is 3 + 5? ").strip()
    responses['add_2'] = input("What is 12 + 8? ").strip()
    responses['add_3'] = input("What is 45 + 27? ").strip()
    responses['add_4'] = input("What is 125 + 234? ").strip()
    responses['add_multiple'] = input("What is 5 + 3 + 7? ").strip()

    # SUBTRACTION
    print("\n--- SUBTRACTION ---")
    responses['sub_1'] = input("What is 8 - 3? ").strip()
    responses['sub_2'] = input("What is 25 - 12? ").strip()
    responses['sub_3'] = input("What is 100 - 45? ").strip()
    responses['sub_4'] = input("What is 456 - 123? ").strip()
    responses['sub_borrow'] = input("What is 25 - 18? ").strip()

    # MULTIPLICATION
    print("\n--- MULTIPLICATION ---")
    responses['mul_1'] = input("What is 3 × 4? ").strip()
    responses['mul_2'] = input("What is 7 × 8? ").strip()
    responses['mul_3'] = input("What is 12 × 5? ").strip()
    responses['mul_4'] = input("What is 15 × 3? ").strip()
    responses['mul_10'] = input("What is 7 × 10? ").strip()

    # DIVISION
    print("\n--- DIVISION ---")
    responses['div_1'] = input("What is 8 ÷ 2? ").strip()
    responses['div_2'] = input("What is 15 ÷ 3? ").strip()
    responses['div_3'] = input("What is 50 ÷ 10? ").strip()
    responses['div_remainder'] = input("What is 17 ÷ 5? (with remainder if needed) ").strip()
    responses['frac_1'] = input("What is half of 10? ").strip()

    # MIXED OPERATIONS
    print("\n--- MIXED OPERATIONS ---")
    responses['mixed_1'] = input("What is 2 + 3 × 4? ").strip()
    responses['mixed_2'] = input("What is 10 - 2 × 3? ").strip()
    responses['word_1'] = input("If you have 10 apples and eat 3, how many remain? ").strip()
    responses['percent_1'] = input("What is 50% of 20? ").strip()

    # SELF-ASSESSMENT
    print("\n--- SELF-ASSESSMENT ---")
    responses['confidence'] = input("How confident are you in your answers? (very/somewhat/not very): ").strip()
    responses['strategy'] = input("What strategies did you use? (counting, rounding, breaking down, etc.): ").strip()
    responses['finger_use'] = input("Did you use your fingers for counting? (no/yes/sometimes): ").strip()
    responses['math_anxiety'] = input("Do you feel anxious about math? (no/mild/moderate/severe): ").strip()

    return responses


def create_arithmetic_assessment_from_responses(patient_name: str, responses: dict, output_path: Optional[Path] = None) -> ArithmeticCalculationAssessment:
    """
    Create a structured arithmetic assessment object from collected patient responses.

    Args:
        patient_name: Name of the patient
        responses: Dictionary of patient responses from questions
        output_path: Optional path to save JSON output

    Returns:
        ArithmeticCalculationAssessment: Validated assessment object
    """
    # Create assessment object from responses
    assessment_data = {
        "simple_addition": {
            "single_digit_addition": f"3+5={responses.get('add_1', '')}, 12+8={responses.get('add_2', '')}",
            "two_digit_addition": responses.get('add_3', ''),
            "three_digit_addition": responses.get('add_4', ''),
            "multiple_additions": responses.get('add_multiple', ''),
            "addition_speed": "To be assessed",
            "addition_errors": "To be assessed"
        },
        "simple_subtraction": {
            "single_digit_subtraction": f"8-3={responses.get('sub_1', '')}, 25-12={responses.get('sub_2', '')}",
            "two_digit_subtraction": responses.get('sub_3', ''),
            "three_digit_subtraction": responses.get('sub_4', ''),
            "subtraction_with_borrowing": responses.get('sub_borrow', ''),
            "subtraction_speed": "To be assessed",
            "subtraction_errors": "To be assessed"
        },
        "simple_multiplication": {
            "single_digit_multiplication": f"3×4={responses.get('mul_1', '')}, 7×8={responses.get('mul_2', '')}",
            "multiplication_by_ten": responses.get('mul_10', ''),
            "two_digit_multiplication": f"12×5={responses.get('mul_3', '')}, 15×3={responses.get('mul_4', '')}",
            "times_tables_recall": "To be assessed",
            "multiplication_speed": "To be assessed",
            "multiplication_errors": "To be assessed"
        },
        "simple_division": {
            "single_digit_division": f"8÷2={responses.get('div_1', '')}, 15÷3={responses.get('div_2', '')}",
            "division_by_ten": responses.get('div_3', ''),
            "division_with_remainder": responses.get('div_remainder', ''),
            "simple_fractions": responses.get('frac_1', ''),
            "division_speed": "To be assessed",
            "division_errors": "To be assessed"
        },
        "mixed_operations": {
            "order_of_operations": f"2+3×4={responses.get('mixed_1', '')}, 10-2×3={responses.get('mixed_2', '')}",
            "two_step_problems": "Asked during assessment",
            "word_problems_simple": responses.get('word_1', ''),
            "percentage_simple": responses.get('percent_1', ''),
            "mixed_operations_speed": "To be assessed",
            "mixed_operations_errors": "To be assessed"
        },
        "calculation_strategies": {
            "counting_on_fingers": responses.get('finger_use', ''),
            "counting_aloud": "Not observed",
            "calculation_strategies": responses.get('strategy', ''),
            "strategy_efficiency": "To be assessed",
            "self_correction": "To be assessed",
            "confidence_level": responses.get('confidence', '')
        },
        "cognitive_limitations": {
            "dyscalculia_indicators": "Not indicated",
            "working_memory_limitations": "To be assessed",
            "attention_difficulties": "Not observed",
            "anxiety_during_calculation": responses.get('math_anxiety', ''),
            "specific_operation_deficits": "To be assessed",
            "processing_speed": "To be assessed"
        },
        "contextual_factors": {
            "educational_background": "To be assessed",
            "language_barriers": "Not indicated",
            "cultural_numeracy_practices": "To be assessed",
            "fatigue_or_stress_impact": "Not observed",
            "medication_or_health_effects": "None reported",
            "motivation_level": "Good effort"
        },
        "assessment_summary": {
            "calculation_ability_level": "To be determined by clinician",
            "arithmetic_strengths": "To be identified",
            "arithmetic_weaknesses": "To be identified",
            "processing_capabilities": "To be assessed",
            "clinical_significance": "To be determined",
            "recommendations": "Routine cognitive screening",
            "neuropsychological_referral": "Not indicated at this time"
        }
    }

    # Create assessment object
    assessment = ArithmeticCalculationAssessment(**assessment_data)

    # Save to file if path provided
    if output_path is None:
        output_path = Path("outputs") / f"{patient_name.lower().replace(' ', '_')}_arithmetic_calculation.json"

    # Create outputs directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save assessment as JSON
    with open(output_path, 'w') as f:
        json.dump(assessment_data, f, indent=2)

    print(f"\n✓ Assessment saved to: {output_path}")

    return assessment


def evaluate_arithmetic_calculation(
    patient_name: str,
    output_path: Optional[Path] = None,
    use_schema_prompt: bool = True,
    prompt_style: PromptStyle = PromptStyle.DETAILED,
) -> ArithmeticCalculationAssessment:
    """
    Evaluate patient arithmetic calculation capabilities through interactive assessment.

    Args:
        patient_name: Name or identifier of the patient
        output_path: Optional path to save JSON output. Defaults to outputs/{patient_name}_arithmetic_calculation.json
        use_schema_prompt: Whether to use PydanticPromptGenerator for schema
        prompt_style: Style of schema prompt (DETAILED, CONCISE, TECHNICAL)

    Returns:
        ArithmeticCalculationAssessment: Validated arithmetic calculation assessment object
    """
    if not patient_name or not patient_name.strip():
        raise ValueError("Patient name cannot be empty")

    # Ask patient questions interactively
    print(f"\nStarting arithmetic calculation assessment for: {patient_name}")
    responses = ask_arithmetic_questions()

    # Create assessment from responses
    assessment = create_arithmetic_assessment_from_responses(patient_name, responses, output_path)

    return assessment


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Evaluate patient arithmetic calculation capabilities through mental math assessment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default - saves to outputs/patient_arithmetic_calculation.json
  python exam_arithmetic_calculation.py "John Doe"

  # Custom output path
  python exam_arithmetic_calculation.py "John Doe" -o custom_assessment.json

  # With concise prompting
  python exam_arithmetic_calculation.py "John Doe" --concise
        """
    )
    parser.add_argument("patient", nargs='+', help="Name or identifier of the patient")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Path to save JSON output. Defaults to outputs/{patient_name}_arithmetic_calculation.json"
    )
    parser.add_argument(
        "--concise",
        action="store_true",
        help="Use concise prompt style (faster generation)"
    )

    args = parser.parse_args()

    try:
        patient_name = " ".join(args.patient)
        prompt_style = PromptStyle.CONCISE if args.concise else PromptStyle.DETAILED

        result = evaluate_arithmetic_calculation(
            patient_name=patient_name,
            output_path=args.output,
            prompt_style=prompt_style,
        )
        print("✓ Success!")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
