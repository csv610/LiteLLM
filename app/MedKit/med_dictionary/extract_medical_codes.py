#!/usr/bin/env python3
"""
Extract medical codes from medical terms using multiple coding systems.

Supports:
  - RxNorm (drug/medication codes) - no auth required
  - ICD-10-CM (disease classification) - no auth required
  - ICD-11 (disease classification) - no auth required
  - LOINC (lab tests/measurements) - no auth required
  - SNOMED CT (clinical terminology) - requires UMLS_API_KEY
  - MeSH (literature indexing) - requires UMLS_API_KEY

To enable SNOMED CT and MeSH:
  1. Get free API key at https://uts.nlm.nih.gov/uts/signup-login
  2. Set environment variable: export UMLS_API_KEY="your-key"

Input can be:
  - A single medical term (string)
  - Path to a JSON file containing medical terms (dictionary or list)
  - Path to a text file with one term per line

Output: JSON file with term and codes from all available systems
"""

import sys
import os
import json
import argparse
import logging
import requests
import time
from pathlib import Path
from typing import Optional, Dict, List, Any
from tqdm import tqdm
from datetime import datetime

# Configure logging
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"extract_medical_codes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# RxNorm API base URL
RXNORM_API_BASE = "https://rxnav.nlm.nih.gov/REST"

# UMLS-based endpoints for additional codes
SNOMED_UMLS_BASE = "https://uts-ws.nlm.nih.gov/rest"

# Clinical Tables API (no auth required)
CLINICAL_TABLES_BASE = "https://clinicaltables.nlm.nih.gov/api"
ICD10_ENDPOINT = f"{CLINICAL_TABLES_BASE}/icd10cm/v3/search"
ICD11_ENDPOINT = f"{CLINICAL_TABLES_BASE}/icd11_codes/v3/search"
LOINC_ENDPOINT = f"{CLINICAL_TABLES_BASE}/loinc_items/v3/search"

# UMLS API endpoint
UMLS_SEARCH_ENDPOINT = f"{SNOMED_UMLS_BASE}/search/current"


class MedicalCodeExtractor:
    """Extract medical codes from medical terms."""

    def __init__(self):
        """Initialize the extractor."""
        self.rxnorm_session = requests.Session()
        self.clinical_session = requests.Session()
        self.umls_session = requests.Session()
        self.umls_api_key = os.getenv("UMLS_API_KEY")
        self.rate_limit_delay = 0.5  # 500ms between API calls
        self.output_data = []

        if self.umls_api_key:
            logger.info("UMLS API key found - SNOMED CT/MeSH lookups enabled")
        else:
            logger.info("No UMLS API key - SNOMED CT/MeSH lookups will be skipped")

        logger.info("MedicalCodeExtractor initialized")

    def get_rxnorm_codes(self, term: str) -> Optional[List[Dict[str, str]]]:
        """
        Get RxNorm codes for a medical term.

        Returns:
            List of dicts with 'code' (RXCUI) and 'name' keys, or None if not found
        """
        try:
            endpoint = f"{RXNORM_API_BASE}/drugs.json"
            params = {
                "name": term,
                "search": 1
            }

            response = self.rxnorm_session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if "drugGroup" in data and data["drugGroup"].get("conceptGroup"):
                results = []
                for group in data["drugGroup"]["conceptGroup"]:
                    if "conceptProperties" in group:
                        for concept in group["conceptProperties"][:10]:  # Limit to 10
                            rxcui = concept.get("rxcui")
                            name = concept.get("name")
                            if rxcui and name:
                                results.append({"code": rxcui, "name": name})
                return results if results else None

            return None
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error fetching RxNorm codes for '{term}': {e}")
            return None
        except json.JSONDecodeError as e:
            logger.warning(f"Error parsing RxNorm response for '{term}': {e}")
            return None
        finally:
            time.sleep(self.rate_limit_delay)

    def get_icd10_codes(self, term: str) -> Optional[List[Dict[str, str]]]:
        """Get ICD-10-CM codes for a medical term using Clinical Tables API."""
        try:
            params = {
                "sf": "code,name",
                "terms": term,
                "maxList": 10
            }

            response = self.clinical_session.get(ICD10_ENDPOINT, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            # Clinical Tables returns: [count, codes[], null, [[code, name]...]]
            if len(data) >= 4 and data[3]:
                results = [{"code": item[0], "name": item[1]} for item in data[3]]
                logger.info(f"Found {len(results)} ICD-10 codes for '{term}'")
                return results if results else None

            return None
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error fetching ICD-10 codes for '{term}': {e}")
            return None
        except (json.JSONDecodeError, IndexError, KeyError, TypeError) as e:
            logger.warning(f"Error parsing ICD-10 response for '{term}': {e}")
            return None
        finally:
            time.sleep(self.rate_limit_delay)

    def get_icd11_codes(self, term: str) -> Optional[List[Dict[str, str]]]:
        """Get ICD-11 codes for a medical term using Clinical Tables API."""
        try:
            params = {
                "sf": "code,name",
                "terms": term,
                "maxList": 10
            }

            response = self.clinical_session.get(ICD11_ENDPOINT, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            # Clinical Tables returns: [count, codes[], null, [[code, name]...]]
            if len(data) >= 4 and data[3]:
                results = [{"code": item[0], "name": item[1]} for item in data[3]]
                logger.info(f"Found {len(results)} ICD-11 codes for '{term}'")
                return results if results else None

            return None
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error fetching ICD-11 codes for '{term}': {e}")
            return None
        except (json.JSONDecodeError, IndexError, KeyError, TypeError) as e:
            logger.warning(f"Error parsing ICD-11 response for '{term}': {e}")
            return None
        finally:
            time.sleep(self.rate_limit_delay)

    def get_loinc_codes(self, term: str) -> Optional[List[Dict[str, str]]]:
        """Get LOINC codes for a medical term using Clinical Tables API."""
        try:
            params = {
                "type": "question",
                "terms": term,
                "maxList": 10
            }

            response = self.clinical_session.get(LOINC_ENDPOINT, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            # Clinical Tables returns: [count, codes[], null, [[name]...]]
            if len(data) >= 4 and data[1] and data[3]:
                results = []
                for code, name_list in zip(data[1], data[3]):
                    # name_list is [name_string]
                    name = name_list[0] if name_list else ""
                    if code and name:
                        results.append({"code": code, "name": name})

                if results:
                    logger.info(f"Found {len(results)} LOINC codes for '{term}'")
                    return results

            return None
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error fetching LOINC codes for '{term}': {e}")
            return None
        except (json.JSONDecodeError, IndexError, KeyError, TypeError) as e:
            logger.warning(f"Error parsing LOINC response for '{term}': {e}")
            return None
        finally:
            time.sleep(self.rate_limit_delay)

    def get_snomed_codes(self, term: str) -> Optional[List[Dict[str, str]]]:
        """Get SNOMED CT codes using UMLS API. Requires UMLS_API_KEY environment variable."""
        if not self.umls_api_key:
            logger.debug(f"Skipping SNOMED lookup for '{term}' - no API key configured")
            return None

        try:
            params = {
                "apiKey": self.umls_api_key,
                "string": term,
                "sabs": "SNOMEDCT_US",
                "returnIdType": "code",
                "pageSize": 10
            }

            response = self.umls_session.get(UMLS_SEARCH_ENDPOINT, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            results = []

            if "result" in data and "results" in data["result"]:
                for item in data["result"]["results"][:10]:
                    if "ui" in item and "name" in item:
                        results.append({
                            "code": item["ui"],
                            "name": item["name"]
                        })

            if results:
                logger.info(f"Found {len(results)} SNOMED CT codes for '{term}'")
                return results
            return None

        except requests.exceptions.RequestException as e:
            logger.warning(f"Error fetching SNOMED codes for '{term}': {e}")
            return None
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.warning(f"Error parsing SNOMED response for '{term}': {e}")
            return None
        finally:
            time.sleep(self.rate_limit_delay)

    def get_mesh_codes(self, term: str) -> Optional[List[Dict[str, str]]]:
        """Get MeSH codes using UMLS API. Requires UMLS_API_KEY environment variable."""
        if not self.umls_api_key:
            logger.debug(f"Skipping MeSH lookup for '{term}' - no API key configured")
            return None

        try:
            params = {
                "apiKey": self.umls_api_key,
                "string": term,
                "sabs": "MSH",
                "returnIdType": "code",
                "pageSize": 10
            }

            response = self.umls_session.get(UMLS_SEARCH_ENDPOINT, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            results = []

            if "result" in data and "results" in data["result"]:
                for item in data["result"]["results"][:10]:
                    if "ui" in item and "name" in item:
                        results.append({
                            "code": item["ui"],
                            "name": item["name"]
                        })

            if results:
                logger.info(f"Found {len(results)} MeSH codes for '{term}'")
                return results
            return None

        except requests.exceptions.RequestException as e:
            logger.warning(f"Error fetching MeSH codes for '{term}': {e}")
            return None
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.warning(f"Error parsing MeSH response for '{term}': {e}")
            return None
        finally:
            time.sleep(self.rate_limit_delay)

    def extract_codes_for_term(self, term: str) -> Optional[Dict[str, Any]]:
        """
        Extract all available medical codes for a term from 5 coding systems:
        RxNorm, ICD-10, ICD-11, LOINC, SNOMED CT, and MeSH.

        Returns:
            Dictionary with term and codes, or None if no codes found from any system
        """
        logger.info(f"Extracting codes for term: {term}")

        codes_dict = {}

        # Extract from all 5 systems
        for system_name, method in [
            ("rxnorm", self.get_rxnorm_codes),
            ("icd10", self.get_icd10_codes),
            ("icd11", self.get_icd11_codes),
            ("loinc", self.get_loinc_codes),
            ("snomed_ct", self.get_snomed_codes),
            ("mesh", self.get_mesh_codes),
        ]:
            codes = method(term)
            if codes:
                codes_dict[system_name] = codes

        # Return None only if NO codes found from ANY system
        if not codes_dict:
            logger.warning(f"No codes found from any system for '{term}'")
            return None

        logger.info(f"Found codes from {len(codes_dict)} system(s) for '{term}'")

        return {
            "term": term,
            "codes": codes_dict
        }

    def process_single_term(self, term: str) -> bool:
        """Process a single medical term."""
        try:
            result = self.extract_codes_for_term(term)
            if result:
                self.output_data.append(result)
                return True
            return False
        except Exception as e:
            logger.error(f"Error processing term '{term}': {e}")
            return False

    def load_terms_from_text_file(self, file_path: Path) -> List[str]:
        """Load medical terms from a text file (one per line)."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                terms = [line.strip() for line in f if line.strip()]
            logger.info(f"Loaded {len(terms)} terms from text file: {file_path}")
            return terms
        except Exception as e:
            logger.error(f"Error loading text file '{file_path}': {e}")
            return []

    def load_terms_from_json_file(self, file_path: Path) -> List[str]:
        """Load medical terms from a JSON file (dictionary keys or list items)."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            terms = []
            if isinstance(data, dict):
                terms = list(data.keys())
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "term" in item:
                        terms.append(item["term"])
                    elif isinstance(item, str):
                        terms.append(item)

            logger.info(f"Loaded {len(terms)} terms from JSON file: {file_path}")
            return terms
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in '{file_path}': {e}")
            return []
        except Exception as e:
            logger.error(f"Error loading JSON file '{file_path}': {e}")
            return []

    def process_input(self, input_data: str) -> bool:
        """
        Process input which can be a term, JSON file, or text file.

        Returns:
            True if processing was successful, False otherwise
        """
        input_path = Path(input_data)

        # Check if input is a file
        if input_path.exists() and input_path.is_file():
            logger.info(f"Processing file: {input_data}")

            # Try JSON first
            if input_path.suffix == '.json':
                terms = self.load_terms_from_json_file(input_path)
            elif input_path.suffix == '.txt':
                terms = self.load_terms_from_text_file(input_path)
            else:
                # Try JSON, then text
                terms = self.load_terms_from_json_file(input_path)
                if not terms:
                    terms = self.load_terms_from_text_file(input_path)

            if not terms:
                logger.error(f"No terms found in file: {input_data}")
                return False

            # Process all terms
            successful = 0
            for term in tqdm(terms, desc="Processing terms", unit="term"):
                if self.process_single_term(term):
                    successful += 1

            print(f"\nProcessed {successful}/{len(terms)} terms successfully")
            return successful > 0
        else:
            # Process as single term
            logger.info(f"Processing single term: {input_data}")
            return self.process_single_term(input_data)

    def save_results(self, output_file: Optional[Path] = None) -> Optional[Path]:
        """
        Save extracted codes to a JSON file.

        Args:
            output_file: Output file path (auto-generated if not provided)

        Returns:
            Path to output file if successful, None otherwise
        """
        try:
            if output_file is None:
                output_dir = Path(__file__).parent / "outputs"
                output_dir.mkdir(exist_ok=True)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = output_dir / f"medical_codes_{timestamp}.json"
            else:
                output_file = Path(output_file)
                output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.output_data, f, indent=2, ensure_ascii=False)

            logger.info(f"Results saved to: {output_file}")
            print(f"\nResults saved to: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error saving results: {e}")
            return None

    def get_results(self) -> List[Dict[str, Any]]:
        """Get the extracted codes data."""
        return self.output_data


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Extract medical codes from medical terms using multiple coding systems "
                    "(RxNorm, ICD-10/11, LOINC, SNOMED CT, MeSH)",
        epilog="INPUT can be:\n"
               "  - A single medical term (e.g., 'aspirin', 'diabetes', 'glucose')\n"
               "  - Path to a JSON file with terms as dict keys or list items\n"
               "  - Path to a text file with one term per line\n\n"
               "OPTIONAL: Set UMLS_API_KEY environment variable to enable SNOMED CT and MeSH lookups\n"
               "Get free API key at: https://uts.nlm.nih.gov/uts/signup-login",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "input",
        help="Medical term or path to JSON/text file containing medical terms"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output JSON file path (auto-generated if not specified)"
    )

    args = parser.parse_args()

    try:
        extractor = MedicalCodeExtractor()

        # Process input
        if extractor.process_input(args.input):
            # Save results
            output_path = extractor.save_results(args.output)

            if output_path:
                print(f"\nExtracted codes for {len(extractor.get_results())} term(s)")
                return 0
            else:
                print("Error: Failed to save results")
                return 1
        else:
            print("Error: Failed to extract medical codes")
            return 1

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
