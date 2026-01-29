from pydantic import BaseModel, Field
from typing import List, Optional

class Disease(BaseModel):
    """Disease or medical condition."""
    name: str = Field(description="Name of the disease or condition")
    context: str = Field(description="Context where it was mentioned in the text")


class Medicine(BaseModel):
    """Medicine, drug, or pharmaceutical."""
    name: str = Field(description="Name of the medicine or drug")
    context: str = Field(description="Context where it was mentioned in the text")


class Symptom(BaseModel):
    """Symptom or clinical sign."""
    name: str = Field(description="Name of the symptom or sign")
    context: str = Field(description="Context where it was mentioned in the text")


class Treatment(BaseModel):
    """Treatment or therapeutic procedure."""
    name: str = Field(description="Name of the treatment or procedure")
    context: str = Field(description="Context where it was mentioned in the text")


class Procedure(BaseModel):
    """Medical procedure or test."""
    name: str = Field(description="Name of the procedure or test")
    context: str = Field(description="Context where it was mentioned in the text")


class Specialty(BaseModel):
    """Medical specialty or field."""
    name: str = Field(description="Name of the medical specialty")
    context: str = Field(description="Context where it was mentioned in the text")


class AnatomicalTerm(BaseModel):
    """Anatomical structure or body part."""
    name: str = Field(description="Name of the anatomical structure")
    context: str = Field(description="Context where it was mentioned in the text")


class SideEffect(BaseModel):
    """Side effect or adverse reaction."""
    name: str = Field(description="Name of the side effect")
    related_medicine: Optional[str] = Field(
        description="Medicine or treatment that may cause this side effect",
        default=None
    )
    context: str = Field(description="Context where it was mentioned in the text")


class CausationRelationship(BaseModel):
    """Causation relationship between medical concepts."""
    cause: str = Field(description="The cause (disease, condition, or factor)")
    effect: str = Field(description="The effect or consequence")
    relationship_type: str = Field(
        description="Type of relationship (causes, leads_to, triggers, results_in, etc.)"
    )
    context: str = Field(description="Context where this relationship was mentioned")


class MedicalTermsModel(BaseModel):
    """
    Comprehensive extraction of medical terms from text.
    """
    diseases: List[Disease] = Field(default_factory=list, description="Diseases and conditions found")
    medicines: List[Medicine] = Field(default_factory=list, description="Medicines and drugs found")
    symptoms: List[Symptom] = Field(default_factory=list, description="Symptoms and signs found")
    treatments: List[Treatment] = Field(default_factory=list, description="Treatments found")
    procedures: List[Procedure] = Field(default_factory=list, description="Procedures and tests found")
    specialties: List[Specialty] = Field(default_factory=list, description="Medical specialties found")
    anatomical_terms: List[AnatomicalTerm] = Field(default_factory=list, description="Anatomical structures found")
    side_effects: List[SideEffect] = Field(default_factory=list, description="Side effects and adverse reactions found")
    causation_relationships: List[CausationRelationship] = Field(
        default_factory=list,
        description="Causation relationships between medical concepts"
    )


class ModelOutput(BaseModel):
    data: Optional[MedicalTermsModel] = None
    markdown: Optional[str] = None


