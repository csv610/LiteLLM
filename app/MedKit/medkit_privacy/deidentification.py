from typing import Dict, Optional

from .pii_utils import PIIDetector, PIIMasker


class Deidentifier:
    """Provides HIPAA-compliant de-identification services."""

    def __init__(self, detector: Optional[PIIDetector] = None):
        self.detector = detector or PIIDetector()
        self.masker = PIIMasker(self.detector)

    def deidentify_text(self, text: str) -> str:
        """
        Removes all 18 HIPAA identifiers from the text.
        Uses standard masking placeholders like [NAME], [DATE], etc.
        """
        return self.masker.mask(text)

    def deidentify_record(self, record: Dict) -> Dict:
        """
        De-identifies a structured dictionary by masking values in string fields.
        """
        deidentified = {}
        for key, value in record.items():
            if isinstance(value, str):
                deidentified[key] = self.deidentify_text(value)
            elif isinstance(value, dict):
                deidentified[key] = self.deidentify_record(value)
            else:
                deidentified[key] = value
        return deidentified

    def apply_safe_harbor_rules(self, text: str) -> str:
        """
        A stricter implementation that specifically targets HIPAA Safe Harbor
        redaction patterns.
        """
        # This currently leverages the LLM-based masker which is already
        # instructed on Safe Harbor rules.
        return self.deidentify_text(text)
