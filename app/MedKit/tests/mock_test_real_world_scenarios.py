import pytest
import random
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add project root to sys.path
import sys
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from drug.drug_drug.drug_drug_interaction import DrugDrugInteractionGenerator
from drug.drug_drug.drug_drug_interaction_prompts import DrugDrugInput
from med_dictionary.medical_term_classify import MedicalTermClassifier
from lite.config import ModelConfig

def load_harmful_drug_pairs():
    """Load real drug pairs from the harmful_list.txt file."""
    harmful_list_path = project_root / "drug" / "drug_drug" / "harmful_list.txt"
    pairs = []
    if harmful_list_path.exists():
        with open(harmful_list_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and "," in line:
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) >= 2:
                        pairs.append((parts[0], parts[1]))
    return pairs

def load_categorized_medical_terms():
    """Load categorized medical terms from example_inputs.txt."""
    terms_path = project_root / "med_dictionary" / "assets" / "example_inputs.txt"
    categorized_terms = {}
    current_category = "General"
    
    if terms_path.exists():
        with open(terms_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("# "):
                    current_category = line.replace("# ", "").strip()
                    if current_category not in categorized_terms:
                        categorized_terms[current_category] = []
                elif not line.startswith("##"):
                    categorized_terms[current_category].append(line)
    return categorized_terms

def pytest_generate_tests(metafunc):
    """
    Randomly select inputs for tests requiring real-world data.
    This runs once per test session to generate the parameters.
    """
    if "drug_pair" in metafunc.fixturenames:
        pairs = load_harmful_drug_pairs()
        # Randomly select 5 pairs for this test run
        sample = random.sample(pairs, min(len(pairs), 5)) if pairs else []
        metafunc.parametrize("drug_pair", sample)
    
    if "medical_term" in metafunc.fixturenames:
        categories = load_categorized_medical_terms()
        all_terms = []
        # Take 1-2 random terms from each category for broad coverage
        for cat, terms in categories.items():
            if terms:
                all_terms.extend(random.sample(terms, min(len(terms), 1)))
        
        # Further sample to keep test suite fast
        sample = random.sample(all_terms, min(len(all_terms), 5)) if all_terms else []
        metafunc.parametrize("medical_term", sample)

class TestRealWorldScenarios:
    """Integration tests using real-world clinical datasets."""

    def test_drug_interaction_logic_with_real_pair(self, drug_pair):
        """Verify generator handles real-world drug pairs from harmful_list.txt."""
        med1, med2 = drug_pair
        
        # Mock LiteClient to avoid actual API costs while verifying the logic flow
        with patch("drug.drug_drug.drug_drug_interaction.LiteClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.generate_text.return_value = f"Analysis for {med1} and {med2}"
            
            config = ModelConfig(model="test-model")
            generator = DrugDrugInteractionGenerator(config)
            
            user_input = DrugDrugInput(
                medicine1=med1,
                medicine2=med2,
                age=random.randint(18, 95)
            )
            
            # Execute generation
            result = generator.generate_text(user_input, structured=False)
            
            # Assertions
            assert result is not None
            assert med1 in result or med2 in result
            
            # Verify the prompt construction
            args, kwargs = mock_instance.generate_text.call_args
            model_input = kwargs.get('model_input') or args[0]
            
            assert med1.lower() in model_input.user_prompt.lower()
            assert med2.lower() in model_input.user_prompt.lower()

    def test_medical_classification_with_real_term(self, medical_term):
        """Verify classifier handles real-world terms from example_inputs.txt."""
        
        with patch("med_dictionary.medical_term_classify.LiteClient") as MockClient:
            mock_instance = MockClient.return_value
            # Simulated structured response
            mock_instance.generate_text.return_value = (
                '{"category": "Clinical", "subcategory": "General", '
                f'"definition": "A real-world medical term: {medical_term}"}}'
            )
            
            config = ModelConfig(model="test-model")
            # Use a unique temp output for each term to avoid race conditions if parallelized
            temp_output = Path(f"test_output_{random.randint(1000, 9999)}.json")
            classifier = MedicalTermClassifier(config, output_file=temp_output)
            
            # Execute classification
            classifier.classify(medical_term)
            
            # Assertions
            assert len(classifier.classifications) > 0
            found_term = any(c.get("term") == medical_term for c in classifier.classifications)
            assert found_term, f"Term '{medical_term}' not found in results"
            
            # Cleanup
            if temp_output.exists():
                temp_output.unlink()

    def test_privacy_deidentification_with_real_intake(self):
        """Verify de-identification using a realistic clinical intake note."""
        from medkit_privacy.deidentification import Deidentifier
        
        intake_path = project_root / "medkit_privacy" / "assets" / "pii_sample_input.txt"
        if not intake_path.exists():
            pytest.skip("pii_sample_input.txt not found")
            
        with open(intake_path, "r", encoding="utf-8") as f:
            real_text = f.read()
            
        deidentifier = Deidentifier()
        deidentified_text = deidentifier.deidentify_text(real_text)
        
        # Assertions: Check that specific real PII from the asset is removed
        assert "Alexander J. Hamilton-Smythe" not in deidentified_text
        assert "456 Wall St" not in deidentified_text
        assert "555-123-4567" not in deidentified_text
        assert "999-00-1111" not in deidentified_text
        
        # Verify placeholders exist
        assert "[" in deidentified_text and "]" in deidentified_text
