from typing import Dict, Type
from .base_recognizer import BaseRecognizer
from lite.config import ModelConfig

class RecognizerFactory:
    """Factory for creating medical entity recognizers."""
    
    _registry: Dict[str, Type[BaseRecognizer]] = {}

    @classmethod
    def register(cls, name: str, recognizer_class: Type[BaseRecognizer]):
        """Register a new recognizer class."""
        cls._registry[name.lower()] = recognizer_class

    @classmethod
    def get(cls, name: str, model_config: ModelConfig) -> BaseRecognizer:
        """
        Get an instance of a registered recognizer.
        
        Args:
            name: The registered name of the recognizer (e.g., 'drug', 'disease').
            model_config: Configuration to initialize the recognizer with.
            
        Returns:
            An instance of the requested recognizer.
        """
        # Ensure all are registered - this is a simple way for now
        # Ideally this would be done via dynamic discovery or in __init__.py
        if not cls._registry:
            cls._initialize_registry()

        recognizer_class = cls._registry.get(name.lower())
        if not recognizer_class:
            raise ValueError(f"No recognizer registered with name: {name}. "
                             f"Available: {list(cls._registry.keys())}")
        return recognizer_class(model_config)

    @classmethod
    def _initialize_registry(cls):
        """Initialize the registry with all available recognizers."""
        from .drug.drug_recognizer import DrugIdentifier
        from .disease.disease_recognizer import DiseaseIdentifier
        from .medical_condition.medical_condition_identifier import MedicalConditionIdentifier
        from .clinical_sign.clinical_sign_recognizer import ClinicalSignIdentifier
        from .medical_procedure.medical_procedure_identifier import MedicalProcedureIdentifier
        from .medication_class.medication_class_recognizer import MedicationClassIdentifier
        from .imaging_finding.imaging_finding_recognizer import ImagingFindingIdentifier
        from .medical_vaccine.medical_vaccine_identifier import MedicalVaccineIdentifier
        from .genetic_variant.genetic_variant_recognizer import GeneticVariantIdentifier
        from .medical_supplement.medical_supplement_identifier import MedicalSupplementIdentifier
        from .medical_test.medical_test_identifier import MedicalTestIdentifier
        from .medical_coding.medical_coding_recognizer import MedicalCodingIdentifier
        from .medical_device.medical_device_identifier import MedicalDeviceIdentifier
        from .medical_pathogen.medical_pathogen_identifier import MedicalPathogenIdentifier
        from .medical_anatomy.medical_anatomy_identifier import MedicalAnatomyIdentifier
        from .med_abbreviation.medical_abbreviation_recognizer import MedicalAbbreviationIdentifier
        from .lab_unit.lab_unit_recognizer import LabUnitIdentifier
        from .medical_symptom.medical_symptom_identifier import MedicalSymptomIdentifier
        from .medical_specialty.medical_specialty_identifier import MedicalSpecialtyIdentifier

        cls.register("drug", DrugIdentifier)
        cls.register("disease", DiseaseIdentifier)
        cls.register("condition", MedicalConditionIdentifier)
        cls.register("clinical_sign", ClinicalSignIdentifier)
        cls.register("procedure", MedicalProcedureIdentifier)
        cls.register("med_class", MedicationClassIdentifier)
        cls.register("imaging", ImagingFindingIdentifier)
        cls.register("vaccine", MedicalVaccineIdentifier)
        cls.register("genetic", GeneticVariantIdentifier)
        cls.register("supplement", MedicalSupplementIdentifier)
        cls.register("test", MedicalTestIdentifier)
        cls.register("coding", MedicalCodingIdentifier)
        cls.register("device", MedicalDeviceIdentifier)
        cls.register("pathogen", MedicalPathogenIdentifier)
        cls.register("anatomy", MedicalAnatomyIdentifier)
        cls.register("abbreviation", MedicalAbbreviationIdentifier)
        cls.register("lab_unit", LabUnitIdentifier)
        cls.register("symptom", MedicalSymptomIdentifier)
        cls.register("specialty", MedicalSpecialtyIdentifier)

    @classmethod
    def list_available(cls) -> list[str]:
        """List all registered recognizer names."""
        if not cls._registry:
            cls._initialize_registry()
        return list(cls._registry.keys())
