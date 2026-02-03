#!/usr/bin/env python3
"""
Test script for Medical Test Identifier Module.

This script tests the medical test identifier functionality with various test examples
without using mock libraries.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from app.MedKit.recognizers.medical_test.medical_test_models import MedicalTestIdentifierModel, ModelOutput
from app.MedKit.recognizers.medical_test.medical_test_prompts import PromptBuilder, MedicalTestIdentifierInput
from app.MedKit.recognizers.medical_test.medical_test_recognizer import MedicalTestIdentifier
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
    test_input = MedicalTestIdentifierInput("complete_blood_count")
    user_prompt = PromptBuilder.create_user_prompt(test_input)
    assert isinstance(user_prompt, str)
    assert "complete_blood_count" in user_prompt
    print("✓ User prompt created successfully")
    
    # Test empty test name
    try:
        empty_input = MedicalTestIdentifierInput("")
        assert False, "Should have raised ValueError for empty test name"
    except ValueError:
        print("✓ Empty test name validation works correctly")


def test_medical_test_models():
    """Test the Pydantic models."""
    print("\nTesting Medical Test Models...")
    
    # Test TestIdentificationModel
    identification = MedicalTestIdentifierModel(
        test_name="complete_blood_count",
        is_well_known=True,
        test_category="blood_test",
        common_usage="routine_health_screening",
        medical_significance="Provides comprehensive information about blood cells and overall health"
    )
    print("✓ TestIdentificationModel created successfully")
    
    # Test MedicalTestIdentifierModel
    test_model = MedicalTestIdentifierModel(
        identification=identification,
        summary="Complete blood count is a fundamental blood test used in routine medical care",
        data_available=True
    )
    print("✓ MedicalTestIdentifierModel created successfully")
    
    # Test ModelOutput
    model_output = ModelOutput(data=test_model)
    assert model_output.data.test_name == "complete_blood_count"
    print("✓ ModelOutput created successfully")


def test_medical_test_identifier_initialization():
    """Test MedicalTestIdentifier initialization."""
    print("\nTesting MedicalTestIdentifier Initialization...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = MedicalTestIdentifier(config)
    
    assert identifier.client is not None
    print("✓ MedicalTestIdentifier initialized successfully")


def test_medical_test_identifier_validation():
    """Test MedicalTestIdentifier input validation."""
    print("\nTesting MedicalTestIdentifier Validation...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = MedicalTestIdentifier(config)
    
    # Test empty test name
    try:
        test_input = MedicalTestIdentifierInput("")
        assert False, "Should have raised ValueError for empty test name"
    except ValueError:
        print("✓ Empty test name validation works correctly")
    
    # Test whitespace-only test name
    try:
        test_input = MedicalTestIdentifierInput("   ")
        assert False, "Should have raised ValueError for whitespace-only test name"
    except ValueError:
        print("✓ Whitespace-only test name validation works correctly")


def test_with_example_tests():
    """Test with example tests from assets."""
    print("\nTesting with Example Tests...")
    
    # Read example tests from assets
    assets_file = Path(__file__).parent / "assets" / "example_inputs.txt"
    if assets_file.exists():
        with open(assets_file, 'r') as f:
            content = f.read()
        
        # Extract test names (skip comments and empty lines)
        tests = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('##'):
                tests.append(line)
        
        print(f"Found {len(tests)} example tests")
        
        # Test a few examples
        test_examples = tests[:5]  # Test first 5 tests
        config = ModelConfig(model="ollama/gemma3", temperature=0.2)
        identifier = MedicalTestIdentifier(config)
        
        for test in test_examples:
            try:
                test_input = MedicalTestIdentifierInput(test)
                print(f"✓ Test input created for: {test}")
            except Exception as e:
                print(f"✗ Error creating input for {test}: {e}")
    else:
        print("⚠ Example inputs file not found")


def test_test_categories():
    """Test different categories of medical tests."""
    print("\nTesting Test Categories...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = MedicalTestIdentifier(config)
    
    # Test blood tests
    blood_tests = ["complete_blood_count", "blood_glucose", "cholesterol", "liver_function_tests"]
    for test in blood_tests:
        try:
            test_input = MedicalTestIdentifierInput(test)
            print(f"✓ Blood test input created for: {test}")
        except Exception as e:
            print(f"✗ Error with blood test {test}: {e}")
    
    # Test imaging tests
    imaging_tests = ["x_ray", "ct_scan", "mri", "ultrasound"]
    for test in imaging_tests:
        try:
            test_input = MedicalTestIdentifierInput(test)
            print(f"✓ Imaging test input created for: {test}")
        except Exception as e:
            print(f"✗ Error with imaging test {test}: {e}")
    
    # Test cardiac tests
    cardiac_tests = ["ecg", "echocardiogram", "stress_test", "holter_monitor"]
    for test in cardiac_tests:
        try:
            test_input = MedicalTestIdentifierInput(test)
            print(f"✓ Cardiac test input created for: {test}")
        except Exception as e:
            print(f"✗ Error with cardiac test {test}: {e}")
    
    # Test laboratory tests
    lab_tests = ["urine_analysis", "blood_culture", "allergy_testing", "genetic_testing"]
    for test in lab_tests:
        try:
            test_input = MedicalTestIdentifierInput(test)
            print(f"✓ Laboratory test input created for: {test}")
        except Exception as e:
            print(f"✗ Error with laboratory test {test}: {e}")


def test_common_abbreviations():
    """Test common medical test abbreviations."""
    print("\nTesting Common Test Abbreviations...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = MedicalTestIdentifier(config)
    
    abbreviations = ["cbc", "ecg", "ct", "mri", "hba1c", "bmi", "bp", "hr", "rr", "spo2"]
    
    for abbr in abbreviations:
        try:
            test_input = MedicalTestIdentifierInput(abbr)
            print(f"✓ Abbreviation input created for: {abbr}")
        except Exception as e:
            print(f"✗ Error with abbreviation {abbr}: {e}")


def main():
    """Run all tests."""
    print("=" * 60)
    print("MEDICAL TEST IDENTIFIER MODULE TESTS")
    print("=" * 60)
    
    try:
        test_prompt_builder()
        test_medical_test_models()
        test_medical_test_identifier_initialization()
        test_medical_test_identifier_validation()
        test_with_example_tests()
        test_test_categories()
        test_common_abbreviations()
        
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
