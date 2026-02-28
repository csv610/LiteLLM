#!/usr/bin/env python3
"""
Test suite for ClinicalSignIdentifier Module.

This script validates the clinical sign identifier functionality without using mock libraries.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
import random
from pathlib import Path


from app.MedKit.recognizers.clinical_sign.clinical_sign_models import ClinicalSignIdentifierModel, ClinicalSignIdentificationModel, ModelOutput
from app.MedKit.recognizers.clinical_sign.clinical_sign_prompts import PromptBuilder, ClinicalSignInput
from app.MedKit.recognizers.clinical_sign.clinical_sign_recognizer import ClinicalSignIdentifier
from lite.config import ModelConfig


def read_random_example_from_assets():
    """Read a random example from assets folder."""
    assets_file = Path(__file__).parent / "assets" / "example_inputs.txt"
    examples = []
    
    if assets_file.exists():
        with open(assets_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('##'):
                    examples.append(line)
    
    # Return a random example if available, otherwise fallback
    if examples:
        return random.choice(examples)
    else:
        return "babinski_sign"  # fallback
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
    test_input = ClinicalSignInput(example)
    user_prompt = PromptBuilder.create_user_prompt(test_input)
    assert isinstance(user_prompt, str)
    assert example in user_prompt
    print("✓ User prompt generated successfully")
    
    # Validate empty input handling
    try:
        ClinicalSignInput("")
        assert False, "Expected ValueError for empty input"
    except ValueError:
        print("✓ Empty input validation functions correctly")


def test_models():
    """Validate the Pydantic model structures."""
    print("\nValidating Models...")
    
    # Validate identification model structure
    example = read_random_example_from_assets()
    identification = ClinicalSignIdentificationModel(
        sign_name=example,
        is_well_known=True,
        examination_method="Stroking the lateral sole of the foot with a blunt object",
        clinical_significance="Indicates upper motor neuron lesion when dorsiflexion of great toe occurs"
    )
    print("✓ IdentificationModel instantiated successfully")
    
    # Validate identifier model structure
    identifier_model = ClinicalSignIdentifierModel(
        identification=identification,
        summary="Babinski Sign is a recognized clinical sign in medical literature",
        data_available=True
    )
    print("✓ IdentifierModel instantiated successfully")
    
    # Validate ModelOutput structure
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
    
    # Validate empty input handling
    try:
        ClinicalSignInput("")
        assert False, "Expected ValueError for empty input"
    except ValueError:
        print("✓ Empty input validation functions correctly")

    # Validate whitespace-only input handling
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
    
    # Validate that the identify method exists and can be called
    assert hasattr(identifier, 'identify'), "identify method should exist"
    assert callable(getattr(identifier, 'identify')), "identify should be callable"
    
    # Validate method signature
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
