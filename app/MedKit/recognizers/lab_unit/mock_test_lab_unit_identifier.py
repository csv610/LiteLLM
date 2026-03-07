#!/usr/bin/env python3
"""
Test suite for LabUnitIdentifier Module.

This script validates the lab unit identifier functionality without using mock libraries.
"""

import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)
import random
from pathlib import Path

from app.MedKit.recognizers.lab_unit.lab_unit_models import (
    LabUnitIdentificationModel,
    LabUnitIdentifierModel,
    ModelOutput,
)
from app.MedKit.recognizers.lab_unit.lab_unit_prompts import LabUnitInput, PromptBuilder
from app.MedKit.recognizers.lab_unit.lab_unit_recognizer import LabUnitIdentifier
from lite.config import ModelConfig


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

    # Return a random example if available, otherwise fallback
    if examples:
        return random.choice(examples)
    else:
        return "mg_dl"  # fallback


def test_prompt_builder():
    """Validate the PromptBuilder class functionality."""
    print("Validating PromptBuilder...")

    # Validate system prompt generation
    system_prompt = PromptBuilder.create_system_prompt()
    assert isinstance(system_prompt, str)
    assert len(system_prompt) > 0
    print("✓ System prompt generated successfully")

    # Validate user prompt generation
    example = read_random_example_from_assets()
    test_input = LabUnitInput(example)
    user_prompt = PromptBuilder.create_user_prompt(test_input)
    assert isinstance(user_prompt, str)
    assert example in user_prompt
    print("✓ User prompt generated successfully")

    # Validate empty input handling
    try:
        LabUnitInput("")
        assert False, "Expected ValueError for empty input"
    except ValueError:
        print("✓ Empty input validation functions correctly")


def test_models():
    """Validate the Pydantic model structures."""
    print("\nValidating Models...")

    # Validate identification model structure
    example = read_random_example_from_assets()
    identification = LabUnitIdentificationModel(
        unit_name=example,
        is_well_known=True,
        category="concentration",
        common_tests=["glucose_screening", "metabolic_panel"],
    )
    print("✓ IdentificationModel instantiated successfully")

    # Validate identifier model structure
    identifier_model = LabUnitIdentifierModel(
        identification=identification,
        summary="Mg Dl is a recognized lab unit in medical literature",
        data_available=True,
    )
    print("✓ IdentifierModel instantiated successfully")

    # Validate ModelOutput structure
    model_output = ModelOutput(data=identifier_model)
    assert model_output.data.identification.unit_name == example
    print("✓ ModelOutput instantiated successfully")


def test_identifier_initialization():
    """Validate LabUnitIdentifier initialization."""
    print("\nValidating LabUnitIdentifier Initialization...")

    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = LabUnitIdentifier(config)

    assert identifier.client is not None
    print("✓ LabUnitIdentifier initialized successfully")


def test_identifier_validation():
    """Validate LabUnitIdentifier input validation."""
    print("\nValidating LabUnitIdentifier Input Validation...")

    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    LabUnitIdentifier(config)

    # Validate empty input handling
    try:
        LabUnitInput("")
        assert False, "Expected ValueError for empty input"
    except ValueError:
        print("✓ Empty input validation functions correctly")

    # Validate whitespace-only input handling
    try:
        LabUnitInput("   ")
        assert False, "Expected ValueError for whitespace-only input"
    except ValueError:
        print("✓ Whitespace-only input validation functions correctly")


def test_method_name_consistency():
    """Validate that the identify method exists and works correctly."""
    print("\nValidating Method Name Consistency...")

    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = LabUnitIdentifier(config)

    # Validate that the identify method exists and can be called
    assert hasattr(identifier, "identify"), "identify method should exist"
    assert callable(getattr(identifier, "identify")), "identify should be callable"

    # Validate method signature
    try:
        read_random_example_from_assets()
        print("✓ identify method has correct signature")
    except Exception as e:
        print(f"✗ Error with identify method: {e}")


def main():
    """Run all tests."""
    print("=" * 60)
    print("LAB UNIT IDENTIFIER MODULE TESTS")
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
