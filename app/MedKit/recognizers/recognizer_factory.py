from typing import Dict, Type

from lite.config import ModelConfig

from .base_recognizer import BaseRecognizer


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
        if not cls._registry:
            cls._initialize_registry()

        recognizer_class = cls._registry.get(name.lower())
        if not recognizer_class:
            raise ValueError(
                f"No recognizer registered with name: {name}. "
                f"Available: {list(cls._registry.keys())}"
            )
        return recognizer_class(model_config)

    @classmethod
    def _initialize_registry(cls):
        """Initialize the registry with all available recognizers."""
        from .clinical_sign.nonagentic.clinical_sign_recognizer import (
            ClinicalSignIdentifier,
        )
        from .disease.nonagentic.disease_recognizer import DiseaseIdentifier
        from .drug.nonagentic.drug_recognizer import DrugIdentifier
        from .genetic_variant.nonagentic.genetic_variant_recognizer import (
            GeneticVariantIdentifier,
        )
        from .imaging_finding.nonagentic.imaging_finding_recognizer import (
            ImagingFindingIdentifier,
        )
        from .lab_unit.nonagentic.lab_unit_recognizer import LabUnitIdentifier
        from .med_abbreviation.nonagentic.med_abbreviation_recognizer import (
            MedicalAbbreviationIdentifier,
        )
        from .med_anatomy.nonagentic.med_anatomy_identifier import (
            MedicalAnatomyIdentifier,
        )
        from .med_coding.nonagentic.med_coding_recognizer import MedicalCodingIdentifier
        from .med_condition.nonagentic.med_condition_identifier import (
            MedicalConditionIdentifier,
        )
        from .med_device.nonagentic.med_device_identifier import MedicalDeviceIdentifier
        from .med_pathogen.nonagentic.med_pathogen_identifier import (
            MedicalPathogenIdentifier,
        )
        from .med_procedure.nonagentic.med_procedure_identifier import (
            MedicalProcedureIdentifier,
        )
        from .med_specialty.nonagentic.med_specialty_identifier import (
            MedicalSpecialtyIdentifier,
        )
        from .med_supplement.nonagentic.med_supplement_identifier import (
            MedicalSupplementIdentifier,
        )
        from .med_symptom.nonagentic.med_symptom_identifier import (
            MedicalSymptomIdentifier,
        )
        from .med_test.nonagentic.med_test_identifier import MedicalTestIdentifier
        from .med_vaccine.nonagentic.med_vaccine_identifier import (
            MedicalVaccineIdentifier,
        )
        from .medication_class.nonagentic.medication_class_recognizer import (
            MedicationClassIdentifier,
        )

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
