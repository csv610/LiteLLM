# MedKit Privacy & Compliance Module

The `medkit_privacy` module provides a state-of-the-art framework for HIPAA and GDPR-compliant handling of sensitive mental health data. It leverages Large Language Models (LLMs) to provide context-aware PII detection and enforces strict regulatory standards for data security, de-identification, and anonymization.

## Core Modules

### 1. `Deidentifier` (HIPAA Safe Harbor)
Provides high-level API for HIPAA-compliant de-identification.
- **Text De-identification**: Removes all 18 HIPAA identifiers with standardized masking.
- **Structured Record De-identification**: Recursively masks patient information in JSON-like structures.
- **Safe Harbor Compliance**: Specifically tuned for the US Department of Health and Human Services standards.

### 2. `Anonymizer` (GDPR Irreversibility)
Provides stricter, irreversible data cleaning for GDPR compliance.
- **Generalization**: Buckets specific ages into decade ranges (e.g., "age 24" becomes "age 20-30").
- **Suppression**: Identifies and removes unique characteristics (`INDIRECT_ID`) to prevent "jigsaw identification."
- **Noise Addition**: Implements basic Laplace-style noise for privacy-preserving numerical data.

### 3. `PIIDetector` & `PIIMasker`
The underlying LLM-based engines (`ollama/gemma3`) for context-aware identification of names, dates, locations, and sensitive personal categories (political, religious, etc.).

## Quick Start

### De-identification (HIPAA)
```python
from medkit_privacy.deidentification import Deidentifier

deidentifier = Deidentifier()
masked_note = deidentifier.deidentify_text("Patient Jane Doe (DOB: 05/12/1985) lives at 123 Maple Ave.")
# Result: "Patient [NAME] ([DATE]) lives at [LOCATION]."
```

### Anonymization (GDPR)
```python
from medkit_privacy.anonymization import Anonymizer

anonymizer = Anonymizer()
anonymized_note = anonymizer.anonymize_text("Patient is age 24 and the only left-handed Treasury Secretary.")
# Result: "REDACTED is age 20-30 and [DE-IDENTIFIED CHARACTERISTIC]."
```

## Examples & Assets

Explore the `assets/` folder for practical implementation guides:
- `example_deidentification.py`: HIPAA-compliant de-identification workflow.
- `example_anonymization.py`: GDPR-compliant anonymization and noise addition.
- `example_workflow.py`: A complete script demonstrating the full module lifecycle.

## Security Standards

- **Retention**: Chat Sessions (1 year), Audit Logs (7 years).
- **Access Control**: User-only read/write permissions for all stored PHI.
- **PII Redaction**: All text must be masked or anonymized before being stored in audit logs.
