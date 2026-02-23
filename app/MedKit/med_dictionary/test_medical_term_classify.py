import unittest
from unittest.mock import MagicMock, patch
import json
from pathlib import Path
from medical_term_classify import MedicalTermClassifier
from lite.config import ModelConfig

class TestMedicalTermClassifier(unittest.TestCase):
    def setUp(self):
        # Setup model config
        self.model_config = ModelConfig(model="test-model")
        
        # Patch outputs folder and classified.json to avoid modifying real data
        self.temp_output_dir = Path("./temp_test_outputs")
        self.temp_output_dir.mkdir(exist_ok=True)
        self.mock_output_file = self.temp_output_dir / "classified.json"
        
        # Initial empty classifications
        with open(self.mock_output_file, 'w') as f:
            json.dump([], f)

    def tearDown(self):
        # Cleanup
        if self.mock_output_file.exists():
            self.mock_output_file.unlink()
        if self.temp_output_dir.exists():
            self.temp_output_dir.rmdir()

    @patch('medical_term_classify.LiteClient')
    @patch('medical_term_classify.Path')
    def test_classify_new_term(self, MockPath, MockLiteClient):
        # Setup mocks
        # Configure Path mock to return our test file path
        def mock_path_side_effect(*args, **kwargs):
            if "outputs" in args or (len(args) > 1 and args[1] == "outputs"):
                 return self.temp_output_dir
            if "classified.json" in args:
                 return self.mock_output_file
            return MagicMock(spec=Path)
            
        # This is tricky because of Path(__file__).parent / "outputs" / "classified.json"
        # Let's simplify by patching MedicalTermClassifier.output_file directly after init
        
        mock_client_instance = MockLiteClient.return_value
        mock_client_instance.generate_text.return_value = json.dumps({
            "category": "Drug",
            "subcategory": "Antibiotic"
        })

        classifier = MedicalTermClassifier(self.model_config)
        classifier.output_file = self.mock_output_file
        
        # Test classification
        count = classifier.classify("penicillin")
        
        self.assertEqual(count, 1)
        self.assertEqual(len(classifier.classifications), 1)
        self.assertEqual(classifier.classifications[0]["term"], "penicillin")
        self.assertEqual(classifier.classifications[0]["category"], "Drug")
        
        # Verify generate_text was called
        mock_client_instance.generate_text.assert_called_once()

    @patch('medical_term_classify.LiteClient')
    def test_classify_existing_term(self, MockLiteClient):
        # Setup existing term
        initial_data = [{"term": "aspirin", "category": "Drug", "subcategory": "NSAID"}]
        with open(self.mock_output_file, 'w') as f:
            json.dump(initial_data, f)
            
        classifier = MedicalTermClassifier(self.model_config)
        classifier.output_file = self.mock_output_file
        classifier.existing_terms = {"aspirin"} # Force it for the test
        
        # Test classifying same term again
        count = classifier.classify("aspirin")
        
        self.assertEqual(count, 0)
        # Should not have called LLM
        MockLiteClient.return_value.generate_text.assert_not_called()

if __name__ == '__main__':
    unittest.main()
