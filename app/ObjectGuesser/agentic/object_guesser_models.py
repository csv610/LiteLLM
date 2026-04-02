from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class GameState(BaseModel):
    action: str = Field(..., description="Next action for the game, such as ASK_QUESTION or MAKE_GUESS.")
    content: str = Field(..., description="Question or guess content associated with the action.")


class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)


__all__ = ["GameState", "ModelOutput"]
