from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class ModelOutput(BaseModel):
    """
    Standardized artifact envelope for all multi-agentic and LLM outputs.
    """
    # Tier 1: Core Facts/Extraction (Machine-readable)
    data: Optional[Any] = Field(default=None, description="Structured domain-specific data (JSON/Pydantic)")
    
    # Tier 3: Final Synthesis (Human-readable)
    markdown: Optional[str] = Field(default=None, description="Final human-ready report in Markdown format")
    
    # Tier 2: Process Artifacts (Traceability/Audit/Reasoning)
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict, 
        description="Internal process data like safety audits, agent debates, or reasoning chains"
    )
