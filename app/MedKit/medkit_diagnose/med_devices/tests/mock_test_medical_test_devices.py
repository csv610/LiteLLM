import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from medical_test_devices import MedicalTestDeviceGuide
from medical_test_devices_models import ModelOutput


class TestMedicalTestDeviceGuide(unittest.TestCase):
    @patch("medical_test_devices.LiteClient")
    @patch("medical_test_devices.ModelConfig")
    def test_init(self, mock_model_config, mock_lite_client):
        # Setup
        model_config = MagicMock()
        model_config.model = "test-model"

        # Action
        guide = MedicalTestDeviceGuide(model_config)

        # Assert
        self.assertEqual(guide.model_config, model_config)
        mock_lite_client.assert_called_once_with(model_config)

    @patch("medical_test_devices.LiteClient")
    @patch("medical_test_devices.ModelConfig")
    @patch("medical_test_devices.PromptBuilder")
    def test_generate_text_unstructured(
        self, mock_prompt_builder, mock_model_config, mock_lite_client
    ):
        # Setup
        model_config = MagicMock()
        model_config.model = "test-model"
        guide = MedicalTestDeviceGuide(model_config)

        mock_prompt_builder.create_system_prompt.return_value = "system prompt"
        mock_prompt_builder.create_user_prompt.return_value = "user prompt"

        expected_output = ModelOutput(markdown="device info")
        guide.client.generate_text.return_value = expected_output

        # Action
        result = guide.generate_text("Ultrasound", structured=False)

        # Assert
        self.assertEqual(result, expected_output)
        self.assertEqual(guide.device_name, "Ultrasound")
        guide.client.generate_text.assert_called_once()
        args, kwargs = guide.client.generate_text.call_args
        model_input = kwargs["model_input"]
        self.assertEqual(model_input.system_prompt, "system prompt")
        self.assertEqual(model_input.user_prompt, "user prompt")
        self.assertIsNone(model_input.response_format)

    @patch("medical_test_devices.LiteClient")
    @patch("medical_test_devices.ModelConfig")
    @patch("medical_test_devices.PromptBuilder")
    def test_generate_text_structured(
        self, mock_prompt_builder, mock_model_config, mock_lite_client
    ):
        from medical_test_devices_models import MedicalDeviceInfoModel

        # Setup
        model_config = MagicMock()
        model_config.model = "test-model"
        guide = MedicalTestDeviceGuide(model_config)

        mock_prompt_builder.create_system_prompt.return_value = "system prompt"
        mock_prompt_builder.create_user_prompt.return_value = "user prompt"

        expected_output = ModelOutput(data=MagicMock(spec=MedicalDeviceInfoModel))
        guide.client.generate_text.return_value = expected_output

        # Action
        result = guide.generate_text("Ultrasound", structured=True)

        # Assert
        self.assertEqual(result, expected_output)
        guide.client.generate_text.assert_called_once()
        args, kwargs = guide.client.generate_text.call_args
        model_input = kwargs["model_input"]
        self.assertEqual(model_input.response_format, MedicalDeviceInfoModel)

    @patch("medical_test_devices.save_model_response")
    @patch("medical_test_devices.LiteClient")
    @patch("medical_test_devices.ModelConfig")
    def test_save(self, mock_model_config, mock_lite_client, mock_save_response):
        # Setup
        model_config = MagicMock()
        guide = MedicalTestDeviceGuide(model_config)
        result = ModelOutput(markdown="test content")
        output_path = Path("test.json")

        mock_save_response.return_value = Path("test.md")

        # Action
        # When result is a string (but here it's ModelOutput, wait)
        # The code has: if isinstance(result, str) and output_path.suffix == ".json":
        # But result is ModelOutput in generate_text.
        # Wait, if result is a string... let's check the code again.
        # "if isinstance(result, str) and output_path.suffix == '.json':"
        # However, generate_text returns ModelOutput.

        saved_path = guide.save(result, output_path)

        # Assert
        mock_save_response.assert_called_once_with(result, output_path)
        self.assertEqual(saved_path, Path("test.md"))


if __name__ == "__main__":
    unittest.main()
