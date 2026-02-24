from pydantic import BaseModel, Field
from typing import List, Optional

class MediaCaptionModel(BaseModel):
    """AI generated caption for medical media."""
    title: str = Field(description="Short descriptive title for the media")
    caption: str = Field(description="Comprehensive medical caption describing the media")
    key_entities: List[str] = Field(description="Key medical entities visible or discussed (anatomy, pathology, tools)")
    clinical_context: str = Field(description="Typical clinical context where this media would be relevant")

class MediaSummaryModel(BaseModel):
    """AI generated summary for medical media or topic."""
    topic: str = Field(description="The main medical topic of the media")
    summary: str = Field(description="A concise summary of the key information presented")
    clinical_significance: str = Field(description="The medical or clinical importance of the topic")
    target_audience: str = Field(description="Recommended audience (Student, Resident, Specialist, Patient)")

class MedicalMediaModel(BaseModel):
    """Combined media analysis model."""
    caption: Optional[MediaCaptionModel] = None
    summary: Optional[MediaSummaryModel] = None

class ModelOutput(BaseModel):
    data: Optional[MedicalMediaModel] = None
    markdown: Optional[str] = None
