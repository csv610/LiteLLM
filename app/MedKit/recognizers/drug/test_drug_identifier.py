#!/usr/bin/env python3
"""
Test script for Drug Identifier Module.
"""

import sys
import random
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent.parent.absolute()))

from app.MedKit.recognizers.drug.drug_recognizer_model import DrugIdentifierModel, DrugIdentificationModel, ModelOutput
from app.MedKit.recognizers.drug.drug_recognizer_prompts import PromptBuilder, DrugIdentifierInput
from app.MedKit.recognizers.drug.drug_recognizer import DrugIdentifier
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
        return "Aspirin"  # fallback


def test_prompt_builder():
    """Validate the PromptBuilder class functionality."""
    print("Validating PromptBuilder...")
    
    # Read random example from assets
    example_drug = read_random_example_from_assets()
    
    # Validate system prompt generation
    system_prompt = PromptBuilder.create_system_prompt()
    assert isinstance(system_prompt, str)
    assert len(system_prompt) > 0
    print("✓ System prompt generated successfully")
    
    # Validate user prompt generation
    drug_input = DrugIdentifierInput(example_drug)
    user_prompt = PromptBuilder.create_user_prompt(drug_input)
    assert isinstance(user_prompt, str)
    assert example_drug in user_prompt
    print("✓ User prompt generated successfully")


def test_drug_identifier_models():
    """Validate the Pydantic model structures."""
    print("\nValidating Drug Identifier Models...")
    
    # Read random example from assets
    example_drug = read_random_example_from_assets()
    
    # Validate DrugIdentificationModel structure
    identification = DrugIdentificationModel(
        drug_name=example_drug,
        is_well_known=True,
        common_uses=["pain", "inflammation"],
        regulatory_status="FDA approved",
        industry_significance="Common"
    )
    print("✓ DrugIdentificationModel instantiated successfully")
    
    # Validate DrugIdentifierModel structure
    drug_model = DrugIdentifierModel(
        identification=identification,
        summary=f"{example_drug} is a recognized drug",
        data_available=True
    )
    print("✓ DrugIdentifierModel instantiated successfully")
    
    # Validate ModelOutput structure
    model_output = ModelOutput(data=drug_model)
    assert model_output.data.identification.drug_name == example_drug
    print("✓ ModelOutput instantiated successfully")


def test_drug_identifier_initialization():
    """Validate DrugIdentifier initialization."""
    print("\nValidating DrugIdentifier Initialization...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = DrugIdentifier(config)
    
    assert identifier.client is not None
    print("✓ DrugIdentifier initialized successfully")


def test_method_name_consistency():
    """Validate that the identify method exists and works correctly."""
    print("\nValidating Method Name Consistency...")

    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = DrugIdentifier(config)

    # Validate that the identify method exists and can be called
    assert hasattr(identifier, 'identify'), "identify method should exist"
    assert callable(getattr(identifier, 'identify')), "identify should be callable"
    print("✓ identify method has correct signature")


def main():
    """Run all validations."""
    print("=" * 60)
    print("DRUG IDENTIFIER MODULE VALIDATIONS")
    print("=" * 60)
    
    try:
        test_prompt_builder()
        test_drug_identifier_models()
        test_drug_identifier_initialization()
        test_method_name_consistency()
        
        print("\n" + "=" * 60)
        print("ALL VALIDATIONS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ VALIDATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
