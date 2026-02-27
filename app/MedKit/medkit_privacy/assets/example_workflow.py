"""Example workflow demonstrating the MedKit Privacy & Compliance Manager."""

import json
import os
from medkit_privacy.privacy_compliance import PrivacyManager


def run_example():
    # 1. Initialize the PrivacyManager
    # Data is stored in ~/.medkit/sessions by default with restricted permissions (0o700)
    manager = PrivacyManager()

    # 2. Mock obtaining patient consent
    # In a real app, this would be handled via display_consent_form() or a web UI
    print("--- 1. HIPAA Consent ---")
    print("Capturing informed consent...")
    consent_accepted = True  # Mocked

    if not consent_accepted:
        print("Consent declined. Exiting.")
        return

    # 3. Create and Save a Secure Session
    print("\n--- 2. Session Creation ---")
    session = manager.create_session(patient_name="Jane Doe", age=30, gender="F")
    session.consent_obtained = True
    session.hipaa_acknowledged = True

    session_path = manager.save_session(session)
    print(f"Session saved securely: {session_path}")
    print(f"File permissions: {oct(os.stat(session_path).st_mode & 0o777)}")

    # 4. LLM-Based PII Detection and Masking
    print("\n--- 3. PII Masking (LLM-Based) ---")
    raw_note = (
        "Patient Jane Doe (DOB: 05/12/1995) can be reached at jane.doe@email.com."
    )
    print(f"Original: {raw_note}")

    masked_note = manager.mask_pii(raw_note)
    print(f"Masked:   {masked_note}")

    # 5. Secure Audit Logging
    print("\n--- 4. HIPAA Audit Logging ---")
    manager.log_audit_event(
        session_id=session.session_id,
        action="DATA_ACCESS",
        details=f"Masked note: {masked_note}",
    )
    print(f"Audit event logged for session: {session.session_id}")

    # 6. Generate Compliance Report
    print("\n--- 5. Compliance Report ---")
    report = manager.generate_compliance_report()
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    run_example()
