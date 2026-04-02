#!/usr/bin/env python3
"""
Unified Smoke Test Suite for Medical Entity Recognizers.

This module provides comprehensive smoke tests for all medical entity recognizers.
Run with: python -m pytest tests/test_recognizers_smoke.py -v
Or: python tests/test_recognizers_smoke.py
"""

import sys
import traceback
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Type

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lite.config import ModelConfig

from app.MedKit.recognizers.base_recognizer import BaseRecognizer, ModelOutput
from app.MedKit.recognizers.recognizer_factory import RecognizerFactory


class TestRunner:
    """Test runner for smoke tests."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors: List[str] = []

    def run_test(self, name: str, test_fn: Callable[[], None]) -> bool:
        """Run a single test and track results."""
        try:
            test_fn()
            print(f"  ✓ {name}")
            self.passed += 1
            return True
        except AssertionError as e:
            print(f"  ✗ {name}: {e}")
            self.errors.append(f"{name}: {e}")
            self.failed += 1
            return False
        except Exception as e:
            print(f"  ✗ {name}: {type(e).__name__}: {e}")
            self.errors.append(f"{name}: {type(e).__name__}: {e}")
            self.failed += 1
            return False

    def summary(self) -> None:
        """Print test summary."""
        total = self.passed + self.failed
        print(f"\n{'=' * 60}")
        print(f"TEST SUMMARY: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"FAILED: {self.failed}")
            for error in self.errors:
                print(f"  - {error}")
        print(f"{'=' * 60}")


def test_base_recognizer_abstract():
    """Test that BaseRecognizer cannot be instantiated directly."""
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    try:
        BaseRecognizer(config)
        assert False, "BaseRecognizer should be abstract"
    except TypeError:
        pass  # Expected


def test_factory_registry():
    """Test that factory registry initializes correctly."""
    registry = RecognizerFactory.list_available()
    assert len(registry) > 0, "Registry should not be empty"
    expected = [
        "drug",
        "disease",
        "condition",
        "clinical_sign",
        "procedure",
        "med_class",
        "imaging",
        "vaccine",
        "genetic",
        "supplement",
        "test",
        "coding",
        "device",
        "pathogen",
        "anatomy",
        "abbreviation",
        "lab_unit",
        "symptom",
        "specialty",
    ]
    for name in expected:
        assert name in registry, f"'{name}' should be in registry"


def test_factory_get_recognizer():
    """Test that factory can create recognizers."""
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)

    # Test a few key recognizers
    recognizers_to_test = ["drug", "disease", "anatomy", "vaccine"]

    for name in recognizers_to_test:
        recognizer = RecognizerFactory.get(name, config)
        assert recognizer is not None, f"Recognizer '{name}' should not be None"
        assert isinstance(recognizer, BaseRecognizer), (
            f"Recognizer '{name}' should extend BaseRecognizer"
        )
        assert hasattr(recognizer, "identify"), (
            f"Recognizer '{name}' should have identify method"
        )
        assert callable(getattr(recognizer, "identify")), (
            f"Recognizer '{name}' identify should be callable"
        )


def test_model_config():
    """Test ModelConfig creation."""
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    assert config.model == "ollama/gemma3"
    assert config.temperature == 0.2


def test_drug_models():
    """Test DrugRecognizer model instantiation."""
    from app.MedKit.recognizers.drug.shared.drug_recognizer_model import (
        DrugIdentificationModel,
        DrugIdentifierModel,
        ModelOutput,
    )

    identification = DrugIdentificationModel(
        drug_name="Aspirin",
        is_well_known=True,
        common_uses=["pain", "inflammation"],
        regulatory_status="FDA approved",
        industry_significance="Common NSAID",
    )
    assert identification.drug_name == "Aspirin"

    drug_model = DrugIdentifierModel(
        identification=identification,
        summary="Aspirin is a well-known drug",
        data_available=True,
    )
    assert drug_model.summary == "Aspirin is a well-known drug"

    # Test ModelOutput with metadata
    output = ModelOutput(data=drug_model, metadata={"source": "test"})
    assert output.data is not None
    assert output.metadata == {"source": "test"}


def test_disease_models():
    """Test DiseaseRecognizer model instantiation."""
    from app.MedKit.recognizers.disease.shared.disease_identifier_models import (
        DiseaseIdentificationModel,
        DiseaseIdentifierModel,
        ModelOutput,
    )

    identification = DiseaseIdentificationModel(
        disease_name="Hypertension",
        is_well_known=True,
        common_symptoms=["headache", "dizziness"],
        prevalence="Common",
        medical_significance="Major cardiovascular risk factor",
    )

    disease_model = DiseaseIdentifierModel(
        identification=identification,
        summary="Hypertension is a common cardiovascular condition",
        data_available=True,
    )

    output = ModelOutput(data=disease_model, metadata={"test": True})
    assert output.metadata is not None


def test_anatomy_models():
    """Test MedicalAnatomy model instantiation."""
    from app.MedKit.recognizers.med_anatomy.shared.med_anatomy_identifier_models import (
        MedicalAnatomyIdentificationModel,
        MedicalAnatomyIdentifierModel,
        ModelOutput,
    )

    identification = MedicalAnatomyIdentificationModel(
        structure_name="heart",
        is_well_known=True,
        system="cardiovascular",
        location="thorax",
        clinical_significance="Central circulation pump",
    )

    anatomy_model = MedicalAnatomyIdentifierModel(
        identification=identification,
        summary="The heart is a well-known anatomical structure",
        data_available=True,
    )

    output = ModelOutput(data=anatomy_model)
    assert output.data.identification.structure_name == "heart"


def test_prompt_builders():
    """Test that all prompt builders work correctly."""
    from app.MedKit.recognizers.drug.shared.drug_recognizer_prompts import (
        DrugIdentifierInput,
        PromptBuilder as DrugPromptBuilder,
    )
    from app.MedKit.recognizers.disease.shared.disease_identifier_prompts import (
        DiseaseIdentifierInput,
        PromptBuilder as DiseasePromptBuilder,
    )
    from app.MedKit.recognizers.med_anatomy.shared.med_anatomy_identifier_prompts import (
        MedicalAnatomyIdentifierInput,
        PromptBuilder as AnatomyPromptBuilder,
    )

    # Test Drug prompts
    drug_input = DrugIdentifierInput("Aspirin")
    drug_system = DrugPromptBuilder.create_system_prompt()
    drug_user = DrugPromptBuilder.create_user_prompt(drug_input)
    assert len(drug_system) > 0
    assert "Aspirin" in drug_user

    # Test Disease prompts
    disease_input = DiseaseIdentifierInput("diabetes")
    disease_system = DiseasePromptBuilder.create_system_prompt()
    disease_user = DiseasePromptBuilder.create_user_prompt(disease_input)
    assert len(disease_system) > 0
    assert "diabetes" in disease_user

    # Test Anatomy prompts
    anatomy_input = MedicalAnatomyIdentifierInput("heart")
    anatomy_system = AnatomyPromptBuilder.create_system_prompt()
    anatomy_user = AnatomyPromptBuilder.create_user_prompt(anatomy_input)
    assert len(anatomy_system) > 0
    assert "heart" in anatomy_user


def test_input_validation():
    """Test input validation across recognizers."""
    from app.MedKit.recognizers.drug.shared.drug_recognizer_prompts import (
        DrugIdentifierInput,
    )
    from app.MedKit.recognizers.disease.shared.disease_identifier_prompts import (
        DiseaseIdentifierInput,
    )
    from app.MedKit.recognizers.med_anatomy.shared.med_anatomy_identifier_prompts import (
        MedicalAnatomyIdentifierInput,
    )

    # Test empty input validation
    for InputClass in [
        DrugIdentifierInput,
        DiseaseIdentifierInput,
        MedicalAnatomyIdentifierInput,
    ]:
        try:
            InputClass("")
            assert False, (
                f"{InputClass.__name__} should raise ValueError for empty input"
            )
        except ValueError:
            pass

        try:
            InputClass("   ")
            assert False, (
                f"{InputClass.__name__} should raise ValueError for whitespace input"
            )
        except ValueError:
            pass


def test_specialty_models():
    """Test MedicalSpecialty model instantiation."""
    from app.MedKit.recognizers.med_specialty.shared.med_specialty_models import (
        MedicalSpecialtyIdentificationModel,
        MedicalSpecialtyIdentifierModel,
        ModelOutput,
    )

    identification = MedicalSpecialtyIdentificationModel(
        specialty_name="Cardiology",
        is_well_known=True,
        organs_treated=["heart", "blood vessels"],
        common_procedures=["echocardiogram", "cardiac catheterization"],
        clinical_scope="Heart disease management",
    )

    specialty_model = MedicalSpecialtyIdentifierModel(
        identification=identification,
        summary="Cardiology is a well-known medical specialty",
        data_available=True,
    )

    output = ModelOutput(data=specialty_model, metadata={"category": "test"})
    assert output.metadata["category"] == "test"


def test_symptom_models():
    """Test MedicalSymptom model instantiation."""
    from app.MedKit.recognizers.med_symptom.shared.med_symptom_models import (
        MedicalSymptomIdentificationModel,
        MedicalSymptomIdentifierModel,
        ModelOutput,
    )

    identification = MedicalSymptomIdentificationModel(
        symptom_name="chest pain",
        is_well_known=True,
        associated_conditions=["angina", "myocardial infarction"],
        severity_indicators="Radiation to arm, jaw, sweating",
        clinical_description="Discomfort in chest area",
    )

    symptom_model = MedicalSymptomIdentifierModel(
        identification=identification,
        summary="Chest pain is a significant symptom",
        data_available=True,
    )

    output = ModelOutput(data=symptom_model)
    assert output.data.data_available is True


def test_procedure_models():
    """Test MedicalProcedure model instantiation."""
    from app.MedKit.recognizers.med_procedure.shared.med_procedure_models import (
        MedicalProcedureIdentificationModel,
        MedicalProcedureIdentifierModel,
        ModelOutput,
    )

    identification = MedicalProcedureIdentificationModel(
        procedure_name="appendectomy",
        is_well_known=True,
        procedure_type="surgical",
        indications=["appendicitis"],
        clinical_significance="Emergency surgical procedure",
    )

    procedure_model = MedicalProcedureIdentifierModel(
        identification=identification,
        summary="Appendectomy is a common surgical procedure",
        data_available=True,
    )

    output = ModelOutput(data=procedure_model)
    assert output.data.identification.procedure_name == "appendectomy"


def test_vaccine_models():
    """Test MedicalVaccine model instantiation."""
    from app.MedKit.recognizers.med_vaccine.shared.med_vaccine_models import (
        VaccineIdentificationModel,
        VaccineIdentifierModel,
        ModelOutput,
    )

    identification = VaccineIdentificationModel(
        vaccine_name="MMR",
        is_well_known=True,
        target_diseases=["measles", "mumps", "rubella"],
        vaccine_type="Live-attenuated",
        standard_schedule="Two doses in childhood",
    )

    vaccine_model = VaccineIdentifierModel(
        identification=identification,
        summary="MMR is a standard childhood vaccine",
        data_available=True,
    )

    output = ModelOutput(data=vaccine_model)
    assert output.data is not None


def test_pathogen_models():
    """Test MedicalPathogen model instantiation."""
    from app.MedKit.recognizers.med_pathogen.shared.med_pathogen_models import (
        PathogenIdentificationModel,
        PathogenIdentifierModel,
        ModelOutput,
    )

    identification = PathogenIdentificationModel(
        pathogen_name="Staphylococcus aureus",
        is_well_known=True,
        pathogen_type="bacteria",
        associated_infections=["skin infections", "pneumonia", "sepsis"],
        clinical_significance="Common cause of hospital-acquired infections",
    )

    pathogen_model = PathogenIdentifierModel(
        identification=identification,
        summary="S. aureus is a significant bacterial pathogen",
        data_available=True,
    )

    output = ModelOutput(data=pathogen_model)
    assert output.data.identification.pathogen_type == "bacteria"


def test_clinical_sign_models():
    """Test ClinicalSign model instantiation."""
    from app.MedKit.recognizers.clinical_sign.shared.clinical_sign_models import (
        ClinicalSignIdentificationModel,
        ClinicalSignIdentifierModel,
        ModelOutput,
    )

    identification = ClinicalSignIdentificationModel(
        sign_name="Babinski sign",
        is_well_known=True,
        examination_method="Stroking lateral sole of foot",
        clinical_significance="Indicates upper motor neuron lesion",
    )

    sign_model = ClinicalSignIdentifierModel(
        identification=identification,
        summary="Babinski sign is a classic neurological finding",
        data_available=True,
    )

    output = ModelOutput(data=sign_model)
    assert output.data.identification.sign_name == "Babinski sign"


def run_all_tests():
    """Run all smoke tests."""
    runner = TestRunner()

    print("=" * 60)
    print("MEDICAL ENTITY RECOGNIZERS - SMOKE TEST SUITE")
    print("=" * 60)

    # Core infrastructure tests
    print("\n--- Core Infrastructure ---")
    runner.run_test("BaseRecognizer is abstract", test_base_recognizer_abstract)
    runner.run_test("Factory registry initialization", test_factory_registry)
    runner.run_test("Factory creates recognizers", test_factory_get_recognizer)
    runner.run_test("ModelConfig creation", test_model_config)

    # Model tests
    print("\n--- Model Tests ---")
    runner.run_test("Drug models", test_drug_models)
    runner.run_test("Disease models", test_disease_models)
    runner.run_test("Anatomy models", test_anatomy_models)
    runner.run_test("Specialty models", test_specialty_models)
    runner.run_test("Symptom models", test_symptom_models)
    runner.run_test("Procedure models", test_procedure_models)
    runner.run_test("Vaccine models", test_vaccine_models)
    runner.run_test("Pathogen models", test_pathogen_models)
    runner.run_test("Clinical sign models", test_clinical_sign_models)

    # Integration tests
    print("\n--- Integration Tests ---")
    runner.run_test("Prompt builders", test_prompt_builders)
    runner.run_test("Input validation", test_input_validation)

    runner.summary()

    if runner.failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
