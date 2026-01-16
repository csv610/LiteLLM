"""mental_health_assessment - Red flag detection and chat session management.

This module provides red flag detection utilities and integrates with Pydantic
data models for mental health assessment. The core data models are defined in
mental_health_assessment_models.py.

Also includes chat session models for conversation management and privacy/consent tracking.

QUICK START:
    from mental_health_assessment_models import (
        MentalHealthAssessment, PHQ9Assessment, GAD7Assessment
    )

    # Create a PHQ-9 depression assessment
    phq9 = PHQ9Assessment(
        depressed_mood=2,
        sleep_disturbance=2,
        fatigue=3,
        appetite_change=1,
        guilt_shame=2,
        concentration=2,
        psychomotor=1,
        suicidal_ideation=0,
        functional_impairment=2
    )
    print(f"PHQ-9 Score: {phq9.total_score}/27")
    print(f"Severity: {phq9.severity}")

    # Create a chat session
    from mental_health_assessment import ChatSession, ChatMessage
    session = ChatSession(
        session_id="sess_123",
        patient_name="Jane Doe",
        age=28,
        gender="F",
        consent_obtained=True,
        hipaa_acknowledged=True
    )

COMMON USES:
    1. Detecting mental health emergency keywords and red flags
    2. Managing chat sessions with assessment linkage
    3. Working with comprehensive mental health assessment data
    4. Tracking privacy consent and HIPAA compliance

KEY CONCEPTS:
    - Red Flag Detection: Emergency categorization system with keywords and severity levels
      for mental health crises (suicidal ideation, self-harm, psychosis, etc.)
    - Chat Sessions: Complete conversation tracking with message history, red flag
      detection, assessment linkage, and session status management
    - Assessment Models: Located in mental_health_assessment_models.py with PHQ-9, GAD-7,
      symptom categories, risk assessment, and clinical diagnostic information
    - Privacy Compliance: PrivacyConsent and AuditLog models for HIPAA compliance
      and data access tracking
"""

from typing import List, Dict, Optional
from .mental_health_assessment_models import (
    PHQ9Assessment,
    GAD7Assessment,
    MoodSymptoms,
    AnxietySymptoms,
    CognitiveSymptoms,
    PhysicalSymptoms,
    TraumaSymptoms,
    PsychoticSymptoms,
    SubstanceUseIndicators,
    RiskAssessment,
    MentalHealthHistory,
    SocialFunctioning,
    MentalHealthCondition,
    TreatmentRecommendation,
    MentalHealthAssessment,
)

try:
    from .models import ChatMessage, ChatSession, PrivacyConsent, AuditLog
except ImportError:
    try:
        from medkit.mental_health.models import ChatMessage, ChatSession, PrivacyConsent, AuditLog
    except ImportError:
        from models import ChatMessage, ChatSession, PrivacyConsent, AuditLog

# ==================== Red Flag Detection ====================

class RedFlagCategory:
    """Mental health emergency categories."""

    MENTAL_HEALTH_RED_FLAGS = {
        "suicidal_ideation": {
            "keywords": ["suicide", "kill myself", "don't want to live", "better off dead", "harm myself",
                        "end my life", "take my own life", "goodbye cruel world", "final goodbye"],
            "severity": "emergency",
            "recommendation": "Immediate suicide risk assessment, crisis line, emergency services"
        },
        "active_self_harm": {
            "keywords": ["cutting myself", "burning myself", "hurting myself", "self injury", "harming",
                        "starving", "binge eating", "pulling hair out"],
            "severity": "emergency",
            "recommendation": "Assess frequency and severity, crisis intervention, emergency department"
        },
        "psychotic_symptoms": {
            "keywords": ["hearing voices", "seeing things", "aliens", "government tracking", "conspiracy",
                        "mind reading", "thoughts not mine", "hallucinations"],
            "severity": "urgent",
            "recommendation": "Psychiatric evaluation, possible hospitalization, antipsychotic medication"
        },
        "harm_to_others": {
            "keywords": ["hurt someone", "attack", "violent thoughts", "harm others", "kill",
                        "going to hit", "planning to hurt"],
            "severity": "emergency",
            "recommendation": "Safety assessment, potential hospitalization, mandatory reporting"
        },
        "acute_panic": {
            "keywords": ["can't breathe", "chest pain anxiety", "dying", "losing control", "panic attack",
                        "overwhelming anxiety"],
            "severity": "urgent",
            "recommendation": "Breathing exercises, anxiety management, medical evaluation to rule out cardiac issues"
        },
        "severe_depression": {
            "keywords": ["hopeless", "nothing matters", "pointless", "give up", "no point in living",
                        "never get better"],
            "severity": "urgent",
            "recommendation": "Suicide risk assessment, antidepressant medication, intensive therapy"
        },
        "acute_trauma": {
            "keywords": ["just happened", "attack", "assault", "rape", "accident just now", "traumatic event"],
            "severity": "urgent",
            "recommendation": "Crisis support, trauma-informed care, reporting assistance if needed"
        }
    }
