# Medical Images

This module classifies medical images and stores the result in a structured format.

## Files

- `med_images.py`: classification logic.
- `med_images_cli.py`: CLI interface.
- `med_images_models.py`: schemas.
- `med_images_prompts.py`: prompts.

## Agentic Approach Integration

This module is designed to be used within the MedKit agentic framework, particularly by the DiagnosticAgent when image analysis is required:

1. **DiagnosticAgent Utilization**: When assessing a patient's condition involves medical imaging, the DiagnosticAgent may need to classify or analyze medical images.
2. **Image Analysis Workflow**: The module provides structured classification results that the DiagnosticAgent can use when:
   - Analyzing radiological images (X-rays, CT scans, MRIs)
   - Classifying pathological specimens
   - Identifying potential abnormalities in medical imagery
3. **Workflow Integration**:
   - User query about medical images → TriageAgent identifies diagnostic need involving imaging
   - DiagnosticAgent engages and may invoke this module for image classification
   - ValidationAgent checks the classification results for consistency with clinical expectations
   - SynthesisAgent incorporates image analysis findings into the final diagnostic report

## Limitations

- Classification accuracy depends on model capability and image quality.
- The module is not a diagnostic device and should not guide treatment decisions.
