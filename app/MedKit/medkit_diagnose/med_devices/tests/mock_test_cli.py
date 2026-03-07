import sys
import unittest
from unittest.mock import patch

from medical_test_devices_cli import get_user_arguments


class TestCLI(unittest.TestCase):
    def test_get_user_arguments_basic(self):
        test_args = ["medical_test_devices_cli.py", "Ultrasound"]
        with patch.object(sys, "argv", test_args):
            args = get_user_arguments()
            self.assertEqual(args.test_device, "Ultrasound")
            self.assertEqual(args.output_dir, "outputs")
            self.assertEqual(args.model, "ollama/gemma3")
            self.assertFalse(args.structured)

    def test_get_user_arguments_custom(self):
        test_args = [
            "medical_test_devices_cli.py",
            "CT Scanner",
            "-d",
            "custom_outputs",
            "-m",
            "gpt-4",
            "-s",
            "-v",
            "3",
        ]
        with patch.object(sys, "argv", test_args):
            args = get_user_arguments()
            self.assertEqual(args.test_device, "CT Scanner")
            self.assertEqual(args.output_dir, "custom_outputs")
            self.assertEqual(args.model, "gpt-4")
            self.assertTrue(args.structured)
            self.assertEqual(args.verbosity, 3)

    @patch("medical_test_devices_cli.MedicalTestDeviceGuide")
    @patch("medical_test_devices_cli.configure_logging")
    @patch("medical_test_devices_cli.Path.mkdir")
    def test_create_report_from_file(self, mock_mkdir, mock_log, mock_guide_class):
        import argparse

        from medical_test_devices_cli import create_medical_test_device_report

        # Setup
        mock_guide = mock_guide_class.return_value
        args = argparse.Namespace(
            test_device="assets/device_list.txt",
            output_dir="outputs",
            model="test-model",
            verbosity=2,
            structured=False,
        )

        # Create a mock file
        with patch(
            "builtins.open", unittest.mock.mock_open(read_data="Device1\nDevice2\n")
        ):
            with patch("medical_test_devices_cli.Path.is_file", return_value=True):
                create_medical_test_device_report(args)

        # Assert
        self.assertEqual(mock_guide.generate_text.call_count, 2)
        mock_guide.generate_text.assert_any_call("Device1", structured=False)
        mock_guide.generate_text.assert_any_call("Device2", structured=False)


if __name__ == "__main__":
    unittest.main()
