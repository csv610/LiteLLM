"""
rxnorm_client.py - RxNorm Drug Database Client

Provides a lightweight, object-oriented client for interacting with the U.S. National Library of Medicine's
RxNorm API. RxNorm is a standardized naming system for clinical drugs and drug delivery mechanisms.

QUICK START:
    from rxnorm_client import RxNormClient

    # Basic usage
    with RxNormClient() as client:
        # Get drug identifier
        rxcui = client.get_identifier("aspirin")

        # Get drug properties
        properties = client.get_properties(rxcui)

        # Validate drug name
        is_valid = client.check_valid_drug("metformin")

        # Handle misspelled drug names
        rxcui = client.get_approx_match("asiprin")  # Returns aspirin's RxCUI

COMMON USES:
    1. Look up drug identifiers (RxCUI) from drug names
    2. Retrieve standardized drug properties and information
    3. Validate drug names against the RxNorm database
    4. Handle misspelled or variant drug names
    5. Build drug reference systems and prescribing tools

API REFERENCE:
    - RxNorm is maintained by the U.S. National Library of Medicine
    - Base URL: https://rxnav.nlm.nih.gov/REST
    - No API key required for public access

EXAMPLE WORKFLOW:
    client = RxNormClient()

    # Step 1: Get RxCUI identifier
    rxcui = client.get_identifier("metformin")  # Returns RxCUI

    # Step 2: Get full drug information
    props = client.get_properties(rxcui)

    # Step 3: Clean up
    client.close()

CLI USAGE:
    python rxnorm_client.py aspirin
    python rxnorm_client.py "ibuprofen 200mg"
"""

import requests
import sys
from typing import Optional, Dict, Any


class RxNormError(Exception):
    """
    Custom exception for RxNorm API errors.

    Raised when RxNorm API requests fail due to HTTP errors or invalid responses.

    Example:
        try:
            client = RxNormClient()
            rxcui = client.get_identifier("invalid_drug_xyz")
        except RxNormError as e:
            print(f"API error: {e}")
    """
    pass


class RxNormClient:
    """
    A lightweight, object-oriented client for interacting with the U.S. NLM RxNorm API.

    RxNorm is the standardized naming system for clinical drugs and drug delivery mechanisms
    maintained by the U.S. National Library of Medicine. Each drug is assigned a unique
    RxCUI (RxNorm Concept Unique Identifier).

    Attributes:
        BASE_URL (str): RxNorm API base URL (https://rxnav.nlm.nih.gov/REST)
        session (requests.Session): HTTP session for API requests

    Example:
        # Using context manager (recommended)
        with RxNormClient() as client:
            rxcui = client.get_identifier("aspirin")
            properties = client.get_properties(rxcui)

        # Manual session management
        client = RxNormClient()
        try:
            identifier = client.get_identifier("metformin")
        finally:
            client.close()
    """

    BASE_URL = "https://rxnav.nlm.nih.gov/REST"

    def __init__(self, user_agent: str = "RxNormClient/1.0"):
        """
        Initialize RxNormClient with optional custom User-Agent.

        Args:
            user_agent (str): Custom User-Agent header for API requests (default: "RxNormClient/1.0")
        """
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})

    # ------------------------------------------------------------------
    # Core methods
    # ------------------------------------------------------------------
    def get_identifier(self, name: str) -> Optional[str]:
        """
        Get the RxNorm Concept Unique Identifier (RxCUI) for a given drug name.

        Searches the RxNorm database for an exact match of the drug name.
        The RxCUI is the primary identifier used in the RxNorm system.

        Args:
            name (str): The drug name to search for (e.g., "aspirin", "metformin 500mg")

        Returns:
            Optional[str]: The RxCUI identifier string if found, else None

        Raises:
            RxNormError: If the API request fails

        Example:
            client = RxNormClient()
            rxcui = client.get_identifier("aspirin")
            # Returns something like "207381"
        """
        url = f"{self.BASE_URL}/rxcui.json"
        response = self.session.get(url, params={"name": name})
        self._check_response(response)

        data = response.json()
        ids = data.get("idGroup", {}).get("rxnormId")
        return ids[0] if ids else None

    def get_properties(self, identifier: str) -> Dict[str, Any]:
        """
        Get all available RxNorm properties for a given drug identifier (RxCUI).

        Retrieves comprehensive information about a drug including name, synonyms,
        strength, dose form, route of administration, and other attributes.

        Args:
            identifier (str): RxNorm Concept Unique Identifier (RxCUI)

        Returns:
            Dict[str, Any]: Dictionary containing properties like:
                - name: Drug name
                - synonym: List of alternative names
                - strength: Drug strength
                - doseForm: Route of administration
                - route: How drug is administered

        Raises:
            RxNormError: If the API request fails

        Example:
            client = RxNormClient()
            props = client.get_properties("207381")  # aspirin
            # Returns: {"rxcui": "207381", "name": "Aspirin", ...}
        """
        url = f"{self.BASE_URL}/rxcui/{identifier}/properties.json"
        response = self.session.get(url)
        self._check_response(response)
        return response.json()

    def get_approx_match(self, name: str) -> Optional[str]:
        """
        Get approximate matches for a misspelled or variant drug name.

        Uses fuzzy matching to find similar drug names in the RxNorm database.
        Useful for handling user input errors or alternative naming conventions.

        Args:
            name (str): The approximate or misspelled drug name (e.g., "asiprin" instead of "aspirin")

        Returns:
            Optional[str]: The RxCUI of the best matching drug, else None

        Raises:
            RxNormError: If the API request fails

        Example:
            client = RxNormClient()
            rxcui = client.get_approx_match("asiprin")  # Misspelled
            # Returns RxCUI for "aspirin"
        """
        url = f"{self.BASE_URL}/approximateTerm.json"
        response = self.session.get(url, params={"term": name})
        self._check_response(response)

        candidates = response.json().get("approximateGroup", {}).get("candidate", [])
        if not candidates:
            return None
        # Return the RxCUI of the top candidate
        return candidates[0].get("rxcui")

    def check_valid_drug(self, name: str) -> bool:
        """
        Quickly verify if a given name is a valid drug in the RxNorm database.

        Attempts exact match first, then falls back to approximate matching.
        More efficient than get_identifier() if you only need a yes/no answer.

        Args:
            name (str): Drug name to validate

        Returns:
            bool: True if drug is found in RxNorm (exact or approximate), False otherwise

        Example:
            client = RxNormClient()
            if client.check_valid_drug("metformin"):
                print("Drug is valid")
            else:
                print("Drug not found")
        """
        identifier = self.get_identifier(name)
        if identifier:
            return True
        # Try approximate match fallback
        return bool(self.get_approx_match(name))

    # ------------------------------------------------------------------
    # Utility & internal
    # ------------------------------------------------------------------
    def _check_response(self, response: requests.Response):
        """
        Check HTTP response for errors and raise exception if needed.

        Args:
            response (requests.Response): HTTP response object

        Raises:
            RxNormError: If response status code indicates an error
        """
        if not response.ok:
            raise RxNormError(f"HTTP {response.status_code}: {response.text[:200]}")

    def close(self):
        """
        Close the underlying HTTP session.

        Should be called when done with the client to release resources.
        Automatically called when using context manager.

        Example:
            client = RxNormClient()
            try:
                rxcui = client.get_identifier("aspirin")
            finally:
                client.close()
        """
        self.session.close()

    # Context manager support
    def __enter__(self):
        """Support for 'with' statement (context manager)."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close session when exiting 'with' block."""
        self.close()


# ----------------------------------------------------------------------
# CLI function
# ----------------------------------------------------------------------
def cli():
    """
    Command-line interface for RxNorm client.

    Usage:
        python rxnorm_client.py <drug_name>

    Arguments:
        drug_name: Name of the drug to look up in RxNorm

    Examples:
        python rxnorm_client.py aspirin
        python rxnorm_client.py "metformin 500mg"

    Outputs:
        - Drug validity status
        - RxCUI identifier if found
        - Drug properties (name, synonyms, strength, etc.)
    """
    drug_name = sys.argv[1]

    with RxNormClient() as client:
        print(f"🔍 Checking '{drug_name}' in RxNorm...")

        if client.check_valid_drug(drug_name):
            identifier = client.get_identifier(drug_name)
            print(f"✅ {drug_name} is valid. Identifier (RxCUI) = {identifier}")
            props = client.get_properties(identifier)
            print(f"📘 Retrieved {len(props)} properties.")
            print(props)
        else:
            print(f"⚠️ No valid RxNorm entry found for '{drug_name}'.")


if __name__ == "__main__":
    cli()

