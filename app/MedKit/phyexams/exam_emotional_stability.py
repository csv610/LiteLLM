"""
Emotional Stability Assessment

Evaluate patient emotional stability through structured questionnaire
using BaseModel definitions and the MedKit AI client with schema-aware prompting.
"""

import sys
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional

# Fix import paths
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.medkit_client import MedKitClient
from utils.pydantic_prompt_generator import PromptStyle


class MoodAssessment(BaseModel):
    """Questions about patient's current mood state."""
    current_mood: str = Field(description="Patient's current emotional mood state (happy, sad, neutral, anxious, angry, etc.)")
    mood_frequency: str = Field(description="How frequently mood changes occur during the day")
    mood_intensity: str = Field(description="Intensity of mood on a scale and how long episodes last")
    mood_triggers: str = Field(description="Identified triggers for mood changes or emotional episodes, comma-separated")


class StressAndAnxiety(BaseModel):
    """Assessment of stress and anxiety levels."""
    stress_level: str = Field(description="Current stress level reported by patient")
    anxiety_symptoms: str = Field(description="Physical and mental anxiety symptoms experienced, comma-separated")
    anxiety_frequency: str = Field(description="How often anxiety episodes occur and their duration")
    stress_management_techniques: str = Field(description="Current coping mechanisms used for stress, comma-separated")


class EmotionalRegulation(BaseModel):
    """Ability to manage and regulate emotions."""
    emotion_control: str = Field(description="Patient's ability to control emotional responses")
    impulse_control: str = Field(description="Ability to manage impulsive emotional reactions")
    emotional_responses: str = Field(description="Typical emotional responses to challenging situations")
    recovery_time: str = Field(description="Time required to recover from emotional episodes")


class SocialAndRelationships(BaseModel):
    """Assessment of social functioning and relationships."""
    social_engagement: str = Field(description="Level of social interaction and engagement with others")
    relationship_satisfaction: str = Field(description="Quality and stability of personal relationships")
    social_support_system: str = Field(description="Availability of emotional support from family/friends, comma-separated")
    isolation_feelings: str = Field(description="Feelings of loneliness or social isolation")


class SleepAndEnergy(BaseModel):
    """Sleep quality and energy levels."""
    sleep_quality: str = Field(description="Quality of sleep reported by patient (insomnia, oversleeping, interrupted, etc.)")
    sleep_duration: str = Field(description="Typical hours of sleep per night")
    energy_levels: str = Field(description="Daily energy levels and consistency")
    fatigue_patterns: str = Field(description="Patterns of fatigue or lack of motivation")


class CopingMechanisms(BaseModel):
    """Patient's coping strategies and resilience."""
    positive_coping: str = Field(description="Healthy coping mechanisms used, comma-separated")
    negative_coping: str = Field(description="Unhealthy or avoidant coping patterns identified, comma-separated")
    resilience_factors: str = Field(description="Factors that contribute to emotional resilience, comma-separated")
    problem_solving_ability: str = Field(description="Patient's ability to address problems constructively")


class MentalHealthHistory(BaseModel):
    """History of mental health concerns."""
    past_episodes: str = Field(description="History of depression, anxiety, or other mental health episodes")
    treatment_history: str = Field(description="Previous mental health treatments or therapies received")
    family_history: str = Field(description="Family history of mental health conditions, comma-separated")
    current_medications: str = Field(description="Current medications affecting mood or mental health, comma-separated")


class LifeEvents(BaseModel):
    """Recent and significant life events."""
    recent_stressors: str = Field(description="Recent major life stressors or changes, comma-separated")
    positive_events: str = Field(description="Recent positive life events, comma-separated")
    grief_or_loss: str = Field(description="Experience of loss or grief and current processing stage")
    major_life_changes: str = Field(description="Recent significant life transitions, comma-separated")


class SelfPerception(BaseModel):
    """Patient's perception of themselves."""
    self_esteem: str = Field(description="Overall self-esteem and self-worth assessment")
    self_confidence: str = Field(description="Level of confidence in abilities and decision-making")
    self_criticism: str = Field(description="Level of self-criticism or negative self-talk patterns")
    personal_goals: str = Field(description="Current personal goals and sense of purpose, comma-separated")


class AssessmentSummary(BaseModel):
    """Overall assessment findings and recommendations."""
    stability_level: str = Field(description="Overall emotional stability rating (stable, moderate, concerning)")
    key_strengths: str = Field(description="Key emotional strengths identified, comma-separated")
    areas_of_concern: str = Field(description="Areas requiring attention or support, comma-separated")
    recommendations: str = Field(description="Recommendations for improving emotional stability, comma-separated")
    professional_referral: str = Field(description="Whether professional mental health referral is recommended and rationale")


class EmotionalStabilityAssessment(BaseModel):
    """
    Comprehensive emotional stability assessment.

    Organized as a collection of BaseModel sections, each representing
    a distinct aspect of emotional and mental health evaluation.
    """
    # Current emotional state
    mood_assessment: MoodAssessment

    # Stress and anxiety evaluation
    stress_and_anxiety: StressAndAnxiety

    # Emotional regulation capacity
    emotional_regulation: EmotionalRegulation

    # Social functioning
    social_and_relationships: SocialAndRelationships

    # Physical health indicators
    sleep_and_energy: SleepAndEnergy

    # Coping strategies
    coping_mechanisms: CopingMechanisms

    # Historical context
    mental_health_history: MentalHealthHistory
    life_events: LifeEvents

    # Self-perception
    self_perception: SelfPerception

    # Final assessment
    assessment_summary: AssessmentSummary


def ask_patient_questions() -> dict:
    """
    Ask patient questions interactively and collect responses.
    Returns a dictionary of patient responses to be used in assessment.
    """
    print("\n" + "="*60)
    print("EMOTIONAL STABILITY ASSESSMENT")
    print("="*60)
    print("\nMEASURES: Evaluates patient's emotional stability through assessment of:")
    print("  • Mood state and emotional regulation capacity")
    print("  • Stress levels and anxiety symptoms")
    print("  • Coping mechanisms and resilience factors")
    print("  • Social functioning and relationship quality")
    print("  • Sleep patterns and energy levels")
    print("  • Self-perception and confidence")
    print("  • Mental health history and current life stressors")

    print("\nTOP 10 KEY ASSESSMENT QUESTIONS:")
    print("  1. What is your current emotional mood state?")
    print("  2. How frequently do you experience mood changes throughout the day?")
    print("  3. What are the identified triggers for your mood changes or emotional episodes?")
    print("  4. How would you rate your current stress level (1-10)?")
    print("  5. Do you experience anxiety symptoms? If yes, describe them (physical/mental).")
    print("  6. How well can you control your emotional responses in challenging situations?")
    print("  7. Do you have a reliable support system and close relationships to rely on?")
    print("  8. How would you describe your sleep quality and typical sleep duration?")
    print("  9. What healthy coping strategies do you use to manage stress and emotions?")
    print(" 10. Have you experienced any significant mental health episodes or life stressors?")

    print("\n" + "="*60)
    print("EMOTIONAL STABILITY ASSESSMENT QUESTIONNAIRE")
    print("="*60)

    responses = {}

    # MOOD ASSESSMENT
    print("\n--- MOOD ASSESSMENT ---")
    responses['current_mood'] = input("How would you describe your current mood? (e.g., happy, sad, anxious, neutral): ").strip()
    responses['mood_frequency'] = input("How often do your moods change during the day? ").strip()
    responses['mood_intensity'] = input("On a scale of 1-10, how intense are your mood changes? How long do they last? ").strip()
    responses['mood_triggers'] = input("What triggers your mood changes? (comma-separated): ").strip()

    # STRESS AND ANXIETY
    print("\n--- STRESS AND ANXIETY ---")
    responses['stress_level'] = input("How would you rate your current stress level (1-10)? ").strip()
    responses['anxiety_symptoms'] = input("Do you experience anxiety symptoms? If yes, describe them (physical/mental): ").strip()
    responses['anxiety_frequency'] = input("How often do you experience anxiety and how long do episodes last? ").strip()
    responses['stress_management'] = input("What techniques do you use to manage stress? (comma-separated): ").strip()

    # EMOTIONAL REGULATION
    print("\n--- EMOTIONAL REGULATION ---")
    responses['emotion_control'] = input("How well can you control your emotional responses? ").strip()
    responses['impulse_control'] = input("How well do you manage impulsive emotional reactions? ").strip()
    responses['emotional_responses'] = input("How do you typically respond to challenging situations? ").strip()
    responses['recovery_time'] = input("How long does it typically take you to recover from emotional episodes? ").strip()

    # SOCIAL AND RELATIONSHIPS
    print("\n--- SOCIAL AND RELATIONSHIPS ---")
    responses['social_engagement'] = input("How often do you engage socially with others? ").strip()
    responses['relationship_quality'] = input("How satisfied are you with your close relationships? ").strip()
    responses['social_support'] = input("Do you have people you can rely on for support? Who? ").strip()
    responses['loneliness'] = input("Do you feel lonely or isolated? How often? ").strip()

    # SLEEP AND ENERGY
    print("\n--- SLEEP AND ENERGY ---")
    responses['sleep_quality'] = input("How would you describe your sleep quality? ").strip()
    responses['sleep_duration'] = input("How many hours of sleep do you typically get per night? ").strip()
    responses['energy_levels'] = input("How would you describe your daily energy levels? ").strip()
    responses['fatigue_patterns'] = input("Do you experience fatigue or lack of motivation? When? ").strip()

    # COPING MECHANISMS
    print("\n--- COPING MECHANISMS ---")
    responses['positive_coping'] = input("What healthy coping strategies do you use? (comma-separated): ").strip()
    responses['negative_coping'] = input("Do you use any unhealthy coping patterns? (comma-separated): ").strip()
    responses['resilience_factors'] = input("What factors help you stay resilient? (comma-separated): ").strip()
    responses['problem_solving'] = input("How do you typically address problems? ").strip()

    # MENTAL HEALTH HISTORY
    print("\n--- MENTAL HEALTH HISTORY ---")
    responses['past_episodes'] = input("Have you ever experienced depression, anxiety, or other mental health issues? ").strip()
    responses['treatment_history'] = input("Have you received any mental health treatment or therapy? ").strip()
    responses['family_history'] = input("Does mental health issues run in your family? (comma-separated): ").strip()
    responses['current_medications'] = input("Are you currently on any medications affecting mood? ").strip()

    # LIFE EVENTS
    print("\n--- LIFE EVENTS ---")
    responses['recent_stressors'] = input("What recent major life stressors or changes have you experienced? (comma-separated): ").strip()
    responses['positive_events'] = input("What recent positive events have you experienced? (comma-separated): ").strip()
    responses['grief_or_loss'] = input("Have you experienced loss or grief? How are you processing it? ").strip()
    responses['life_changes'] = input("What significant life transitions are you going through? (comma-separated): ").strip()

    # SELF PERCEPTION
    print("\n--- SELF PERCEPTION ---")
    responses['self_esteem'] = input("How would you rate your self-esteem? ").strip()
    responses['self_confidence'] = input("How confident are you in your abilities? ").strip()
    responses['self_criticism'] = input("How self-critical are you? Do you engage in negative self-talk? ").strip()
    responses['personal_goals'] = input("What are your current personal goals and sense of purpose? (comma-separated): ").strip()

    return responses


def create_assessment_from_responses(patient_name: str, responses: dict, output_path: Optional[Path] = None) -> EmotionalStabilityAssessment:
    """
    Create a structured assessment object from collected patient responses.

    Args:
        patient_name: Name of the patient
        responses: Dictionary of patient responses from questions
        output_path: Optional path to save JSON output

    Returns:
        EmotionalStabilityAssessment: Validated assessment object
    """
    import json

    # Create assessment object from responses
    assessment_data = {
        "mood_assessment": {
            "current_mood": responses.get('current_mood', ''),
            "mood_frequency": responses.get('mood_frequency', ''),
            "mood_intensity": responses.get('mood_intensity', ''),
            "mood_triggers": responses.get('mood_triggers', '')
        },
        "stress_and_anxiety": {
            "stress_level": responses.get('stress_level', ''),
            "anxiety_symptoms": responses.get('anxiety_symptoms', ''),
            "anxiety_frequency": responses.get('anxiety_frequency', ''),
            "stress_management_techniques": responses.get('stress_management', '')
        },
        "emotional_regulation": {
            "emotion_control": responses.get('emotion_control', ''),
            "impulse_control": responses.get('impulse_control', ''),
            "emotional_responses": responses.get('emotional_responses', ''),
            "recovery_time": responses.get('recovery_time', '')
        },
        "social_and_relationships": {
            "social_engagement": responses.get('social_engagement', ''),
            "relationship_satisfaction": responses.get('relationship_quality', ''),
            "social_support_system": responses.get('social_support', ''),
            "isolation_feelings": responses.get('loneliness', '')
        },
        "sleep_and_energy": {
            "sleep_quality": responses.get('sleep_quality', ''),
            "sleep_duration": responses.get('sleep_duration', ''),
            "energy_levels": responses.get('energy_levels', ''),
            "fatigue_patterns": responses.get('fatigue_patterns', '')
        },
        "coping_mechanisms": {
            "positive_coping": responses.get('positive_coping', ''),
            "negative_coping": responses.get('negative_coping', ''),
            "resilience_factors": responses.get('resilience_factors', ''),
            "problem_solving_ability": responses.get('problem_solving', '')
        },
        "mental_health_history": {
            "past_episodes": responses.get('past_episodes', ''),
            "treatment_history": responses.get('treatment_history', ''),
            "family_history": responses.get('family_history', ''),
            "current_medications": responses.get('current_medications', '')
        },
        "life_events": {
            "recent_stressors": responses.get('recent_stressors', ''),
            "positive_events": responses.get('positive_events', ''),
            "grief_or_loss": responses.get('grief_or_loss', ''),
            "major_life_changes": responses.get('life_changes', '')
        },
        "self_perception": {
            "self_esteem": responses.get('self_esteem', ''),
            "self_confidence": responses.get('self_confidence', ''),
            "self_criticism": responses.get('self_criticism', ''),
            "personal_goals": responses.get('personal_goals', '')
        },
        "assessment_summary": {
            "stability_level": "To be determined by clinician",
            "key_strengths": "To be determined by clinician",
            "areas_of_concern": "To be determined by clinician",
            "recommendations": "To be determined by clinician",
            "professional_referral": "To be determined by clinician"
        }
    }

    # Create assessment object
    assessment = EmotionalStabilityAssessment(**assessment_data)

    # Save to file if path provided
    if output_path is None:
        output_path = Path("outputs") / f"{patient_name.lower().replace(' ', '_')}_emotional_stability.json"

    # Create outputs directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save assessment as JSON
    with open(output_path, 'w') as f:
        json.dump(assessment_data, f, indent=2)

    print(f"\n✓ Assessment saved to: {output_path}")

    return assessment


def evaluate_emotional_stability(
    patient_name: str,
    output_path: Optional[Path] = None,
    use_schema_prompt: bool = True,
    prompt_style: PromptStyle = PromptStyle.DETAILED,
) -> EmotionalStabilityAssessment:
    """
    Evaluate patient emotional stability through interactive questionnaire.

    Args:
        patient_name: Name or identifier of the patient
        output_path: Optional path to save JSON output. Defaults to outputs/{patient_name}_emotional_stability.json
        use_schema_prompt: Whether to use PydanticPromptGenerator for schema
        prompt_style: Style of schema prompt (DETAILED, CONCISE, TECHNICAL)

    Returns:
        EmotionalStabilityAssessment: Validated emotional stability assessment object
    """
    if not patient_name or not patient_name.strip():
        raise ValueError("Patient name cannot be empty")

    # Ask patient questions interactively
    print(f"\nStarting emotional stability assessment for: {patient_name}")
    responses = ask_patient_questions()

    # Create assessment from responses
    assessment = create_assessment_from_responses(patient_name, responses, output_path)

    return assessment


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Evaluate patient emotional stability through structured assessment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default - saves to outputs/patient_emotional_stability.json
  python emotional_stability.py "John Doe"

  # Custom output path
  python emotional_stability.py "John Doe" -o custom_assessment.json

  # With concise prompting
  python emotional_stability.py "John Doe" --concise
        """
    )
    parser.add_argument("patient", nargs='+', help="Name or identifier of the patient")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Path to save JSON output. Defaults to outputs/{patient_name}_emotional_stability.json"
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

        result = evaluate_emotional_stability(
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
