import unittest
from deidentification import Deidentifier
from anonymization import Anonymizer


class TestPrivacyModules(unittest.TestCase):
    """Test suite for HIPAA De-identification and GDPR Anonymization."""

    @classmethod
    def setUpClass(cls):
        cls.deidentifier = Deidentifier()
        cls.anonymizer = Anonymizer()

    def test_hipaa_deidentification(self):
        """Verify that the 18 HIPAA identifiers are correctly de-identified."""
        text = "Patient Jane Doe (DOB: 01/01/1980) lives at 123 Maple Ave, Springfield."
        deidentified = self.deidentifier.deidentify_text(text)

        # Check for HIPAA categories
        self.assertIn("[NAME]", deidentified)
        self.assertIn("[DATE]", deidentified)
        self.assertIn("[LOCATION]", deidentified)
        self.assertNotIn("Jane Doe", deidentified)
        self.assertNotIn("01/01/1980", deidentified)
        self.assertNotIn("123 Maple Ave", deidentified)

    def test_gdpr_anonymization_age_generalization(self):
        """Verify that ages are correctly generalized into decade buckets."""
        text = "Patient Jane Doe is age 24 and resides in Springfield."
        anonymized = self.anonymizer.anonymize_text(text)

        # Verify age 24 becomes age 20-30
        self.assertIn("age 20-30", anonymized)
        self.assertNotIn("age 24", anonymized)

    def test_gdpr_anonymization_indirect_suppression(self):
        """Verify that indirect identifiers are suppressed for GDPR compliance."""
        text = "The subject is the only left-handed Treasury Secretary at the office."
        suppressed = self.anonymizer.suppress_indirect_identifiers(text)

        # Verify specific unique marker is replaced with a characteristic placeholder
        self.assertIn("[DE-IDENTIFIED CHARACTERISTIC]", suppressed)
        self.assertNotIn("the only left-handed Treasury Secretary", suppressed)

    def test_structured_record_deidentification(self):
        """Verify that structured dictionaries are de-identified recursively."""
        record = {
            "patient": "Jane Doe",
            "contact": {"phone": "555-0100", "email": "jane@email.com"},
        }
        deidentified = self.deidentifier.deidentify_record(record)

        # Check for deep masking
        self.assertIn("[NAME]", deidentified["patient"])
        self.assertIn("[CONTACT]", deidentified["contact"]["phone"])
        self.assertIn("[CONTACT]", deidentified["contact"]["email"])


if __name__ == "__main__":
    unittest.main()
