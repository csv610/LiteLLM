import pytest
import json
import sys
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Add project root and MedKit path to sys.path
root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))
sys.path.insert(0, str(root_path / "app" / "MedKit" / "drug" / "medicine" / "drugbank"))

from drugbank_medicine_cli import cli
from drugbank_medicine_models import MedicineInfo, BasicInfo


class TestCLIIntegration:
    """Integration tests for CLI functionality"""

    @patch("drugbank_medicine_cli.DrugBankMedicine")
    def test_cli_successful_execution(self, mock_analyzer_class):
        """Test successful CLI execution with mocked DrugBankMedicine"""
        # Create sample medicine data
        sample_response = MedicineInfo(
            basic_info=BasicInfo(
                name="Aspirin",
                drugbank_id="DB00945",
                synonyms=["Acetylsalicylic acid"],
            ),
            classification={
                "drug_type": "small_molecule",
                "groups": ["approved"],
                "categories": ["Analgesics"],
            },
        )

        # Mock DrugBankMedicine
        mock_analyzer = MagicMock()
        mock_analyzer.generate_text.return_value = sample_response
        mock_analyzer_class.return_value = mock_analyzer

        # Change to temp directory to avoid file conflicts
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)

            try:
                cli("Aspirin", "gemini/gemini-2.5-flash", 0.2)

                # Verify DrugBankMedicine was called correctly
                mock_analyzer_class.assert_called_once()

                # Check that file was created in outputs/aspirin.json
                expected_path = Path("outputs/aspirin.json")
                assert expected_path.exists()

                # Verify file contents
                with open(expected_path, "r") as f:
                    data = json.load(f)
                    assert data["basic_info"]["name"] == "Aspirin"
                    assert data["basic_info"]["drugbank_id"] == "DB00945"
            finally:
                os.chdir(original_cwd)

    @patch("drugbank_medicine_cli.DrugBankMedicine")
    def test_cli_with_special_characters_in_medicine_name(self, mock_analyzer_class):
        """Test CLI with special characters in medicine name"""
        sample_response = MedicineInfo(
            basic_info=BasicInfo(name="Drug Name", synonyms=[]),
        )

        mock_analyzer = MagicMock()
        mock_analyzer.generate_text.return_value = sample_response
        mock_analyzer_class.return_value = mock_analyzer

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)

            try:
                cli("Drug<>Name|Test", "gemini/gemini-2.5-flash", 0.2)

                # Check sanitized filename in outputs/
                expected_path = Path("outputs/drugnametest.json")
                assert expected_path.exists()
            finally:
                os.chdir(original_cwd)

    @patch("drugbank_medicine_cli.DrugBankMedicine")
    def test_cli_with_invalid_json_response(self, mock_analyzer_class):
        """Test CLI error handling for invalid JSON (though now it handles non-JSON if not structured)"""
        # If generate_text returns a string, it's saved as .md
        mock_analyzer = MagicMock()
        mock_analyzer.generate_text.side_effect = Exception("Analysis failed")
        mock_analyzer_class.return_value = mock_analyzer

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)

            try:
                result = cli("Aspirin", "gemini/gemini-2.5-flash", 0.2)
                assert result == 1
            finally:
                os.chdir(original_cwd)

    @patch("drugbank_medicine_cli.DrugBankMedicine")
    def test_cli_custom_model_parameter(self, mock_analyzer_class):
        """Test CLI with custom model parameter"""
        sample_response = MedicineInfo(
            basic_info=BasicInfo(name="Test Drug", synonyms=[]),
        )

        mock_analyzer = MagicMock()
        mock_analyzer.generate_text.return_value = sample_response
        mock_analyzer_class.return_value = mock_analyzer

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)

            try:
                cli("Test Drug", "gpt-4", 0.5)

                # Verify ModelConfig was created with correct parameters
                call_args = mock_analyzer_class.call_args
                assert call_args[0][0].model == "gpt-4"
                assert call_args[0][0].temperature == 0.5
            finally:
                os.chdir(original_cwd)

    @patch("drugbank_medicine_cli.DrugBankMedicine")
    def test_cli_temperature_parameter(self, mock_analyzer_class):
        """Test CLI with different temperature values"""
        sample_response = MedicineInfo(
            basic_info=BasicInfo(name="Test Drug", synonyms=[]),
        )

        mock_analyzer = MagicMock()
        mock_analyzer.generate_text.return_value = sample_response
        mock_analyzer_class.return_value = mock_analyzer

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)

            try:
                cli("Test Drug", "gemini/gemini-2.5-flash", 0.8)

                call_args = mock_analyzer_class.call_args
                assert call_args[0][0].temperature == 0.8
            finally:
                os.chdir(original_cwd)

    @patch("drugbank_medicine_cli.DrugBankMedicine")
    def test_cli_output_file_structure(self, mock_analyzer_class):
        """Test that output JSON has correct structure"""
        from drugbank_medicine_models import MedicineInfo, BasicInfo, Classification

        sample_response = MedicineInfo(
            basic_info=BasicInfo(
                name="Ibuprofen",
                drugbank_id="DB01050",
                synonyms=["Brufen", "Advil"],
                description="A nonsteroidal anti-inflammatory drug",
            ),
            classification=Classification()
        )
        mock_analyzer = MagicMock()
        mock_analyzer.generate_text.return_value = sample_response
        mock_analyzer_class.return_value = mock_analyzer
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)

            try:
                cli("Ibuprofen", "gemini/gemini-2.5-flash", 0.2)

                expected_path = Path("outputs/ibuprofen.json")
                with open(expected_path, "r") as f:
                    data = json.load(f)

                # Verify structure
                assert "basic_info" in data
                assert data["basic_info"]["name"] == "Ibuprofen"
                assert data["basic_info"]["drugbank_id"] == "DB01050"
                assert len(data["basic_info"]["synonyms"]) == 2
                assert "classification" in data
            finally:
                os.chdir(original_cwd)

    def test_cli_argparse_integration(self):
        """Test CLI argument parsing"""
        import argparse

        # Simulate argparse for the CLI
        parser = argparse.ArgumentParser(
            description="Fetch comprehensive medicine information using LiteClient."
        )
        parser.add_argument(
            "medicine", help="Name of the medicine to fetch information for"
        )
        parser.add_argument(
            "-m",
            "--model",
            default="gemini/gemini-2.5-flash",
            help="Model to use (default: gemini/gemini-2.5-flash)",
        )
        parser.add_argument(
            "-t",
            "--temperature",
            type=float,
            default=0.2,
            help="Temperature for model response (default: 0.2)",
        )

        # Test default arguments
        args = parser.parse_args(["Aspirin"])
        assert args.medicine == "Aspirin"
        assert args.model == "gemini/gemini-2.5-flash"
        assert args.temperature == 0.2

        # Test custom arguments
        args = parser.parse_args(
            ["Ibuprofen", "-m", "gpt-4", "-t", "0.7"]
        )
        assert args.medicine == "Ibuprofen"
        assert args.model == "gpt-4"
        assert args.temperature == 0.7


class TestErrorHandling:
    """Test error handling in CLI"""

    @patch("drugbank_medicine_cli.DrugBankMedicine")
    def test_file_write_error(self, mock_analyzer_class):
        """Test handling of file write errors"""
        sample_response = {
            "basic_info": {"name": "Test Drug", "synonyms": []},
        }

        mock_analyzer = MagicMock()
        mock_analyzer.generate_text.return_value = sample_response
        mock_analyzer_class.return_value = mock_analyzer

        # Mocking Path.mkdir to fail or something that causes an error in create_drugbank_medicine_report
        with patch("pathlib.Path.mkdir", side_effect=IOError("Permission denied")):
            result = cli("Test Drug", "gemini/gemini-2.5-flash", 0.2)
            assert result == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
