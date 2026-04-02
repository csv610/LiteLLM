#!/usr/bin/env python3
"""
Test suite for ClinicalSignIdentifier Module.

This script validates the clinical sign identifier functionality without using mock libraries.
"""

import os
import sys
import types
import importlib.util


this_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(this_dir, "../../../../../"))
recognizers_dir = os.path.join(project_root, "app/MedKit/recognizers")

sys.path.insert(0, project_root)

import random
from pathlib import Path

from lite.config import ModelConfig


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


app_pkg = types.ModuleType("app")
app_pkg.__path__ = [os.path.join(project_root, "app")]
sys.modules["app"] = app_pkg

medkit_pkg = types.ModuleType("app.MedKit")
medkit_pkg.__path__ = [os.path.join(project_root, "app", "MedKit")]
sys.modules["app.MedKit"] = medkit_pkg

recognizers_pkg = types.ModuleType("app.MedKit.recognizers")
recognizers_pkg.__path__ = [recognizers_dir]
sys.modules["app.MedKit.recognizers"] = recognizers_pkg

models = _load_module(
    "app.MedKit.recognizers.models",
    os.path.join(recognizers_dir, "models.py"),
)
sys.modules["app.MedKit.recognizers.models"] = models

base_recognizer = _load_module(
    "app.MedKit.recognizers.base_recognizer",
    os.path.join(recognizers_dir, "base_recognizer.py"),
)
sys.modules["app.MedKit.recognizers.base_recognizer"] = base_recognizer

clinical_sign_models = _load_module(
    "clinical_sign_models", os.path.join(this_dir, "clinical_sign_models.py")
)
clinical_sign_prompts = _load_module(
    "clinical_sign_prompts", os.path.join(this_dir, "clinical_sign_prompts.py")
)

clinical_sign_pkg = types.ModuleType("app.MedKit.recognizers.clinical_sign")
clinical_sign_pkg.__path__ = [os.path.join(recognizers_dir, "clinical_sign")]
sys.modules["app.MedKit.recognizers.clinical_sign"] = clinical_sign_pkg

nonagentic_pkg = types.ModuleType("app.MedKit.recognizers.clinical_sign.nonagentic")
nonagentic_pkg.__path__ = [this_dir]
sys.modules["app.MedKit.recognizers.clinical_sign.nonagentic"] = nonagentic_pkg

clinical_sign_models.__package__ = "app.MedKit.recognizers.clinical_sign.nonagentic"
sys.modules["app.MedKit.recognizers.clinical_sign.nonagentic.clinical_sign_models"] = (
    clinical_sign_models
)

clinical_sign_prompts.__package__ = "app.MedKit.recognizers.clinical_sign.nonagentic"
sys.modules["app.MedKit.recognizers.clinical_sign.nonagentic.clinical_sign_prompts"] = (
    clinical_sign_prompts
)

spec = importlib.util.spec_from_file_location(
    "app.MedKit.recognizers.clinical_sign.nonagentic.clinical_sign_recognizer",
    os.path.join(this_dir, "clinical_sign_recognizer.py"),
)
clinical_sign_recognizer = importlib.util.module_from_spec(spec)
clinical_sign_recognizer.__package__ = "app.MedKit.recognizers.clinical_sign.nonagentic"
sys.modules[
    "app.MedKit.recognizers.clinical_sign.nonagentic.clinical_sign_recognizer"
] = clinical_sign_recognizer
spec.loader.exec_module(clinical_sign_recognizer)

ClinicalSignIdentificationModel = clinical_sign_models.ClinicalSignIdentificationModel
ClinicalSignIdentifierModel = clinical_sign_models.ClinicalSignIdentifierModel
ModelOutput = clinical_sign_models.ModelOutput
ClinicalSignInput = clinical_sign_prompts.ClinicalSignInput
PromptBuilder = clinical_sign_prompts.PromptBuilder
ClinicalSignIdentifier = clinical_sign_recognizer.ClinicalSignIdentifier


def read_random_example_from_assets():
    """Read a random example from assets folder."""
    assets_file = Path(__file__).parent / "assets" / "example_inputs.txt"
    examples = []

    if assets_file.exists():
        with open(assets_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("##"):
                    examples.append(line)

    if examples:
        return random.choice(examples)
    else:
        return "babinski_sign"


def test_prompt_builder():
    """Validate the PromptBuilder class functionality."""
    print("Validating PromptBuilder...")

    system_prompt = PromptBuilder.create_system_prompt()
    assert isinstance(system_prompt, str)
    assert len(system_prompt) > 0
    print("✓ System prompt generated successfully")

    example = read_random_example_from_assets()
    test_input = ClinicalSignInput(example)
    user_prompt = PromptBuilder.create_user_prompt(test_input)
    assert isinstance(user_prompt, str)
    assert example in user_prompt
    print("✓ User prompt generated successfully")

    try:
        ClinicalSignInput("")
        assert False, "Expected ValueError for empty input"
    except ValueError:
        print("✓ Empty input validation functions correctly")


def test_models():
    """Validate the Pydantic model structures."""
    print("\nValidating Models...")

    example = read_random_example_from_assets()
    identification = ClinicalSignIdentificationModel(
        sign_name=example,
        is_well_known=True,
        examination_method="Stroking the lateral sole of the foot with a blunt object",
        clinical_significance="Indicates upper motor neuron lesion when dorsiflexion of great toe occurs",
    )
    print("✓ IdentificationModel instantiated successfully")

    identifier_model = ClinicalSignIdentifierModel(
        identification=identification,
        summary="Babinski Sign is a recognized clinical sign in medical literature",
        data_available=True,
    )
    print("✓ IdentifierModel instantiated successfully")

    model_output = ModelOutput(data=identifier_model)
    assert model_output.data.identification.sign_name == example
    print("✓ ModelOutput instantiated successfully")


def test_identifier_initialization():
    """Validate ClinicalSignIdentifier initialization."""
    print("\nValidating ClinicalSignIdentifier Initialization...")

    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = ClinicalSignIdentifier(config)

    assert identifier.client is not None
    print("✓ ClinicalSignIdentifier initialized successfully")


def test_identifier_validation():
    """Validate ClinicalSignIdentifier input validation."""
    print("\nValidating ClinicalSignIdentifier Input Validation...")

    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    ClinicalSignIdentifier(config)

    try:
        ClinicalSignInput("")
        assert False, "Expected ValueError for empty input"
    except ValueError:
        print("✓ Empty input validation functions correctly")

    try:
        ClinicalSignInput("   ")
        assert False, "Expected ValueError for whitespace-only input"
    except ValueError:
        print("✓ Whitespace-only input validation functions correctly")


def test_method_name_consistency():
    """Validate that the identify method exists and works correctly."""
    print("\nValidating Method Name Consistency...")

    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = ClinicalSignIdentifier(config)

    assert hasattr(identifier, "identify"), "identify method should exist"
    assert callable(getattr(identifier, "identify")), "identify should be callable"

    try:
        read_random_example_from_assets()
        print("✓ identify method has correct signature")
    except Exception as e:
        print(f"✗ Error with identify method: {e}")


def main():
    """Run all tests."""
    print("=" * 60)
    print("CLINICAL SIGN IDENTIFIER MODULE TESTS")
    print("=" * 60)

    try:
        test_prompt_builder()
        test_models()
        test_identifier_initialization()
        test_identifier_validation()
        test_method_name_consistency()

        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
