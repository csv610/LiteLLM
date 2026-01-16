"""
Judgment Assessment

Evaluate patient judgment capabilities through assessment of social/family
obligations, future planning, and responses to hypothetical situations using
BaseModel definitions and the MedKit AI client with schema-aware prompting.
"""

import sys
import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional, List

# Fix import paths
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.pydantic_prompt_generator import PromptStyle
from core.medkit_client import MedKitClient


class JudgmentQuestion(BaseModel):
    """A single clinical judgment question with guidance."""
    question_number: int = Field(description="Question number (1-10)")
    question_text: str = Field(description="The clinical question to ask the patient")
    assessment_domain: str = Field(description="Domain being assessed (e.g., insight, financial judgment, safety)")
    clinical_significance: str = Field(description="Why this question matters clinically")
    interpretation_guide: str = Field(description="How to interpret patient responses")


class ClinicalJudgmentQuestions(BaseModel):
    """Top 10 clinical judgment assessment questions from doctor perspective."""
    questions: List[JudgmentQuestion] = Field(description="List of 10 clinical judgment assessment questions")
    assessment_context: str = Field(description="Clinical context for these questions")


class PatientConcernQuestion(BaseModel):
    """A question about patient-reported judgment concerns."""
    question_number: int = Field(description="Question number (1-10)")
    question_text: str = Field(description="Question asking about patient's own judgment")
    concern_area: str = Field(description="Area of judgment being explored")
    follow_up_guidance: str = Field(description="How to follow up on responses")


class PatientReportedConcerns(BaseModel):
    """Top 10 patient-reported judgment concerns."""
    questions: List[PatientConcernQuestion] = Field(description="List of 10 patient-reported judgment questions")
    context: str = Field(description="Context for eliciting patient concerns")


class SocialObligations(BaseModel):
    """Assessment of patient's ability to meet social obligations."""
    social_commitment_awareness: str = Field(description="Patient's awareness of social commitments (appointments, gatherings, dates) - aware/somewhat aware/unaware/forgetful")
    social_follow_through: str = Field(description="Ability to follow through on social commitments - consistent/usually follows through/frequently fails/rarely follows through")
    reliability_to_friends: str = Field(description="How reliable is patient to friends? Very reliable/mostly reliable/sometimes unreliable/unreliable")
    punctuality: str = Field(description="Punctuality to appointments and social events - always on time/usually on time/frequently late/consistently late/very late")
    cancellation_pattern: str = Field(description="Pattern of canceling or postponing social events - never/rarely/occasionally/frequently/always without reason")
    social_responsibility_awareness: str = Field(description="Awareness of responsibility to others - good awareness/adequate awareness/limited awareness/no awareness")
    impact_of_behavior_others: str = Field(description="Understanding of how their behavior impacts others - good understanding/some understanding/limited understanding/no understanding")


class FamilyObligations(BaseModel):
    """Assessment of patient's ability to meet family obligations."""
    family_commitment_fulfillment: str = Field(description="Ability to meet family obligations (caregiving, financial support, household responsibilities) - fully manages/manages most/manages some/does not manage")
    childcare_responsibility: str = Field(description="If applicable, ability to manage childcare responsibilities - manages well/manages adequately/manages poorly/unable/not applicable")
    elder_care_responsibility: str = Field(description="If applicable, ability to care for aging parents or relatives - manages well/manages adequately/manages poorly/unable/not applicable")
    financial_obligations_family: str = Field(description="Ability to meet financial family obligations - pays regularly/mostly pays/frequently misses/does not pay/not applicable")
    household_management: str = Field(description="Ability to manage household responsibilities - well-maintained/adequate/neglected/severely neglected")
    family_communication: str = Field(description="Communication with family members - regular and appropriate/adequate/minimal/estranged/conflicted")
    family_problem_resolution: str = Field(description="Approach to resolving family conflicts - constructive/attempts to resolve/avoids/contributes to conflict/aggressive")
    family_awareness: str = Field(description="Awareness of family needs and dynamics - good awareness/adequate awareness/limited awareness/unaware")


class BusinessAffairs(BaseModel):
    """Assessment of patient's ability to manage business and practical affairs."""
    job_performance: str = Field(description="Work performance and reliability - excellent/good/adequate/poor/unable to work. Any recent issues?")
    attendance_punctuality_work: str = Field(description="Work attendance and punctuality - excellent/good/adequate/poor. Frequent absences or tardiness?")
    financial_management: str = Field(description="Ability to manage finances (bills, budgeting, spending) - manages well/adequate/struggles/unable")
    bill_payment: str = Field(description="Paying bills on time - always on time/usually on time/frequently late/chronic non-payment")
    debt_management: str = Field(description="Management of debt obligations - no significant debt/managing well/struggling/significant unpaid debt")
    spending_control: str = Field(description="Control over spending and impulse purchases - good control/adequate control/poor control/reckless spending")
    property_maintenance: str = Field(description="Maintenance of living space and possessions - well-maintained/adequate/neglected/hoarding/dangerous conditions")
    long_term_planning: str = Field(description="Ability to plan for long-term needs (savings, insurance, retirement) - good planning/adequate planning/minimal planning/no planning")
    document_management: str = Field(description="Management of important documents (legal, medical, financial) - well-organized/adequate/disorganized/lost/unable to manage")


class FuturePlanning(BaseModel):
    """Assessment of patient's ability to plan for the future."""
    short_term_goals: str = Field(description="Short-term goals (next few months) - has clear goals/some goals/vague goals/no goals/unrealistic goals")
    medium_term_planning: str = Field(description="Medium-term planning (next 1-2 years) - thoughtful plans/some planning/minimal planning/no planning")
    long_term_vision: str = Field(description="Long-term vision (5+ years) - clear vision/some vision/vague/no vision/unrealistic")
    goal_achievability: str = Field(description="Realistic assessment of goal achievability - realistic goals/some realistic/mostly unrealistic/unrealistic")
    planning_obstacles: str = Field(description="Awareness of obstacles to goals - good awareness/some awareness/limited awareness/no awareness")
    contingency_planning: str = Field(description="Ability to plan for contingencies - plans for challenges/some contingency/no contingency planning/inflexible")
    education_career_planning: str = Field(description="Planning for education or career development - active planning/some planning/minimal/no planning")
    retirement_planning: str = Field(description="Planning for retirement or long-term financial security - has plan/minimal plan/no plan/not applicable")
    goal_motivation: str = Field(description="Motivation to achieve goals - highly motivated/motivated/low motivation/unmotivated/appears depressed or hopeless")


class HypotheticalSituations(BaseModel):
    """Assessment of judgment through responses to hypothetical situations."""
    found_stamped_envelope: str = Field(description="What would you do if you found a stamped, addressed envelope? Patient response: would mail it/would return to sender/would discard/would open it/would keep it. Appropriateness of response?")
    found_envelope_reasoning: str = Field(description="Reasoning behind response to found envelope - considers owner's needs/considers consequences/selfish/no clear reasoning/inappropriate reasoning")
    red_light_stopped: str = Field(description="What would you do if stopped for running a red light? Patient response: acknowledge mistake/blame others/argue with officer/appropriate response to officer/hostile or defensive. Quality of response?")
    red_light_reasoning: str = Field(description="Reasoning behind response to traffic stop - takes responsibility/blames circumstances/defensive/aggressive/appropriate understanding of error")
    house_fire_evacuation: str = Field(description="What would you do if your house was on fire? Patient response: evacuate immediately/help family first/get valuables/call 911/hazardous behavior/appropriate response?")
    fire_safety_reasoning: str = Field(description="Reasoning about fire safety - prioritizes life/property over life/doesn't think things through/appropriate safety understanding")
    lost_wallet_finding: str = Field(description="What would you do if you found someone's wallet with ID and money? Patient response: return it/attempt to find owner/keep money/keep it all/appropriate response?")
    wallet_reasoning: str = Field(description="Reasoning about found wallet - considers owner's situation/ethical consideration/selfish/no consideration/appropriate ethics")
    medication_error: str = Field(description="What would you do if prescribed wrong medication dose? Patient response: call doctor/take it anyway/wait/ask pharmacist/appropriate response?")
    medication_safety: str = Field(description="Reasoning about medication safety - prioritizes personal safety/doesn't think it through/seeks help/appropriate medical judgment")
    financial_offer: str = Field(description="What would you do if offered financial gain through questionable means? Patient response: refuse/seek advice/accept/not think about legality/appropriate judgment?")
    financial_judgment: str = Field(description="Reasoning about ethical financial decisions - considers legality/ethical concerns/motivated by greed/no ethical consideration")


class RiskAssessment(BaseModel):
    """Assessment of patient's ability to recognize and avoid risky situations."""
    personal_safety_awareness: str = Field(description="Awareness of personal safety risks - good awareness/adequate awareness/limited awareness/poor awareness")
    risky_behavior_involvement: str = Field(description="Involvement in risky behaviors - avoids risky situations/some caution/frequently engages in risk/reckless")
    substance_misuse_judgment: str = Field(description="Judgment regarding alcohol/substance use - avoids/uses responsibly/uses despite risks/reckless use")
    sexual_judgment: str = Field(description="Judgment regarding sexual decisions - exercises caution/makes reasonable choices/poor judgment/reckless decisions/puts self at risk")
    financial_risk: str = Field(description="Ability to avoid financial risks (scams, predatory lending, etc.) - good judgment/adequate/poor/susceptible/easily exploited")
    legal_judgment: str = Field(description="Judgment to stay within legal boundaries - follows laws/mostly follows/frequently violates/no regard for law")
    vulnerability_to_exploitation: str = Field(description="Vulnerability to exploitation by others - not vulnerable/slightly vulnerable/moderately vulnerable/highly vulnerable/easily taken advantage of")
    self_protective_behavior: str = Field(description="Demonstrates self-protective behaviors - yes consistently/usually/sometimes/rarely/no")


class DecisionMakingProcess(BaseModel):
    """Assessment of patient's decision-making process and approach."""
    decision_spontaneity: str = Field(description="Decision-making style - thoughtful and deliberate/mostly thoughtful/impulsive/very impulsive/reckless")
    gathering_information: str = Field(description="Gathers relevant information before deciding - always/usually/sometimes/rarely/never")
    considers_consequences: str = Field(description="Considers consequences of decisions - thoroughly/usually/sometimes/rarely/ignores consequences")
    seeks_input: str = Field(description="Seeks input or advice from others - regularly/usually/sometimes/rarely/makes decisions alone")
    adapts_decisions: str = Field(description="Ability to adapt or change decisions based on new information - flexible/mostly flexible/somewhat rigid/inflexible/refuses to change")
    decision_quality_overall: str = Field(description="Overall quality of decisions - consistently good/usually good/mixed/usually poor/consistently poor")
    learns_from_mistakes: str = Field(description="Ability to learn from past poor decisions - learns well/learns somewhat/limited learning/does not learn/repeats mistakes")
    decision_regret: str = Field(description="Frequency of regret over decisions - rarely/occasionally/frequently/constantly/no reflection on decisions")


class CognitiveLimitations(BaseModel):
    """Assessment of cognitive limitations affecting judgment."""
    impulsivity: str = Field(description="Impulsivity affecting judgment - not present/mild/moderate/severe. Acts without thinking?")
    mania_poor_judgment: str = Field(description="If applicable, evidence of poor judgment from manic episodes - not present/possible/evident. History of reckless behavior during highs?")
    substance_influence: str = Field(description="Impact of substance use on judgment - not a factor/possible factor/likely factor/clear factor")
    executive_dysfunction: str = Field(description="Executive dysfunction affecting planning and judgment - not present/mild/moderate/severe")
    memory_impact: str = Field(description="Memory problems affecting judgment (forgetting obligations, plans) - not impacting/mild impact/moderate impact/severe impact")
    cognitive_decline: str = Field(description="Cognitive decline affecting judgment - not present/possible/evident. Age-appropriate or concerning?")
    reality_testing: str = Field(description="Ability to test reality and assess situations accurately - good/adequate/poor/impaired. Confused or delusional thinking?")


class ContextualFactors(BaseModel):
    """Contextual factors affecting judgment assessment."""
    mental_health_status: str = Field(description="Current mental health status impacting judgment - stable/somewhat impacted/significantly impacted/crisis")
    medication_compliance: str = Field(description="Compliance with psychiatric medications - compliant/mostly compliant/non-compliant/not on medications")
    substance_use_current: str = Field(description="Current substance use affecting judgment - none/occasional/frequent/intoxicated now")
    sleep_deprivation: str = Field(description="Sleep deprivation affecting judgment - adequate sleep/mild deprivation/moderate deprivation/severe/chronic insomnia")
    stress_level: str = Field(description="Current stress level affecting judgment - minimal/mild/moderate/severe/overwhelming")
    environmental_influences: str = Field(description="Environmental influences on judgment (peers, family, social media, etc.) - positive influences/neutral/some negative/strong negative influences")
    cultural_values: str = Field(description="Cultural or religious values influencing judgment - guides appropriate decisions/generally positive/conflicts with social norms/limits judgment")


class AssessmentSummary(BaseModel):
    """Overall judgment assessment findings and clinical recommendations."""
    judgment_capacity_overall: str = Field(description="Overall judgment capacity - intact/mildly impaired/moderately impaired/severely impaired/unable to judge")
    social_judgment: str = Field(description="Social judgment capability - good/adequate/poor. Considers impact on others?")
    practical_judgment: str = Field(description="Practical judgment for daily living - good/adequate/poor. Manages affairs appropriately?")
    hypothetical_situation_performance: str = Field(description="Performance on hypothetical situation responses - appropriate responses/mostly appropriate/some inappropriate/predominantly inappropriate/hazardous responses")
    decision_making_quality: str = Field(description="Overall decision-making quality - consistently good/usually good/mixed/usually poor/consistently poor")
    areas_of_good_judgment: str = Field(description="Areas where judgment is intact or strong, comma-separated")
    areas_of_impaired_judgment: str = Field(description="Areas where judgment is impaired or questionable, comma-separated")
    risk_behaviors: str = Field(description="Identified risky or hazardous behaviors - none/minor/moderate/significant/dangerous")
    hazardous_behavior_present: str = Field(description="Hazardous or inappropriate behavior identified? No/yes. If yes, describe")
    safety_concerns: str = Field(description="Safety concerns for patient or others - none/mild/moderate/significant/immediate danger")
    judgment_consistency: str = Field(description="Consistency of judgment across situations - consistent/inconsistent/variable/pattern of poor judgment")
    underlying_factors: str = Field(description="Underlying factors affecting judgment (impulsivity, substance use, mental illness, cognitive decline, etc.), comma-separated")
    recommendations: str = Field(description="Clinical recommendations (monitoring, support, limit autonomy, supervised finances, etc.), comma-separated")
    capacity_concerns: str = Field(description="Concerns about decision-making capacity? No/yes. If yes, specific recommendations for support?")


class JudgementAssessment(BaseModel):
    """
    Comprehensive judgment assessment.

    Organized as a collection of BaseModel sections, each representing
    distinct aspects of judgment evaluation. Includes assessment of social
    and family obligations, business/practical affairs, future planning,
    responses to hypothetical situations, risk assessment, decision-making
    process, and cognitive limitations affecting judgment.
    """
    # Social obligations
    social_obligations: SocialObligations

    # Family obligations
    family_obligations: FamilyObligations

    # Business and practical affairs
    business_affairs: BusinessAffairs

    # Future planning capability
    future_planning: FuturePlanning

    # Responses to hypothetical situations
    hypothetical_situations: HypotheticalSituations

    # Risk assessment and avoidance
    risk_assessment: RiskAssessment

    # Decision-making process
    decision_making_process: DecisionMakingProcess

    # Cognitive limitations affecting judgment
    cognitive_limitations: CognitiveLimitations

    # Contextual factors
    contextual_factors: ContextualFactors

    # Final assessment
    assessment_summary: AssessmentSummary


def generate_clinical_questions(
    client: MedKitClient,
    patient_context: Optional[str] = None,
    prompt_style: PromptStyle = PromptStyle.DETAILED,
) -> ClinicalJudgmentQuestions:
    """
    Generate top 10 clinical judgment assessment questions using LLM.

    Args:
        client: MedKitClient instance for LLM generation
        patient_context: Optional patient context for question generation
        prompt_style: Style of prompt generation (DETAILED, CONCISE, TECHNICAL)

    Returns:
        ClinicalJudgmentQuestions with 10 LLM-generated clinical questions
    """
    context_note = f"\nPatient context: {patient_context}" if patient_context else ""

    subject = f"""Generate 10 clinical judgment assessment questions from a doctor's perspective.

These should assess patient judgment across key domains: insight, financial decisions, safety awareness,
medical compliance, impulse control, reality testing, and functional capacity. Questions should be appropriate
for psychiatric evaluation and capable of identifying impaired judgment.{context_note}"""

    sys_prompt = """You are an expert psychiatrist specializing in clinical judgment assessment.

Generate structured clinical questions that are:
- Assessing judgment across key domains: insight, financial decisions, safety awareness, medical compliance, impulse control, reality testing, functional capacity
- Appropriate for psychiatric evaluation
- Capable of identifying impaired judgment
- Adhering to current psychiatric standards and guidelines

Return structured JSON matching the exact schema provided, with all required fields populated."""

    return client.generate_text(
        prompt=subject,
        schema=ClinicalJudgmentQuestions,
        sys_prompt=sys_prompt,
    )


def generate_patient_concerns(
    client: MedKitClient,
    patient_context: Optional[str] = None,
    prompt_style: PromptStyle = PromptStyle.DETAILED,
) -> PatientReportedConcerns:
    """
    Generate top 10 patient-reported judgment concern questions using LLM.

    Args:
        client: MedKitClient instance for LLM generation
        patient_context: Optional patient context for question generation
        prompt_style: Style of prompt generation (DETAILED, CONCISE, TECHNICAL)

    Returns:
        PatientReportedConcerns with 10 LLM-generated patient questions
    """
    context_note = f"\nPatient context: {patient_context}" if patient_context else ""

    subject = f"""Generate 10 questions that explore patient-reported concerns about their own judgment
and decision-making abilities.

These should assess the patient's perspective on: decision difficulty, trust in relationships, money management
confidence, regret about past decisions, how others perceive their judgment, self-understanding, pressure resistance,
learning from mistakes, changes in judgment, and family concerns. Questions should be open-ended and encourage
detailed responses.{context_note}"""

    sys_prompt = """You are an expert psychiatrist specializing in patient-reported judgment concerns.

Generate structured clinical questions that are:
- Open-ended to encourage detailed responses
- Assessing patient's self-perspective on judgment and decision-making
- Exploring trust, confidence, regret, and self-understanding
- Following current psychiatric standards and guidelines

Return structured JSON matching the exact schema provided, with all required fields populated."""

    return client.generate_text(
        prompt=subject,
        schema=PatientReportedConcerns,
        sys_prompt=sys_prompt,
    )


def ask_judgement_questions(
    client: Optional[MedKitClient] = None,
    patient_context: Optional[str] = None,
    prompt_style: PromptStyle = PromptStyle.DETAILED,
) -> dict:
    """
    Ask patient judgement assessment questions interactively.

    If client is provided, uses LLM to generate dynamic questions.
    Otherwise, uses fallback hardcoded questions.

    Args:
        client: Optional MedKitClient for LLM question generation
        patient_context: Optional patient context for question customization
        prompt_style: Style of prompt generation

    Returns:
        Dictionary of patient responses to judgment questions
    """
    print("\n" + "="*60)
    print("JUDGEMENT ASSESSMENT")
    print("="*60)
    print()
    print("MEASURES: This assessment evaluates the patient's practical judgment, decision-making")
    print("  ability, and understanding of social obligations and consequences.")
    print("  • Ability to fulfill social and family obligations")
    print("  • Management of business affairs and finances")
    print("  • Future planning and goal-setting capabilities")
    print("  • Response to hypothetical situations requiring sound judgment")
    print("  • Risk assessment and ability to avoid hazardous decisions")
    print()
    print("TOP 10 KEY ASSESSMENT QUESTIONS:")
    print("  1. Do you keep your appointments with friends and family?")
    print("  2. How well do you manage household responsibilities?")
    print("  3. Are you able to pay your bills on time?")
    print("  4. Do you have short-term and long-term goals?")
    print("  5. What would you do if you found a stamped, addressed envelope?")
    print("  6. What would you do if stopped for running a red light?")
    print("  7. What would you do if your house was on fire?")
    print("  8. What would you do if you found someone's wallet?")
    print("  9. How do you make important decisions in your life?")
    print(" 10. Do you consider the consequences of your actions?")
    print()
    print("="*60)
    print("DETAILED JUDGEMENT QUESTIONNAIRE")
    print("="*60)

    responses = {}

    # Generate clinical questions via LLM if client provided
    if client:
        print("\nGenerating clinical judgment questions...")
        try:
            clinical_qs = generate_clinical_questions(client, patient_context, prompt_style)
            print("\n" + "="*60)
            print("TOP 10 CLINICAL JUDGMENT QUESTIONS")
            print("="*60)

            for q in clinical_qs.questions:
                response = input(f"{q.question_number}. {q.question_text}\n> ").strip()
                responses[f'q{q.question_number}_clinical'] = response
                if q.interpretation_guide:
                    print(f"   [Clinical note: {q.clinical_significance}]\n")
        except Exception as e:
            print(f"Warning: Could not generate clinical questions via LLM: {e}")
            print("Using fallback questions...\n")

    # If no LLM generated questions, use fallback
    if not any(k.startswith('q') for k in responses.keys()):
        print("\n" + "="*60)
        print("TOP 10 CLINICAL JUDGMENT QUESTIONS (Fallback)")
        print("="*60)

        responses['q1_insight'] = input("1. Do you believe there is anything wrong with your thinking or behavior right now?: ").strip()
        responses['q2_consequences'] = input("2. If you spent all your money on something today, how would you manage next month?: ").strip()
        responses['q3_dangerous_situation'] = input("3. What would you do if you found yourself in a dangerous or unsafe situation?: ").strip()
        responses['q4_advice_following'] = input("4. If a doctor advised you against something, but you wanted to do it anyway, what would you do?: ").strip()
        responses['q5_medical_decision'] = input("5. How do you decide whether to take prescribed medications or follow medical advice?: ").strip()
        responses['q6_risky_behavior'] = input("6. Have you engaged in activities that could harm you or others? What made you do that?: ").strip()
        responses['q7_problem_solving'] = input("7. When facing a serious problem, what steps do you take to solve it?: ").strip()
        responses['q8_impulse_control'] = input("8. Do you sometimes act without thinking about the consequences? Can you give an example?: ").strip()
        responses['q9_reality_awareness'] = input("9. Do you ever have unusual beliefs or experiences that others say aren't real?: ").strip()
        responses['q10_capacity_awareness'] = input("10. Do you feel capable of managing your own finances, health decisions, and daily responsibilities?: ").strip()

    # Generate patient concerns via LLM if client provided
    if client:
        print("\nGenerating patient-reported concern questions...")
        try:
            patient_qs = generate_patient_concerns(client, patient_context, prompt_style)
            print("\n" + "="*60)
            print("TOP 10 PATIENT-REPORTED JUDGMENT CONCERNS")
            print("="*60)

            for q in patient_qs.questions:
                response = input(f"{q.question_number}. {q.question_text}\n> ").strip()
                responses[f'p{q.question_number}_concern'] = response
                if q.follow_up_guidance:
                    print(f"   [Follow-up: {q.follow_up_guidance}]\n")
        except Exception as e:
            print(f"Warning: Could not generate patient questions via LLM: {e}")
            print("Using fallback questions...\n")

    # If no LLM generated questions, use fallback
    if not any(k.startswith('p') for k in responses.keys()):
        print("\n" + "="*60)
        print("TOP 10 PATIENT-REPORTED JUDGMENT CONCERNS (Fallback)")
        print("="*60)

        responses['p1_decision_difficulty'] = input("1. Do you find it hard to make decisions? What makes it difficult?: ").strip()
        responses['p2_trust_others'] = input("2. Do you trust people easily, or do you find it hard to know who to trust?: ").strip()
        responses['p3_money_management'] = input("3. How do you feel about your ability to manage money?: ").strip()
        responses['p4_regret_decisions'] = input("4. How often do you regret decisions you've made? Any recent examples?: ").strip()
        responses['p5_others_opinion'] = input("5. Do you think other people think you make good decisions? What have they said?: ").strip()
        responses['p6_understand_yourself'] = input("6. Do you understand yourself and how you think? Any areas you're unsure about?: ").strip()
        responses['p7_pressure_decisions'] = input("7. How do you react when people pressure you to do something you're unsure about?: ").strip()
        responses['p8_learn_mistakes'] = input("8. Can you learn from your mistakes, or do you tend to repeat them?: ").strip()
        responses['p9_judgment_changes'] = input("9. Have you noticed your judgment or decision-making changing over time?: ").strip()
        responses['p10_family_concerns'] = input("10. Has your family or friends expressed concern about your judgment or decisions?: ").strip()

    # OLD QUESTIONS (KEPT FOR BACKWARDS COMPATIBILITY)
    print("\n--- SOCIAL JUDGMENT ---")
    responses['family_obligation'] = input("If your family needed money, would you help even if you couldn't afford it? How would you handle it?: ").strip()
    responses['friend_conflict'] = input("If two friends disagreed, how would you handle it?: ").strip()

    # FINANCIAL JUDGMENT
    print("\n--- FINANCIAL JUDGMENT ---")
    responses['financial_offer'] = input("If someone offered you a 'guaranteed' investment return, what would you do?: ").strip()
    responses['unexpected_money'] = input("If you unexpectedly received money, what would you do?: ").strip()

    # SAFETY JUDGMENT
    print("\n--- SAFETY JUDGMENT ---")
    responses['red_light'] = input("What would you do if the traffic light turned red while you're crossing the street?: ").strip()
    responses['house_fire'] = input("If your house caught fire and you had time to save a few things, what would you prioritize?: ").strip()
    responses['lost_wallet'] = input("If you found a wallet with money, what would you do?: ").strip()

    # HEALTH JUDGMENT
    print("\n--- HEALTH JUDGMENT ---")
    responses['medication_error'] = input("If you noticed a medication error, what would you do?: ").strip()
    responses['illness_decision'] = input("When should someone see a doctor for an illness?: ").strip()

    # ETHICAL JUDGMENT
    print("\n--- ETHICAL JUDGMENT ---")
    responses['ethical_dilemma'] = input("If you could gain something by breaking a small rule, would you? Why or why not?: ").strip()
    responses['honesty_test'] = input("Would you tell the truth even if it caused problems?: ").strip()

    # FUTURE PLANNING
    print("\n--- FUTURE PLANNING ---")
    responses['retirement_planning'] = input("How would you plan for your retirement?: ").strip()
    responses['major_decision'] = input("How do you make major life decisions?: ").strip()

    # JUDGMENT QUALITY
    print("\n--- JUDGMENT QUALITY ---")
    responses['decision_process'] = input("Do you think before acting or act impulsively? (think/impulsive/mixed): ").strip()
    responses['judgment_confidence'] = input("How confident are you in your judgments? (very/somewhat/uncertain): ").strip()

    # SOCIAL OBLIGATIONS
    print("\n--- SOCIAL OBLIGATIONS ---")
    responses['social_commitment_awareness'] = input("How aware are you of social commitments (appointments, gatherings)?: ").strip()
    responses['social_follow_through'] = input("How well do you follow through on social commitments?: ").strip()
    responses['reliability_to_friends'] = input("How reliable are you to your friends?: ").strip()
    responses['punctuality'] = input("How punctual are you to appointments and social events?: ").strip()
    responses['cancellation_pattern'] = input("How often do you cancel or postpone social events?: ").strip()
    responses['social_responsibility_awareness'] = input("How aware are you of your responsibility to others?: ").strip()
    responses['impact_of_behavior_others'] = input("Do you understand how your behavior impacts others?: ").strip()

    # FAMILY OBLIGATIONS
    print("\n--- FAMILY OBLIGATIONS ---")
    responses['family_commitment_fulfillment'] = input("How well do you meet family obligations (caregiving, financial, household)?: ").strip()
    responses['childcare_responsibility'] = input("If applicable, how well do you manage childcare responsibilities?: ").strip()
    responses['elder_care_responsibility'] = input("If applicable, how well do you care for aging relatives?: ").strip()
    responses['financial_obligations_family'] = input("Do you meet financial family obligations on time?: ").strip()
    responses['household_management'] = input("How well do you manage household responsibilities?: ").strip()
    responses['family_communication'] = input("How do you communicate with family members?: ").strip()
    responses['family_problem_resolution'] = input("How do you approach resolving family conflicts?: ").strip()
    responses['family_awareness'] = input("How aware are you of family needs and dynamics?: ").strip()

    # BUSINESS AND PRACTICAL AFFAIRS
    print("\n--- BUSINESS AND PRACTICAL AFFAIRS ---")
    responses['job_performance'] = input("How would you describe your work performance and reliability?: ").strip()
    responses['attendance_punctuality_work'] = input("How are your attendance and punctuality at work?: ").strip()
    responses['financial_management'] = input("How well do you manage finances (bills, budgeting, spending)?: ").strip()
    responses['bill_payment'] = input("Do you pay bills on time?: ").strip()
    responses['debt_management'] = input("How do you manage debt obligations?: ").strip()
    responses['spending_control'] = input("Do you have good control over spending and impulse purchases?: ").strip()
    responses['property_maintenance'] = input("How well do you maintain your living space and possessions?: ").strip()
    responses['long_term_planning'] = input("Do you plan for long-term needs (savings, insurance, retirement)?: ").strip()
    responses['document_management'] = input("How do you manage important documents (legal, medical, financial)?: ").strip()

    # FUTURE PLANNING
    print("\n--- FUTURE PLANNING ---")
    responses['short_term_goals'] = input("What are your short-term goals (next few months)?: ").strip()
    responses['medium_term_planning'] = input("How do you plan for the medium term (1-2 years)?: ").strip()
    responses['long_term_vision'] = input("What is your long-term vision (5+ years)?: ").strip()
    responses['goal_achievability'] = input("Are your goals realistic and achievable?: ").strip()
    responses['planning_obstacles'] = input("Are you aware of obstacles to achieving your goals?: ").strip()
    responses['contingency_planning'] = input("Do you plan for contingencies or unexpected challenges?: ").strip()
    responses['education_career_planning'] = input("Do you plan for education or career development?: ").strip()
    responses['retirement_planning'] = input("Do you have plans for retirement or long-term financial security?: ").strip()
    responses['goal_motivation'] = input("How motivated are you to achieve your goals?: ").strip()

    # HYPOTHETICAL SITUATIONS
    print("\n--- HYPOTHETICAL SITUATIONS ---")
    responses['found_stamped_envelope'] = input("If you found a stamped, addressed envelope, what would you do?: ").strip()
    responses['found_envelope_reasoning'] = input("What is your reasoning behind that choice?: ").strip()
    responses['red_light_stopped'] = input("If stopped by police for running a red light, how would you respond?: ").strip()
    responses['red_light_reasoning'] = input("What is your reasoning about traffic safety?: ").strip()
    responses['house_fire_evacuation'] = input("If your house caught fire, what would you do?: ").strip()
    responses['fire_safety_reasoning'] = input("What is your reasoning about fire safety?: ").strip()
    responses['lost_wallet_finding'] = input("If you found someone's wallet with ID and money, what would you do?: ").strip()
    responses['wallet_reasoning'] = input("What is your reasoning about found property?: ").strip()
    responses['medication_error'] = input("If prescribed the wrong medication dose, what would you do?: ").strip()
    responses['medication_safety'] = input("What is your reasoning about medication safety?: ").strip()
    responses['financial_offer'] = input("If offered financial gain through questionable means, what would you do?: ").strip()
    responses['financial_judgment'] = input("What is your reasoning about ethical financial decisions?: ").strip()

    # RISK ASSESSMENT
    print("\n--- RISK ASSESSMENT ---")
    responses['personal_safety_awareness'] = input("How aware are you of personal safety risks?: ").strip()
    responses['risky_behavior_involvement'] = input("Do you engage in risky behaviors?: ").strip()
    responses['substance_misuse_judgment'] = input("How do you judge alcohol or substance use?: ").strip()
    responses['sexual_judgment'] = input("How do you make sexual decisions?: ").strip()
    responses['financial_risk'] = input("Can you avoid financial risks (scams, predatory lending)?: ").strip()
    responses['legal_judgment'] = input("Do you stay within legal boundaries?: ").strip()
    responses['vulnerability_to_exploitation'] = input("Do you feel vulnerable to exploitation?: ").strip()
    responses['self_protective_behavior'] = input("Do you demonstrate self-protective behaviors?: ").strip()

    # DECISION-MAKING PROCESS
    print("\n--- DECISION-MAKING PROCESS ---")
    responses['decision_spontaneity'] = input("Is your decision-making thoughtful or impulsive?: ").strip()
    responses['gathering_information'] = input("Do you gather information before deciding?: ").strip()
    responses['considers_consequences'] = input("Do you consider consequences of decisions?: ").strip()
    responses['seeks_input'] = input("Do you seek input or advice from others?: ").strip()
    responses['adapts_decisions'] = input("Can you adapt decisions based on new information?: ").strip()
    responses['decision_quality_overall'] = input("How would you rate your overall decision quality?: ").strip()
    responses['learns_from_mistakes'] = input("Do you learn from past poor decisions?: ").strip()
    responses['decision_regret'] = input("How often do you regret your decisions?: ").strip()

    # COGNITIVE LIMITATIONS
    print("\n--- COGNITIVE LIMITATIONS ---")
    responses['impulsivity'] = input("How much does impulsivity affect your judgment?: ").strip()
    responses['mania_poor_judgment'] = input("Have you had manic episodes affecting judgment?: ").strip()
    responses['substance_influence'] = input("Does substance use impact your judgment?: ").strip()
    responses['executive_dysfunction'] = input("Do you have difficulty with planning and judgment?: ").strip()
    responses['memory_impact'] = input("Do memory problems affect your judgment?: ").strip()
    responses['cognitive_decline'] = input("Have you noticed cognitive changes?: ").strip()
    responses['reality_testing'] = input("Can you accurately assess situations?: ").strip()

    # CONTEXTUAL FACTORS
    print("\n--- CONTEXTUAL FACTORS ---")
    responses['mental_health_status'] = input("How is your current mental health status?: ").strip()
    responses['medication_compliance'] = input("How well do you comply with medications?: ").strip()
    responses['substance_use_current'] = input("Are you currently using any substances?: ").strip()
    responses['sleep_deprivation'] = input("How is your sleep quality?: ").strip()
    responses['stress_level'] = input("What is your current stress level?: ").strip()
    responses['environmental_influences'] = input("What environmental influences affect your judgment?: ").strip()
    responses['cultural_values'] = input("How do cultural or religious values influence your judgment?: ").strip()

    return responses


def create_judgement_assessment_from_responses(patient_name: str, responses: dict, output_path: Optional[Path] = None) -> JudgementAssessment:
    """
    Create a structured judgement assessment object from collected patient responses.
    """
    assessment_data = {
        "social_obligations": {
            "social_commitment_awareness": responses.get('social_commitment_awareness', ''),
            "social_follow_through": responses.get('social_follow_through', ''),
            "reliability_to_friends": responses.get('reliability_to_friends', ''),
            "punctuality": responses.get('punctuality', ''),
            "cancellation_pattern": responses.get('cancellation_pattern', ''),
            "social_responsibility_awareness": responses.get('social_responsibility_awareness', ''),
            "impact_of_behavior_others": responses.get('impact_of_behavior_others', '')
        },
        "family_obligations": {
            "family_commitment_fulfillment": responses.get('family_commitment_fulfillment', ''),
            "childcare_responsibility": responses.get('childcare_responsibility', ''),
            "elder_care_responsibility": responses.get('elder_care_responsibility', ''),
            "financial_obligations_family": responses.get('financial_obligations_family', ''),
            "household_management": responses.get('household_management', ''),
            "family_communication": responses.get('family_communication', ''),
            "family_problem_resolution": responses.get('family_problem_resolution', ''),
            "family_awareness": responses.get('family_awareness', '')
        },
        "business_affairs": {
            "job_performance": responses.get('job_performance', ''),
            "attendance_punctuality_work": responses.get('attendance_punctuality_work', ''),
            "financial_management": responses.get('financial_management', ''),
            "bill_payment": responses.get('bill_payment', ''),
            "debt_management": responses.get('debt_management', ''),
            "spending_control": responses.get('spending_control', ''),
            "property_maintenance": responses.get('property_maintenance', ''),
            "long_term_planning": responses.get('long_term_planning', ''),
            "document_management": responses.get('document_management', '')
        },
        "future_planning": {
            "short_term_goals": responses.get('short_term_goals', ''),
            "medium_term_planning": responses.get('medium_term_planning', ''),
            "long_term_vision": responses.get('long_term_vision', ''),
            "goal_achievability": responses.get('goal_achievability', ''),
            "planning_obstacles": responses.get('planning_obstacles', ''),
            "contingency_planning": responses.get('contingency_planning', ''),
            "education_career_planning": responses.get('education_career_planning', ''),
            "retirement_planning": responses.get('retirement_planning', ''),
            "goal_motivation": responses.get('goal_motivation', '')
        },
        "hypothetical_situations": {
            "found_stamped_envelope": responses.get('found_stamped_envelope', ''),
            "found_envelope_reasoning": responses.get('found_envelope_reasoning', ''),
            "red_light_stopped": responses.get('red_light_stopped', ''),
            "red_light_reasoning": responses.get('red_light_reasoning', ''),
            "house_fire_evacuation": responses.get('house_fire_evacuation', ''),
            "fire_safety_reasoning": responses.get('fire_safety_reasoning', ''),
            "lost_wallet_finding": responses.get('lost_wallet_finding', ''),
            "wallet_reasoning": responses.get('wallet_reasoning', ''),
            "medication_error": responses.get('medication_error', ''),
            "medication_safety": responses.get('medication_safety', ''),
            "financial_offer": responses.get('financial_offer', ''),
            "financial_judgment": responses.get('financial_judgment', '')
        },
        "risk_assessment": {
            "personal_safety_awareness": responses.get('personal_safety_awareness', ''),
            "risky_behavior_involvement": responses.get('risky_behavior_involvement', ''),
            "substance_misuse_judgment": responses.get('substance_misuse_judgment', ''),
            "sexual_judgment": responses.get('sexual_judgment', ''),
            "financial_risk": responses.get('financial_risk', ''),
            "legal_judgment": responses.get('legal_judgment', ''),
            "vulnerability_to_exploitation": responses.get('vulnerability_to_exploitation', ''),
            "self_protective_behavior": responses.get('self_protective_behavior', '')
        },
        "decision_making_process": {
            "decision_spontaneity": responses.get('decision_spontaneity', ''),
            "gathering_information": responses.get('gathering_information', ''),
            "considers_consequences": responses.get('considers_consequences', ''),
            "seeks_input": responses.get('seeks_input', ''),
            "adapts_decisions": responses.get('adapts_decisions', ''),
            "decision_quality_overall": responses.get('decision_quality_overall', ''),
            "learns_from_mistakes": responses.get('learns_from_mistakes', ''),
            "decision_regret": responses.get('decision_regret', '')
        },
        "cognitive_limitations": {
            "impulsivity": responses.get('impulsivity', ''),
            "mania_poor_judgment": responses.get('mania_poor_judgment', ''),
            "substance_influence": responses.get('substance_influence', ''),
            "executive_dysfunction": responses.get('executive_dysfunction', ''),
            "memory_impact": responses.get('memory_impact', ''),
            "cognitive_decline": responses.get('cognitive_decline', ''),
            "reality_testing": responses.get('reality_testing', '')
        },
        "contextual_factors": {
            "mental_health_status": responses.get('mental_health_status', ''),
            "medication_compliance": responses.get('medication_compliance', ''),
            "substance_use_current": responses.get('substance_use_current', ''),
            "sleep_deprivation": responses.get('sleep_deprivation', ''),
            "stress_level": responses.get('stress_level', ''),
            "environmental_influences": responses.get('environmental_influences', ''),
            "cultural_values": responses.get('cultural_values', '')
        },
        "assessment_summary": {
            "judgment_capacity_overall": "To be determined by clinician",
            "social_judgment": "To be determined by clinician",
            "practical_judgment": "To be determined by clinician",
            "hypothetical_situation_performance": "To be determined by clinician",
            "decision_making_quality": "To be determined by clinician",
            "areas_of_good_judgment": "To be identified",
            "areas_of_impaired_judgment": "To be identified",
            "risk_behaviors": "To be assessed",
            "hazardous_behavior_present": "No",
            "safety_concerns": "None",
            "judgment_consistency": "To be determined",
            "underlying_factors": "To be identified",
            "recommendations": "Routine assessment",
            "capacity_concerns": "No"
        }
    }

    assessment = JudgementAssessment(**assessment_data)

    if output_path is None:
        output_path = Path("outputs") / f"{patient_name.lower().replace(' ', '_')}_judgement.json"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(assessment.model_dump(), f, indent=2)

    print(f"\n✓ Assessment saved to: {output_path}")

    return assessment


def evaluate_judgement(
    patient_name: str,
    output_path: Optional[Path] = None,
    use_schema_prompt: bool = True,
    prompt_style: PromptStyle = PromptStyle.DETAILED,
    client: Optional[MedKitClient] = None,
    patient_context: Optional[str] = None,
) -> JudgementAssessment:
    """
    Evaluate patient judgement capabilities through interactive questionnaire.

    Args:
        patient_name: Name/identifier of the patient
        output_path: Optional path to save assessment JSON
        use_schema_prompt: Whether to use schema-aware prompting
        prompt_style: Style of prompt generation
        client: Optional MedKitClient for LLM question generation
        patient_context: Optional patient context for question customization

    Returns:
        JudgementAssessment with validated responses
    """
    if not patient_name or not patient_name.strip():
        raise ValueError("Patient name cannot be empty")

    print(f"\nStarting judgement assessment for: {patient_name}")
    responses = ask_judgement_questions(client, patient_context, prompt_style)

    assessment = create_judgement_assessment_from_responses(patient_name, responses, output_path)

    return assessment


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Evaluate patient judgment capability through structured assessment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default - saves to outputs/patient_judgement.json
  python exam_judgement.py "John Doe"

  # Custom output path
  python exam_judgement.py "John Doe" -o custom_assessment.json

  # With concise prompting
  python exam_judgement.py "John Doe" --concise

Judgment Assessment Protocol:
  1. SOCIAL OBLIGATIONS:
     - How do you meet social commitments (appointments, gatherings)?
     - Are you reliable to your friends?
     - How punctual are you to social events?
     - Do you understand impact of your behavior on others?

  2. FAMILY OBLIGATIONS:
     - How do you meet family responsibilities (caregiving, financial, household)?
     - Do you maintain regular communication with family?
     - How do you handle family conflicts?
     - Are you aware of family members' needs?

  3. BUSINESS AND PRACTICAL AFFAIRS:
     - How is your work performance and attendance?
     - Do you pay bills on time?
     - How do you manage money and spending?
     - Do you maintain your living space?
     - Do you have long-term financial plans?

  4. FUTURE PLANNING:
     - What are your goals for the next 6 months? 1 year? 5 years?
     - Are these goals realistic?
     - How do you plan to achieve them?
     - What obstacles might get in the way?
     - How motivated are you to pursue goals?

  5. HYPOTHETICAL SITUATIONS (Present scenarios):
     - What would you do if you found a stamped, addressed envelope?
     - What would you do if stopped for running a red light?
     - What would you do if your house was on fire?
     - What would you do if you found someone's wallet with ID and money?
     - What would you do if prescribed wrong medication dose?
     - What would you do if offered money through questionable means?

  6. RISK ASSESSMENT:
     - Do you recognize dangerous situations?
     - Do you engage in risky behaviors?
     - Can you avoid being exploited?

  EXPECTED: Able to evaluate situations and provide appropriate responses,
            managing family and business affairs appropriately.
  UNEXPECTED: Responses indicating hazardous behavior or inappropriate action.
        """
    )
    parser.add_argument("patient", nargs='*', default=['unknown'], help="Name or identifier of the patient (default: 'unknown')")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Path to save JSON output. Defaults to outputs/{patient_name}_judgement.json"
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

        result = evaluate_judgement(
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
