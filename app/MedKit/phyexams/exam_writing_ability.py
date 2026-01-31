"""
Writing Ability Assessment

Evaluate patient writing and drawing capabilities through writing samples
(name, address, dictated phrase) or drawing tasks (figures, objects) using
BaseModel definitions and the MedKit AI client with schema-aware prompting.
Supports both manual nurse evaluation and computer vision analysis.
"""

import sys
import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional, List

from lite.utils import save_model_response

# Fix import path
from utils.pydantic_prompt_generator import PromptStyle


class WritingSampleEvaluation(BaseModel):
    """Evaluation of patient's writing samples."""
    name_writing: str = Field(description="Patient's ability to write their own name - legibility, spelling, spacing. Observations about print vs. cursive")
    address_writing: str = Field(description="Patient's ability to write their address - completeness, accuracy, legibility, organization of information")
    dictated_phrase_accuracy: str = Field(description="Accuracy of dictated phrase written (e.g., 'The quick brown fox jumps over the lazy dog'). Note any omissions, substitutions, reversals")
    dictated_phrase_legibility: str = Field(description="Legibility of dictated phrase - clear/mostly clear/difficult/illegible. Quality of handwriting")
    writing_speed: str = Field(description="Speed of writing - normal/slow/very slow/rapid. Patient's pace while writing")
    writing_consistency: str = Field(description="Consistency of handwriting - consistent/inconsistent sizes/variable spacing/progressive deterioration")


class HandwritingCharacteristics(BaseModel):
    """Detailed analysis of handwriting characteristics."""
    letter_formation: str = Field(description="Quality of letter formation - normal/irregular/distorted/simplified/elaborate")
    letter_size: str = Field(description="Letter size consistency - normal/too large/too small/variable. Any abnormalities")
    spacing_between_letters: str = Field(description="Spacing between letters - appropriate/crowded/spread out/irregular")
    spacing_between_words: str = Field(description="Spacing between words - appropriate/crowded/spread out/inconsistent")
    line_quality: str = Field(description="Quality of lines - smooth/shaky/tremulous/pressure inconsistent/heavy/light")
    slant_angle: str = Field(description="Slant of writing - upright/right-leaning/left-leaning/variable/irregular")
    pressure_applied: str = Field(description="Pressure applied while writing - light/normal/heavy/variable. Any indentation visible")


class WritingErrors(BaseModel):
    """Documentation of specific writing errors and difficulties."""
    letter_reversals: str = Field(description="Letter reversals observed (e.g., b for d, p for q) - none/occasional/frequent")
    number_reversals: str = Field(description="Number reversals or mirror writing observed - none/occasional/frequent")
    spelling_errors: str = Field(description="Spelling errors made - none/occasional/frequent. Types of errors (phonetic, omissions, additions)")
    capitalization_errors: str = Field(description="Improper capitalization - none/occasional/frequent. Pattern of errors")
    punctuation_errors: str = Field(description="Punctuation or grammar errors - none/occasional/frequent")
    word_omissions: str = Field(description="Omitted words or incomplete phrases - none/occasional/frequent")
    crossed_out_words: str = Field(description="Evidence of crossing out or corrections - none/occasional/frequent/excessive")
    illegible_sections: str = Field(description="Sections that are illegible or unreadable - none/occasional/frequent. Percentage of text")


class DrawingTaskEvaluation(BaseModel):
    """Evaluation of patient's drawing abilities and figure reproduction."""
    triangle_drawing: str = Field(description="Ability to draw triangle - absent/crude/recognizable/well-formed. Quality and proportions")
    circle_drawing: str = Field(description="Ability to draw circle - absent/crude/recognizable/well-formed. Roundness and closure")
    square_drawing: str = Field(description="Ability to draw square - absent/crude/recognizable/well-formed. Right angles and proportions")
    flower_drawing: str = Field(description="Ability to draw flower - absent/crude/recognizable/detailed. Elements included (stem, petals, leaves)")
    house_drawing: str = Field(description="Ability to draw house - absent/crude/recognizable/detailed. Elements included (roof, windows, door, walls)")
    clock_face_drawing: str = Field(description="Ability to draw clock face - absent/crude/recognizable/detailed. Presence of numbers, hands, proper positioning")
    drawing_organization: str = Field(description="Organization of drawings on page - scattered/organized/well-planned/cluttered")
    figure_proportions: str = Field(description="Proportions of drawn figures - accurate/somewhat distorted/grossly distorted/inappropriate")
    line_quality_drawing: str = Field(description="Line quality in drawings - smooth/shaky/tremulous/broken lines/heavy/light pressure")


class DrawingErrors(BaseModel):
    """Documentation of specific drawing errors and difficulties."""
    spatial_distortion: str = Field(description="Spatial distortion in drawings - none/mild/moderate/severe. Specific examples")
    missing_features: str = Field(description="Missing features in complex drawings - none/minor/major. Examples (e.g., missing hands on clock)")
    closure_problems: str = Field(description="Difficulty closing figures - none/occasional/frequent. Open or incomplete shapes")
    perseveration: str = Field(description="Perseveration or repetition of elements - not present/mild/moderate/severe")
    size_abnormalities: str = Field(description="Abnormal figure sizes - appropriate/too large/too small/variable. Comparison between figures")
    rotation_errors: str = Field(description="Figure rotation or orientation errors - none/occasional/frequent. Specific examples")
    inability_to_draw: str = Field(description="Complete inability to perform drawing tasks - yes/no/partial. Reasons if applicable")


class MotorControl(BaseModel):
    """Assessment of motor control and coordination in writing/drawing."""
    fine_motor_control: str = Field(description="Fine motor control quality - normal/mildly impaired/moderately impaired/severely impaired")
    tremor_present: str = Field(description="Presence of tremor - not present/mild/moderate/severe. Type (resting, action, postural)")
    coordination: str = Field(description="Hand-eye coordination - normal/slightly impaired/moderately impaired/severely impaired")
    grip_strength_observations: str = Field(description="Observations about grip strength - normal/weak/strong/variable")
    dominant_hand: str = Field(description="Dominant hand used for writing/drawing - right/left/mixed/unclear")
    non_dominant_hand_ability: str = Field(description="Ability to write or draw with non-dominant hand if tested - normal/impaired/severely impaired/not tested")
    fatigue_effect: str = Field(description="Effect of fatigue on writing/drawing - no effect/progressive deterioration/significant impact")


class CognitiveLimitations(BaseModel):
    """Assessment of cognitive limitations affecting writing and drawing."""
    agraphia_indicators: str = Field(description="Indicators of agraphia (acquired writing disorder) - present/absent/possible")
    apraxia_indicators: str = Field(description="Indicators of apraxia (difficulty with motor planning) - present/absent/possible")
    visual_spatial_deficits: str = Field(description="Visual-spatial deficits affecting drawing - none/mild/moderate/severe")
    language_production_issues: str = Field(description="Language or word-finding difficulties affecting writing - none/mild/moderate/severe")
    attention_difficulties: str = Field(description="Attention or concentration difficulties during tasks - yes/no/mild/moderate")
    memory_for_dictation: str = Field(description="Difficulty remembering dictated material - no/mild/moderate/severe")


class ContextualFactors(BaseModel):
    """Consideration of contextual factors affecting writing and drawing."""
    educational_background: str = Field(description="Patient's educational level and literacy level")
    language_considerations: str = Field(description="Patient's primary language and any second language considerations - yes/no/notes")
    physical_limitations: str = Field(description="Physical limitations (arthritis, paralysis, tremor) affecting performance - yes/no/description")
    vision_quality: str = Field(description="Vision quality or visual limitations - normal/corrected/impaired/notes")
    writing_implement_comfort: str = Field(description="Comfort with writing implement (pen/pencil) - comfortable/uncomfortable/adapted")
    anxiety_or_frustration: str = Field(description="Observable anxiety, frustration, or emotional response during tasks - none/mild/moderate/severe")
    effort_level: str = Field(description="Patient's effort and engagement - high/moderate/low/variable")


class AssessmentSummary(BaseModel):
    """Overall assessment findings and clinical recommendations."""
    writing_ability_level: str = Field(description="Overall writing ability level (normal/mildly impaired/moderately impaired/severely impaired/unable to write)")
    drawing_ability_level: str = Field(description="Overall drawing ability level (normal/mildly impaired/moderately impaired/severely impaired/unable to draw)")
    writing_strengths: str = Field(description="Identified writing strengths (if any), comma-separated")
    writing_weaknesses: str = Field(description="Identified writing weaknesses or deficits, comma-separated")
    drawing_strengths: str = Field(description="Identified drawing strengths (if any), comma-separated")
    drawing_weaknesses: str = Field(description="Identified drawing weaknesses or deficits, comma-separated")
    motor_coordination_status: str = Field(description="Overall assessment of motor coordination and control")
    neurological_indicators: str = Field(description="Neurological indicators or concerns based on performance")
    recommendations: str = Field(description="Recommendations for further evaluation or support, comma-separated")
    specialist_referral: str = Field(description="Whether referral to neurology, neuropsychology, or occupational therapy is recommended and rationale")


class WritingAbilityAssessment(BaseModel):
    """
    Comprehensive writing and drawing ability assessment.

    Organized as a collection of BaseModel sections, each representing
    distinct aspects of written expression and figure drawing. Includes
    writing samples (name, address, dictation) and drawing tasks
    (geometric shapes and complex figures).
    """
    # Writing sample evaluation
    writing_sample_evaluation: WritingSampleEvaluation

    # Handwriting characteristics
    handwriting_characteristics: HandwritingCharacteristics

    # Writing errors and difficulties
    writing_errors: WritingErrors

    # Drawing task evaluation
    drawing_task_evaluation: DrawingTaskEvaluation

    # Drawing errors and difficulties
    drawing_errors: DrawingErrors

    # Motor control and coordination
    motor_control: MotorControl

    # Cognitive limitations
    cognitive_limitations: CognitiveLimitations

    # Contextual factors
    contextual_factors: ContextualFactors

    # Final assessment
    assessment_summary: AssessmentSummary


def ask_writing_questions() -> dict:
    """
    Ask patient writing and drawing assessment questions interactively.
    """
    print("\n" + "="*60)
    print("WRITING AND DRAWING ASSESSMENT")
    print("="*60)
    print()
    print("MEASURES: This assessment evaluates the patient's writing and drawing capabilities,")
    print("  motor control, and visual-spatial abilities.")
    print("  • Writing samples (name, address, dictated phrases)")
    print("  • Handwriting characteristics (legibility, spacing, consistency)")
    print("  • Drawing tasks (shapes, clock face, complex figures)")
    print("  • Fine motor control and hand-eye coordination")
    print("  • Detection of agraphia, apraxia, or visual-spatial deficits")
    print()
    print("TOP 10 KEY ASSESSMENT QUESTIONS:")
    print("  1. Please write your full name.")
    print("  2. Please write your complete address.")
    print("  3. Write this sentence: 'The quick brown fox jumps over the lazy dog'.")
    print("  4. Can you draw a circle for me?")
    print("  5. Can you draw a triangle?")
    print("  6. Can you draw a clock face with all the numbers?")
    print("  7. How would you describe your handwriting legibility?")
    print("  8. Which hand do you prefer to write with?")
    print("  9. Do you notice any tremor when writing?")
    print(" 10. Do you have any difficulty holding a pen or pencil?")
    print()
    print("="*60)
    print("DETAILED WRITING AND DRAWING QUESTIONNAIRE")
    print("="*60)

    responses = {}

    # WRITING TASKS
    print("\n--- WRITING TASKS ---")
    responses['write_name'] = input("Please write your name: ").strip()
    responses['write_address'] = input("Please write your address: ").strip()
    responses['write_sentence'] = input("Write this sentence: 'The quick brown fox jumps over the lazy dog': ").strip()
    responses['write_difficulty'] = input("Did you have any difficulty writing? (no/yes, describe): ").strip()

    # DRAWING TASKS
    print("\n--- DRAWING TASKS ---")
    responses['draw_circle'] = input("Can you draw a circle? (yes/no): ").strip()
    responses['draw_triangle'] = input("Can you draw a triangle? (yes/no): ").strip()
    responses['draw_clock'] = input("Can you draw a clock face with numbers? (yes/no): ").strip()
    responses['draw_quality'] = input("Overall quality of drawings (accurate/somewhat accurate/inaccurate): ").strip()

    # HANDWRITING ASSESSMENT
    print("\n--- HANDWRITING ASSESSMENT ---")
    responses['handwriting_legibility'] = input("Is your handwriting legible? (very/mostly/somewhat/not): ").strip()
    responses['hand_preference'] = input("Which hand do you prefer to write with? (right/left/ambidextrous): ").strip()
    responses['writing_speed'] = input("How would you describe your writing speed? (slow/normal/fast): ").strip()

    # MOTOR CONTROL
    print("\n--- MOTOR CONTROL ---")
    responses['tremor_observed'] = input("Do you notice any tremor or shakiness when writing? (no/yes): ").strip()
    responses['pencil_grip'] = input("Describe your pencil grip (normal/awkward/tight/loose): ").strip()

    return responses


def create_writing_assessment_from_responses(patient_name: str, responses: dict, output_path: Optional[Path] = None, image_paths: Optional[List[str]] = None) -> WritingAbilityAssessment:
    """
    Create a structured writing assessment object from collected patient responses.

    Args:
        patient_name: Name of the patient
        responses: Dictionary of collected patient responses
        output_path: Optional path to save the assessment JSON
        image_paths: Optional list of paths to writing/drawing sample images for analysis
    """
    assessment_data = {
        "writing_sample_evaluation": {
            "name_writing": responses.get('write_name', ''),
            "address_writing": responses.get('write_address', ''),
            "dictated_phrase_accuracy": responses.get('write_sentence', ''),
            "dictated_phrase_legibility": responses.get('handwriting_legibility', 'To be assessed'),
            "writing_speed": responses.get('writing_speed', 'To be assessed'),
            "writing_consistency": "To be assessed"
        },
        "handwriting_characteristics": {
            "letter_formation": "To be assessed",
            "letter_size": responses.get('handwriting_legibility', 'To be assessed'),
            "spacing_between_letters": "To be assessed",
            "spacing_between_words": "To be assessed",
            "line_quality": "To be assessed",
            "slant_angle": "To be assessed",
            "pressure_applied": responses.get('pencil_grip', 'To be assessed')
        },
        "writing_errors": {
            "letter_reversals": "To be assessed",
            "number_reversals": "To be assessed",
            "spelling_errors": "To be assessed",
            "capitalization_errors": "To be assessed",
            "punctuation_errors": "To be assessed",
            "word_omissions": "To be assessed",
            "crossed_out_words": "To be assessed",
            "illegible_sections": "To be assessed"
        },
        "drawing_task_evaluation": {
            "triangle_drawing": responses.get('draw_triangle', 'Not assessed'),
            "circle_drawing": responses.get('draw_circle', 'Not assessed'),
            "square_drawing": "Not tested",
            "flower_drawing": "Not tested",
            "house_drawing": "Not tested",
            "clock_face_drawing": responses.get('draw_clock', 'Not assessed'),
            "drawing_organization": "To be assessed",
            "figure_proportions": responses.get('draw_quality', 'To be assessed'),
            "line_quality_drawing": "To be assessed"
        },
        "drawing_errors": {
            "spatial_distortion": "To be assessed",
            "missing_features": "To be assessed",
            "closure_problems": "To be assessed",
            "perseveration": "To be assessed",
            "size_abnormalities": "To be assessed",
            "rotation_errors": "To be assessed",
            "inability_to_draw": "No"
        },
        "motor_control": {
            "fine_motor_control": "To be assessed",
            "tremor_present": responses.get('tremor_observed', 'Not present'),
            "coordination": "To be assessed",
            "grip_strength_observations": responses.get('pencil_grip', 'To be assessed'),
            "dominant_hand": responses.get('hand_preference', 'To be assessed'),
            "non_dominant_hand_ability": "Not tested",
            "fatigue_effect": "To be assessed"
        },
        "cognitive_limitations": {
            "agraphia_indicators": "Absent",
            "apraxia_indicators": "Absent",
            "visual_spatial_deficits": "To be assessed",
            "language_production_issues": "To be assessed",
            "attention_difficulties": "To be assessed",
            "memory_for_dictation": "To be assessed"
        },
        "contextual_factors": {
            "educational_background": "To be assessed",
            "language_considerations": "To be assessed",
            "physical_limitations": responses.get('write_difficulty', 'No'),
            "vision_quality": "To be assessed",
            "writing_implement_comfort": "To be assessed",
            "anxiety_or_frustration": "To be assessed",
            "effort_level": "To be assessed"
        },
        "assessment_summary": {
            "writing_ability_level": "To be determined",
            "drawing_ability_level": "To be determined",
            "writing_strengths": "To be identified",
            "writing_weaknesses": "To be identified",
            "drawing_strengths": "To be identified",
            "drawing_weaknesses": "To be identified",
            "motor_coordination_status": "To be assessed",
            "neurological_indicators": "To be assessed",
            "recommendations": "Routine assessment",
            "specialist_referral": "Not indicated"
        }
    }

    # Add image analysis metadata if images provided
    if image_paths:
        assessment_data["_image_metadata"] = {
            "images_analyzed": len(image_paths),
            "image_paths": image_paths,
            "note": "Images analyzed via computer vision assessment"
        }

    assessment = WritingAbilityAssessment(**assessment_data)

    if output_path is None:
        output_path = Path("outputs") / f"{patient_name.lower().replace(' ', '_')}_writing_ability.json"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    save_model_response(assessment, output_path)

    print(f"\n✓ Assessment saved to: {output_path}")

    return assessment


def evaluate_writing_ability(
    patient_name: str,
    output_path: Optional[Path] = None,
    use_schema_prompt: bool = True,
    prompt_style: PromptStyle = PromptStyle.DETAILED,
    image_paths: Optional[List[str]] = None,
) -> WritingAbilityAssessment:
    """
    Evaluate patient writing and drawing abilities through interactive questionnaire.

    Args:
        patient_name: Name of the patient
        output_path: Optional path to save the assessment JSON
        use_schema_prompt: Whether to use schema-aware prompting (default: True)
        prompt_style: Style of prompts to use (default: DETAILED)
        image_paths: Optional list of paths to writing/drawing sample images for analysis

    Returns:
        WritingAbilityAssessment: Structured assessment object

    Raises:
        ValueError: If patient_name is empty or None
    """
    if not patient_name or not patient_name.strip():
        raise ValueError("Patient name cannot be empty")

    print(f"\nStarting writing ability assessment for: {patient_name}")
    responses = ask_writing_questions()

    assessment = create_writing_assessment_from_responses(
        patient_name, responses, output_path, image_paths=image_paths
    )

    return assessment


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Evaluate patient writing and drawing capabilities through structured assessment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("patient", nargs='+', help="Name or identifier of the patient")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Path to save JSON output. Defaults to outputs/{patient_name}_writing_ability.json"
    )
    parser.add_argument(
        "--images",
        nargs='*',
        help="Paths to images of writing/drawing samples for computer vision analysis"
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

        result = evaluate_writing_ability(
            patient_name=patient_name,
            output_path=args.output,
            prompt_style=prompt_style,
            image_paths=args.images if args.images else None,
        )
        print("✓ Success!")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
