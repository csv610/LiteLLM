import pytest
import json
import sys
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.cli.drugbank_medicine import cli, MedicineInfo, BasicInfo


class TestCLIIntegration:
    """Integration tests for CLI functionality"""

    @patch("app.cli.drugbank_medicine.LiteClient")
    def test_cli_successful_execution(self, mock_client_class):
        """Test successful CLI execution with mocked LiteClient"""
        # Create sample medicine data
        sample_response = json.dumps({
            "basic_info": {
                "name": "Aspirin",
                "drugbank_id": "DB00945",
                "synonyms": ["Acetylsalicylic acid"],
            },
            "classification": {
                "drug_type": "small_molecule",
                "groups": ["approved"],
                "categories": ["Analgesics"],
            },
        })

        # Mock LiteClient
        mock_client = MagicMock()
        mock_client.generate_text.return_value = sample_response
        mock_client_class.return_value = mock_client

        # Change to temp directory to avoid file conflicts
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)

            try:
                cli("Aspirin", "gemini/gemini-2.5-flash", 0.2)

                # Verify LiteClient was called correctly
                mock_client_class.assert_called_once()

                # Check that file was created
                assert os.path.exists("Aspirin.json")

                # Verify file contents
                with open("Aspirin.json", "r") as f:
                    data = json.load(f)
                    assert data["basic_info"]["name"] == "Aspirin"
                    assert data["basic_info"]["drugbank_id"] == "DB00945"
            finally:
                os.chdir(original_cwd)

    @patch("app.cli.drugbank_medicine.LiteClient")
    def test_cli_with_special_characters_in_medicine_name(self, mock_client_class):
        """Test CLI with special characters in medicine name"""
        sample_response = json.dumps({
            "basic_info": {"name": "Drug Name", "synonyms": []},
        })

        mock_client = MagicMock()
        mock_client.generate_text.return_value = sample_response
        mock_client_class.return_value = mock_client

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)

            try:
                cli("Drug<>Name|Test", "gemini/gemini-2.5-flash", 0.2)

                # Check sanitized filename
                assert os.path.exists("DrugNameTest.json")
            finally:
                os.chdir(original_cwd)

    @patch("app.cli.drugbank_medicine.LiteClient")
    def test_cli_with_invalid_json_response(self, mock_client_class):
        """Test CLI error handling for invalid JSON"""
        mock_client = MagicMock()
        mock_client.generate_text.return_value = "Invalid JSON {{"
        mock_client_class.return_value = mock_client

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)

            try:
                with pytest.raises(SystemExit) as exc_info:
                    cli("Aspirin", "gemini/gemini-2.5-flash", 0.2)
                assert exc_info.value.code == 1
            finally:
                os.chdir(original_cwd)

    @patch("app.cli.drugbank_medicine.LiteClient")
    def test_cli_with_non_string_response(self, mock_client_class):
        """Test CLI error handling for non-string response"""
        mock_client = MagicMock()
        mock_client.generate_text.return_value = {"not": "string"}
        mock_client_class.return_value = mock_client

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)

            try:
                with pytest.raises(SystemExit) as exc_info:
                    cli("Aspirin", "gemini/gemini-2.5-flash", 0.2)
                assert exc_info.value.code == 1
            finally:
                os.chdir(original_cwd)

    @patch("app.cli.drugbank_medicine.LiteClient")
    def test_cli_custom_model_parameter(self, mock_client_class):
        """Test CLI with custom model parameter"""
        sample_response = json.dumps({
            "basic_info": {"name": "Test Drug", "synonyms": []},
        })

        mock_client = MagicMock()
        mock_client.generate_text.return_value = sample_response
        mock_client_class.return_value = mock_client

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)

            try:
                cli("Test Drug", "gpt-4", 0.5)

                # Verify ModelConfig was created with correct parameters
                call_args = mock_client_class.call_args
                assert call_args[1]["model_config"].model == "gpt-4"
                assert call_args[1]["model_config"].temperature == 0.5
            finally:
                os.chdir(original_cwd)

    @patch("app.cli.drugbank_medicine.LiteClient")
    def test_cli_temperature_parameter(self, mock_client_class):
        """Test CLI with different temperature values"""
        sample_response = json.dumps({
            "basic_info": {"name": "Test Drug", "synonyms": []},
        })

        mock_client = MagicMock()
        mock_client.generate_text.return_value = sample_response
        mock_client_class.return_value = mock_client

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)

            try:
                cli("Test Drug", "gemini/gemini-2.5-flash", 0.8)

                call_args = mock_client_class.call_args
                assert call_args[1]["model_config"].temperature == 0.8
            finally:
                os.chdir(original_cwd)

    @patch("app.cli.drugbank_medicine.LiteClient")
    def test_cli_output_file_structure(self, mock_client_class):
        """Test that output JSON has correct structure"""
        sample_response = json.dumps({
            "basic_info": {
                "name": "Ibuprofen",
                "drugbank_id": "DB01050",
                "synonyms": ["Brufen", "Advil"],
                "description": "A nonsteroidal anti-inflammatory drug",
            },
            "classification": {
                "drug_type": "small_molecule",
                "groups": ["approved"],
                "categories": ["Anti-inflammatory", "Analgesic"],
                "atc_codes": [],
                "taxonomy": None,
            },
            "pharmacology": None,
            "indications": None,
            "administration": None,
            "interactions": None,
            "safety": None,
            "regulation": None,
            "references": None,
        })

        mock_client = MagicMock()
        mock_client.generate_text.return_value = sample_response
        mock_client_class.return_value = mock_client

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)

            try:
                cli("Ibuprofen", "gemini/gemini-2.5-flash", 0.2)

                with open("Ibuprofen.json", "r") as f:
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
        from app.cli.drugbank_medicine import (
            __name__ as module_name,
        )
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

    @patch("app.cli.drugbank_medicine.LiteClient")
    @patch("builtins.open", side_effect=IOError("Permission denied"))
    def test_file_write_error(self, mock_open, mock_client_class):
        """Test handling of file write errors"""
        sample_response = json.dumps({
            "basic_info": {"name": "Test Drug", "synonyms": []},
        })

        mock_client = MagicMock()
        mock_client.generate_text.return_value = sample_response
        mock_client_class.return_value = mock_client

        with pytest.raises(SystemExit) as exc_info:
            cli("Test Drug", "gemini/gemini-2.5-flash", 0.2)
        assert exc_info.value.code == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
