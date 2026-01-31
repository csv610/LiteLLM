"""Pytest configuration and shared fixtures for MedKit test suite.

This module provides:
1. Mock classes for LiteClient and related dependencies
2. Fixture functions for common test data and configurations
3. Test utilities for assertions and comparisons
"""

import sys
import logging
from pathlib import Path
from unittest.mock import patch
from typing import Any, Dict, Optional

import pytest
from pydantic import BaseModel

# Add project paths
LITE_ROOT = Path(__file__).parent.parent.parent.parent
if str(LITE_ROOT) not in sys.path:
    sys.path.insert(0, str(LITE_ROOT))


# ==============================================================================
# MOCK CLASSES
# ==============================================================================


class MockModelResponse(BaseModel):
    """Mock response model for testing structured outputs."""
    status: str
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


class MockLiteClient:
    """Mock LiteClient for testing without API calls.

    Simulates LiteClient behavior without making actual LLM calls.
    Can be configured to return different responses for different inputs.
    """

    def __init__(self, model_config=None):
        """Initialize mock client."""
        self.model_config = model_config
        self.call_count = 0
        self.last_model_input = None
        self.responses = {}
        self.default_response = "Mock LLM Response"
        self.should_raise_error = False
        self.error_to_raise = Exception("Mock LLM Error")

    def set_response(self, key: str, response: Any) -> None:
        """Set a response for specific input."""
        self.responses[key] = response

    def set_default_response(self, response: Any) -> None:
        """Set default response for unmapped inputs."""
        self.default_response = response

    def set_error_mode(self, should_raise: bool = True,
                      error: Optional[Exception] = None) -> None:
        """Configure error mode for testing error handling."""
        self.should_raise_error = should_raise
        if error:
            self.error_to_raise = error

    def generate_text(self, model_input=None, model_config=None):
        """Mock generate_text method."""
        self.call_count += 1
        self.last_model_input = model_input

        if self.should_raise_error:
            raise self.error_to_raise

        if model_input and hasattr(model_input, 'user_prompt'):
            prompt_key = model_input.user_prompt[:50]
            if prompt_key in self.responses:
                return self.responses[prompt_key]

        return self.default_response

    @staticmethod
    def create_message(model_input):
        """Mock create_message method."""
        return [{"role": "user", "content": model_input.user_prompt}]

    def reset(self) -> None:
        """Reset mock state."""
        self.call_count = 0
        self.last_model_input = None
        self.responses = {}
        self.should_raise_error = False


class MockFileSystem:
    """Mock file system for testing file operations."""

    def __init__(self):
        """Initialize mock filesystem."""
        self.files: Dict[str, str] = {}
        self.directories: set = {Path("outputs")}
        self.write_count = 0
        self.read_count = 0

    def write_file(self, path: Path, content: str) -> None:
        """Simulate file write."""
        self.files[str(path)] = content
        self.write_count += 1

    def read_file(self, path: Path) -> str:
        """Simulate file read."""
        self.read_count += 1
        if str(path) not in self.files:
            raise FileNotFoundError(f"File not found: {path}")
        return self.files[str(path)]

    def file_exists(self, path: Path) -> bool:
        """Check if file exists."""
        return str(path) in self.files

    def dir_exists(self, path: Path) -> bool:
        """Check if directory exists."""
        return str(path) in self.directories

    def create_dir(self, path: Path) -> None:
        """Create directory."""
        self.directories.add(str(path))

    def reset(self) -> None:
        """Reset mock filesystem."""
        self.files = {}
        self.directories = {Path("outputs")}
        self.write_count = 0
        self.read_count = 0


# ==============================================================================
# FIXTURES - Configuration and Logging
# ==============================================================================


@pytest.fixture
def temp_output_dir(tmp_path):
    """Provide a temporary output directory for test files."""
    output_dir = tmp_path / "outputs"
    output_dir.mkdir(exist_ok=True)
    return output_dir


@pytest.fixture
def capture_logs():
    """Capture log output for testing logging behavior."""
    log_records = []

    class TestHandler(logging.Handler):
        def emit(self, record):
            log_records.append(record)

    handler = TestHandler()
    logger = logging.getLogger()
    logger.addHandler(handler)

    yield log_records

    logger.removeHandler(handler)


@pytest.fixture
def suppress_logging():
    """Suppress logging during tests for cleaner output."""
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)


# ==============================================================================
# FIXTURES - Mock Clients and Dependencies
# ==============================================================================


@pytest.fixture
def mock_lite_client():
    """Provide a mock LiteClient for testing."""
    return MockLiteClient()


@pytest.fixture
def mock_file_system():
    """Provide a mock filesystem for testing file operations."""
    return MockFileSystem()


@pytest.fixture
def mock_model_config():
    """Provide a mock ModelConfig for testing."""
    from lite.config import ModelConfig
    return ModelConfig(model="test/model", temperature=0.7)


@pytest.fixture
def mock_model_input():
    """Provide a mock ModelInput for testing."""
    from lite.config import ModelInput
    return ModelInput(
        system_prompt="You are a test assistant.",
        user_prompt="Test question?"
    )


# ==============================================================================
# FIXTURES - Sample Test Data
# ==============================================================================


@pytest.fixture
def sample_disease_data():
    """Provide sample disease information data."""
    return {
        "name": "Hypertension",
        "description": "A chronic condition with elevated blood pressure.",
        "symptoms": ["Headaches", "Dizziness", "Chest pain"],
        "causes": ["Genetics", "Obesity", "Stress"],
        "treatment": "Medications and lifestyle changes"
    }


@pytest.fixture
def sample_drug_data():
    """Provide sample drug information data."""
    return {
        "name": "Metformin",
        "type": "Antidiabetic",
        "indication": "Type 2 Diabetes",
        "dosage": "500mg-2000mg daily",
        "side_effects": ["Nausea", "Diarrhea"],
        "contraindications": ["Kidney disease", "Heart failure"]
    }


@pytest.fixture
def sample_interaction_data():
    """Provide sample drug interaction data."""
    return {
        "drug1": "Warfarin",
        "drug2": "Aspirin",
        "severity": "High",
        "interaction_type": "Pharmacodynamic",
        "mechanism": "Increased bleeding risk",
        "recommendations": "Monitor INR levels closely"
    }


@pytest.fixture
def sample_structured_response():
    """Provide sample structured response model."""
    return MockModelResponse(
        status="success",
        data={
            "analysis": "Test analysis",
            "findings": ["Finding 1", "Finding 2"]
        },
        metadata={"source": "test", "version": "1.0"}
    )


# ==============================================================================
# FIXTURES - CLI Argument Sets
# ==============================================================================


@pytest.fixture
def basic_cli_args():
    """Provide basic CLI arguments for testing."""
    return [
        "-m", "test/model",
        "-t", "0.7",
        "-v", "2"
    ]


@pytest.fixture
def disease_cli_args():
    """Provide disease CLI arguments for testing."""
    return [
        "Hypertension",
        "-m", "test/model",
        "-t", "0.7",
        "-v", "2",
        "-s"  # structured output
    ]


@pytest.fixture
def drug_interaction_cli_args():
    """Provide drug interaction CLI arguments for testing."""
    return [
        "Warfarin",
        "Aspirin",
        "-m", "test/model",
        "-t", "0.7",
        "-a", "65",
        "-v", "2"
    ]


@pytest.fixture
def medicine_cli_args():
    """Provide medicine CLI arguments for testing."""
    return [
        "Aspirin",
        "-m", "test/model",
        "-t", "0.7",
        "-v", "2",
        "-j"  # json output
    ]


# ==============================================================================
# FIXTURES - Context Managers and Patches
# ==============================================================================


@pytest.fixture
def mock_liteclient_patch(mock_lite_client):
    """Patch LiteClient globally for tests."""
    with patch('lite.lite_client.LiteClient', return_value=mock_lite_client):
        yield mock_lite_client


@pytest.fixture
def mock_save_function():
    """Mock the save_model_response function."""
    with patch('lite.utils.save_model_response') as mock_save:
        mock_save.return_value = Path("test_output.json")
        yield mock_save


@pytest.fixture
def mock_path_mkdir(tmp_path):
    """Mock Path.mkdir to use temp directory."""
    original_mkdir = Path.mkdir

    def mock_mkdir(self, *args, **kwargs):
        # Only use actual mkdir for temp paths
        if str(tmp_path) in str(self):
            original_mkdir(self, *args, **kwargs)

    with patch.object(Path, 'mkdir', mock_mkdir):
        yield


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================


def assert_valid_cli_args(args):
    """Assert that CLI arguments are valid."""
    assert isinstance(args, list), "Arguments should be a list"
    assert all(isinstance(arg, str) for arg in args), "All args should be strings"


def assert_model_response(response, expected_type=None):
    """Assert that a model response is valid."""
    assert response is not None, "Response should not be None"

    if expected_type is not None:
        assert isinstance(response, expected_type), \
            f"Response should be {expected_type.__name__}, got {type(response).__name__}"


def assert_file_operations(mock_fs, min_writes=1, min_reads=0):
    """Assert expected file operations occurred."""
    assert mock_fs.write_count >= min_writes, \
        f"Expected at least {min_writes} writes, got {mock_fs.write_count}"
    assert mock_fs.read_count >= min_reads, \
        f"Expected at least {min_reads} reads, got {mock_fs.read_count}"


def create_test_model(*args, **kwargs) -> MockModelResponse:
    """Create a test model instance."""
    return MockModelResponse(
        status="success",
        data={"test": "data"},
        **kwargs
    )


# ==============================================================================
# PYTEST HOOKS AND CONFIGURATION
# ==============================================================================


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


# Suppress debug logging during tests by default
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("litellm").setLevel(logging.WARNING)
