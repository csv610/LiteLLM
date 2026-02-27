# MedKit Privacy & Compliance Module

The `medkit_privacy` module provides a state-of-the-art framework for ensuring HIPAA-compliant handling of sensitive mental health data. It leverages Large Language Models (LLMs) to provide context-aware PII detection and enforces strict regulatory standards for data security and auditing.

## Key Features

- **Exclusively LLM-Based PII Detection**: Uses `ollama/gemma3` for high-fidelity, context-aware identification of sensitive information, far surpassing traditional regex-based methods.
- **HIPAA Safe Harbor Compliance**: Explicitly trained to identify all 18 HIPAA identifiers, including:
  - Nuanced geographical de-identification (Zip code rules).
  - Specialized date handling for individuals age 90+.
  - Comprehensive identification of names, MRNs, SSNs, and more.
- **Structured Pydantic Output**: Utilizes Pydantic models for type-safe, validated PII detection and index correction.
- **Secure Audit Logging**: Maintains a detailed audit trail with a mandatory 7-year retention policy.
- **Data Security**: Enforced file-system permissions (`0o700` directories, `0o600` files) for all patient data.

## Architecture

The module follows the Single Responsibility Principle, decomposing compliance tasks into focused services orchestrated by a central `PrivacyManager`:

- **`PIIDetector`**: The LLM engine for structured PII identification.
- **`PIIMasker`**: Coordinates with the detector to redact sensitive text.
- **`AuditLogger`**: Manages secure, long-term compliance logs.
- **`SessionRepository`**: Handles encrypted-grade storage for chat sessions.

## Quick Start

### Programmatic Usage

```python
from medkit_privacy.privacy_compliance import PrivacyManager

# Initialize the manager (defaults to ollama/gemma3)
manager = PrivacyManager()

# Mask sensitive data in a clinical note
note = "Patient Jane Doe (DOB: 05/12/1985) lives at 123 Maple Ave."
masked_note = manager.mask_pii(note)
# Result: "Patient [NAME] ([DATE]) lives at [LOCATION]."

# Log a HIPAA-compliant audit event
manager.log_audit_event(
    session_id="session-123",
    action="DATA_ACCESS",
    details=f"Processed note: {masked_note}"
)
```

### CLI Commands

- **Detect PII (JSON output)**:
  ```bash
  python privacy_cli.py detect "My name is Alexander Hamilton"
  ```
- **Mask PII in Text**:
  ```bash
  python privacy_cli.py mask "Contact me at 555-0199"
  ```
- **Generate Compliance Report**:
  ```bash
  python privacy_cli.py report
  ```

## Examples & Assets

Explore the `assets/` folder for practical implementation guides:
- `pii_sample_input.txt`: Sample clinical text for testing.
- `sample_session.json`: Reference structure for patient records.
- `example_workflow.py`: A complete Python script demonstrating the full module lifecycle.

## Security Standards

- **Retention**: Chat Sessions (1 year), Audit Logs (7 years).
- **Access Control**: User-only read/write permissions for all stored PHI.
- **PII Redaction**: All text must be masked before being stored in audit logs.
