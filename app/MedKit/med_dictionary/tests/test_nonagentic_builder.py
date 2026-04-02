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

from nonagentic.builder import NonAgenticDictionaryBuilder
from lite.config import ModelConfig

class TestNonAgenticBuilder(unittest.TestCase):
    def setUp(self):
        self.model_config = ModelConfig(model="test-model")
        # Patch LiteClient to avoid actual API calls
        with patch('nonagentic.builder.LiteClient') as MockClient:
            self.mock_client = MockClient.return_value
            self.builder = NonAgenticDictionaryBuilder(self.model_config)
            # Override output file for testing
            self.builder.output_file = Path(__file__).parent / "test_outputs" / "test_nonagentic.json"
            self.builder.output_file.parent.mkdir(parents=True, exist_ok=True)
            self.builder.definitions = []
            self.builder.existing_terms = set()

    def tearDown(self):
        if self.builder.output_file.exists():
            self.builder.output_file.unlink()
        if self.builder.output_file.parent.exists():
            self.builder.output_file.parent.rmdir()

    @patch('nonagentic.builder.load_terms_from_file')
    def test_build_single_term(self, mock_load):
        term = "Aspirin"
        definition = "A medication used to reduce pain, fever, or inflammation."
        self.mock_client.generate_text.return_value = definition
        
        self.builder.build(term)
        
        self.assertEqual(len(self.builder.definitions), 1)
        self.assertEqual(self.builder.definitions[0]['term'], term)
        self.assertEqual(self.builder.definitions[0]['definition'], definition)
        self.mock_client.generate_text.assert_called_once()

    def test_load_definitions_empty(self):
        defs = self.builder._load_definitions()
        self.assertEqual(defs, [])

if __name__ == '__main__':
    unittest.main()
