"""Mental Health Assessment Pydantic Models

This module contains all Pydantic data models for mental health assessment,
including assessment tools, symptom categories, risk assessment, and diagnostic information.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# ==================== Assessment Tools & Scales ====================

class PHQ9Assessment(BaseModel):
    """PHQ-9: Patient Health Questionnaire for Depression Screening (0-27 scale)."""
    depressed_mood: int = Field(0, ge=0, le=3, description="Little interest or pleasure in activities")
    sleep_disturbance: int = Field(0, ge=0, le=3, description="Trouble falling/staying asleep or sleeping too much")
    fatigue: int = Field(0, ge=0, le=3, description="Feeling tired or having little energy")
    appetite_change: int = Field(0, ge=0, le=3, description="Poor appetite or overeating")
    guilt_shame: int = Field(0, ge=0, le=3, description="Feeling bad about yourself or that you are a failure")
    concentration: int = Field(0, ge=0, le=3, description="Trouble concentrating on things")
    psychomotor: int = Field(0, ge=0, le=3, description="Moving or speaking so slowly/fast others could have noticed")
    suicidal_ideation: int = Field(0, ge=0, le=3, description="Thoughts that you would be better off dead")
    functional_impairment: int = Field(0, ge=0, le=3, description="Difficulty with work, school, home, or relationships")

    @property
    def total_score(self) -> int:
        """Calculate total PHQ-9 score."""
        return sum([self.depressed_mood, self.sleep_disturbance, self.fatigue,
                   self.appetite_change, self.guilt_shame, self.concentration,
                   self.psychomotor, self.suicidal_ideation, self.functional_impairment])

    @property
    def severity(self) -> str:
        """Map score to severity level."""
        score = self.total_score
        if score < 5:
            return "minimal"
        elif score < 10:
            return "mild"
        elif score < 15:
            return "moderate"
        elif score < 20:
            return "moderately severe"
        else:
            return "severe"


class GAD7Assessment(BaseModel):
    """GAD-7: Generalized Anxiety Disorder-7 Assessment (0-21 scale)."""
    worry_frequency: int = Field(0, ge=0, le=3, description="Feeling nervous, anxious or on edge")
    worry_control: int = Field(0, ge=0, le=3, description="Not being able to stop or control worrying")
    worry_concentration: int = Field(0, ge=0, le=3, description="Worrying too much about different things")
    irritability: int = Field(0, ge=0, le=3, description="Trouble relaxing")
    restlessness: int = Field(0, ge=0, le=3, description="Being so restless that it's hard to sit still")
    fatigue_anxiety: int = Field(0, ge=0, le=3, description="Becoming easily annoyed or irritable")
    fear_catastrophe: int = Field(0, ge=0, le=3, description="Afraid something awful might happen")

    @property
    def total_score(self) -> int:
        """Calculate total GAD-7 score."""
        return sum([self.worry_frequency, self.worry_control, self.worry_concentration,
                   self.irritability, self.restlessness, self.fatigue_anxiety, self.fear_catastrophe])

    @property
    def severity(self) -> str:
        """Map score to severity level."""
        score = self.total_score
        if score < 5:
            return "minimal"
        elif score < 10:
            return "mild"
        elif score < 15:
            return "moderate"
        else:
            return "severe"


# ==================== Mental Health Symptom Categories ====================

class MoodSymptoms(BaseModel):
    """Depressive and mood-related symptoms."""
    persistent_depressed_mood: bool = Field(False, description="Feeling sad, empty, or hopeless")
    anhedonia: bool = Field(False, description="Loss of interest or pleasure in activities")
    worthlessness: bool = Field(False, description="Feelings of worthlessness or excessive guilt")
    hopelessness: bool = Field(False, description="Pessimism about the future")
    emotional_numbness: bool = Field(False, description="Emotional numbness or flattening")
    irritability_mood: bool = Field(False, description="Irritability or anger outbursts")
    mood_cycling: bool = Field(False, description="Cycling between depressed and elevated moods")
    elevated_mood_episodes: bool = Field(False, description="Periods of unusually elevated or expansive mood")
    grandiosity: bool = Field(False, description="Inflated self-esteem or grandiose beliefs")


class AnxietySymptoms(BaseModel):
    """Anxiety-related symptoms."""
    generalized_worry: bool = Field(False, description="Excessive worry about multiple things")
    panic_attacks: bool = Field(False, description="Sudden episodes of intense fear or panic")
    specific_phobias: bool = Field(False, description="Intense fear of specific objects or situations")
    social_anxiety: bool = Field(False, description="Anxiety in social situations")
    agoraphobia: bool = Field(False, description="Fear of being in situations hard to escape from")
    physical_tension: bool = Field(False, description="Muscle tension, headaches, or physical symptoms from anxiety")
    sleep_anxiety: bool = Field(False, description="Difficulty sleeping due to anxiety")
    avoidance_behaviors: bool = Field(False, description="Avoiding situations that trigger anxiety")
    obsessions: bool = Field(False, description="Intrusive thoughts or obsessions")
    compulsions: bool = Field(False, description="Repetitive behaviors or rituals")


class CognitiveSymptoms(BaseModel):
    """Cognitive and concentration difficulties."""
    poor_concentration: bool = Field(False, description="Difficulty concentrating or paying attention")
    indecisiveness: bool = Field(False, description="Indecisiveness or difficulty making decisions")
    memory_problems: bool = Field(False, description="Memory problems or forgetfulness")
    racing_thoughts: bool = Field(False, description="Racing or accelerated thoughts")
    slow_thinking: bool = Field(False, description="Slow thinking or mental processing")
    negative_self_talk: bool = Field(False, description="Persistent negative self-criticism")
    cognitive_rigidity: bool = Field(False, description="Difficulty changing thinking patterns")


class PhysicalSymptoms(BaseModel):
    """Physical manifestations of mental health conditions."""
    sleep_disturbance: bool = Field(False, description="Insomnia, hypersomnia, or irregular sleep")
    appetite_change: bool = Field(False, description="Significant change in appetite or weight")
    fatigue: bool = Field(False, description="Persistent fatigue or low energy")
    psychomotor_retardation: bool = Field(False, description="Slowed movements or speech")
    psychomotor_agitation: bool = Field(False, description="Restlessness or excessive activity")
    physical_pain: bool = Field(False, description="Unexplained body pain or somatic symptoms")
    gastrointestinal_symptoms: bool = Field(False, description="Nausea, stomach pain, or digestive issues")


class TraumaSymptoms(BaseModel):
    """Trauma and PTSD-related symptoms."""
    intrusive_memories: bool = Field(False, description="Unwanted traumatic memories or flashbacks")
    nightmares: bool = Field(False, description="Nightmares related to trauma")
    hypervigilance: bool = Field(False, description="Being constantly on alert or startled easily")
    emotional_numbness: bool = Field(False, description="Emotional numbness or detachment")
    avoidance: bool = Field(False, description="Avoiding reminders of trauma")
    blame_self: bool = Field(False, description="Self-blame about the traumatic event")
    negative_beliefs: bool = Field(False, description="Negative beliefs about self or world")


class PsychoticSymptoms(BaseModel):
    """Psychotic features."""
    hallucinations: bool = Field(False, description="Seeing, hearing, or sensing things others don't")
    delusions: bool = Field(False, description="Fixed false beliefs not based on reality")
    disorganized_speech: bool = Field(False, description="Disorganized or incoherent speech")
    disorganized_behavior: bool = Field(False, description="Disorganized behavior or catatonia")
    thought_insertion: bool = Field(False, description="Feeling thoughts are being inserted into mind")
    thought_broadcasting: bool = Field(False, description="Belief that others can hear your thoughts")
    paranoia: bool = Field(False, description="Paranoid or persecutory beliefs")


class SubstanceUseIndicators(BaseModel):
    """Substance use and behavioral patterns."""
    substance_use_frequency: str = Field(description="None, occasional, regular, or daily")
    substances_used: List[str] = Field(default=[], description="Types: alcohol, cannabis, cocaine, opioids, stimulants, hallucinogens, etc.")
    age_of_first_use: Optional[int] = Field(description="Age when substance use started")
    substance_induced_symptoms: bool = Field(description="Symptoms appear only during or after use")
    tolerance_development: bool = Field(description="Need increasing amounts for desired effect")
    withdrawal_symptoms: bool = Field(description="Experiencing withdrawal symptoms")
    failed_reduction_attempts: bool = Field(description="Unsuccessful attempts to cut down use")


# ==================== Risk Assessment ====================

class RiskAssessment(BaseModel):
    """Mental health risk assessment - CRITICAL for patient safety."""
    suicidal_ideation: bool = Field(description="Current thoughts about suicide")
    suicidal_ideation_frequency: Optional[str] = Field(None, description="Passive, active, or persistent")
    suicide_plan_method: Optional[str] = Field(None, description="If yes, what method considered")
    access_to_means: Optional[bool] = Field(None, description="Access to methods (weapons, pills, etc.)")
    previous_suicide_attempts: int = Field(0, ge=0, description="Number of previous attempts")
    self_harm_behavior: bool = Field(description="Non-suicidal self-injury (cutting, burning, etc.)")
    harm_to_others: bool = Field(description="Thoughts about harming others")
    violence_history: bool = Field(description="History of violent behavior")
    substance_abuse_severity: str = Field("none", description="none, mild, moderate, severe")
    homelessness_risk: bool = Field(description="Risk of or currently homeless")
    overall_risk_level: str = Field("low", description="low, moderate, high, or immediate")
    crisis_resources_aware: bool = Field(description="Patient aware of crisis resources")


class MentalHealthHistory(BaseModel):
    """Psychiatric history and background."""
    previous_diagnoses: List[str] = Field(default=[], description="Previous mental health diagnoses")
    age_of_onset: Optional[int] = Field(description="Age when first symptoms appeared")
    previous_treatment: List[str] = Field(default=[], description="Previous therapy types: CBT, DBT, medication, hospitalization, etc.")
    hospitalization_history: int = Field(0, ge=0, description="Number of psychiatric hospitalizations")
    medication_trials: List[str] = Field(default=[], description="Medications previously tried")
    current_medications: List[str] = Field(default=[], description="Current psychiatric medications")
    family_mental_health_history: List[str] = Field(default=[], description="Family members with mental health conditions")
    trauma_history: List[str] = Field(default=[], description="Types of trauma experienced")
    significant_life_events: List[str] = Field(default=[], description="Recent major life stressors")


class SocialFunctioning(BaseModel):
    """Assessment of social and occupational functioning."""
    relationship_quality: str = Field("good", description="good, fair, poor, or isolated")
    social_support_system: str = Field("adequate", description="adequate, limited, or minimal")
    employment_status: str = Field(description="employed, unemployed, student, retired, disabled")
    occupational_functioning: str = Field("functioning", description="functioning well, some difficulty, significant impairment, unable to work")
    family_relationships: str = Field("stable", description="stable, conflicted, or estranged")
    living_situation: str = Field(description="Lives with family, alone, partner, homeless, etc.")


# ==================== Mental Health Condition Profiles ====================

class MentalHealthCondition(BaseModel):
    """DSM-5/ICD-11 mental health condition with diagnostic criteria."""
    condition_name: str = Field(description="Name of condition (e.g., Major Depressive Disorder)")
    diagnostic_code_dsm5: str = Field(description="DSM-5 diagnostic code")
    diagnostic_code_icd11: str = Field(description="ICD-11 diagnostic code")
    condition_type: str = Field(description="Category: mood, anxiety, trauma, psychotic, personality, eating, sleep, ADHD, substance")
    severity: str = Field("mild", description="mild, moderate, severe, or very severe")
    duration: str = Field(description="Duration of symptoms (weeks, months, years)")
    diagnostic_criteria_met: List[str] = Field(description="Specific DSM-5/ICD-11 criteria met")
    differential_diagnoses: List[str] = Field(default=[], description="Other conditions to rule out")
    confidence_level: str = Field("moderate", description="low, moderate, high - clinician confidence")


class TreatmentRecommendation(BaseModel):
    """Evidence-based treatment recommendations."""
    psychotherapy_types: List[str] = Field(description="CBT, DBT, psychodynamic, ACT, etc.")
    medication_class_considerations: List[str] = Field(description="SSRI, SNRI, antipsychotic, mood stabilizer, etc.")
    lifestyle_interventions: List[str] = Field(default=[], description="Exercise, sleep hygiene, meditation, etc.")
    referral_type: Optional[str] = Field(None, description="Psychiatry, psychology, crisis intervention, hospitalization, etc.")
    urgency_of_care: str = Field("routine", description="routine, urgent, emergency")
    emergency_contact_needed: bool = Field(description="Requires immediate intervention")


# ==================== Mental Health Assessment Report ====================

class MentalHealthAssessment(BaseModel):
    """Comprehensive mental health assessment report."""
    assessment_date: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Date of assessment")
    session_id: str = Field(description="Unique session identifier")

    # Demographics
    patient_name: str = Field(description="Patient name")
    age: int = Field(ge=13, le=120, description="Patient age")
    gender: str = Field(description="Gender identity")

    # Presenting problem
    chief_complaint: str = Field(description="Main reason for seeking help")
    complaint_duration: str = Field(description="How long symptoms have been present")
    complaint_onset: str = Field(description="Sudden or gradual onset")

    # Assessment tools
    phq9_assessment: PHQ9Assessment = Field(description="PHQ-9 depression screening")
    gad7_assessment: GAD7Assessment = Field(description="GAD-7 anxiety screening")

    # Symptom presentation
    mood_symptoms: MoodSymptoms = Field(description="Mood-related symptoms")
    anxiety_symptoms: AnxietySymptoms = Field(description="Anxiety-related symptoms")
    cognitive_symptoms: CognitiveSymptoms = Field(description="Cognitive difficulties")
    physical_symptoms: PhysicalSymptoms = Field(description="Physical manifestations")
    trauma_symptoms: TraumaSymptoms = Field(description="Trauma-related symptoms")
    psychotic_symptoms: PsychoticSymptoms = Field(description="Psychotic features if present")
    substance_use: SubstanceUseIndicators = Field(description="Substance use patterns")

    # History
    mental_health_history: MentalHealthHistory = Field(description="Psychiatric background")
    social_functioning: SocialFunctioning = Field(description="Social and occupational functioning")

    # Risk assessment (CRITICAL)
    risk_assessment: RiskAssessment = Field(description="Risk assessment for self-harm and violence")

    # Clinical impression
    primary_diagnosis: MentalHealthCondition = Field(description="Primary mental health condition")
    secondary_diagnoses: List[MentalHealthCondition] = Field(default=[], description="Additional diagnoses if present")

    # Treatment
    treatment_recommendations: TreatmentRecommendation = Field(description="Recommended treatment approach")

    # Clinical notes
    clinical_summary: str = Field(description="Clinician's summary and observations")
    clinical_notes: str = Field(description="Additional clinical notes or concerns")
