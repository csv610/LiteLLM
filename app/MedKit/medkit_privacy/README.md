# MedKit Privacy

This package contains privacy-oriented helpers such as anonymization, de-identification, audit logging, and compliance-related utilities.

## Files

- `privacy_cli.py`: CLI interface.
- `anonymization.py`, `deidentification.py`: text-processing helpers.
- `audit_logger.py`, `session_repository.py`: audit and session support.
- `privacy_compliance.py`, `pii_utils.py`: compliance and PII helpers.

## Why It Matters

Medical workflows often need privacy tooling alongside generation or extraction modules.

## Limitations

- These utilities can reduce risk but do not guarantee regulatory compliance by themselves.
- Local policy and legal review remain necessary.
