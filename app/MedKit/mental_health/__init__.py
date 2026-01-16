"""
Mental Health Assessment and Support modules.

Comprehensive mental health assessment tools, chatbots, and interview systems with crisis detection.
"""

# Import models first (no external dependencies)
from .models import ChatSession, ChatMessage, PrivacyConsent, AuditLog

# Import other modules
from .mental_health_assessment import MentalHealthAssessment
from .sane_interview import SANEInterviewChatbot

__all__ = [
    "MentalHealthAssessment",
    "SANEInterviewChatbot",
    "ChatSession",
    "ChatMessage",
    "PrivacyConsent",
    "AuditLog",
]

# Lazy imports for modules with external dependencies
def __getattr__(name):
    if name == "MentalHealthChatEngine":
        from .mental_health_chat import MentalHealthChatEngine
        return MentalHealthChatEngine
    elif name == "MentalHealthReportGenerator":
        from .mental_health_report import MentalHealthReportGenerator
        return MentalHealthReportGenerator
    elif name == "MentalHealthChatApp":
        from .mental_health_chat_app import MentalHealthChatApp
        return MentalHealthChatApp
    elif name == "MedicalConsultation":
        from .sympton_detection_chat import MedicalConsultation
        return MedicalConsultation
    elif name == "LLMAssistedSANEChatbot":
        from .llm_sane_interview import LLMAssistedSANEChatbot
        return LLMAssistedSANEChatbot
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
