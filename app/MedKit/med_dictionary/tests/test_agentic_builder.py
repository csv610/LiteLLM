import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
import sys
import json

# Add project roots to sys.path
project_root = Path(__file__).parent.parent
litellm_root = project_root.parent.parent.parent.parent
for path in [project_root, project_root.parent, litellm_root]:
    if str(path) not in sys.path:
        sys.path.append(str(path))

from agentic.builder import AgenticDictionaryBuilder
from lite.config import ModelConfig

class TestAgenticBuilder(unittest.TestCase):
    def setUp(self):
        self.model_config = ModelConfig(model="test-model")
        # Patch LiteClient to avoid actual API calls
        with patch('agentic.builder.LiteClient') as MockClient:
            self.mock_client = MockClient.return_value
            self.builder = AgenticDictionaryBuilder(self.model_config)
            # Override output file for testing
            self.builder.output_file = Path(__file__).parent / "test_outputs" / "test_agentic.json"
            self.builder.output_file.parent.mkdir(parents=True, exist_ok=True)
            self.builder.definitions = []
            self.builder.existing_terms = set()

    def tearDown(self):
        if self.builder.output_file.exists():
            self.builder.output_file.unlink()
        if self.builder.output_file.parent.exists():
            self.builder.output_file.parent.rmdir()

    def test_process_term_agentic_success(self):
        term = "Hypertension"
        
        # Define side effects for the multi-step workflow
        # Step 1: Verification, Step 2: Draft, Step 3: Refinement
        self.mock_client.generate_text.side_effect = [
            "This is a medical term for high blood pressure. [YES]",
            "Draft: A condition where blood pressure is high.",
            "Condition characterized by persistently elevated arterial blood pressure."
        ]
        
        result = self.builder.process_term_agentic(term)
        
        self.assertEqual(result, "Condition characterized by persistently elevated arterial blood pressure.")
        self.assertEqual(self.mock_client.generate_text.call_count, 3)

    def test_process_term_agentic_non_medical(self):
        term = "Table"
        
        # Step 1: Verification fails
        self.mock_client.generate_text.return_value = "This is furniture, not a medical term. [NO]"
        
        result = self.builder.process_term_agentic(term)
        
        self.assertEqual(result, "Not a medically recognized term.")
        self.assertEqual(self.mock_client.generate_text.call_count, 1)

    @patch('agentic.builder.load_terms_from_file')
    def test_build_success(self, mock_load):
        term = "Anemia"
        self.mock_client.generate_text.side_effect = [
            "Blood condition. [YES]",
            "Draft: Low red blood cells.",
            "Condition marked by a deficiency of red blood cells or hemoglobin."
        ]
        
        self.builder.build(term)
        
        self.assertEqual(len(self.builder.definitions), 1)
        self.assertEqual(self.builder.definitions[0]['term'], term)
        self.assertEqual(self.builder.definitions[0]['definition'], "Condition marked by a deficiency of red blood cells or hemoglobin.")

if __name__ == '__main__':
    unittest.main()
