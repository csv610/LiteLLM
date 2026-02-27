import json
from pathlib import Path
from typing import Optional, List, Dict

# Use relative imports for models
try:
    from ..mental_health.models import ChatSession
    from lite.utils import save_model_response
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
        messages: List = []
        assessment_data: Optional[Dict] = None
        session_status: str = "active"
        emergency_triggered: bool = False

    def save_model_response(model, file_path):
        """Fallback save_model_response."""
        with open(file_path, "w") as f:
            f.write(model.model_dump_json(indent=2))


class SessionRepository:
    """Manages secure session storage and file-level security."""

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.chmod(0o700)

    def save_session(self, session: ChatSession) -> Optional[Path]:
        """Save session to file with secure permissions."""
        try:
            session_file = self.data_dir / f"{session.session_id}.json"

            # Save using utility or standard json
            if "save_model_response" in globals():
                save_model_response(session, session_file)
            else:
                with open(session_file, "w") as f:
                    json.dump(
                        session.model_dump()
                        if hasattr(session, "model_dump")
                        else session.dict(),
                        f,
                        indent=2,
                        default=str,
                    )

            # Set secure permissions
            session_file.chmod(0o600)
            return session_file
        except Exception as e:
            print(f"Error saving session: {e}")
            return None

    def load_session(self, session_id: str) -> Optional[ChatSession]:
        """Load session from file."""
        try:
            session_file = self.data_dir / f"{session_id}.json"
            if not session_file.exists():
                return None

            with open(session_file, "r") as f:
                data = json.load(f)

            return ChatSession(**data)
        except Exception as e:
            print(f"Error loading session: {e}")
            return None

    def list_sessions(self) -> List[Path]:
        """List all session files."""
        return list(self.data_dir.glob("*.json"))

    def delete_session(self, session_id: str) -> bool:
        """Delete session file."""
        try:
            session_file = self.data_dir / f"{session_id}.json"
            if session_file.exists():
                session_file.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False
