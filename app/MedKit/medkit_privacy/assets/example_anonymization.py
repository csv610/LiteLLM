"""Example demonstrating GDPR-compliant Anonymization."""

from medkit_privacy.anonymization import Anonymizer
import json

def run_anonymization_example():
    anonymizer = Anonymizer()
    
    # Example 1: Irreversible Text Anonymization
    clinical_note = "Patient Jane Doe (age 24) is the only left-handed Treasury Secretary at the office."
    print("--- 1. Irreversible Anonymization ---")
    print(f"Original: {clinical_note}")
    
    anonymized_text = anonymizer.anonymize_text(clinical_note)
    print(f"Anonymized (Age Generalized): {anonymized_text}")

    # Example 2: Suppressing Indirect Identifiers
    unique_marker = "Patient has a distinct butterfly tattoo on her left shoulder and is the only person from Little Village in this clinic."
    print("
--- 2. Suppressing Indirect Identifiers ---")
    print(f"Original: {unique_marker}")
    
    anonymized_marker = anonymizer.suppress_indirect_identifiers(unique_marker)
    print(f"Suppressed: {anonymized_marker}")

    # Example 3: Adding Noise for Differential Privacy
    hr_value = 72.5
    noisy_hr = anonymizer.add_noise(hr_value, epsilon=0.5)
    print("
--- 3. Adding Noise for Differential Privacy ---")
    print(f"Original Heart Rate: {hr_value}")
    print(f"Anonymized (Noisy) Heart Rate: {noisy_hr:.2f}")

if __name__ == "__main__":
    run_anonymization_example()
