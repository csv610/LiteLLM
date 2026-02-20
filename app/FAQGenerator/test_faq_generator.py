import unittest
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch
from lite import ModelConfig
from faq_generator import FAQGenerator, FAQInput
from faq_generator_models import FAQ, FAQResponse

class TestFAQGenerator(unittest.TestCase):
    def setUp(self):
        self.model_config = ModelConfig(model="openai/gpt-4o")
        # We'll initialize generator inside tests where we can control the mock

    @patch('faq_generator.LiteClient')
    def test_generate_success(self, MockLiteClient):
        mock_client_instance = MockLiteClient.return_value
        mock_response = FAQResponse(
            topic="Artificial Intelligence",
            difficulty="medium",
            num_faqs=2,
            faqs=[
                FAQ(question="What is Artificial Intelligence?", answer="It is the simulation of human intelligence by machines.", difficulty="medium"),
                FAQ(question="What is Machine Learning?", answer="ML is a subset of AI focused on algorithms.", difficulty="medium")
            ]
        )
        mock_client_instance.generate_text.return_value = mock_response

        generator = FAQGenerator(self.model_config)
        faq_input = FAQInput(input_source="AI", num_faqs=2, difficulty="medium")
        
        faqs = generator.generate_text(faq_input)
        self.assertEqual(len(faqs), 2)
        mock_client_instance.generate_text.assert_called_once()

    @patch('faq_generator.LiteClient')
    def test_generate_retry_on_failure(self, MockLiteClient):
        mock_client_instance = MockLiteClient.return_value
        # Fail twice, succeed on third
        mock_client_instance.generate_text.side_effect = [
            RuntimeError("API Timeout"),
            RuntimeError("API Overload"),
            FAQResponse(
                topic="AI", difficulty="medium", num_faqs=1,
                faqs=[FAQ(question="What is AI testing?", answer="Testing AI systems for reliability.", difficulty="medium")]
            )
        ]

        generator = FAQGenerator(self.model_config)
        faq_input = FAQInput(input_source="AI", num_faqs=1, difficulty="medium")
        
        faqs = generator.generate_text(faq_input)
        self.assertEqual(len(faqs), 1)
        self.assertEqual(mock_client_instance.generate_text.call_count, 3)

    @patch('faq_generator.LiteClient')
    def test_file_size_limit(self, MockLiteClient):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("a" * (6 * 1024 * 1024)) # 6MB
            temp_path = f.name
        
        try:
            generator = FAQGenerator(self.model_config)
            large_input = FAQInput(input_source=temp_path, num_faqs=5, difficulty="medium")
            with self.assertRaisesRegex(ValueError, "File too large"):
                generator.generate_text(large_input)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    @patch('faq_generator.LiteClient')
    def test_save_to_file_sanitization(self, MockLiteClient):
        generator = FAQGenerator(self.model_config)
        faqs = [FAQ(question="Test valid question?", answer="Test valid answer.", difficulty="medium")]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # We use a path that exists for input_source to avoid resolution errors, 
            # but we'll check how the filename is constructed.
            input_file = os.path.join(tmpdir, "dangerous/../../secret.txt")
            bad_input = FAQInput(input_source="secret.txt", num_faqs=1, difficulty="medium", output_dir=tmpdir)
            
            output_path = generator.save_to_file(faqs, bad_input)
            
            self.assertTrue(os.path.exists(output_path))
            filename = os.path.basename(output_path)
            self.assertIn("secret", filename)
            self.assertNotIn("..", filename)

    def test_config_validation(self):
        with self.assertRaises(ValueError):
            FAQInput(input_source="", num_faqs=5, difficulty="medium")
        with self.assertRaises(ValueError):
            FAQInput(input_source="AI", num_faqs=0, difficulty="medium")

if __name__ == '__main__':
    unittest.main()
