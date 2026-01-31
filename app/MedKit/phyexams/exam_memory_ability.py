"""
Memory Ability Assessment

Evaluate patient memory capabilities through immediate recall, recent memory,
and remote memory testing using BaseModel definitions and the MedKit AI client
with schema-aware prompting.
"""

import sys
import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional

from lite.utils import save_model_response

# Fix import path
from utils.pydantic_prompt_generator import PromptStyle


class ImmediateRecall(BaseModel):
    """Patient's ability for immediate recall of new information."""
    sentence_repetition: str = Field(description="Patient's ability to repeat a dictated sentence (e.g., 'The quick brown fox jumps over the lazy dog'). Accuracy - perfect/mostly correct/partial/unable. Specific omissions or errors")
    number_sequence_forward: str = Field(description="Ability to repeat number sequences forward (starting with 3 digits, progressing to 8+ digits). Maximum sequence length repeated correctly. Examples of sequences tried")
    number_sequence_backward: str = Field(description="Ability to repeat number sequences backward (starting with 2 digits, progressing to 6+ digits). Maximum sequence length repeated correctly. Examples tested")
    digit_span_forward: str = Field(description="Digit span forward score - normal (5-8 digits)/low-normal/impaired/severely impaired")
    digit_span_backward: str = Field(description="Digit span backward score - normal (4-6 digits)/low-normal/impaired/severely impaired")
    immediate_recall_speed: str = Field(description="Speed of response to recall tasks - immediate/slight delay/significant delay/very delayed")
    immediate_recall_effort: str = Field(description="Patient's effort and concentration during immediate recall tasks - good/fair/poor/inconsistent")
    immediate_recall_errors: str = Field(description="Types of errors in immediate recall - none/occasional/frequent. Types (omissions, substitutions, additions, transpositions)")


class RecentMemory(BaseModel):
    """Patient's ability to remember new information over minutes to hours."""
    objects_presented: str = Field(description="List of objects or words presented to patient for recent memory test. Standard objects: carpet, iris, bench, fortune. Or alternative objects if used")
    immediate_object_recall: str = Field(description="Patient's ability to recall presented objects immediately after presentation - all correct/mostly correct/partial/unable")
    five_minute_recall: str = Field(description="Patient's ability to recall objects after 5 minutes - all correct/mostly correct/partial/unable. Specific items missed or confused")
    ten_minute_recall: str = Field(description="Patient's ability to recall objects after 10 minutes - all correct/mostly correct/partial/unable. Specific items missed or confused")
    cuing_response: str = Field(description="Response to cuing or hints if recall is impaired - improves with cues/no improvement/partial improvement")
    recognition_memory: str = Field(description="Ability to recognize objects when presented with multiple choices (if recall impaired) - excellent/good/fair/poor")
    object_retention: str = Field(description="Retention curve - stable/declining/fluctuating. Does performance worsen over time?")
    recent_memory_score: str = Field(description="Overall recent memory performance score - normal/mild impairment/moderate impairment/severe impairment")


class RemoteMemory(BaseModel):
    """Patient's ability to recall verifiable past events and established knowledge."""
    mothers_maiden_name: str = Field(description="Ability to recall mother's maiden name - accurate/partially correct/unable/does not apply")
    high_school_name: str = Field(description="Ability to recall high school name and location - accurate/partially correct/unable/does not apply")
    parents_occupations: str = Field(description="Ability to recall parents' occupations - accurate/partially correct/vague/unable")
    childhood_address: str = Field(description="Ability to recall childhood address or addresses lived - accurate/partially correct/vague/unable")
    significant_family_events: str = Field(description="Ability to recall significant family events (marriages, births, deaths, moves) - clear/somewhat clear/vague/unable")
    personal_history_verifiable: str = Field(description="Overall accuracy of verifiable personal history events - accurate/mostly accurate/vague/inaccurate/confabulated")
    common_knowledge: str = Field(description="Knowledge of common knowledge facts (current date, president, major historical events) - accurate/mostly accurate/partial/inaccurate")
    famous_people_dates: str = Field(description="Knowledge of famous historical events and dates (presidents, wars, major events). Accuracy and level of detail")
    childhood_memories: str = Field(description="Ability to recall childhood memories with detail - clear and detailed/clear/vague/unreliable/fragmented")
    temporal_order_accuracy: str = Field(description="Ability to place events in correct temporal order - accurate/mostly accurate/confused/unable")
    remote_memory_consistency: str = Field(description="Consistency of remote memory recall across multiple questions - consistent/somewhat consistent/inconsistent/confabulated")
    confabulation_observed: str = Field(description="Evidence of confabulation (filling in gaps with false memories) - not present/minimal/present/significant")
    recent_current_events: str = Field(description="Knowledge of recent current events (past year) - accurate/mostly accurate/vague/inaccurate")
    remote_memory_level: str = Field(description="Overall remote memory performance - normal/low-normal/mildly impaired/moderately impaired/severely impaired")


class WorkingMemory(BaseModel):
    """Patient's ability to hold and manipulate information temporarily."""
    digit_manipulation: str = Field(description="Ability to manipulate information mentally (e.g., recite digits backward, count backward from 20). Accuracy and speed")
    word_manipulation: str = Field(description="Ability to manipulate words (e.g., spell word backward, anagram tasks). Success and speed")
    attention_span: str = Field(description="Sustained attention during memory tasks - good/fair/poor. Distractibility observed")
    concentration_ability: str = Field(description="Ability to concentrate - normal/mildly impaired/moderately impaired/severely impaired")
    task_switching: str = Field(description="Ability to switch between different memory tasks - smooth/effortful/confused/unable")
    working_memory_capacity: str = Field(description="Working memory capacity - normal/low-normal/impaired/severely impaired")


class MemoryEncoding(BaseModel):
    """Assessment of how patient encodes and processes information."""
    attention_during_encoding: str = Field(description="Patient's attention during information presentation - alert/distracted/confused/unable to focus")
    encoding_strategy: str = Field(description="Observed encoding strategy used - none/passive/active/semantic/visual/rehearsal")
    strategy_effectiveness: str = Field(description="Effectiveness of encoding strategy - efficient/moderately effective/ineffective/absent")
    learning_rate: str = Field(description="Rate of learning across repeated presentations - normal/slow/very slow/no improvement")
    retrieval_cues_helpful: str = Field(description="Whether retrieval cues help memory performance - yes significantly/mildly/no/not tested")


class MemoryLossPatterns(BaseModel):
    """Documentation of specific memory loss patterns and characteristics."""
    amnesia_type: str = Field(description="Type of amnesia if present - not present/anterograde (difficulty forming new memories)/retrograde (loss of past memories)/global")
    memory_loss_timeline: str = Field(description="Timeline of memory loss - acute/gradual/fluctuating/specific period affected")
    memory_islands: str = Field(description="Preserved islands of memory within otherwise impaired memory - present/absent/unclear")
    emotional_memory: str = Field(description="Emotional or autobiographical memory - preserved/impaired/fragmented")
    semantic_memory: str = Field(description="Semantic memory (facts, knowledge) - preserved/impaired")
    procedural_memory: str = Field(description="Procedural memory (skills, how-to knowledge) if assessed - preserved/impaired/not tested")
    consistency_across_tests: str = Field(description="Consistency of memory impairment across different types of memory tests - consistent/inconsistent/variable")


class CognitiveLimitations(BaseModel):
    """Assessment of underlying cognitive limitations affecting memory."""
    attention_deficit: str = Field(description="Attention deficit contributing to memory problems - not present/mild/moderate/severe")
    processing_speed: str = Field(description="Slow processing speed affecting memory encoding - not present/mild/moderate/severe")
    executive_dysfunction: str = Field(description="Executive dysfunction affecting memory strategy use - not present/mild/moderate/severe")
    language_comprehension: str = Field(description="Language comprehension difficulties affecting understanding of tasks - not present/yes/mild/severe")
    dementia_indicators: str = Field(description="Indicators of dementia or progressive cognitive decline - not present/possible/probable/consistent with dementia")
    delirium_indicators: str = Field(description="Indicators of delirium or acute cognitive changes - not present/mild/moderate/severe")
    depression_cognitive_impact: str = Field(description="Cognitive impact of depression (pseudodementia) - not present/possible/evident")


class ContextualFactors(BaseModel):
    """Consideration of contextual factors affecting memory performance."""
    sleep_quality: str = Field(description="Recent sleep quality and quantity - adequate/inadequate/poor. Impact on memory")
    stress_level: str = Field(description="Current stress or anxiety level affecting performance - minimal/moderate/high/severe")
    emotional_state: str = Field(description="Patient's emotional state during testing - calm/anxious/depressed/frustrated/other")
    medications: str = Field(description="Current medications that may affect memory - none/possible impact/known memory effects")
    substance_use: str = Field(description="Alcohol or substance use affecting cognition - not reported/possible/acknowledged/significant")
    head_injury_history: str = Field(description="History of head injuries or concussions - none/remote/recent/multiple")
    medical_conditions: str = Field(description="Medical conditions affecting memory (thyroid, B12 deficiency, sleep apnea, etc.) - none/possible/known/documented")
    education_level: str = Field(description="Education level and premorbid cognitive function - high/average/low/limited")
    motivation_effort: str = Field(description="Patient's motivation and effort during testing - good/fair/poor/suspected malingering")


class AssessmentSummary(BaseModel):
    """Overall assessment findings and clinical recommendations."""
    immediate_recall_level: str = Field(description="Overall immediate recall ability - normal/low-normal/mildly impaired/moderately impaired/severely impaired")
    recent_memory_level: str = Field(description="Overall recent memory ability - normal/low-normal/mildly impaired/moderately impaired/severely impaired")
    remote_memory_level: str = Field(description="Overall remote memory ability - normal/low-normal/mildly impaired/moderately impaired/severely impaired")
    working_memory_level: str = Field(description="Overall working memory ability - normal/low-normal/mildly impaired/moderately impaired/severely impaired")
    overall_memory_status: str = Field(description="Overall memory status - normal/age-appropriate/low-normal/mildly impaired/moderately impaired/severely impaired")
    memory_strengths: str = Field(description="Identified memory strengths (memory types relatively preserved), comma-separated")
    memory_weaknesses: str = Field(description="Identified memory weaknesses or impairments, comma-separated")
    memory_disorder_type: str = Field(description="Type of memory disorder if present (amnesia, dementia, mild cognitive impairment, etc.) or none")
    contributing_factors: str = Field(description="Contributing factors to memory impairment (depression, attention, sleep, medications, etc.), comma-separated")
    recommendations: str = Field(description="Recommendations for cognitive support, rehabilitation, or lifestyle modifications, comma-separated")
    specialist_referral: str = Field(description="Whether neuropsychological or neurology referral is recommended and rationale")


class MemoryAbilityAssessment(BaseModel):
    """
    Comprehensive memory ability assessment.

    Organized as a collection of BaseModel sections, each representing
    distinct aspects of memory function. Includes immediate recall (digit span,
    sentence repetition), recent memory (object/word recall after delay),
    remote memory (verifiable personal history and common knowledge), and
    working memory assessment.
    """
    # Immediate recall of new information
    immediate_recall: ImmediateRecall

    # Recent memory - retention over minutes
    recent_memory: RecentMemory

    # Remote memory - past events and verifiable knowledge
    remote_memory: RemoteMemory

    # Working memory capacity
    working_memory: WorkingMemory

    # Memory encoding and processing
    memory_encoding: MemoryEncoding

    # Specific memory loss patterns
    memory_loss_patterns: MemoryLossPatterns

    # Cognitive limitations affecting memory
    cognitive_limitations: CognitiveLimitations

    # Contextual factors
    contextual_factors: ContextualFactors

    # Final assessment
    assessment_summary: AssessmentSummary


def ask_memory_questions() -> dict:
    """
    Ask patient memory assessment questions interactively and collect responses.
    Returns a dictionary of patient responses to be used in assessment.
    """
    print("\n" + "="*60)
    print("MEMORY ABILITY ASSESSMENT")
    print("="*60)
    print("\nMEASURES: Evaluates patient's memory capabilities across:")
    print("  • Immediate recall (digit span, sentence repetition)")
    print("  • Recent memory (object/word recall over minutes)")
    print("  • Remote memory (verifiable past events and knowledge)")
    print("  • Working memory (mental manipulation of information)")
    print("  • Memory encoding and processing strategies")
    print("  • Specific patterns of memory loss if present")
    print("  • Cognitive factors affecting memory function")

    print("\nTOP 10 KEY ASSESSMENT QUESTIONS:")
    print("  1. Can you repeat this sentence exactly: 'The quick brown fox jumps over the lazy dog'?")
    print("  2. What is the maximum number of digits you can repeat forward (e.g., 5-8 digits)?")
    print("  3. What is the maximum number of digits you can repeat backward (e.g., 4-6 digits)?")
    print("  4. Can you recall objects presented earlier (immediate, 5-min, 10-min delays)?")
    print("  5. What is your mother's maiden name and childhood address (remote memory)?")
    print("  6. Do you know today's date, current leader, and major historical events?")
    print("  7. Can you manipulate information mentally (spell words backward, count backward)?")
    print("  8. Have you noticed any memory problems in daily life? When did they start?")
    print("  9. Are you on medications or have conditions that might affect memory?")
    print(" 10. How is your sleep quality and current stress level?")

    print("\n" + "="*60)
    print("DETAILED MEMORY ASSESSMENT QUESTIONNAIRE")
    print("="*60)

    responses = {}

    # IMMEDIATE RECALL
    print("\n--- IMMEDIATE RECALL ---")
    print("I will test your ability to repeat information I give you.")

    responses['sentence_repetition'] = input("I'll say a sentence. Please repeat it exactly: 'The quick brown fox jumps over the lazy dog': ").strip()

    print("\nNow I'll give you number sequences to repeat.")
    responses['number_seq_forward_3'] = input("  Repeat these numbers: 2, 4, 7: ").strip()
    responses['number_seq_forward_5'] = input("  Repeat these numbers: 3, 8, 1, 6, 9: ").strip()
    responses['number_seq_forward_7'] = input("  Repeat these numbers: 5, 2, 8, 9, 1, 4, 3: ").strip()
    responses['number_seq_backward_3'] = input("  Repeat these numbers backward: 1, 5, 9: ").strip()
    responses['number_seq_backward_5'] = input("  Repeat these numbers backward: 3, 8, 2, 7, 4: ").strip()

    responses['immediate_recall_effort'] = input("How well did you concentrate on these tasks? (good/fair/poor): ").strip()

    # RECENT MEMORY - Present objects to remember
    print("\n--- RECENT MEMORY ---")
    print("I will show you four words to remember. You'll recall them in a few minutes.")
    print("Listen carefully: CARPET, IRIS, BENCH, FORTUNE")
    responses['objects_presented'] = "carpet, iris, bench, fortune"

    responses['immediate_object_recall'] = input("Now immediately, please list the 4 words you heard: ").strip()

    # 5-minute recall simulation (user can wait or proceed)
    input("Press Enter when you're ready for 5-minute recall (or simulate the delay): ")
    responses['five_minute_recall'] = input("Can you recall those 4 words from earlier? ").strip()

    input("Press Enter when you're ready for 10-minute recall: ")
    responses['ten_minute_recall'] = input("Can you still recall those 4 words? ").strip()

    responses['cuing_response'] = input("If you forgot any, would hints help you remember? (yes/no/maybe): ").strip()

    # REMOTE MEMORY - Verifiable past events
    print("\n--- REMOTE MEMORY ---")
    print("I'll ask you about personal events and common knowledge.")

    responses['mothers_maiden_name'] = input("What is your mother's maiden name? ").strip()
    responses['high_school_name'] = input("What was the name of your high school? ").strip()
    responses['parents_occupations'] = input("What were your parents' occupations? ").strip()
    responses['childhood_address'] = input("Can you describe a childhood address where you lived? ").strip()
    responses['significant_family_events'] = input("Can you recall significant family events (births, marriages, moves)? ").strip()

    responses['common_knowledge_date'] = input("What is today's date? ").strip()
    responses['common_knowledge_president'] = input("Who is the current U.S. president (or leader of your country)? ").strip()
    responses['historical_event'] = input("Can you name a major historical event from the past 50 years? ").strip()

    responses['childhood_memories'] = input("Can you describe a clear childhood memory with details? ").strip()

    # WORKING MEMORY - Manipulation tasks
    print("\n--- WORKING MEMORY ---")
    print("Now I'll ask you to manipulate information mentally.")

    responses['digits_backward'] = input("I'll say numbers, please repeat them backward: 5, 3, 8, 1. Your answer: ").strip()
    responses['word_backward'] = input("Spell the word 'WORLD' backward: ").strip()
    responses['count_backward'] = input("Count backward from 20 to 10 as fast as you can: ").strip()
    responses['attention_during_tasks'] = input("How easily did you concentrate during these tasks? (easily/somewhat/difficult): ").strip()

    # MEMORY PATTERNS AND CONTEXTUAL FACTORS
    print("\n--- MEMORY CONTEXT ---")
    responses['memory_problems_noticed'] = input("Have you noticed any memory problems in daily life? (no/occasional/frequent/significant): ").strip()
    responses['memory_loss_timeline'] = input("If yes, did it start suddenly or gradually? ").strip()
    responses['current_medications'] = input("Are you on any medications that might affect memory? ").strip()
    responses['sleep_quality'] = input("How is your sleep quality recently? (good/fair/poor): ").strip()
    responses['stress_level'] = input("How is your current stress level? (low/moderate/high): ").strip()
    responses['recent_head_injury'] = input("Have you had any recent head injuries or concussions? (no/yes): ").strip()

    return responses


def create_memory_assessment_from_responses(patient_name: str, responses: dict, output_path: Optional[Path] = None) -> MemoryAbilityAssessment:
    """
    Create a structured memory assessment object from collected patient responses.

    Args:
        patient_name: Name of the patient
        responses: Dictionary of patient responses from questions
        output_path: Optional path to save JSON output

    Returns:
        MemoryAbilityAssessment: Validated assessment object
    """
    # Create assessment object from responses
    assessment_data = {
        "immediate_recall": {
            "sentence_repetition": responses.get('sentence_repetition', ''),
            "number_sequence_forward": f"3-digit: {responses.get('number_seq_forward_3', '')}, 5-digit: {responses.get('number_seq_forward_5', '')}, 7-digit: {responses.get('number_seq_forward_7', '')}",
            "number_sequence_backward": f"3-digit: {responses.get('number_seq_backward_3', '')}, 5-digit: {responses.get('number_seq_backward_5', '')}",
            "digit_span_forward": "To be assessed by clinician",
            "digit_span_backward": "To be assessed by clinician",
            "immediate_recall_speed": "immediate",
            "immediate_recall_effort": responses.get('immediate_recall_effort', ''),
            "immediate_recall_errors": "To be assessed by clinician"
        },
        "recent_memory": {
            "objects_presented": responses.get('objects_presented', ''),
            "immediate_object_recall": responses.get('immediate_object_recall', ''),
            "five_minute_recall": responses.get('five_minute_recall', ''),
            "ten_minute_recall": responses.get('ten_minute_recall', ''),
            "cuing_response": responses.get('cuing_response', ''),
            "recognition_memory": "To be assessed by clinician",
            "object_retention": "To be assessed by clinician",
            "recent_memory_score": "To be assessed by clinician"
        },
        "remote_memory": {
            "mothers_maiden_name": responses.get('mothers_maiden_name', ''),
            "high_school_name": responses.get('high_school_name', ''),
            "parents_occupations": responses.get('parents_occupations', ''),
            "childhood_address": responses.get('childhood_address', ''),
            "significant_family_events": responses.get('significant_family_events', ''),
            "personal_history_verifiable": "To be verified",
            "common_knowledge": f"Current date: {responses.get('common_knowledge_date', '')}, Leader: {responses.get('common_knowledge_president', '')}, Historical event: {responses.get('historical_event', '')}",
            "famous_people_dates": "To be assessed by clinician",
            "childhood_memories": responses.get('childhood_memories', ''),
            "temporal_order_accuracy": "To be assessed by clinician",
            "remote_memory_consistency": "To be assessed by clinician",
            "confabulation_observed": "Not indicated",
            "recent_current_events": "To be assessed by clinician",
            "remote_memory_level": "To be assessed by clinician"
        },
        "working_memory": {
            "digit_manipulation": responses.get('digits_backward', ''),
            "word_manipulation": responses.get('word_backward', ''),
            "attention_span": responses.get('attention_during_tasks', ''),
            "concentration_ability": "To be assessed by clinician",
            "task_switching": "To be assessed by clinician",
            "working_memory_capacity": "To be assessed by clinician"
        },
        "memory_encoding": {
            "attention_during_encoding": "Alert and responsive",
            "encoding_strategy": "To be assessed by clinician",
            "strategy_effectiveness": "To be assessed by clinician",
            "learning_rate": "To be assessed by clinician",
            "retrieval_cues_helpful": responses.get('cuing_response', '')
        },
        "memory_loss_patterns": {
            "amnesia_type": "Not indicated" if responses.get('memory_problems_noticed', '').lower() == 'no' else "To be assessed by clinician",
            "memory_loss_timeline": responses.get('memory_loss_timeline', 'Not reported'),
            "memory_islands": "To be assessed by clinician",
            "emotional_memory": "To be assessed by clinician",
            "semantic_memory": "To be assessed by clinician",
            "procedural_memory": "Not tested",
            "consistency_across_tests": "To be assessed by clinician"
        },
        "cognitive_limitations": {
            "attention_deficit": "To be assessed by clinician",
            "processing_speed": "To be assessed by clinician",
            "executive_dysfunction": "To be assessed by clinician",
            "language_comprehension": "No issues noted",
            "dementia_indicators": "Not indicated",
            "delirium_indicators": "Not indicated",
            "depression_cognitive_impact": "To be assessed by clinician"
        },
        "contextual_factors": {
            "sleep_quality": responses.get('sleep_quality', ''),
            "stress_level": responses.get('stress_level', ''),
            "emotional_state": "Cooperative and alert",
            "medications": responses.get('current_medications', ''),
            "substance_use": "Not addressed",
            "head_injury_history": responses.get('recent_head_injury', ''),
            "medical_conditions": "Not addressed",
            "education_level": "To be assessed by clinician",
            "motivation_effort": "Good cooperation demonstrated"
        },
        "assessment_summary": {
            "immediate_recall_level": "To be determined by clinician",
            "recent_memory_level": "To be determined by clinician",
            "remote_memory_level": "To be determined by clinician",
            "working_memory_level": "To be determined by clinician",
            "overall_memory_status": "To be determined by clinician",
            "memory_strengths": "To be determined by clinician",
            "memory_weaknesses": "To be determined by clinician",
            "memory_disorder_type": "None indicated",
            "contributing_factors": "To be determined by clinician",
            "recommendations": "Routine memory screening, lifestyle modifications",
            "specialist_referral": "Not indicated at this time"
        }
    }

    # Create assessment object
    assessment = MemoryAbilityAssessment(**assessment_data)

    # Save to file if path provided
    if output_path is None:
        output_path = Path("outputs") / f"{patient_name.lower().replace(' ', '_')}_memory_ability.json"

    # Create outputs directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save assessment as JSON
    save_model_response(assessment, output_path)

    print(f"\n✓ Assessment saved to: {output_path}")

    return assessment


def evaluate_memory_ability(
    patient_name: str,
    output_path: Optional[Path] = None,
    use_schema_prompt: bool = True,
    prompt_style: PromptStyle = PromptStyle.DETAILED,
) -> MemoryAbilityAssessment:
    """
    Evaluate patient memory capabilities through interactive questionnaire.

    Args:
        patient_name: Name or identifier of the patient
        output_path: Optional path to save JSON output. Defaults to outputs/{patient_name}_memory_ability.json
        use_schema_prompt: Whether to use PydanticPromptGenerator for schema
        prompt_style: Style of schema prompt (DETAILED, CONCISE, TECHNICAL)

    Returns:
        MemoryAbilityAssessment: Validated memory ability assessment object
    """
    if not patient_name or not patient_name.strip():
        raise ValueError("Patient name cannot be empty")

    # Ask patient questions interactively
    print(f"\nStarting memory ability assessment for: {patient_name}")
    responses = ask_memory_questions()

    # Create assessment from responses
    assessment = create_memory_assessment_from_responses(patient_name, responses, output_path)

    return assessment


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Evaluate patient memory capabilities through structured assessment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("patient", nargs='+', help="Name or identifier of the patient")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Path to save JSON output. Defaults to outputs/{patient_name}_memory_ability.json"
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

        result = evaluate_memory_ability(
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
