from pydantic import BaseModel, Field
from typing import Optional, Any

class ModelOutput(BaseModel):
    data: Optional[Any] = None
    markdown: Optional[str] = None
    metadata: Optional[dict] = Field(default_factory=dict)
