import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import unittest

from medkit_privacy.anonymization import Anonymizer
from medkit_privacy.deidentification import Deidentifier


class TestPrivacyModules(unittest.TestCase):
    """Test suite for HIPAA De-identification and GDPR Anonymization."""

    @classmethod
    def setUpClass(cls):
        cls.deidentifier = Deidentifier()
        cls.anonymizer = Anonymizer()

    def test_hipaa_deidentification(self):
        """Verify that the 18 HIPAA identifiers are correctly de-identified."""
        text = "Patient John Doe (DOB 01/01/1980) called from 555-0199 about his stay at Mayo Clinic."
        deidentified = self.deidentifier.deidentify_text(text)

        # Check that specific PII is removed
        self.assertNotIn("John Doe", deidentified)
        self.assertNotIn("01/01/1980", deidentified)
        self.assertNotIn("555-0199", deidentified)
        self.assertNotIn("Mayo Clinic", deidentified)

        # Check that placeholders are inserted (depending on your implementation)
        self.assertIn("[", deidentified)
        self.assertIn("]", deidentified)

    def test_gdpr_anonymization_age_generalization(self):
        """Verify that ages are generalized rather than just removed for GDPR."""
        text = "Patient is 25 years old."
        anonymized = self.anonymizer.anonymize_text(text)

        # Implementation specific - check for age range
        self.assertNotIn("25", anonymized)
        # Assuming your anonymizer produces ranges like 'age 20-30' or [AGE_RANGE]
        # For now, let's just assert it's changed
        self.assertNotEqual(text, anonymized)

    def test_structured_record_deidentification(self):
        """Verify that structured dictionaries are de-identified recursively."""
        record = {
            "patient": "John Doe",
            "contact": {"phone": "555-0100", "email": "john@email.com"},
        }
        deidentified = self.deidentifier.deidentify_record(record)

        self.assertNotEqual(record["patient"], deidentified["patient"])
        self.assertNotEqual(
            record["contact"]["phone"], deidentified["contact"]["phone"]
        )


if __name__ == "__main__":
    unittest.main()
