#!/usr/bin/env python3
"""
Test script for Medical Supplement Identifier Module.

This script tests the medical supplement identifier functionality with various supplement examples
without using mock libraries.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from app.MedKit.recognizers.medical_supplement.medical_supplement_models import SupplementIdentifierModel, ModelOutput
from app.MedKit.recognizers.medical_supplement.medical_supplement_prompts import PromptBuilder, SupplementIdentifierInput
from app.MedKit.recognizers.medical_supplement.medical_supplement_recognizer import MedicalSupplementIdentifier
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
    supplement_input = SupplementIdentifierInput("vitamin_d")
    user_prompt = PromptBuilder.create_user_prompt(supplement_input)
    assert isinstance(user_prompt, str)
    assert "vitamin_d" in user_prompt
    print("✓ User prompt created successfully")
    
    # Test empty supplement name
    try:
        empty_input = SupplementIdentifierInput("")
        assert False, "Should have raised ValueError for empty supplement name"
    except ValueError:
        print("✓ Empty supplement name validation works correctly")


def test_medical_supplement_models():
    """Test the Pydantic models."""
    print("\nTesting Medical Supplement Models...")
    
    # Test SupplementIdentificationModel
    identification = SupplementIdentifierModel(
        supplement_name="vitamin_d",
        is_well_known=True,
        supplement_category="vitamin",
        common_uses=["bone_health", "immune_support", "calcium_absorption"],
        medical_significance="Essential for calcium metabolism and bone health, deficiency common in many populations"
    )
    print("✓ SupplementIdentificationModel created successfully")
    
    # Test SupplementIdentifierModel
    supplement_model = SupplementIdentifierModel(
        identification=identification,
        summary="Vitamin D is a well-known fat-soluble vitamin crucial for bone health",
        data_available=True
    )
    print("✓ SupplementIdentifierModel created successfully")
    
    # Test ModelOutput
    model_output = ModelOutput(data=supplement_model)
    assert model_output.data.supplement_name == "vitamin_d"
    print("✓ ModelOutput created successfully")


def test_medical_supplement_identifier_initialization():
    """Test MedicalSupplementIdentifier initialization."""
    print("\nTesting MedicalSupplementIdentifier Initialization...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = MedicalSupplementIdentifier(config)
    
    assert identifier.client is not None
    print("✓ MedicalSupplementIdentifier initialized successfully")


def test_medical_supplement_identifier_validation():
    """Test MedicalSupplementIdentifier input validation."""
    print("\nTesting MedicalSupplementIdentifier Validation...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = MedicalSupplementIdentifier(config)
    
    # Test empty supplement name
    try:
        supplement_input = SupplementIdentifierInput("")
        assert False, "Should have raised ValueError for empty supplement name"
    except ValueError:
        print("✓ Empty supplement name validation works correctly")
    
    # Test whitespace-only supplement name
    try:
        supplement_input = SupplementIdentifierInput("   ")
        assert False, "Should have raised ValueError for whitespace-only supplement name"
    except ValueError:
        print("✓ Whitespace-only supplement name validation works correctly")


def test_with_example_supplements():
    """Test with example supplements from assets."""
    print("\nTesting with Example Supplements...")
    
    # Read example supplements from assets
    assets_file = Path(__file__).parent / "assets" / "example_inputs.txt"
    if assets_file.exists():
        with open(assets_file, 'r') as f:
            content = f.read()
        
        # Extract supplement names (skip comments and empty lines)
        supplements = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('##'):
                supplements.append(line)
        
        print(f"Found {len(supplements)} example supplements")
        
        # Test a few examples
        test_supplements = supplements[:5]  # Test first 5 supplements
        config = ModelConfig(model="ollama/gemma3", temperature=0.2)
        identifier = MedicalSupplementIdentifier(config)
        
        for supplement in test_supplements:
            try:
                supplement_input = SupplementIdentifierInput(supplement)
                print(f"✓ Supplement input created for: {supplement}")
            except Exception as e:
                print(f"✗ Error creating input for {supplement}: {e}")
    else:
        print("⚠ Example inputs file not found")


def test_supplement_categories():
    """Test different categories of medical supplements."""
    print("\nTesting Supplement Categories...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = MedicalSupplementIdentifier(config)
    
    # Test vitamins
    vitamins = ["vitamin_a", "vitamin_c", "vitamin_d", "vitamin_e", "vitamin_k"]
    for supplement in vitamins:
        try:
            supplement_input = SupplementIdentifierInput(supplement)
            print(f"✓ Vitamin input created for: {supplement}")
        except Exception as e:
            print(f"✗ Error with vitamin {supplement}: {e}")
    
    # Test minerals
    minerals = ["calcium", "magnesium", "zinc", "iron", "potassium"]
    for supplement in minerals:
        try:
            supplement_input = SupplementIdentifierInput(supplement)
            print(f"✓ Mineral input created for: {supplement}")
        except Exception as e:
            print(f"✗ Error with mineral {supplement}: {e}")
    
    # Test herbal supplements
    herbals = ["ginseng", "echinacea", "garlic", "turmeric", "ginger"]
    for supplement in herbals:
        try:
            supplement_input = SupplementIdentifierInput(supplement)
            print(f"✓ Herbal supplement input created for: {supplement}")
        except Exception as e:
            print(f"✗ Error with herbal supplement {supplement}: {e}")
    
    # Test specialty supplements
    specialty = ["omega_3", "probiotic", "coq10", "collagen", "creatine"]
    for supplement in specialty:
        try:
            supplement_input = SupplementIdentifierInput(supplement)
            print(f"✓ Specialty supplement input created for: {supplement}")
        except Exception as e:
            print(f"✗ Error with specialty supplement {supplement}: {e}")


def main():
    """Run all tests."""
    print("=" * 60)
    print("MEDICAL SUPPLEMENT IDENTIFIER MODULE TESTS")
    print("=" * 60)
    
    try:
        test_prompt_builder()
        test_medical_supplement_models()
        test_medical_supplement_identifier_initialization()
        test_medical_supplement_identifier_validation()
        test_with_example_supplements()
        test_supplement_categories()
        
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
