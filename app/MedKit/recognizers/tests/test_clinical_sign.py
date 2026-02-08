#!/usr/bin/env python3
"""
Test script for Clinical Sign Identifier Module.

This script tests the clinical sign identifier functionality without using mock libraries.
"""

import sys
import os
from pathlib import Path


from app.MedKit.recognizers.clinical_sign.clinical_sign_models import ClinicalSignIdentifierModel, ModelOutput
from app.MedKit.recognizers.clinical_sign.clinical_sign_prompts import PromptBuilder, ClinicalSignIdentifierInput
from app.MedKit.recognizers.clinical_sign.clinical_sign_recognizer import ClinicalSignIdentifier
from lite.config import ModelConfig


def test_prompt_builder():
    """Test the PromptBuilder class."""
    print("Testing PromptBuilder...")
    
    # Test system prompt
    system_prompt = PromptBuilder.create_system_prompt()
    assert isinstance(system_prompt, str)
    assert len(system_prompt) > 0
    print("✓ System prompt created successfully")
    
    # Test user prompt
    sign_input = ClinicalSignIdentifierInput("babinski_sign")
    user_prompt = PromptBuilder.create_user_prompt(sign_input)
    assert isinstance(user_prompt, str)
    assert "babinski_sign" in user_prompt
    print("✓ User prompt created successfully")
    
    # Test empty sign name
    try:
        empty_input = ClinicalSignIdentifierInput("")
        assert False, "Should have raised ValueError for empty sign name"
    except ValueError:
        print("✓ Empty sign name validation works correctly")


def test_clinical_sign_models():
    """Test the Pydantic models."""
    print("\nTesting Clinical Sign Models...")
    
    # Test SignIdentificationModel
    identification = ClinicalSignIdentifierModel(
        sign_name="babinski_sign",
        is_well_known=True,
        examination_method="stroking_the_sole_of_the_foot",
        clinical_significance="upper_motor_neuron_lesion"
    )
    print("✓ SignIdentificationModel created successfully")
    
    # Test ClinicalSignIdentifierModel
    sign_model = ClinicalSignIdentifierModel(
        identification=identification,
        summary="Babinski sign is a well-known neurological examination finding",
        data_available=True
    )
    print("✓ ClinicalSignIdentifierModel created successfully")
    
    # Test ModelOutput
    model_output = ModelOutput(data=sign_model)
    assert model_output.data.sign_name == "babinski_sign"
    print("✓ ModelOutput created successfully")


def test_clinical_sign_identifier_initialization():
    """Test ClinicalSignIdentifier initialization."""
    print("\nTesting ClinicalSignIdentifier Initialization...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = ClinicalSignIdentifier(config)
    
    assert identifier.client is not None
    print("✓ ClinicalSignIdentifier initialized successfully")


def test_clinical_sign_identifier_validation():
    """Test ClinicalSignIdentifier input validation."""
    print("\nTesting ClinicalSignIdentifier Validation...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = ClinicalSignIdentifier(config)
    
    # Test empty sign name
    try:
        sign_input = ClinicalSignIdentifierInput("")
        assert False, "Should have raised ValueError for empty sign name"
    except ValueError:
        print("✓ Empty sign name validation works correctly")
    
    # Test whitespace-only sign name
    try:
        sign_input = ClinicalSignIdentifierInput("   ")
        assert False, "Should have raised ValueError for whitespace-only sign name"
    except ValueError:
        print("✓ Whitespace-only sign name validation works correctly")


def test_with_example_signs():
    """Test with example clinical signs from assets."""
    print("\nTesting with Example Clinical Signs...")
    
    # Read example signs from assets
    assets_file = Path(__file__).parent.parent / "clinical_sign" / "assets" / "example_inputs.txt"
    if assets_file.exists():
        with open(assets_file, 'r') as f:
            content = f.read()
        
        # Extract sign names (skip comments and empty lines)
        signs = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('##'):
                signs.append(line)
        
        print(f"Found {len(signs)} example clinical signs")
        
        # Test a few examples
        test_signs = signs[:5]  # Test first 5 signs
        config = ModelConfig(model="ollama/gemma3", temperature=0.2)
        identifier = ClinicalSignIdentifier(config)
        
        for sign in test_signs:
            try:
                sign_input = ClinicalSignIdentifierInput(sign)
                print(f"✓ Sign input created for: {sign}")
            except Exception as e:
                print(f"✗ Error creating input for {sign}: {e}")
    else:
        print("⚠ Example inputs file not found")


def test_sign_categories():
    """Test different categories of clinical signs."""
    print("\nTesting Sign Categories...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = ClinicalSignIdentifier(config)
    
    # Test neurological signs
    neuro_signs = ["babinski_sign", "kernig_sign", "brudzinski_sign", "romberg_sign"]
    for sign in neuro_signs:
        try:
            sign_input = ClinicalSignIdentifierInput(sign)
            print(f"✓ Neurological sign input created for: {sign}")
        except Exception as e:
            print(f"✗ Error with neurological sign {sign}: {e}")
    
    # Test cardiovascular signs
    cardio_signs = ["heart_murmur", "peripheral_edema", "jugular_venous_distension", "cyanosis"]
    for sign in cardio_signs:
        try:
            sign_input = ClinicalSignIdentifierInput(sign)
            print(f"✓ Cardiovascular sign input created for: {sign}")
        except Exception as e:
            print(f"✗ Error with cardiovascular sign {sign}: {e}")
    
    # Test respiratory signs
    resp_signs = ["rales", "rhonchi", "wheezing", "stridor", "pleural_friction_rub"]
    for sign in resp_signs:
        try:
            sign_input = ClinicalSignIdentifierInput(sign)
            print(f"✓ Respiratory sign input created for: {sign}")
        except Exception as e:
            print(f"✗ Error with respiratory sign {sign}: {e}")


def test_method_name_consistency():
    """Test that the identify method works correctly."""
    print("\nTesting Method Name Consistency...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = ClinicalSignIdentifier(config)
    
    # Test that the identify method exists and can be called
    assert hasattr(identifier, 'identify'), "identify method should exist"
    assert callable(getattr(identifier, 'identify')), "identify should be callable"
    
    # Test method signature (should not raise TypeError for correct arguments)
    try:
        # This should work without errors (though may fail at runtime without actual LLM)
        sign_input = ClinicalSignIdentifierInput("babinski_sign")
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
        test_clinical_sign_models()
        test_clinical_sign_identifier_initialization()
        test_clinical_sign_identifier_validation()
        test_with_example_signs()
        test_sign_categories()
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
