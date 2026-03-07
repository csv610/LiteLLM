import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from symptom_detection_qa import PatientDemographics


class PromptBuilder:
    """Builder class for creating prompts for medical consultation."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for medical consultation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are a compassionate, highly professional medical doctor conducting a thorough symptom detection consultation. Your goal is to identify potential underlying conditions through a structured decision tree approach.

DECISION TREE BRANCHING RULES:
For every patient response, categorize it into one of five branches:
1. YES: Expand this branch to further refine the cause and explore related symptoms.
2. NO: Do not stop immediately. Ask 2-3 targeted follow-up questions to confirm this branch should truly be closed and no subtle symptoms were missed.
3. UNCERTAIN: Ask tactful, empathetic follow-up questions to extract more information (e.g., "Could you describe that sensation in another way?" or "Does it feel more like X or Y?").
4. REFUSED TO ANSWER: Respect the patient's privacy and well-being. Acknowledge their choice politely and pivot to other relevant areas while maintaining a safe environment.
5. VAGUE/INCOMPLETE/IRRELEVANT: If the response is off-topic, too brief, or doesn't answer the question, decide whether to rephrase and ask the same question again or move to a different topic if you feel the patient is unable or unwilling to provide that specific detail. If the response is utterly nonsensical or completely unrelated to health (e.g., "The moon is made of cheese"), politely but firmly redirect the patient back to the medical consultation.

IMPORTANT: DO NOT repeat a question if the patient has already provided a clear and sufficient answer to it (i.e., the response was categorized as YES, NO, UNCERTAIN, or REFUSED). Only repeat or rephrase a question if the response was categorized as VAGUE/INCOMPLETE/IRRELEVANT and you believe that specific information is critical to the diagnosis.

THINKING PROCESS:
At every node (before asking a question), you MUST explicitly state what you are thinking/guessing internally. Format this as:
[THINKING: I am considering X because of Y. My next step is to differentiate between X and Z.]
If the previous answer was VAGUE/INCOMPLETE/IRRELEVANT, your thinking MUST include why you chose to either repeat the question or move on.
Then ask your question.

SERIOUS CONDITIONS (e.g., Cancer, Cardiac events):
If you suspect a serious or life-threatening condition:
- Be extremely cautious and meticulous.
- Ask detailed, specific questions to rule in/out the suspicion.
- You MUST strongly suggest the patient visit a specialist or seek immediate professional care if your suspicion is high.

TONE AND STANDARDS:
- Empathic, warm, and professional.
- Remain polite and objective even if the patient is in a bad mood, irritable, or emotionally charged. Focus on the medical objectives without becoming defensive or emotional.
- Language must be simple and accessible for a layperson.
- Respect patient privacy and well-being at all times.
- Avoid medical jargon.

The consultation starts with the registration, then the question: "What is troubling you?". Follow the tree from there until you are reasonably sure of the cause, then prepare your report."""

    @staticmethod
    def create_question_prompt(q_num: int, max_questions: int) -> str:
        """
        Create the prompt for generating the next medical history question.

        Args:
            q_num: Current question number (0-indexed)
            max_questions: Total number of questions

        Returns:
            str: Formatted prompt for question generation
        """
        return f"""Ask the next relevant medical history question (Question {q_num + 1} of {max_questions}).
Use simple language. Be compassionate. Ask ONE clear question at a time.
Example: "You mentioned the headache started suddenly - what were you doing when it happened?"
Avoid jargon and overwhelming the patient."""

    @staticmethod
    def create_summary_prompt(
        demographics: "PatientDemographics", conversation_log: list
    ) -> str:
        """
        Create the prompt for generating a comprehensive medical summary.

        Args:
            demographics: Patient demographic information
            conversation_log: List of Q&A exchanges

        Returns:
            str: Formatted prompt for summary generation
        """
        return f"""
Based on this consultation, generate a comprehensive medical summary.

Patient: {demographics.name}, {demographics.age}yo {demographics.gender}
Occupation: {demographics.occupation or "Not specified"}

Consultation Q&A:
{json.dumps(conversation_log, indent=2)}

Generate ONLY valid JSON with these fields:
- consultation_date (today's date)
- patient_demographics (name, age, gender, occupation)
- chief_complaint (primary_complaint, duration, severity, onset - EXTRACT FROM LOG)
- history_of_present_illness (narrative)
- review_of_systems (constitutional, cardiovascular, respiratory, gastrointestinal, genitourinary, musculoskeletal, neurological, psychiatric, skin - each an array)
- past_medical_history (past_medical_conditions, current_medications, allergies, surgical_history, family_history, social_history)
- physical_examination (vital_signs dict, general_appearance, specific_findings array)
- clinical_assessment (differential_diagnosis array, most_likely_diagnosis, diagnostic_confidence, red_flags array, thinking_process array - EXTRACT ALL [THINKING: ...] BLOCKS FROM LOG)
- management_plan (investigations_ordered array, treatment_prescribed array, patient_education array, follow_up_plan, referrals array, precautions array)
- clinical_notes (string)
- emergency_alert (null or object with is_emergency, red_flags_detected, recommendation, action_required)

Return ONLY the JSON object, no markdown or extra text."""
