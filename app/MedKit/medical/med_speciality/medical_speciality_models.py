from pydantic import BaseModel, Field
from typing import List, Optional

class SpecialtyCategory(BaseModel):
    """
    Medical specialty category for organizing related specialties.
    """
    name: str = Field(..., description="Name of the category (e.g., 'Cardiovascular', 'Neurological', 'Digestive')")
    description: str = Field(..., description="Brief description of what this category encompasses")


class Subspecialty(BaseModel):
    """
    Subspecialty within a medical specialty field.
    """
    name: str = Field(..., description="Name of the subspecialty")
    description: str = Field(..., description="Brief description of what the subspecialty focuses on")


class MedicalSpecialist(BaseModel):
    """
    Complete information about a medical specialist and their field.
    """
    specialty_name: str = Field(..., description="Official name of the medical specialty")
    category: SpecialtyCategory = Field(..., description="Category this specialty belongs to")
    description: str = Field(..., description="Detailed description of what this specialist does")
    treats: List[str] = Field(..., description="List of conditions, diseases, or body systems treated")
    common_referral_reasons: List[str] = Field(..., description="Common reasons patients see this specialist")
    subspecialties: Optional[List[Subspecialty]] = Field(default=None, description="Subspecialties within this field")
    is_surgical: bool = Field(default=False, description="Whether this is primarily a surgical specialty")
    patient_population: Optional[str] = Field(default=None, description="Specific patient population if applicable (e.g., 'children', 'elderly', 'women')")


class MedicalSpecialistDatabase(BaseModel):
    """
    Complete database of medical specialists with query methods.
    """
    specialists: List[MedicalSpecialist] = Field(
        ...,
        description="Comprehensive list of all medical specialists including primary care, surgical, diagnostic, and subspecialty fields"
    )

    def get_by_category(self, category_name: str) -> List[MedicalSpecialist]:
        """
        Get all specialists in a specific category.
        """
        return [s for s in self.specialists if s.category.name.lower() == category_name.lower()]

    def get_all_categories(self) -> List[SpecialtyCategory]:
        """
        Get all unique specialty categories in the database.
        """
        seen = {}
        for s in self.specialists:
            if s.category.name not in seen:
                seen[s.category.name] = s.category
        return list(seen.values())

    def get_surgical_specialists(self) -> List[MedicalSpecialist]:
        """
        Get all surgical specialists in the database.
        """
        return [s for s in self.specialists if s.is_surgical]

    def search_by_condition(self, condition: str) -> List[MedicalSpecialist]:
        """
        Search for specialists who treat a specific condition.
        """
        condition_lower = condition.lower()
        return [s for s in self.specialists
                if any(condition_lower in treat.lower() for treat in s.treats)]
