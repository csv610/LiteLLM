"""
Abstract Reasoning Assessment

Evaluate patient abstract reasoning capabilities through interpretation of
fables, proverbs, metaphors, and analogies using BaseModel definitions
and the MedKit AI client with schema-aware prompting.
"""

import sys
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional
import json

# Fix import path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.pydantic_prompt_generator import PromptStyle


class ProverbInterpretation(BaseModel):
    """Patient's interpretation of common proverbs."""
    stitch_in_time_meaning: str = Field(description="Patient's explanation of 'A stitch in time saves nine' - what it means and its relevance to life")
    stitch_in_time_application: str = Field(description="Example of how this proverb applies to real-life situations")
    bird_in_hand_meaning: str = Field(description="Patient's explanation of 'A bird in the hand is worth two in the bush' - its meaning and significance")
    bird_in_hand_application: str = Field(description="Example of how this proverb applies to decision-making or priorities")
    rolling_stone_meaning: str = Field(description="Patient's explanation of 'A rolling stone gathers no moss' - what it means and interpretations")
    rolling_stone_application: str = Field(description="Example or perspective on how this proverb relates to life experience or personal values")


class FableComprehension(BaseModel):
    """Patient's ability to understand and extract lessons from fables."""
    moral_extraction: str = Field(description="Patient's ability to identify the moral or lesson from a fable")
    character_analysis: str = Field(description="Patient's understanding of character motivations and actions in fables")
    symbolic_thinking: str = Field(description="Ability to identify symbolic elements and their meanings in stories")
    abstract_application: str = Field(description="Ability to apply fable lessons to abstract or general life principles")


class MetaphorAndAnalogy(BaseModel):
    """Patient's comprehension of metaphors and analogies."""
    metaphor_understanding: str = Field(description="Ability to interpret and explain metaphorical language")
    analogy_reasoning: str = Field(description="Ability to understand relationships in analogies and complete patterns (e.g., 'A is to B as C is to ___')")
    figure_of_speech_comprehension: str = Field(description="Understanding of idioms, figures of speech, and non-literal language")
    symbol_interpretation: str = Field(description="Ability to interpret symbols and their abstract meanings in different contexts")


class ConceptualThinking(BaseModel):
    """Patient's conceptual and abstract thinking abilities."""
    concept_relationships: str = Field(description="Ability to identify relationships between abstract concepts")
    pattern_recognition: str = Field(description="Ability to recognize patterns, similarities, and differences in abstract ideas")
    generalization_ability: str = Field(description="Ability to generalize from specific examples to broader abstract principles")
    hypothesis_formation: str = Field(description="Ability to form and reason about hypothetical or abstract scenarios")


class SymbolicProcessing(BaseModel):
    """Patient's ability to process symbolic and representational thinking."""
    symbolic_language: str = Field(description="Comfort and ability with symbolic representations (e.g., math symbols, metaphors)")
    abstract_problem_solving: str = Field(description="Ability to solve problems that require abstract or symbolic reasoning")
    representation_switching: str = Field(description="Ability to switch between different representations of the same concept")
    logical_reasoning: str = Field(description="Ability to follow abstract logical reasoning and deduction")


class CognitiveLimitations(BaseModel):
    """Assessment of cognitive limitations or difficulties with abstract thinking."""
    concrete_thinking_tendency: str = Field(description="Tendency toward literal or concrete interpretation rather than abstract")
    abstraction_difficulty: str = Field(description="Specific areas where abstract reasoning becomes challenging")
    reasoning_flexibility: str = Field(description="Ability to shift perspectives or consider multiple interpretations")
    conceptual_gaps: str = Field(description="Identified gaps or limitations in abstract conceptual understanding")


class CulturalAndContextualFactors(BaseModel):
    """Consideration of cultural background and contextual influences on reasoning."""
    cultural_proverb_familiarity: str = Field(description="Familiarity with proverbs and idioms from patient's cultural background")
    language_considerations: str = Field(description="Any language barriers or differences affecting abstract reasoning assessment")
    educational_background: str = Field(description="Patient's educational level and how it relates to abstract reasoning capabilities")
    contextual_understanding: str = Field(description="Ability to understand how context influences meaning and interpretation")


class AssessmentSummary(BaseModel):
    """Overall assessment findings and clinical recommendations."""
    abstract_reasoning_level: str = Field(description="Overall abstract reasoning capability level (high, moderate, limited, impaired)")
    cognitive_strengths: str = Field(description="Identified cognitive strengths in abstract reasoning, comma-separated")
    areas_of_difficulty: str = Field(description="Areas where abstract reasoning is impaired or limited, comma-separated")
    clinical_significance: str = Field(description="Clinical significance of findings and relationship to diagnosis or condition")
    recommendations: str = Field(description="Recommendations for cognitive support, therapy, or further assessment, comma-separated")
    neuropsychological_referral: str = Field(description="Whether neuropsychological evaluation is recommended and rationale")


class AbstractReasoningAssessment(BaseModel):
    """
    Comprehensive abstract reasoning assessment.

    Organized as a collection of BaseModel sections, each representing
    a distinct aspect of abstract reasoning and cognitive evaluation.
    Includes assessment through proverbs, fables, metaphors, and analogies.
    """
    # Interpretation of classical proverbs
    proverb_interpretation: ProverbInterpretation

    # Understanding of fables and moral reasoning
    fable_comprehension: FableComprehension

    # Metaphor and analogy processing
    metaphor_and_analogy: MetaphorAndAnalogy

    # Conceptual and abstract thinking
    conceptual_thinking: ConceptualThinking

    # Symbolic processing abilities
    symbolic_processing: SymbolicProcessing

    # Identified limitations
    cognitive_limitations: CognitiveLimitations

    # Cultural and contextual factors
    cultural_and_contextual_factors: CulturalAndContextualFactors

    # Final assessment
    assessment_summary: AssessmentSummary


def display_exam_overview() -> None:
    """
    Display a quick overview of the abstract reasoning exam before questions begin.
    """
    print("\n" + "="*70)
    print("ABSTRACT REASONING ASSESSMENT - EXAM OVERVIEW")
    print("="*70)

    print("\n📋 PURPOSE:")
    print("   This assessment evaluates your ability to think abstractly,")
    print("   understand figurative language, and reason about concepts.")

    print("\n🎯 WHAT IS MEASURED:")
    print("   1. Proverb Interpretation     - Understanding of wisdom and life lessons")
    print("   2. Fable Comprehension       - Extracting moral lessons from stories")
    print("   3. Metaphor & Analogy        - Understanding figurative language")
    print("   4. Conceptual Thinking       - Abstract pattern recognition")
    print("   5. Symbolic Processing       - Working with symbols and logic")
    print("   6. Cognitive Limitations     - Areas of difficulty (if any)")
    print("   7. Cultural & Context        - Background influences on reasoning")

    print("\n❓ ASSESSMENT FORMAT:")
    print("   • Interactive questions with open-ended responses")
    print("   • No right or wrong answers - focus on your thinking process")
    print("   • Estimated time: 10-15 minutes")
    print("   • Results saved to JSON file for clinical review")

    print("\n" + "="*70 + "\n")


def ask_abstract_reasoning_questions() -> dict:
    """
    Ask patient abstract reasoning assessment questions interactively.
    Returns a dictionary of patient responses to be used in assessment.
    """
    print("\n" + "="*60)
    print("ABSTRACT REASONING ASSESSMENT - QUESTIONS")
    print("="*60)
    print()
    print("MEASURES: This assessment evaluates the patient's ability to think abstractly, interpret")
    print("  figurative language, and understand symbolic relationships.")
    print("  • Proverb interpretation and understanding of wisdom")
    print("  • Ability to extract moral lessons from stories and fables")
    print("  • Comprehension of metaphors, analogies, and idioms")
    print("  • Pattern recognition and conceptual thinking")
    print("  • Symbolic processing and logical reasoning capabilities")
    print()
    print("TOP 10 KEY ASSESSMENT QUESTIONS:")
    print("  1. What does 'A stitch in time saves nine' mean?")
    print("  2. Can you explain the moral of the tortoise and hare story?")
    print("  3. What does it mean when someone says 'Life is a journey'?")
    print("  4. Complete: Dog is to puppy as cat is to ___?")
    print("  5. What does 'raining cats and dogs' mean?")
    print("  6. What do happiness and sadness have in common?")
    print("  7. What pattern do you see in: 2, 4, 8, 16, ___?")
    print("  8. If all birds could not fly, how would the world be different?")
    print("  9. Do you prefer thinking in concrete facts or abstract ideas?")
    print(" 10. Can you see things from different perspectives?")
    print()
    print("="*60)
    print("DETAILED ABSTRACT REASONING QUESTIONNAIRE")
    print("="*60)

    responses = {}

    # PROVERBS
    print("\n--- PROVERB INTERPRETATION ---")
    responses['stitch_meaning'] = input("What does 'A stitch in time saves nine' mean to you?: ").strip()
    responses['stitch_example'] = input("Can you give an example of how this applies to life?: ").strip()
    responses['bird_meaning'] = input("What does 'A bird in the hand is worth two in the bush' mean?: ").strip()
    responses['rolling_meaning'] = input("What does 'A rolling stone gathers no moss' mean?: ").strip()

    # FABLES
    print("\n--- FABLE AND STORY COMPREHENSION ---")
    responses['story_lesson'] = input("If you heard a story about a tortoise and hare racing, what lesson would it teach?: ").strip()
    responses['character_action'] = input("Why do you think characters in stories behave the way they do?: ").strip()

    # METAPHORS AND ANALOGIES
    print("\n--- METAPHORS AND ANALOGIES ---")
    responses['metaphor'] = input("What does it mean when someone says 'Life is a journey'?: ").strip()
    responses['analogy'] = input("Dog is to puppy as cat is to ___?: ").strip()
    responses['idiom'] = input("What does 'raining cats and dogs' mean?: ").strip()

    # CONCEPTUAL THINKING
    print("\n--- ABSTRACT THINKING ---")
    responses['abstract_concept'] = input("What do happiness and sadness have in common?: ").strip()
    responses['pattern'] = input("What pattern do you see in: 2, 4, 8, 16, ___?: ").strip()
    responses['hypothesis'] = input("If all birds could not fly, how would the world be different?: ").strip()

    # COGNITIVE STYLE
    print("\n--- COGNITIVE STYLE ---")
    responses['abstract_comfort'] = input("Do you prefer to think in concrete facts or abstract ideas? (concrete/abstract/both): ").strip()
    responses['perspective_shift'] = input("Can you easily see things from different perspectives? (easily/sometimes/difficult): ").strip()

    return responses


def create_abstract_reasoning_assessment_from_responses(patient_name: str, responses: dict, output_path: Optional[Path] = None) -> AbstractReasoningAssessment:
    """
    Create a structured abstract reasoning assessment object from collected patient responses.

    Args:
        patient_name: Name of the patient
        responses: Dictionary of patient responses from questions
        output_path: Optional path to save JSON output

    Returns:
        AbstractReasoningAssessment: Validated assessment object
    """
    # Create assessment object from responses
    assessment_data = {
        "proverb_interpretation": {
            "stitch_in_time_meaning": responses.get('stitch_meaning', ''),
            "stitch_in_time_application": responses.get('stitch_example', ''),
            "bird_in_hand_meaning": responses.get('bird_meaning', ''),
            "bird_in_hand_application": "To be assessed by clinician",
            "rolling_stone_meaning": responses.get('rolling_meaning', ''),
            "rolling_stone_application": "To be assessed by clinician"
        },
        "fable_comprehension": {
            "moral_extraction": responses.get('story_lesson', ''),
            "character_analysis": responses.get('character_action', ''),
            "symbolic_thinking": "To be assessed",
            "abstract_application": "To be assessed"
        },
        "metaphor_and_analogy": {
            "metaphor_understanding": responses.get('metaphor', ''),
            "analogy_reasoning": responses.get('analogy', ''),
            "figure_of_speech_comprehension": responses.get('idiom', ''),
            "symbol_interpretation": "To be assessed"
        },
        "conceptual_thinking": {
            "concept_relationships": responses.get('abstract_concept', ''),
            "pattern_recognition": responses.get('pattern', ''),
            "generalization_ability": "To be assessed",
            "hypothesis_formation": responses.get('hypothesis', '')
        },
        "symbolic_processing": {
            "symbolic_language": responses.get('abstract_comfort', ''),
            "abstract_problem_solving": responses.get('abstract_comfort', ''),
            "representation_switching": "To be assessed",
            "logical_reasoning": "To be assessed"
        },
        "cognitive_limitations": {
            "concrete_thinking_tendency": "To be assessed",
            "abstraction_difficulty": "Not indicated",
            "reasoning_flexibility": responses.get('perspective_shift', ''),
            "conceptual_gaps": "None indicated"
        },
        "cultural_and_contextual_factors": {
            "cultural_proverb_familiarity": "To be assessed",
            "language_considerations": "No barriers noted",
            "educational_background": "To be assessed",
            "contextual_understanding": "Demonstrated"
        },
        "assessment_summary": {
            "abstract_reasoning_level": "To be determined by clinician",
            "cognitive_strengths": "To be identified",
            "areas_of_difficulty": "To be identified",
            "clinical_significance": "To be determined",
            "recommendations": "Cognitive assessment as needed",
            "neuropsychological_referral": "Not indicated at this time"
        }
    }

    # Create assessment object
    assessment = AbstractReasoningAssessment(**assessment_data)

    # Save to file if path provided
    if output_path is None:
        output_path = Path("outputs") / f"{patient_name.lower().replace(' ', '_')}_abstract_reasoning.json"

    # Create outputs directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save assessment as JSON
    with open(output_path, 'w') as f:
        json.dump(assessment_data, f, indent=2)

    print(f"\n✓ Assessment saved to: {output_path}")

    return assessment


def evaluate_abstract_reasoning(
    patient_name: str,
    output_path: Optional[Path] = None,
    use_schema_prompt: bool = True,
    prompt_style: PromptStyle = PromptStyle.DETAILED,
) -> AbstractReasoningAssessment:
    """
    Evaluate patient abstract reasoning capabilities through interactive questionnaire.

    Args:
        patient_name: Name or identifier of the patient
        output_path: Optional path to save JSON output. Defaults to outputs/{patient_name}_abstract_reasoning.json
        use_schema_prompt: Whether to use PydanticPromptGenerator for schema
        prompt_style: Style of schema prompt (DETAILED, CONCISE, TECHNICAL)

    Returns:
        AbstractReasoningAssessment: Validated abstract reasoning assessment object
    """
    if not patient_name or not patient_name.strip():
        raise ValueError("Patient name cannot be empty")

    # Display exam overview
    print(f"\n{'='*70}")
    print(f"Patient: {patient_name}")
    print(f"{'='*70}")
    display_exam_overview()

    # Ask patient questions interactively
    responses = ask_abstract_reasoning_questions()

    # Create assessment from responses
    assessment = create_abstract_reasoning_assessment_from_responses(patient_name, responses, output_path)

    return assessment


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Evaluate patient abstract reasoning capabilities through structured assessment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default - saves to outputs/patient_abstract_reasoning.json
  python exam_abstract_reasoning.py "John Doe"

  # Custom output path
  python exam_abstract_reasoning.py "John Doe" -o custom_assessment.json

  # With concise prompting
  python exam_abstract_reasoning.py "John Doe" --concise
        """
    )
    parser.add_argument("-u", "--patient", nargs='+', default='unknown', help="Name or identifier of the patient")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Path to save JSON output. Defaults to outputs/{patient_name}_abstract_reasoning.json"
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

        result = evaluate_abstract_reasoning(
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
