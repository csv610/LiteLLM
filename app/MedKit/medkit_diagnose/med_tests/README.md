# Medical Tests

This module generates structured descriptions of laboratory or diagnostic tests.

## Files

- `medical_test_info.py`: generation logic.
- `medical_test_info_cli.py`: CLI interface.
- `medical_test_info_models.py`: schemas.
- `medical_test_info_prompts.py`: prompts.

## Why It Matters

Test descriptions often need to combine purpose, specimen, interpretation context, and limitations in a reusable format.

## Agentic Approach Integration

This module is designed to be used within the MedKit agentic framework, particularly by the DiagnosticAgent:

1. **DiagnosticAgent Utilization**: When assessing a patient's condition, the DiagnosticAgent may need to interpret laboratory results or understand diagnostic procedures.
2. **Information Retrieval**: The module provides structured descriptions of tests that the DiagnosticAgent can reference when:
   - Explaining what a particular test measures
   - Describing specimen requirements
   - Providing interpretation context
   - Outlining limitations and considerations
3. **Workflow Integration**:
   - User query about test results → TriageAgent identifies diagnostic need
   - DiagnosticAgent engages and may consult this module for test information
   - ValidationAgent checks the information against current standards
   - SynthesisAgent incorporates test explanations into the final diagnostic report

## Limitations

- Reference ranges and interpretation rules vary by lab, method, and patient context.
- Output should be checked against current clinical references.
