"""rxnorm_client - RxNorm Drug Database Client

Provides a lightweight, object-oriented client for interacting with the U.S. National Library of Medicine's
RxNorm API. RxNorm is a standardized naming system for clinical drugs and drug delivery mechanisms.
"""

import requests
from typing import Optional, Dict, Any

class RxNormError(Exception):
    """Custom exception for RxNorm API errors."""
    pass

class RxNormClient:
    """
    A lightweight, object-oriented client for interacting with the U.S. NLM RxNorm API.
    """

    BASE_URL = "https://rxnav.nlm.nih.gov/REST"

    def __init__(self, user_agent: str = "RxNormClient/1.0"):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})

    def get_identifier(self, name: str) -> Optional[str]:
        """Get the RxNorm Concept Unique Identifier (RxCUI) for a given drug name."""
        url = f"{self.BASE_URL}/rxcui.json"
        response = self.session.get(url, params={"name": name})
        self._check_response(response)

        data = response.json()
        ids = data.get("idGroup", {}).get("rxnormId")
        return ids[0] if ids else None

    def get_properties(self, identifier: str) -> Dict[str, Any]:
        """Get all available RxNorm properties for a given drug identifier (RxCUI)."""
        url = f"{self.BASE_URL}/rxcui/{identifier}/properties.json"
        response = self.session.get(url)
        self._check_response(response)
        return response.json()

    def get_approx_match(self, name: str) -> Optional[str]:
        """Get approximate matches for a misspelled or variant drug name."""
        url = f"{self.BASE_URL}/approximateTerm.json"
        response = self.session.get(url, params={"term": name})
        self._check_response(response)

        candidates = response.json().get("approximateGroup", {}).get("candidate", [])
        if not candidates:
            return None
        return candidates[0].get("rxcui")

    def check_valid_drug(self, name: str) -> bool:
        """Quickly verify if a given name is a valid drug in the RxNorm database."""
        identifier = self.get_identifier(name)
        if identifier:
            return True
        return bool(self.get_approx_match(name))

    def _check_response(self, response: requests.Response):
        """Check HTTP response for errors and raise exception if needed."""
        if not response.ok:
            raise RxNormError(f"HTTP {response.status_code}: {response.text[:200]}")

    def close(self):
        """Close the underlying HTTP session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
