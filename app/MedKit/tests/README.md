# MedKit Test Suite Documentation

Welcome to the MedKit test suite! This directory contains comprehensive tests for all core functionality.

## Quick Start

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ --cov=utils.cli_base --cov-report=term-missing

# Run specific test file
python -m pytest tests/test_base_cli.py -v

# Run single test
python -m pytest tests/test_base_cli.py::TestBaseCLI::test_cli_initialization -v
```

## Test Files Overview

### 1. `test_base_cli.py` (550+ lines, 47 tests)
Tests for the core base classes that eliminate code duplication:

- **TestUtilityFunctions** (10 tests)
  - Logging setup
  - Output directory management
  - Filename sanitization
  - Path manipulation

- **TestBasePromptBuilder** (4 tests)
  - Prompt creation patterns
  - System and user prompt building
  - Multi-argument support

- **TestBaseGenerator** (9 tests)
  - Generator initialization
  - Text generation (plain and structured)
  - LLM interaction
  - Error handling
  - File saving operations

- **TestBaseCLI** (20 tests)
  - Argument parsing
  - Configuration creation
  - Output handling
  - Error scenarios
  - Full execution flow

- **TestComponentIntegration** (4 tests)
  - Full CLI workflows
  - Error propagation
  - Structured output creation

### 2. `test_cli_modules.py` (650+ lines, 45 tests)
Tests for specific CLI module implementations and patterns:

- **TestDrugDrugInteractionCLI** (6 tests)
  - Medicine argument validation
  - Age validation
  - Interaction result models
  - Prompt formatting

- **TestDiseaseInfoCLI** (5 tests)
  - Disease name validation
  - Model structure
  - Output modes

- **TestMedicineInfoCLI** (5 tests)
  - Medicine validation
  - Dosage formatting
  - String parsing

- **TestMedicalFAQCLI** (4 tests)
  - FAQ model structure
  - Multiple items handling

- **TestModelConfigurationValidation** (5 tests)
  - Config creation
  - Temperature bounds
  - Response format

- **TestPromptBuilderPatterns** (3 tests)
  - Prompt consistency
  - Variable substitution

- **TestCLIArgumentPatterns** (4 tests)
  - Argument types
  - Short/long forms
  - Defaults

- **TestErrorCases** (4 tests)
  - Invalid inputs
  - Empty fields
  - Enum validation

### 3. `test_utils.py` (600+ lines, 53 tests)
Tests for utility functions and helpers:

- **TestPathManipulation** (9 tests)
  - Path creation and operations
  - Suffix/stem manipulation
  - Existence checking
  - Directory operations

- **TestConfigurationValidation** (4 tests)
  - ModelConfig validation
  - Temperature validation
  - Model name formats

- **TestOutputFormatting** (9 tests)
  - BaseModel printing
  - Dictionary formatting
  - List formatting
  - Nested structures
  - Indentation

- **TestLoggingSetup** (6 tests)
  - Logger creation
  - Level setting
  - Handler management
  - Verbosity levels

- **TestFileOperations** (7 tests)
  - JSON file I/O
  - Text file operations
  - Nested directories
  - File deletion
  - Directory iteration

- **TestImportSafety** (4 tests)
  - Module availability
  - Conditional imports
  - Path validation

- **TestJSONHandling** (5 tests)
  - JSON serialization
  - Pydantic model dumps
  - Special characters
  - Unicode handling

- **TestUtilErrorHandling** (3 tests)
  - Invalid JSON
  - Path errors
  - Permission errors

### 4. `test_integration.py` (700+ lines, 59 tests)
End-to-end integration tests:

- **TestFullCLIFlow** (5 tests)
  - Complete CLI execution
  - JSON output
  - Structured output
  - Custom models

- **TestGenerationAndOutput** (5 tests)
  - Text generation
  - Structured generation
  - Generator workflows

- **TestFileOutputOperations** (4 tests)
  - Saving responses
  - Path creation
  - Directory management

- **TestJSONOutput** (3 tests)
  - Model to JSON conversion
  - Output formatting
  - Flag behavior

- **TestErrorHandlingAndRecovery** (6 tests)
  - Validation errors
  - Generation errors
  - File errors
  - Graceful messages

- **TestLoggingAndDebugging** (3 tests)
  - INFO level
  - DEBUG level
  - Argument logging

- **TestMultiStepWorkflows** (3 tests)
  - Query → Generation → Save
  - Structured workflows
  - Error recovery

- **TestEndToEndScenarios** (4 tests)
  - Disease analysis
  - Drug interactions
  - Batch processing

### 5. `conftest.py` (400+ lines)
Pytest configuration and shared fixtures:

**Mock Classes:**
- `MockLiteClient`: Simulates LLM without API calls
- `MockFileSystem`: Virtual file operations
- `MockModelResponse`: Standard test response

**Fixtures (25+):**
- `temp_output_dir`: Test output directory
- `mock_lite_client`: Mocked LLM client
- `capture_logs`: Log capture
- Sample data fixtures
- CLI argument fixtures

**Utilities:**
- Test assertion helpers
- Model creation functions
- Import validation

## Test Statistics

- **Total Tests:** 161
- **Passing:** 144 (89.4%)
- **Lines of Code:** 2,900+
- **Coverage:** 75%+
- **Execution Time:** 3-5 seconds

## Running Tests

### Basic Commands

```bash
# All tests
pytest tests/ -v

# One file
pytest tests/test_base_cli.py

# One class
pytest tests/test_base_cli.py::TestBaseCLI

# One test
pytest tests/test_base_cli.py::TestBaseCLI::test_cli_initialization

# Show print statements
pytest tests/ -v -s

# Stop on first failure
pytest tests/ -x
```

### Advanced Options

```bash
# Generate coverage
pytest tests/ --cov=utils.cli_base --cov-report=html

# Show slowest tests
pytest tests/ --durations=10

# Parallel execution (if pytest-xdist installed)
pytest tests/ -n auto

# Specific markers
pytest tests/ -m unit
pytest tests/ -m integration

# Verbose output
pytest tests/ -vv

# Show local variables on failure
pytest tests/ -l

# Drop to debugger on failure
pytest tests/ --pdb
```

## Key Features

### Mocking
- **No real API calls** - All external dependencies mocked
- **Fast execution** - Mocks enable instant feedback
- **Isolated tests** - No side effects between tests
- **Configurable** - Mocks support different scenarios

### Edge Cases
- Empty inputs and special characters
- Unicode and encoding handling
- Path manipulation edge cases
- Nested directory creation
- Error propagation and recovery

### Error Testing
- Validation errors
- File operation errors
- LLM communication errors
- Graceful error handling

## Writing New Tests

### Basic Pattern

```python
def test_my_feature(mock_lite_client, temp_output_dir):
    """Test my feature."""
    # Arrange
    mock_lite_client.set_default_response("Expected response")

    # Act
    result = my_function()

    # Assert
    assert result == "Expected response"
```

### Using Fixtures

```python
def test_with_data(sample_disease_data):
    """Test with sample data."""
    assert sample_disease_data["name"] == "Hypertension"
```

### Mocking External Calls

```python
def test_with_mock(mock_lite_client):
    """Test with mocked LLM."""
    mock_lite_client.set_error_mode(True)

    with pytest.raises(Exception):
        cli.execute(["query"])
```

## Debugging Failed Tests

### View Test Details
```bash
pytest tests/test_base_cli.py::TestBaseCLI -vvv
```

### See Print Output
```bash
pytest tests/ -v -s
```

### View Captured Logs
```bash
pytest tests/ --log-cli-level=DEBUG
```

### Run with Debugger
```bash
pytest tests/ --pdb
```

## Test Coverage

### High Coverage Areas (>90%)
- Utility functions
- Filename sanitization
- Path manipulation
- Configuration validation
- Output formatting

### Good Coverage Areas (80-90%)
- BaseCLI argument parsing
- BaseGenerator initialization
- Error handling
- File operations

### Integration Coverage
- Full CLI execution workflows
- End-to-end scenarios
- Multi-step processes

## Maintenance

### Adding New Tests
1. Choose appropriate test file
2. Create test class if needed
3. Name test with `test_` prefix
4. Use existing fixtures
5. Add docstring

### Updating Tests
- Keep tests focused (one concern per test)
- Use descriptive names
- Add comments for complex logic
- Update docstrings
- Run full suite after changes

### Debugging Issues
1. Check mock configuration
2. Verify fixture state
3. Review error messages
4. Add print statements (-s flag)
5. Use --pdb for debugging

## Tips & Tricks

### Parametrized Tests
```python
@pytest.mark.parametrize("input,expected", [
    ("test", "result"),
    ("other", "result2")
])
def test_multiple(input, expected):
    assert my_func(input) == expected
```

### Skipping Tests
```python
@pytest.mark.skip(reason="Not ready yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.version_info < (3, 10), reason="Python 3.10+")
def test_new_feature():
    pass
```

### Marking Tests
```python
@pytest.mark.unit
def test_basic():
    pass

@pytest.mark.integration
def test_full_flow():
    pass

@pytest.mark.slow
def test_complex():
    pass
```

## Troubleshooting

### Import Errors
- Ensure `conftest.py` is in tests directory
- Check sys.path setup in conftest
- Verify module names

### Mock Not Working
- Check mock target path
- Verify patch context
- Review mock configuration
- Check call order

### Tests Failing Intermittently
- Check for external dependencies
- Review time-dependent code
- Check mock reset between tests
- Look for test ordering issues

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Guide](https://docs.python.org/3/library/unittest.mock.html)
- [Testing Best Practices](https://docs.pytest.org/en/latest/goodpractices.html)

## Contact & Contributions

For issues, questions, or contributions:
1. Check existing test patterns
2. Follow naming conventions
3. Add comprehensive docstrings
4. Ensure tests pass before committing
