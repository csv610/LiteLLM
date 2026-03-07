import json
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from lite.config import ModelConfig
from medical_term_classify import MedicalTermClassifier


class TestMedicalTermClassifier(unittest.TestCase):
    def setUp(self):
        # Setup model config
        self.model_config = ModelConfig(model="test-model")

        # Patch outputs folder and classified.json to avoid modifying real data
        self.temp_output_dir = Path("./temp_test_outputs")
        self.temp_output_dir.mkdir(exist_ok=True)
        self.mock_output_file = self.temp_output_dir / "classified.json"

        # Initial empty classifications
        with open(self.mock_output_file, "w") as f:
            json.dump([], f)

    def tearDown(self):
        # Cleanup
        if self.mock_output_file.exists():
            self.mock_output_file.unlink()
        if self.temp_output_dir.exists():
            self.temp_output_dir.rmdir()

    @patch("medical_term_classify.LiteClient")
    @patch("medical_term_classify.Path")
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
        mock_client_instance.generate_text.return_value = json.dumps(
            {"category": "Drug", "subcategory": "Antibiotic"}
        )

        classifier = MedicalTermClassifier(
            self.model_config, output_file=self.mock_output_file
        )

        # Test classification
        count = classifier.classify("penicillin")

        self.assertEqual(count, 1)
        self.assertEqual(len(classifier.classifications), 1)
        self.assertEqual(classifier.classifications[0]["term"], "penicillin")
        self.assertEqual(classifier.classifications[0]["category"], "Drug")

        # Verify generate_text was called
        mock_client_instance.generate_text.assert_called_once()

    @patch("medical_term_classify.LiteClient")
    def test_classify_existing_term(self, MockLiteClient):
        # Setup existing term
        initial_data = [{"term": "aspirin", "category": "Drug", "subcategory": "NSAID"}]
        with open(self.mock_output_file, "w") as f:
            json.dump(initial_data, f)

        classifier = MedicalTermClassifier(
            self.model_config, output_file=self.mock_output_file
        )

        # Test classifying same term again
        count = classifier.classify("aspirin")

        self.assertEqual(count, 0)
        # Should not have called LLM
        MockLiteClient.return_value.generate_text.assert_not_called()

    @patch("medical_term_classify.LiteClient")
    def test_extract_json_markdown(self, MockLiteClient):
        classifier = MedicalTermClassifier(
            self.model_config, output_file=self.mock_output_file
        )

        # Test markdown JSON block
        text = 'Here is the response:\n```json\n{"category": "Disease", "subcategory": "Infection"}\n```'
        result = classifier._extract_json(text)
        self.assertEqual(result["category"], "Disease")

        # Test markdown without 'json' tag
        text = '```\n{"category": "Procedure", "subcategory": "Surgery"}\n```'
        result = classifier._extract_json(text)
        self.assertEqual(result["category"], "Procedure")

        # Test text with JSON embedded
        text = 'The answer is {"category": "Anatomy", "subcategory": "Organ"} hope this helps.'
        result = classifier._extract_json(text)
        self.assertEqual(result["category"], "Anatomy")

    @patch("medical_term_classify.LiteClient")
    def test_classify_invalid_json(self, MockLiteClient):
        mock_client_instance = MockLiteClient.return_value
        mock_client_instance.generate_text.return_value = "This is not JSON at all."

        classifier = MedicalTermClassifier(
            self.model_config, output_file=self.mock_output_file
        )

        count = classifier.classify("invalid_term")

        self.assertEqual(count, 0)
        self.assertEqual(len(classifier.classifications), 0)

    @patch("medical_term_classify.LiteClient")
    def test_classify_missing_keys(self, MockLiteClient):
        mock_client_instance = MockLiteClient.return_value
        # Missing 'subcategory'
        mock_client_instance.generate_text.return_value = json.dumps(
            {"category": "Disease"}
        )

        classifier = MedicalTermClassifier(
            self.model_config, output_file=self.mock_output_file
        )

        count = classifier.classify("incomplete_term")

        self.assertEqual(count, 0)
        self.assertEqual(len(classifier.classifications), 0)


if __name__ == "__main__":
    unittest.main()
