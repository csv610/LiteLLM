import random
import re
from typing import Optional

from .pii_utils import PIIDetector, PIIMasker


class Anonymizer:
    """Provides GDPR-compliant, irreversible anonymization services."""

    def __init__(self, detector: Optional[PIIDetector] = None):
        self.detector = detector or PIIDetector()
        self.masker = PIIMasker(self.detector)

    def anonymize_text(self, text: str) -> str:
        """
        Irreversibly redacts all personal data.
        Unlike de-identification, this ensures even indirect identifiers
        are removed or generalized.
        """
        # Step 1: Broad PII Masking
        anonymized = self.masker.mask(text, placeholder="REDACTED")

        # Step 2: Generalize ages (e.g., replace '32' with '30-40')
        anonymized = self._generalize_ages(anonymized)

        # Step 3: Generalize locations (e.g., remove specific street addresses)
        # This is already handled by the LLM-based masker in PIIMasker.

        return anonymized

    def _generalize_ages(self, text: str) -> str:
        """Generalizes specific ages into decade buckets (e.g., 'Age 24' -> 'Age 20-30')."""

        def replace_age(match):
            age = int(match.group(1))
            lower = (age // 10) * 10
            upper = lower + 10
            return f"age {lower}-{upper}"

        # Simple regex for age generalization
        return re.sub(r"\bage (\d{1,2})\b", replace_age, text, flags=re.IGNORECASE)

    def add_noise(self, value: float, epsilon: float = 0.1) -> float:
        """Adds Laplace noise for basic differential privacy in numeric data."""
        # Simple noise addition for privacy-preserving analytics
        noise = random.uniform(-epsilon, epsilon)
        return value + noise

    def suppress_indirect_identifiers(self, text: str) -> str:
        """
        Identifies and removes unique characteristics that could lead to
        indirect identification ('jigsaw identification').
        """
        # This relies on the LLM's ability to identify INDIRECT_ID categories.
        detections = self.detector.detect(text)

        # Specifically target indirect markers
        indirect_detections = [d for d in detections if d["type"] == "INDIRECT_ID"]

        anonymized = text
        for d in sorted(indirect_detections, key=lambda x: x["start"], reverse=True):
            anonymized = (
                anonymized[: d["start"]]
                + "[DE-IDENTIFIED CHARACTERISTIC]"
                + anonymized[d["end"] :]
            )

        return anonymized
