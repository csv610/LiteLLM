from lite import ModelOutput


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
