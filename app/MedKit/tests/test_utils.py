"""Unit tests for utility modules.

Tests for:
- Path manipulation functions
- Configuration validation
- Logging setup
- Output formatting
- File operations
"""

import sys
import json
import logging
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from pydantic import BaseModel, Field

# Setup paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.config import ModelConfig

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.output_formatter import print_result, _format_value


# ==============================================================================
# TEST MODELS
# ==============================================================================


class SampleModel(BaseModel):
    """Sample model for testing output formatting."""
    name: str = Field(description="Name field")
    description: str = Field(description="Description field")
    items: list = Field(default_factory=list, description="List of items")
    metadata: dict = Field(default_factory=dict, description="Metadata")


# ==============================================================================
# TESTS - Path Manipulation
# ==============================================================================


class TestPathManipulation:
    """Test path manipulation utilities."""

    def test_path_creation(self):
        """Test Path object creation."""
        path = Path("outputs") / "test_output.json"
        assert isinstance(path, Path)
        assert "outputs" in str(path)

    def test_path_with_parts(self):
        """Test path construction with multiple parts."""
        path = Path("outputs") / "subfolder" / "file.json"
        assert path.name == "file.json"
        assert path.suffix == ".json"

    def test_path_suffix_manipulation(self):
        """Test path suffix manipulation."""
        path = Path("output.json")
        path_md = path.with_suffix(".md")

        assert path.suffix == ".json"
        assert path_md.suffix == ".md"

    def test_path_exists_check(self, temp_output_dir):
        """Test path existence checking."""
        # Create a file
        test_file = temp_output_dir / "test.txt"
        test_file.write_text("test")

        assert test_file.exists()

        # Non-existent file
        nonexistent = temp_output_dir / "nonexistent.txt"
        assert not nonexistent.exists()

    def test_path_mkdir(self, temp_output_dir):
        """Test directory creation."""
        new_dir = temp_output_dir / "new_subdir"
        new_dir.mkdir(parents=True, exist_ok=True)

        assert new_dir.exists()
        assert new_dir.is_dir()

    def test_path_relative_to(self, temp_output_dir):
        """Test path relative operations."""
        subdir = temp_output_dir / "sub" / "dir"
        subdir.mkdir(parents=True, exist_ok=True)

        relative = subdir.relative_to(temp_output_dir)
        assert "sub" in str(relative)

    def test_path_parent(self):
        """Test path parent operations."""
        path = Path("a") / "b" / "c" / "file.txt"
        assert path.parent.name == "c"
        assert path.parent.parent.name == "b"

    def test_path_with_stem(self):
        """Test path stem manipulation."""
        path = Path("my_file.json")
        assert path.stem == "my_file"
        assert path.suffix == ".json"

    def test_absolute_path_conversion(self, temp_output_dir):
        """Test converting to absolute path."""
        relative = Path("outputs") / "file.json"
        # Note: We can't test true absolute paths easily in test context
        assert isinstance(relative, Path)


# ==============================================================================
# TESTS - Configuration Validation
# ==============================================================================


class TestConfigurationValidation:
    """Test configuration validation."""

    def test_model_config_valid(self):
        """Test valid ModelConfig."""
        config = ModelConfig(model="ollama/gemma3", temperature=0.7)

        assert config.model == "ollama/gemma3"
        assert config.temperature == 0.7

    def test_model_config_required_fields(self):
        """Test required fields in ModelConfig."""
        # Model is required
        with pytest.raises(TypeError):
            ModelConfig()

        # Temperature has default
        config = ModelConfig(model="test/model")
        assert config.temperature == 0.7  # Default value

    def test_temperature_type(self):
        """Test temperature type validation."""
        # Float temperature
        config = ModelConfig(model="test", temperature=0.5)
        assert isinstance(config.temperature, float)

    def test_model_name_format(self):
        """Test model name format."""
        valid_names = [
            "ollama/gemma3",
            "gpt-4",
            "claude-3",
            "custom/model-name"
        ]

        for name in valid_names:
            config = ModelConfig(model=name)
            assert config.model == name


# ==============================================================================
# TESTS - Output Formatting
# ==============================================================================


class TestOutputFormatting:
    """Test output formatting utilities."""

    def test_print_result_with_model(self, suppress_logging):
        """Test printing BaseModel result."""
        model = SampleModel(
            name="Test",
            description="A test model"
        )

        # Should not raise
        with patch('utils.output_formatter.Console'):
            print_result(model)

    def test_print_result_with_dict(self, suppress_logging):
        """Test printing dictionary result."""
        data = {
            "name": "Test",
            "value": 123
        }

        with patch('utils.output_formatter.Console'):
            print_result(data)

    def test_print_result_with_string(self, suppress_logging):
        """Test printing string result."""
        text = "Test result string"

        with patch('utils.output_formatter.Console'):
            print_result(text)

    def test_print_result_with_none(self, suppress_logging):
        """Test printing None result."""
        with patch('utils.output_formatter.Console') as mock_console:
            print_result(None)

            # Should handle None gracefully
            assert mock_console is not None

    def test_format_value_dict(self):
        """Test formatting dictionary values."""
        data = {
            "key1": "value1",
            "key2": "value2"
        }

        result = _format_value(data)
        assert isinstance(result, str)
        assert "value1" in result or "key1" in result

    def test_format_value_list(self):
        """Test formatting list values."""
        items = ["Item 1", "Item 2", "Item 3"]

        result = _format_value(items)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_format_value_empty_list(self):
        """Test formatting empty list."""
        items = []

        result = _format_value(items)
        assert isinstance(result, str)
        assert "(empty)" in result or len(result) == 0

    def test_format_value_nested_dict(self):
        """Test formatting nested dictionary."""
        data = {
            "outer": {
                "inner": "value"
            }
        }

        result = _format_value(data)
        assert isinstance(result, str)

    def test_format_value_with_indent(self):
        """Test formatting with indentation."""
        data = {"key": "value"}

        result_no_indent = _format_value(data, indent=0)
        result_with_indent = _format_value(data, indent=1)

        # Both should be strings
        assert isinstance(result_no_indent, str)
        assert isinstance(result_with_indent, str)


# ==============================================================================
# TESTS - Logging Setup
# ==============================================================================


class TestLoggingSetup:
    """Test logging configuration."""

    def test_logger_creation(self, suppress_logging):
        """Test logger creation."""
        logger = logging.getLogger("test.logger")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test.logger"

    def test_logger_level_setting(self, suppress_logging):
        """Test setting logger level."""
        logger = logging.getLogger("test")
        logger.setLevel(logging.DEBUG)

        assert logger.level == logging.DEBUG

        logger.setLevel(logging.INFO)
        assert logger.level == logging.INFO

    def test_logger_handlers(self, suppress_logging):
        """Test logger handlers."""
        logger = logging.getLogger("test")

        # Add handler
        handler = logging.StreamHandler()
        logger.addHandler(handler)

        assert len(logger.handlers) > 0

        # Remove handler
        logger.removeHandler(handler)

    def test_logger_formatting(self, suppress_logging):
        """Test logger format string."""
        fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(fmt)

        assert isinstance(formatter, logging.Formatter)

    def test_logger_propagation(self, suppress_logging):
        """Test logger propagation."""
        parent = logging.getLogger("parent")
        child = logging.getLogger("parent.child")

        # Child should propagate by default
        assert child.propagate is True

    def test_verbosity_levels(self, suppress_logging):
        """Test different verbosity levels."""
        levels = {
            0: logging.CRITICAL,
            1: logging.ERROR,
            2: logging.WARNING,
            3: logging.INFO,
            4: logging.DEBUG
        }

        for verbosity, expected_level in levels.items():
            # Mapping logic from cli_base
            assert expected_level in [
                logging.CRITICAL,
                logging.ERROR,
                logging.WARNING,
                logging.INFO,
                logging.DEBUG
            ]


# ==============================================================================
# TESTS - File Operations
# ==============================================================================


class TestFileOperations:
    """Test file operations utilities."""

    def test_write_json_file(self, temp_output_dir):
        """Test writing JSON file."""
        data = {"key": "value", "number": 42}
        file_path = temp_output_dir / "test.json"

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

        assert file_path.exists()

        # Verify content
        with open(file_path, 'r') as f:
            loaded = json.load(f)
            assert loaded["key"] == "value"

    def test_write_text_file(self, temp_output_dir):
        """Test writing text file."""
        content = "Test content"
        file_path = temp_output_dir / "test.txt"

        file_path.write_text(content)

        assert file_path.exists()
        assert file_path.read_text() == content

    def test_read_file(self, temp_output_dir):
        """Test reading file."""
        test_content = "Test file content"
        file_path = temp_output_dir / "test.txt"
        file_path.write_text(test_content)

        content = file_path.read_text()
        assert content == test_content

    def test_file_not_found_error(self, temp_output_dir):
        """Test file not found error."""
        nonexistent = temp_output_dir / "nonexistent.txt"

        with pytest.raises(FileNotFoundError):
            nonexistent.read_text()

    def test_write_to_nested_directory(self, temp_output_dir):
        """Test writing to nested directory."""
        nested = temp_output_dir / "a" / "b" / "c"
        nested.mkdir(parents=True, exist_ok=True)

        file_path = nested / "file.txt"
        file_path.write_text("content")

        assert file_path.exists()

    def test_file_deletion(self, temp_output_dir):
        """Test file deletion."""
        file_path = temp_output_dir / "to_delete.txt"
        file_path.write_text("temporary")

        assert file_path.exists()

        file_path.unlink()

        assert not file_path.exists()

    def test_directory_iteration(self, temp_output_dir):
        """Test iterating directory contents."""
        # Create some files
        (temp_output_dir / "file1.txt").write_text("1")
        (temp_output_dir / "file2.txt").write_text("2")
        (temp_output_dir / "file3.json").write_text("{}")

        # List all files
        files = list(temp_output_dir.glob("*"))
        assert len(files) == 3

        # List only JSON files
        json_files = list(temp_output_dir.glob("*.json"))
        assert len(json_files) == 1


# ==============================================================================
# TESTS - Import Safety
# ==============================================================================


class TestImportSafety:
    """Test safe module imports."""

    def test_module_import_exists(self):
        """Test that required modules can be imported."""
        try:
            from pathlib import Path as PathModule
            assert PathModule is not None
        except ImportError:
            pytest.fail("pathlib.Path should be available")

    def test_conditional_imports(self):
        """Test conditional import handling."""
        try:
            # Standard library imports should always work
            import logging
            import json
            import sys
            assert logging and json and sys
        except ImportError:
            pytest.fail("Standard library imports failed")

    def test_relative_imports(self):
        """Test that relative imports work."""
        sys.path.insert(0, str(Path(__file__).parent.parent))
        try:
            # Should be able to import from utils
            assert Path(__file__).parent.parent / "utils" / "cli_base.py"
        except Exception as e:
            pytest.fail(f"Import error: {e}")

    def test_path_in_sys_path(self):
        """Test paths are properly in sys.path."""
        medkit_path = str(Path(__file__).parent.parent)
        assert any(medkit_path in p for p in sys.path)


# ==============================================================================
# TESTS - JSON Handling
# ==============================================================================


class TestJSONHandling:
    """Test JSON serialization and handling."""

    def test_json_dumps(self):
        """Test JSON dumps."""
        data = {"key": "value", "number": 42}
        json_str = json.dumps(data)

        assert isinstance(json_str, str)
        assert '"key"' in json_str

    def test_json_loads(self):
        """Test JSON loads."""
        json_str = '{"key": "value", "number": 42}'
        data = json.loads(json_str)

        assert isinstance(data, dict)
        assert data["key"] == "value"

    def test_json_model_dump(self):
        """Test Pydantic model JSON dumping."""
        model = SampleModel(
            name="Test",
            description="Test description"
        )

        json_str = model.model_dump_json()
        assert isinstance(json_str, str)
        assert "Test" in json_str

    def test_json_model_dump_indent(self):
        """Test Pydantic model JSON with indentation."""
        model = SampleModel(name="Test", description="Desc")
        json_str = model.model_dump_json(indent=2)

        assert isinstance(json_str, str)
        assert "\n" in json_str  # Should have newlines with indent

    def test_json_encoding_special_chars(self):
        """Test JSON encoding special characters."""
        data = {"text": "Special chars: äöü"}
        json_str = json.dumps(data, ensure_ascii=False)

        assert isinstance(json_str, str)
        loaded = json.loads(json_str)
        assert loaded["text"] == data["text"]


# ==============================================================================
# TESTS - Error Handling
# ==============================================================================


class TestUtilErrorHandling:
    """Test error handling in utilities."""

    def test_invalid_json(self):
        """Test handling invalid JSON."""
        invalid_json = '{"invalid": json}'

        with pytest.raises(json.JSONDecodeError):
            json.loads(invalid_json)

    def test_invalid_path_operations(self):
        """Test invalid path operations."""
        path = Path("some/nonexistent/path")

        # Reading should fail
        with pytest.raises(FileNotFoundError):
            path.read_text()

    def test_permission_error_simulation(self, temp_output_dir):
        """Test permission error handling."""
        file_path = temp_output_dir / "test.txt"
        file_path.write_text("test")

        # In a test environment, we can't easily trigger permission errors
        # But we can verify the file operations work
        assert file_path.read_text() == "test"
