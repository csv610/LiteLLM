"""Example demonstrating HIPAA-compliant De-identification."""

import json

from medkit_privacy.deidentification import Deidentifier


def run_deidentification_example():
    deidentifier = Deidentifier()

    # Example 1: Text De-identification
    clinical_note = "Patient Jane Doe (DOB: 05/12/1985) was admitted to Springfield General on 02/20/2026."
    print("--- 1. Text De-identification ---")
    print(f"Original: {clinical_note}")

    deidentified_text = deidentifier.deidentify_text(clinical_note)
    print(f"De-identified: {deidentified_text}")

    # Example 2: Structured Record De-identification
    patient_record = {
        "id": "REC-998877",
        "patient_info": {
            "full_name": "Jane S. Doe",
            "contact": "jane.doe@email.com",
            "notes": "Patient lives at 123 Maple Ave, Springfield.",
        },
        "vitals": {"heart_rate": 72, "blood_pressure": "120/80"},
    }

    print("\n--- 2. Structured Record De-identification ---")
    deidentified_record = deidentifier.deidentify_record(patient_record)
    print(json.dumps(deidentified_record, indent=2))


if __name__ == "__main__":
    run_deidentification_example()
