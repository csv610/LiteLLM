from pydantic import BaseModel, Field


class ChunkSummary(BaseModel):
    """Structured summary of a single text chunk from LLM."""

    summary: str = Field(
        description="A concise summary of the text chunk, focusing on key medical facts"
    )


class FinalSummary(BaseModel):
    """Structured combined summary of the entire article from LLM."""

    summary: str = Field(
        description="A comprehensive summary of the entire article, synthesized from chunk summaries"
    )


class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)
