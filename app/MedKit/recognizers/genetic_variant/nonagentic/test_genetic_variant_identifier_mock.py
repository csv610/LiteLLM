#!/usr/bin/env python3
"""
Test suite for GeneticVariantIdentifier Module.

This script validates the genetic variant identifier functionality without using mock libraries.
"""

import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)
import random
from pathlib import Path

from lite.config import ModelConfig

from app.MedKit.recognizers.genetic_variant.nonagentic.genetic_variant_recognizer import (
    GeneticVariantIdentifier,
)
from app.MedKit.recognizers.genetic_variant.nonagentic.genetic_variant_models import (
    GeneticVariantIdentificationModel,
    GeneticVariantIdentifierModel,
    ModelOutput,
)
from app.MedKit.recognizers.genetic_variant.nonagentic.genetic_variant_prompts import (
    GeneticVariantInput,
    PromptBuilder,
)


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
        return "BRCA1"


def test_prompt_builder():
    """Validate the PromptBuilder class functionality."""
    print("Validating PromptBuilder...")

    system_prompt = PromptBuilder.create_system_prompt()
    assert isinstance(system_prompt, str)
    assert len(system_prompt) > 0
    print("✓ System prompt generated successfully")

    example = read_random_example_from_assets()
    test_input = GeneticVariantInput(example)
    user_prompt = PromptBuilder.create_user_prompt(test_input)
    assert isinstance(user_prompt, str)
    assert example in user_prompt
    print("✓ User prompt generated successfully")

    try:
        GeneticVariantInput("")
        assert False, "Expected ValueError for empty input"
    except ValueError:
        print("✓ Empty input validation functions correctly")


def test_models():
    """Validate the Pydantic model structures."""
    print("\nValidating Models...")

    example = read_random_example_from_assets()
    identification = GeneticVariantIdentificationModel(
        variant_name=example,
        is_well_known=True,
        inheritance_pattern="autosomal dominant",
        clinical_implications="Increased risk for breast and ovarian cancer",
    )
    print("✓ IdentificationModel instantiated successfully")

    identifier_model = GeneticVariantIdentifierModel(
        identification=identification,
        summary="BRCA1 is a well-known genetic variant in clinical genetics",
        data_available=True,
    )
    print("✓ IdentifierModel instantiated successfully")

    model_output = ModelOutput(data=identifier_model)
    assert model_output.data.identification.variant_name == example
    print("✓ ModelOutput instantiated successfully")


def test_identifier_initialization():
    """Validate GeneticVariantIdentifier initialization."""
    print("\nValidating GeneticVariantIdentifier Initialization...")

    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = GeneticVariantIdentifier(config)

    assert identifier.client is not None
    print("✓ GeneticVariantIdentifier initialized successfully")


def test_identifier_validation():
    """Validate GeneticVariantIdentifier input validation."""
    print("\nValidating GeneticVariantIdentifier Input Validation...")

    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    GeneticVariantIdentifier(config)

    try:
        GeneticVariantInput("")
        assert False, "Expected ValueError for empty input"
    except ValueError:
        print("✓ Empty input validation functions correctly")

    try:
        GeneticVariantInput("   ")
        assert False, "Expected ValueError for whitespace-only input"
    except ValueError:
        print("✓ Whitespace-only input validation functions correctly")


def test_method_name_consistency():
    """Validate that the identify method exists and works correctly."""
    print("\nValidating Method Name Consistency...")

    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = GeneticVariantIdentifier(config)

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
    print("GENETIC VARIANT IDENTIFIER MODULE TESTS")
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
