"""Unit tests for base CLI classes.

Tests for:
- BaseCLI: Command-line interface base class
- BaseGenerator: LLM generation base class
- BasePromptBuilder: Prompt creation base class
- Utility functions from cli_base module
"""

import sys
import logging
from pathlib import Path
from unittest.mock import MagicMock, patch


import pytest
from pydantic import BaseModel, Field

# Import after path setup
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.config import ModelInput

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.cli_base import (
    BaseCLI, BaseGenerator, BasePromptBuilder,
    setup_logging, get_logger, ensure_output_dir,
    get_default_output_path, sanitize_filename
)


# ==============================================================================
# TEST MODELS AND HELPERS
# ==============================================================================


class TestPromptBuilder(BasePromptBuilder):
    """Test implementation of BasePromptBuilder."""

    @staticmethod
    def create_system_prompt() -> str:
        return "You are a test assistant."

    @staticmethod
    def create_user_prompt(query: str) -> str:
        return f"Answer this: {query}"


class TestResponse(BaseModel):
    """Test response model."""
    result: str = Field(description="Test result")
    metadata: dict = Field(default_factory=dict, description="Test metadata")


class TestGenerator(BaseGenerator):
    """Test implementation of BaseGenerator."""

    def generate_text(self, query: str, structured: bool = False):
        if structured:
            return TestResponse(result=f"Response to: {query}")
        return f"Response to: {query}"


class TestCLI(BaseCLI):
    """Test implementation of BaseCLI."""

    description = "Test CLI"

    def add_arguments(self, parser):
        parser.add_argument("query", help="Test query")
        parser.add_argument("--custom", default="test", help="Custom argument")

    def validate_args(self):
        if not self.args.query.strip():
            raise ValueError("Query cannot be empty")

    def run(self):
        generator = TestGenerator(self.model_config, self.logger)
        return generator.generate_text(self.args.query, self.args.structured)


# ==============================================================================
# TESTS - UTILITY FUNCTIONS
# ==============================================================================


class TestUtilityFunctions:
    """Test utility functions from cli_base module."""

    def test_setup_logging(self, suppress_logging):
        """Test logging setup."""
        logger = setup_logging("test.module")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test.module"

    def test_get_logger(self, suppress_logging):
        """Test get_logger function."""
        logger = get_logger("test.module", verbose=False)
        assert isinstance(logger, logging.Logger)
        assert logger.level == logging.INFO

    def test_get_logger_verbose(self, suppress_logging):
        """Test get_logger with verbose mode."""
        logger = get_logger("test.module", verbose=True)
        assert logger.level == logging.DEBUG

    def test_ensure_output_dir(self, temp_output_dir):
        """Test output directory creation."""
        test_dir = temp_output_dir / "test_subdir"
        ensure_output_dir(test_dir)
        assert test_dir.exists()

    def test_ensure_output_dir_exists(self, temp_output_dir):
        """Test ensure_output_dir with existing directory."""
        ensure_output_dir(temp_output_dir)
        assert temp_output_dir.exists()

    def test_get_default_output_path(self, temp_output_dir):
        """Test default output path generation."""
        path = get_default_output_path(temp_output_dir, "Test Disease", "info")
        assert path == temp_output_dir / "test_disease_info.json"

    def test_get_default_output_path_custom_suffix(self, temp_output_dir):
        """Test default output path with custom suffix."""
        path = get_default_output_path(temp_output_dir, "Hypertension", "analysis")
        assert path == temp_output_dir / "hypertension_analysis.json"

    def test_sanitize_filename(self):
        """Test filename sanitization."""
        assert sanitize_filename("test<file>") == "testfile"
        assert sanitize_filename("path/to\\file") == "pathtofile"
        assert sanitize_filename("file with spaces") == "file_with_spaces"

    def test_sanitize_filename_empty(self):
        """Test sanitize_filename with empty result."""
        assert sanitize_filename("<>") == "output"

    def test_sanitize_filename_unicode(self):
        """Test sanitize_filename with unicode characters."""
        result = sanitize_filename("file:name?test")
        assert "<" not in result
        assert ">" not in result
        assert ":" not in result
        assert "?" not in result


# ==============================================================================
# TESTS - BasePromptBuilder
# ==============================================================================


class TestBasePromptBuilder:
    """Test BasePromptBuilder class."""

    def test_prompt_builder_implementation(self):
        """Test that BasePromptBuilder can be properly subclassed."""
        assert hasattr(TestPromptBuilder, 'create_system_prompt')
        assert hasattr(TestPromptBuilder, 'create_user_prompt')

    def test_system_prompt_creation(self):
        """Test system prompt creation."""
        prompt = TestPromptBuilder.create_system_prompt()
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert "test" in prompt.lower()

    def test_user_prompt_creation(self):
        """Test user prompt creation."""
        query = "test question"
        prompt = TestPromptBuilder.create_user_prompt(query)
        assert isinstance(prompt, str)
        assert query in prompt

    def test_user_prompt_with_multiple_args(self):
        """Test user prompt with multiple arguments."""
        class MultiArgPromptBuilder(BasePromptBuilder):
            @staticmethod
            def create_system_prompt():
                return "System"

            @staticmethod
            def create_user_prompt(a, b, c="default"):
                return f"{a}-{b}-{c}"

        prompt = MultiArgPromptBuilder.create_user_prompt("x", "y", c="z")
        assert prompt == "x-y-z"


# ==============================================================================
# TESTS - BaseGenerator
# ==============================================================================


class TestBaseGenerator:
    """Test BaseGenerator class."""

    def test_generator_initialization(self, mock_model_config):
        """Test generator initialization."""
        generator = TestGenerator(mock_model_config)
        assert generator.model_config == mock_model_config
        assert generator.client is not None
        assert generator.logger is not None

    def test_generator_with_custom_logger(self, mock_model_config, suppress_logging):
        """Test generator with custom logger."""
        custom_logger = logging.getLogger("custom")
        generator = TestGenerator(mock_model_config, custom_logger)
        assert generator.logger == custom_logger

    def test_generate_text_plain(self, mock_model_config):
        """Test plain text generation."""
        generator = TestGenerator(mock_model_config)
        result = generator.generate_text("test query")
        assert isinstance(result, str)
        assert "test query" in result

    def test_generate_text_structured(self, mock_model_config):
        """Test structured generation."""
        generator = TestGenerator(mock_model_config)
        result = generator.generate_text("test query", structured=True)
        assert isinstance(result, TestResponse)
        assert result.result == "Response to: test query"

    def test_ask_llm_success(self, mock_model_config, suppress_logging):
        """Test successful LLM call."""
        with patch.object(TestGenerator, 'generate_text'):
            generator = TestGenerator(mock_model_config)
            generator.client.generate_text = MagicMock(return_value="Test response")

            model_input = ModelInput(user_prompt="Test prompt")
            result = generator._ask_llm(model_input)

            assert result == "Test response"
            generator.client.generate_text.assert_called_once_with(model_input=model_input)

    def test_ask_llm_error_handling(self, mock_model_config, suppress_logging):
        """Test error handling in _ask_llm."""
        generator = TestGenerator(mock_model_config)
        generator.client.generate_text = MagicMock(
            side_effect=Exception("Test error")
        )

        model_input = ModelInput(user_prompt="Test prompt")

        with pytest.raises(Exception, match="Test error"):
            generator._ask_llm(model_input)

    def test_save_structured_model(self, mock_model_config, temp_output_dir):
        """Test saving structured model response."""
        generator = TestGenerator(mock_model_config)
        response = TestResponse(result="Test result")

        with patch('lite.utils.save_model_response') as mock_save:
            mock_save.return_value = temp_output_dir / "output.json"
            output_path = generator.save(response, temp_output_dir / "output.json")

            assert output_path == temp_output_dir / "output.json"
            mock_save.assert_called_once()

    def test_save_string_response_json_path(self, mock_model_config, temp_output_dir):
        """Test saving string response with JSON path converts to markdown."""
        generator = TestGenerator(mock_model_config)
        response = "Test string response"

        with patch('lite.utils.save_model_response') as mock_save:
            mock_save.return_value = temp_output_dir / "output.md"
            output_path = generator.save(response, temp_output_dir / "output.json")

            # Should convert .json to .md for string responses
            call_args = mock_save.call_args
            assert call_args[0][1].suffix == ".md"

    def test_save_string_response_md_path(self, mock_model_config, temp_output_dir):
        """Test saving string response with markdown path."""
        generator = TestGenerator(mock_model_config)
        response = "Test string response"

        with patch('lite.utils.save_model_response') as mock_save:
            mock_save.return_value = temp_output_dir / "output.md"
            output_path = generator.save(response, temp_output_dir / "output.md")

            call_args = mock_save.call_args
            assert call_args[0][1].suffix == ".md"


# ==============================================================================
# TESTS - BaseCLI
# ==============================================================================


class TestBaseCLI:
    """Test BaseCLI class."""

    def test_cli_initialization(self, suppress_logging):
        """Test CLI initialization."""
        cli = TestCLI()
        assert cli.logger is not None
        assert cli.args is None
        assert cli.model_config is None

    def test_get_argument_parser(self, suppress_logging):
        """Test argument parser creation."""
        cli = TestCLI()
        parser = cli.get_argument_parser()

        assert parser is not None
        # Parse test arguments
        args = parser.parse_args(["test_query", "--custom", "value"])
        assert args.query == "test_query"
        assert args.custom == "value"

    def test_common_arguments_included(self, suppress_logging):
        """Test that common arguments are included."""
        cli = TestCLI()
        parser = cli.get_argument_parser()

        # Parse with common arguments
        args = parser.parse_args([
            "query",
            "-m", "custom/model",
            "-t", "0.5",
            "-v", "4"
        ])

        assert args.model == "custom/model"
        assert args.temperature == 0.5
        assert args.verbosity == 4

    def test_argument_parsing_defaults(self, suppress_logging):
        """Test default argument values."""
        cli = TestCLI()
        parser = cli.get_argument_parser()
        args = parser.parse_args(["test_query"])

        assert args.model == "ollama/gemma3"
        assert args.temperature == 0.7
        assert args.verbosity == 2
        assert args.output_dir == Path("outputs")
        assert args.structured is False
        assert args.json_output is False

    def test_validate_args_called(self, suppress_logging):
        """Test that validate_args is called during execution."""
        cli = TestCLI()

        with patch.object(cli, 'validate_args') as mock_validate:
            with patch.object(cli, 'run', return_value="test"):
                cli.execute(["test_query"])
                mock_validate.assert_called_once()

    def test_validate_args_error_handling(self, suppress_logging):
        """Test validation error handling."""
        cli = TestCLI()

        # Execute with empty query (should fail validation)
        result = cli.execute(["  "])  # Only whitespace

        assert result == 1  # Should return error code

    def test_model_config_creation(self, suppress_logging):
        """Test model configuration creation."""
        cli = TestCLI()

        with patch.object(cli, 'run', return_value="test"):
            with patch.object(cli, '_display_result'):
                cli.execute([
                    "test_query",
                    "-m", "test/model",
                    "-t", "0.5"
                ])

                assert cli.model_config.model == "test/model"
                assert cli.model_config.temperature == 0.5

    def test_get_output_path_explicit(self, suppress_logging, temp_output_dir):
        """Test explicit output path."""
        cli = TestCLI()

        with patch.object(cli, 'run', return_value="test"):
            with patch.object(cli, '_display_result'):
                explicit_output = temp_output_dir / "custom_output.json"
                cli.execute([
                    "test_query",
                    "-o", str(explicit_output)
                ])

                path = cli._get_output_path("test", "info")
                assert path == explicit_output

    def test_get_output_path_default(self, suppress_logging, temp_output_dir):
        """Test default output path generation."""
        cli = TestCLI()

        with patch.object(cli, 'run', return_value="test"):
            with patch.object(cli, '_display_result'):
                cli.execute([
                    "test_query",
                    "-d", str(temp_output_dir)
                ])

                path = cli._get_output_path("Test Disease", "info")
                assert "test_disease_info" in str(path)

    def test_output_json_flag(self, suppress_logging, capsys):
        """Test JSON output flag."""
        cli = TestCLI()

        with patch.object(cli, 'run', return_value=TestResponse(result="test")):
            with patch.object(cli, '_display_result'):
                cli.execute(["test_query", "-j"])

                captured = capsys.readouterr()
                assert "result" in captured.out

    def test_structured_output_flag(self, suppress_logging):
        """Test structured output flag."""
        cli = TestCLI()

        with patch.object(cli, 'run', return_value="test"):
            with patch.object(cli, '_display_result'):
                cli.execute(["test_query", "-s"])

                assert cli.args.structured is True

    def test_execute_success(self, suppress_logging):
        """Test successful execution."""
        cli = TestCLI()

        with patch.object(cli, 'run', return_value="test result"):
            with patch.object(cli, '_display_result'):
                result = cli.execute(["test_query"])

                assert result == 0  # Success code

    def test_execute_none_result(self, suppress_logging):
        """Test execution when generator returns None."""
        cli = TestCLI()

        with patch.object(cli, 'run', return_value=None):
            result = cli.execute(["test_query"])

            assert result == 1  # Error code

    def test_execute_exception_handling(self, suppress_logging):
        """Test exception handling during execution."""
        cli = TestCLI()

        with patch.object(cli, 'run', side_effect=Exception("Test error")):
            result = cli.execute(["test_query"])

            assert result == 1  # Error code

    def test_execute_value_error_handling(self, suppress_logging):
        """Test ValueError handling (validation errors)."""
        cli = TestCLI()

        with patch.object(cli, 'validate_args',
                         side_effect=ValueError("Invalid input")):
            result = cli.execute(["test_query"])

            assert result == 1  # Error code

    def test_temperature_validation(self, suppress_logging):
        """Test temperature argument validation."""
        cli = TestCLI()
        parser = cli.get_argument_parser()

        args = parser.parse_args(["test_query", "-t", "0.3"])
        assert 0 <= args.temperature <= 1

    def test_verbosity_choices(self, suppress_logging):
        """Test verbosity argument choices."""
        cli = TestCLI()
        parser = cli.get_argument_parser()

        # Valid choices
        for v in [0, 1, 2, 3, 4]:
            args = parser.parse_args(["test_query", "-v", str(v)])
            assert args.verbosity == v

    def test_display_result_model(self, suppress_logging):
        """Test displaying BaseModel result."""
        cli = TestCLI()

        with patch('utils.output_formatter.print_result') as mock_print:
            response = TestResponse(result="test")
            cli._display_result(response)

            mock_print.assert_called_once()

    def test_logging_setup(self, suppress_logging):
        """Test logging setup during execution."""
        cli = TestCLI()

        with patch('lite.logging_config.configure_logging') as mock_logging:
            with patch.object(cli, 'run', return_value="test"):
                with patch.object(cli, '_display_result'):
                    cli.execute(["test_query", "-v", "3"])

                    mock_logging.assert_called()


# ==============================================================================
# TESTS - Integration between Components
# ==============================================================================


class TestComponentIntegration:
    """Test integration between BaseCLI and BaseGenerator."""

    def test_full_cli_flow(self, suppress_logging, temp_output_dir):
        """Test full CLI execution flow."""
        cli = TestCLI()

        with patch.object(cli, '_display_result'):
            result = cli.execute([
                "test_query",
                "-m", "test/model",
                "-t", "0.5",
                "-d", str(temp_output_dir)
            ])

            assert result == 0
            assert cli.model_config is not None
            assert cli.args.query == "test_query"

    def test_error_propagation_from_generator(self, suppress_logging):
        """Test error propagation from generator to CLI."""
        cli = TestCLI()

        with patch.object(TestGenerator, 'generate_text',
                         side_effect=RuntimeError("Generation failed")):
            result = cli.execute(["test_query"])

            assert result == 1  # Should handle error gracefully

    def test_structured_output_creation(self, suppress_logging):
        """Test structured output creation."""
        cli = TestCLI()

        with patch.object(cli, '_display_result'):
            with patch.object(TestGenerator, 'generate_text',
                             return_value=TestResponse(result="test")):
                result = cli.execute(["test_query", "-s"])

                assert result == 0
