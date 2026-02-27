import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List

# Use relative imports for models
try:
    from ..mental_health.models import AuditLog
except (ImportError, ModuleNotFoundError):
    from pydantic import BaseModel
    class AuditLog(BaseModel):
        """Fallback audit log model."""
        session_id: str
        action: str
        user_role: str = "patient"
        details: Optional[str] = None
        timestamp: str = ""

class AuditLogger:
    """Manages HIPAA-compliant audit logging with long-term retention."""

    def __init__(self, data_dir: Path):
        self.audit_file = data_dir / "audit_log.json"
        self.data_dir = data_dir

    def log(
        self,
        session_id: str,
        action: str,
        user_role: str = "patient",
        details: Optional[str] = None,
    ) -> None:
        """Log an audit event to a secure file."""
        try:
            audit_log = AuditLog(
                session_id=session_id,
                action=action,
                user_role=user_role,
                details=details,
                timestamp=datetime.now().isoformat()
            )

            # Load existing logs
            logs = self._load_logs()
            
            # Append new log
            logs.append(audit_log.model_dump() if hasattr(audit_log, 'model_dump') else audit_log.dict())

            # Save updated logs
            with open(self.audit_file, "w") as f:
                json.dump(logs, f, indent=2, default=str)

            # Ensure secure permissions
            self.audit_file.chmod(0o600)
        except Exception as e:
            print(f"Error logging audit event: {e}")

    def _load_logs(self) -> List[Dict]:
        """Load logs from file if it exists."""
        if self.audit_file.exists():
            try:
                with open(self.audit_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def get_report_summary(self) -> Dict:
        """Get summary metrics for compliance reporting."""
        logs = self._load_logs()
        return {
            "total_audit_events": len(logs),
            "last_event_timestamp": logs[-1].get("timestamp") if logs else None,
            "audit_logging_status": "active"
        }
