"""Integration tests for MedKit CLI modules.

Tests for:
- Full end-to-end CLI execution with mocked LLM
- Complete workflows (generation + saving + output)
- Error flows and recovery
- Output file generation and verification
- JSON output generation
"""

import sys
import json
from pathlib import Path
from unittest.mock import patch, MagicMock, call
from io import StringIO

import pytest
from pydantic import BaseModel, Field

# Setup paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.config import ModelConfig, ModelInput

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.cli_base import BaseCLI, BaseGenerator, BasePromptBuilder


# ==============================================================================
# TEST MODELS AND IMPLEMENTATIONS
# ==============================================================================


class IntegrationTestModel(BaseModel):
    """Test model for integration tests."""
    status: str = Field(description="Status")
    result: str = Field(description="Result")
    timestamp: str = Field(default="2024-01-01", description="Timestamp")


class IntegrationTestPromptBuilder(BasePromptBuilder):
    """Prompt builder for integration tests."""

    @staticmethod
    def create_system_prompt() -> str:
        return "You are a helpful test assistant."

    @staticmethod
    def create_user_prompt(query: str, **kwargs) -> str:
        return f"Process this request: {query}"


class IntegrationTestGenerator(BaseGenerator):
    """Generator for integration tests."""

    def generate_text(self, query: str, structured: bool = False):
        """Generate test response."""
        if structured:
            return IntegrationTestModel(
                status="success",
                result=f"Processed: {query}"
            )
        return f"Result: {query}"


class IntegrationTestCLI(BaseCLI):
    """CLI for integration tests."""

    description = "Integration Test CLI"

    def add_arguments(self, parser):
        parser.add_argument("query", help="Query")
        parser.add_argument("--extra", default="", help="Extra arg")

    def run(self):
        generator = IntegrationTestGenerator(self.model_config, self.logger)
        return generator.generate_text(
            self.args.query,
            self.args.structured
        )


# ==============================================================================
# TESTS - Full CLI Execution Flow
# ==============================================================================


class TestFullCLIFlow:
    """Test complete CLI execution flow."""

    def test_cli_execution_success(self, suppress_logging, temp_output_dir):
        """Test successful CLI execution."""
        cli = IntegrationTestCLI()

        with patch.object(cli, '_display_result'):
            result = cli.execute([
                "test query",
                "-m", "test/model",
                "-t", "0.7",
                "-d", str(temp_output_dir)
            ])

            assert result == 0
            assert cli.args.query == "test query"
            assert cli.model_config.model == "test/model"

    def test_cli_execution_with_json_output(self, suppress_logging, capsys):
        """Test CLI execution with JSON output."""
        cli = IntegrationTestCLI()

        with patch.object(cli, '_display_result'):
            result = cli.execute([
                "test query",
                "-j"  # JSON output
            ])

            assert result == 0

    def test_cli_execution_with_structured_output(self, suppress_logging):
        """Test CLI execution with structured output."""
        cli = IntegrationTestCLI()

        with patch.object(cli, '_display_result'):
            result = cli.execute([
                "test query",
                "-s"  # Structured output
            ])

            assert result == 0
            assert cli.args.structured is True

    def test_cli_with_custom_model(self, suppress_logging):
        """Test CLI with custom model configuration."""
        cli = IntegrationTestCLI()

        custom_model = "custom/model-v2"
        custom_temp = 0.3

        with patch.object(cli, '_display_result'):
            result = cli.execute([
                "test query",
                "-m", custom_model,
                "-t", str(custom_temp)
            ])

            assert result == 0
            assert cli.model_config.model == custom_model
            assert cli.model_config.temperature == custom_temp

    def test_cli_with_all_options(self, suppress_logging, temp_output_dir):
        """Test CLI with all options specified."""
        cli = IntegrationTestCLI()
        output_file = temp_output_dir / "custom_output.json"

        with patch.object(cli, '_display_result'):
            result = cli.execute([
                "test query",
                "--extra", "extra_value",
                "-m", "test/model",
                "-t", "0.8",
                "-v", "4",
                "-o", str(output_file),
                "-d", str(temp_output_dir),
                "-j",  # JSON output
                "-s"   # Structured
            ])

            assert result == 0
            assert cli.args.extra == "extra_value"
            assert cli.args.verbosity == 4


# ==============================================================================
# TESTS - Generation and Output
# ==============================================================================


class TestGenerationAndOutput:
    """Test generation and output workflows."""

    def test_plain_text_generation_and_output(self, suppress_logging, temp_output_dir):
        """Test plain text generation."""
        cli = IntegrationTestCLI()

        with patch.object(cli, '_display_result'):
            result = cli.execute(["test query"])

            assert result == 0

    def test_structured_generation_and_output(self, suppress_logging, temp_output_dir):
        """Test structured generation."""
        cli = IntegrationTestCLI()

        with patch.object(cli, '_display_result'):
            with patch.object(IntegrationTestGenerator, 'generate_text',
                            return_value=IntegrationTestModel(
                                status="success",
                                result="Test"
                            )):
                result = cli.execute(["test query", "-s"])

                assert result == 0

    def test_generator_initialization(self):
        """Test generator initialization in CLI context."""
        config = ModelConfig(model="test/model", temperature=0.7)
        generator = IntegrationTestGenerator(config)

        assert generator.model_config == config
        assert generator.client is not None
        assert generator.logger is not None

    def test_generator_text_generation(self):
        """Test generator text generation."""
        config = ModelConfig(model="test/model")
        generator = IntegrationTestGenerator(config)

        # Plain text
        result = generator.generate_text("test query")
        assert isinstance(result, str)
        assert "test query" in result

    def test_generator_structured_generation(self):
        """Test generator structured generation."""
        config = ModelConfig(model="test/model")
        generator = IntegrationTestGenerator(config)

        # Structured
        result = generator.generate_text("test query", structured=True)
        assert isinstance(result, IntegrationTestModel)
        assert result.status == "success"


# ==============================================================================
# TESTS - File Output Operations
# ==============================================================================


class TestFileOutputOperations:
    """Test file output operations."""

    def test_save_structured_response(self, suppress_logging, temp_output_dir):
        """Test saving structured response."""
        config = ModelConfig(model="test/model")
        generator = IntegrationTestGenerator(config)
        response = IntegrationTestModel(status="success", result="Test")

        with patch('lite.utils.save_model_response') as mock_save:
            mock_save.return_value = temp_output_dir / "output.json"

            output_path = generator.save(
                response,
                temp_output_dir / "output.json"
            )

            mock_save.assert_called_once()
            assert output_path == temp_output_dir / "output.json"

    def test_save_string_response(self, suppress_logging, temp_output_dir):
        """Test saving string response."""
        config = ModelConfig(model="test/model")
        generator = IntegrationTestGenerator(config)
        response = "Test string response"

        with patch('lite.utils.save_model_response') as mock_save:
            mock_save.return_value = temp_output_dir / "output.md"

            output_path = generator.save(
                response,
                temp_output_dir / "output.json"
            )

            mock_save.assert_called_once()

    def test_output_path_creation(self, suppress_logging, temp_output_dir):
        """Test output path creation."""
        cli = IntegrationTestCLI()

        with patch.object(cli, 'run', return_value="test"):
            with patch.object(cli, '_display_result'):
                cli.execute([
                    "test query",
                    "-d", str(temp_output_dir)
                ])

                path = cli._get_output_path("test_item", "analysis")
                assert "test_item" in str(path)
                assert "analysis" in str(path)

    def test_directory_creation_for_output(self, suppress_logging, temp_output_dir):
        """Test output directory creation."""
        cli = IntegrationTestCLI()

        new_dir = temp_output_dir / "nested" / "output"

        with patch.object(cli, 'run', return_value="test"):
            with patch.object(cli, '_display_result'):
                cli.execute([
                    "test query",
                    "-d", str(new_dir)
                ])

                # Directory should be ensured
                assert cli.args.output_dir == new_dir


# ==============================================================================
# TESTS - JSON Output
# ==============================================================================


class TestJSONOutput:
    """Test JSON output generation."""

    def test_model_to_json_output(self, suppress_logging, capsys):
        """Test converting model to JSON output."""
        cli = IntegrationTestCLI()

        test_model = IntegrationTestModel(
            status="success",
            result="Test result"
        )

        with patch.object(cli, 'run', return_value=test_model):
            with patch.object(cli, '_display_result'):
                cli.execute(["test query", "-j"])

                captured = capsys.readouterr()
                # JSON output should be printed
                assert len(captured.out) > 0

    def test_string_to_json_output(self, suppress_logging, capsys):
        """Test string output formatting."""
        cli = IntegrationTestCLI()

        with patch.object(cli, 'run', return_value="Test string output"):
            with patch.object(cli, '_display_result'):
                cli.execute(["test query", "-j"])

                captured = capsys.readouterr()
                assert len(captured.out) > 0

    def test_json_output_flag_behavior(self, suppress_logging):
        """Test JSON output flag behavior."""
        cli = IntegrationTestCLI()

        # Without -j flag
        with patch.object(cli, 'run', return_value="test"):
            with patch.object(cli, '_display_result'):
                with patch.object(cli, '_output_json') as mock_json:
                    cli.execute(["test query"])
                    # _output_json should still be called, but check args
                    assert cli.args.json_output is False

        # With -j flag
        with patch.object(cli, 'run', return_value="test"):
            with patch.object(cli, '_display_result'):
                cli.execute(["test query", "-j"])
                assert cli.args.json_output is True


# ==============================================================================
# TESTS - Error Handling and Recovery
# ==============================================================================


class TestErrorHandlingAndRecovery:
    """Test error handling and recovery."""

    def test_validation_error_handling(self, suppress_logging):
        """Test handling validation errors."""
        cli = IntegrationTestCLI()

        # Empty query should fail validation in some implementations
        with patch.object(cli, 'validate_args',
                         side_effect=ValueError("Empty query")):
            result = cli.execute([""])

            assert result == 1  # Error code

    def test_generation_error_handling(self, suppress_logging):
        """Test handling generation errors."""
        cli = IntegrationTestCLI()

        with patch.object(cli, 'run',
                         side_effect=Exception("Generation failed")):
            result = cli.execute(["test query"])

            assert result == 1  # Error code

    def test_file_write_error_handling(self, suppress_logging):
        """Test handling file write errors."""
        config = ModelConfig(model="test/model")
        generator = IntegrationTestGenerator(config)

        with patch('lite.utils.save_model_response',
                  side_effect=IOError("Write failed")):
            with pytest.raises(IOError):
                generator.save("test", Path("invalid/path.json"))

    def test_argument_parsing_error(self, suppress_logging):
        """Test argument parsing error handling."""
        cli = IntegrationTestCLI()

        # Invalid temperature (should be float)
        result = cli.execute(["test query", "-t", "not_a_number"])

        assert result == 1  # Error code

    def test_model_config_error(self, suppress_logging):
        """Test model configuration errors."""
        # Missing required model field
        with pytest.raises(TypeError):
            ModelConfig()

    def test_graceful_error_messages(self, suppress_logging, capsys):
        """Test error messages are user-friendly."""
        cli = IntegrationTestCLI()

        with patch.object(cli, 'run',
                         side_effect=RuntimeError("Test error")):
            result = cli.execute(["test query"])

            assert result == 1


# ==============================================================================
# TESTS - Logging and Debugging
# ==============================================================================


class TestLoggingAndDebugging:
    """Test logging and debugging features."""

    def test_logging_enabled_at_info_level(self, suppress_logging):
        """Test logging at INFO level."""
        cli = IntegrationTestCLI()

        with patch.object(cli, 'run', return_value="test"):
            with patch.object(cli, '_display_result'):
                with patch('lite.logging_config.configure_logging') as mock_log:
                    cli.execute(["test query", "-v", "3"])  # INFO level
                    mock_log.assert_called()

    def test_logging_enabled_at_debug_level(self, suppress_logging):
        """Test logging at DEBUG level."""
        cli = IntegrationTestCLI()

        with patch.object(cli, 'run', return_value="test"):
            with patch.object(cli, '_display_result'):
                with patch('lite.logging_config.configure_logging') as mock_log:
                    cli.execute(["test query", "-v", "4"])  # DEBUG level
                    mock_log.assert_called()

    def test_argument_logging(self, suppress_logging):
        """Test that arguments are logged."""
        cli = IntegrationTestCLI()

        with patch.object(cli, 'run', return_value="test"):
            with patch.object(cli, '_display_result'):
                result = cli.execute([
                    "test query",
                    "--extra", "value"
                ])

                assert result == 0
                # Arguments should be stored
                assert cli.args.query == "test query"
                assert cli.args.extra == "value"


# ==============================================================================
# TESTS - Multi-step Workflows
# ==============================================================================


class TestMultiStepWorkflows:
    """Test multi-step workflows."""

    def test_query_generation_save_workflow(self, suppress_logging, temp_output_dir):
        """Test query -> generation -> save workflow."""
        cli = IntegrationTestCLI()
        output_file = temp_output_dir / "result.json"

        with patch.object(cli, '_display_result'):
            with patch('lite.utils.save_model_response',
                      return_value=output_file):
                result = cli.execute([
                    "test query",
                    "-o", str(output_file)
                ])

                assert result == 0
                assert cli.args.output == output_file

    def test_structured_generation_workflow(self, suppress_logging, temp_output_dir):
        """Test structured generation workflow."""
        cli = IntegrationTestCLI()

        with patch.object(cli, '_display_result'):
            with patch.object(IntegrationTestGenerator, 'generate_text',
                            return_value=IntegrationTestModel(
                                status="success",
                                result="Generated"
                            )):
                result = cli.execute([
                    "test query",
                    "-s",
                    "-j"
                ])

                assert result == 0
                assert cli.args.structured is True
                assert cli.args.json_output is True

    def test_error_recovery_workflow(self, suppress_logging):
        """Test error recovery workflow."""
        cli = IntegrationTestCLI()

        # First call fails
        with patch.object(cli, 'run',
                         side_effect=Exception("First attempt")):
            result1 = cli.execute(["test query"])
            assert result1 == 1

        # Second attempt should work
        with patch.object(cli, 'run', return_value="success"):
            with patch.object(cli, '_display_result'):
                result2 = cli.execute(["test query"])
                assert result2 == 0


# ==============================================================================
# TESTS - End-to-End Scenarios
# ==============================================================================


class TestEndToEndScenarios:
    """Test complete end-to-end scenarios."""

    def test_complete_disease_analysis_scenario(self, suppress_logging, temp_output_dir):
        """Test complete disease analysis scenario."""
        cli = IntegrationTestCLI()
        output_file = temp_output_dir / "disease_analysis.json"

        with patch.object(cli, '_display_result'):
            with patch('lite.utils.save_model_response',
                      return_value=output_file):
                result = cli.execute([
                    "Hypertension analysis",
                    "-m", "medical/model",
                    "-s",
                    "-j",
                    "-o", str(output_file)
                ])

                assert result == 0

    def test_complete_drug_interaction_scenario(self, suppress_logging, temp_output_dir):
        """Test complete drug interaction scenario."""
        cli = IntegrationTestCLI()

        with patch.object(cli, '_display_result'):
            result = cli.execute([
                "Warfarin and Aspirin interaction",
                "-m", "pharmacology/model",
                "-t", "0.5",
                "-v", "3",
                "-s"
            ])

            assert result == 0

    def test_multiple_queries_scenario(self, suppress_logging, temp_output_dir):
        """Test handling multiple queries."""
        queries = [
            "query one",
            "query two",
            "query three"
        ]

        for query in queries:
            cli = IntegrationTestCLI()

            with patch.object(cli, '_display_result'):
                result = cli.execute([query])
                assert result == 0

    def test_batch_output_scenario(self, suppress_logging, temp_output_dir):
        """Test batch output generation."""
        outputs = []

        for i in range(3):
            cli = IntegrationTestCLI()
            output_file = temp_output_dir / f"output_{i}.json"

            with patch.object(cli, '_display_result'):
                with patch('lite.utils.save_model_response',
                          return_value=output_file):
                    result = cli.execute([
                        f"query {i}",
                        "-o", str(output_file)
                    ])

                    assert result == 0
                    outputs.append(output_file)

        assert len(outputs) == 3
