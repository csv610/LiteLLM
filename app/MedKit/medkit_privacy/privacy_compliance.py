"""Privacy and HIPAA Compliance Manager - Comprehensive healthcare data protection and compliance.

Manages HIPAA-compliant mental health data handling including user consent, audit logging,
data retention policies, right-to-deletion requests, secure session storage, and PII masking.
Handles Protected Health Information (PHI) with strict security and compliance controls.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from uuid import uuid4

# Import modular components - Now exclusively LLM-based for PII
try:
    from .pii_utils import PIIDetector, PIIMasker
    from .audit_logger import AuditLogger
    from .session_repository import SessionRepository
except (ImportError, ValueError):
    from pii_utils import PIIDetector, PIIMasker
    from audit_logger import AuditLogger
    from session_repository import SessionRepository

# Use relative imports for models
try:
    from ..mental_health.models import ChatSession
except (ImportError, ModuleNotFoundError):
    from pydantic import BaseModel

    class ChatSession(BaseModel):
        """Fallback chat session model."""

        session_id: str
        user_id: str
        patient_name: str
        age: int
        gender: str
        consent_obtained: bool = False
        hipaa_acknowledged: bool = False
        messages: list = []
        assessment_data: Optional[Dict] = None
        session_status: str = "active"
        emergency_triggered: bool = False

    class PrivacyConfig:
        """Local privacy configuration."""

        retention_days_session = 365
        retention_days_audit = 2555

# ==================== Privacy Manager ====================


class PrivacyManager:
    """Manages HIPAA-compliant mental health data handling by coordinating modular services."""

    def __init__(self, data_dir: Optional[str] = None):
        """Initialize privacy manager with LLM-based PII detection and secure storage."""
        self.data_dir = (
            Path(data_dir) if data_dir else Path.home() / ".medkit" / "sessions"
        )
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Initialize modular sub-services
        self.detector = PIIDetector()
        self.masker = PIIMasker(self.detector)
        self.audit_logger = AuditLogger(self.data_dir)
        self.repository = SessionRepository(self.data_dir)

    def create_session(self, patient_name: str, age: int, gender: str) -> ChatSession:
        """Create a new chat session."""
        session_id = str(uuid4())
        patient_id = str(uuid4())

        return ChatSession(
            session_id=session_id,
            patient_id=patient_id,
            patient_name=patient_name,
            age=age,
            gender=gender,
            consent_obtained=False,
            hipaa_acknowledged=False,
            messages=[],
            assessment_data=None,
            session_status="active",
            emergency_triggered=False,
        )

    def save_session(self, session: ChatSession) -> Optional[Path]:
        """Delegate session saving to repository."""
        return self.repository.save_session(session)

    def load_session(self, session_id: str) -> Optional[ChatSession]:
        """Delegate session loading to repository."""
        return self.repository.load_session(session_id)

    def display_consent_form(self) -> bool:
        """Display HIPAA consent form."""
        print("\n" + "=" * 80)
        print("HIPAA PRIVACY NOTICE & CONSENT".center(80))
        print("=" * 80 + "\n")

        print("""
Your mental health information is PRIVATE AND PROTECTED.

By using this service, you acknowledge:
1. THIS IS NOT A SUBSTITUTE FOR PROFESSIONAL CARE
2. DATA PRIVACY - Protected under HIPAA
3. DATA RETENTION - Sessions for 1 yr, Audit for 7 yrs
4. SECURITY - Restricted access with full auditing
        """)

        response = input("\nDo you consent to these terms? (yes/no): ").strip().lower()
        return response in ["yes", "y"]

    def log_audit_event(
        self,
        session_id: str,
        action: str,
        user_role: str = "patient",
        details: Optional[str] = None,
    ) -> None:
        """Delegate audit logging to audit logger."""
        self.audit_logger.log(session_id, action, user_role, details)

    def generate_compliance_report(self) -> Dict:
        """Generate HIPAA compliance report by aggregating sub-service reports."""
        audit_summary = self.audit_logger.get_report_summary()
        session_count = (
            len(self.repository.list_sessions()) - 1
        )  # -1 for audit log file

        report = {
            "report_date": datetime.now().isoformat(),
            "sessions_count": max(0, session_count),
            "data_retention_policy": "365 days sessions, 7 years audit",
            "encryption_status": "enabled (restricted file-level access)",
            **audit_summary,
        }
        return report

    def mask_pii(self, text: str) -> str:
        """Delegate PII masking to masker (LLM-based)."""
        return self.masker.mask(text)

    def detect_pii(self, text: str) -> list:
        """Detect PII occurrences using LLM."""
        return self.detector.detect(text)
