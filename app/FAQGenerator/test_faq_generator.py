import unittest
from unittest.mock import MagicMock, patch
from faq_generator import FAQGenerator, FAQConfig
from faq_generator_models import FAQ, FAQResponse

class TestFAQGenerator(unittest.TestCase):
    def setUp(self):
        self.config = FAQConfig(
            input_source="Artificial Intelligence",
            num_faqs=2,
            difficulty="medium",
            output_dir="."
        )
        self.generator = FAQGenerator(self.config)

    @patch('faq_generator.LiteClient')
    def test_generate_success(self, MockLiteClient):
        # Mocking the response from LiteClient
        mock_client_instance = MockLiteClient.return_value
        mock_response = FAQResponse(
            topic="Artificial Intelligence",
            difficulty="medium",
            num_faqs=2,
            faqs=[
                FAQ(question="What is AI?", answer="Artificial Intelligence is...", difficulty="medium"),
                FAQ(question="What is Machine Learning?", answer="ML is a subset of AI...", difficulty="medium")
            ]
        )
        mock_client_instance.generate_text.return_value = mock_response

        # Call generate
        faqs = self.generator.generate()

        # Assertions
        self.assertEqual(len(faqs), 2)
        self.assertEqual(faqs[0].question, "What is AI?")
        self.assertEqual(faqs[1].question, "What is Machine Learning?")
        mock_client_instance.generate_text.assert_called_once()

    def test_config_validation_invalid_faqs(self):
        with self.assertRaises(ValueError):
            FAQConfig(input_source="AI", num_faqs=101, difficulty="medium")

    def test_config_validation_invalid_difficulty(self):
        with self.assertRaises(ValueError):
            FAQConfig(input_source="AI", num_faqs=5, difficulty="expert")

if __name__ == '__main__':
    unittest.main()
