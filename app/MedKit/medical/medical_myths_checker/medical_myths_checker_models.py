from pydantic import BaseModel, Field

class MythAnalysis(BaseModel):
    statement: str = Field(..., description="The medical myth or claim being analyzed.")
    status: str = Field(..., description="Whether the statement is 'TRUE', 'FALSE', or 'UNCERTAIN'. Must be one of these values.")
    explanation: str = Field(..., description="Detailed, medically accurate explanation of why the statement is true, false, or uncertain, backed by evidence-based medicine.")
    peer_reviewed_sources: str = Field(..., description="REQUIRED: Specific peer-reviewed journals, papers, or medical organizations that support or refute the claim. Include journal names and publication years. If no peer-reviewed evidence exists, state 'No peer-reviewed evidence found' and explain what research gaps exist.")
    risk_level: str = Field(default="LOW", description="Health risk level if the myth is believed: 'LOW', 'MODERATE', or 'HIGH'.")


class MythAnalysisResponse(BaseModel):
    myths: list[MythAnalysis]
