from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field



class ChatMessage(BaseModel):
    """Individual chat message in consultation."""
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    role: str = Field(description="'user' or 'assistant'")
    content: str = Field(description="Message content")
    red_flags_detected: List[str] = Field(default=[], description="Any red flags detected in message")


class ChatSession(BaseModel):
    """Mental health chat session with history."""
    session_id: str = Field(description="Unique session identifier")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    # User info
    patient_id: str = Field(description="Unique patient identifier")
    patient_name: str = Field(description="Patient name")
    age: int = Field(description="Patient age")
    gender: str = Field(description="Patient gender")

    # Consent and privacy
    consent_obtained: bool = Field(description="User gave informed consent")
    hipaa_acknowledged: bool = Field(description="User acknowledged privacy practices")

    # Chat history
    messages: List[ChatMessage] = Field(default=[], description="All messages in session")

    # Assessment data
    assessment_data: Optional["MentalHealthAssessment"] = Field(None, description="Final assessment from session")

    # Status
    session_status: str = Field("active", description="active, completed, emergency, or terminated")
    emergency_triggered: bool = Field(False, description="Emergency protocols activated")


class PrivacyConsent(BaseModel):
    """User consent for data collection and processing."""
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    user_name: str = Field(description="Name of person providing consent")
    consent_version: str = Field(description="Version of consent document")
    terms_accepted: bool = Field(description="Accepted terms of service")
    privacy_policy_accepted: bool = Field(description="Accepted privacy policy")
    data_retention_understood: bool = Field(description="Understood data retention practices")
    hipaa_notice_acknowledged: bool = Field(description="Acknowledged HIPAA notice of privacy practices")
    data_sharing_consent: bool = Field(description="Consent to share data with healthcare providers if needed")
    research_consent: bool = Field(False, description="Consent to anonymized research use")


class AuditLog(BaseModel):
    """Audit log entry for HIPAA compliance."""
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    session_id: str = Field(description="Session ID")
    action: str = Field(description="Action performed: data_access, data_modification, data_deletion, assessment_created, report_generated")
    user_role: str = Field(description="Role of user: patient, clinician, admin")
    details: Optional[str] = Field(None, description="Additional details about the action")
