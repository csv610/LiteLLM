# Medical Entity Recognizers - Test Suite

## Overview

This directory contains a comprehensive smoke test suite for all medical entity recognizers. These tests verify that:

1. All recognizers can be instantiated correctly
2. All Pydantic models validate properly
3. All prompt builders generate expected output
4. Input validation works correctly
5. The factory registry is properly configured

## Running Tests

### Run all tests:
```bash
python tests/test_recognizers_smoke.py
```

### Run with pytest (optional):
```bash
pytest tests/test_recognizers_smoke.py -v
```

### Test with coverage:
```bash
pytest tests/test_recognizers_smoke.py --cov=app.MedKit.recognizers -v
```

## Test Structure

### Core Infrastructure Tests
- **BaseRecognizer**: Verifies abstract base class cannot be instantiated
- **RecognizerFactory**: Tests factory registry and recognizer creation
- **ModelConfig**: Validates configuration object creation

### Model Tests
Each recognizer has model instantiation tests:
- **Drug models**: `DrugIdentificationModel`, `DrugIdentifierModel`
- **Disease models**: `DiseaseIdentificationModel`, `DiseaseIdentifierModel`
- **Anatomy models**: `MedicalAnatomyIdentificationModel`, `MedicalAnatomyIdentifierModel`
- **Specialty models**: `MedicalSpecialtyIdentificationModel`, `MedicalSpecialtyIdentifierModel`
- **Symptom models**: `MedicalSymptomIdentificationModel`, `MedicalSymptomIdentifierModel`
- **Procedure models**: `MedicalProcedureIdentificationModel`, `MedicalProcedureIdentifierModel`
- **Vaccine models**: `VaccineIdentificationModel`, `VaccineIdentifierModel`
- **Pathogen models**: `PathogenIdentificationModel`, `PathogenIdentifierModel`
- **Clinical Sign models**: `ClinicalSignIdentificationModel`, `ClinicalSignIdentifierModel`

### Integration Tests
- **Prompt Builders**: Tests all prompt builders generate correct output
- **Input Validation**: Tests empty/whitespace input rejection

## Architecture

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Pytest fixtures and configuration
├── test_recognizers_smoke.py # Unified smoke test suite
└── README.md                # This file
```

## Adding New Tests

When adding a new recognizer:

1. Add model instantiation test to `test_recognizers_smoke.py`
2. Add prompt builder test if custom prompts exist
3. Add input validation test if custom validation exists
4. Update the factory test to include the new recognizer

## Design Principles

1. **No external dependencies**: Tests use only Python standard library
2. **No sys.path manipulation**: Proper package imports only
3. **Fast execution**: All tests are local instantiation tests (no API calls)
4. **Clear output**: Test results show ✓ for pass, ✗ for fail with details
5. **Exit codes**: Non-zero exit code on failure for CI/CD integration

## Continuous Integration

These tests are designed for CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run Recognizer Tests
  run: python tests/test_recognizers_smoke.py
```

## Troubleshooting

### Import Errors
If you see `ModuleNotFoundError`:
- Ensure you're running from the `recognizers/` directory
- Check that `__init__.py` files exist in all module directories

### Model Validation Errors
If model tests fail:
- Check the model file for required field changes
- Update the test to match actual model structure

## License

Same as parent project.
