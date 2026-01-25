from typing import List, Dict, Optional



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
