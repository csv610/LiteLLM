"""rx_med_info - RxNorm and RxClass API client for drug classification and relationships.

This module provides a comprehensive client for the National Library of Medicine's RxNorm
and RxClass APIs, enabling drug classification lookups, therapeutic class hierarchies,
clinical relationships (contraindications, interactions, therapeutic uses), and drug
information retrieval. It abstracts API complexity to provide clean, intuitive methods
for querying drug data.

QUICK START:
    Get drug classes by name:

    >>> from rx_med_info import RxClassClient
    >>> client = RxClassClient()
    >>> result = client.find_class_by_name("Beta blocking agents")
    >>> print(result)

    Get drug classes by RxCUI (drug identifier):

    >>> result = client.get_class_by_rxcui("5002")
    >>> print(result)

    Run examples:

    $ python rx_med_info.py

COMMON USES:
    1. Drug lookup - finding therapeutic classes for medications
    2. Drug interactions - identifying contraindicated drug combinations
    3. Therapeutic alternatives - finding drugs in same class
    4. Disease treatment lookup - finding drugs for specific conditions
    5. Drug hierarchy navigation - exploring ATC or MEDRT classification trees

KEY FEATURES AND COVERAGE AREAS:
    - Drug Lookup: find classes by name, RxCUI, or drug name
    - Class Hierarchies: navigate ATC and MEDRT classification trees
    - Relationships: contraindications, therapeutic uses, preventive uses
    - Class Membership: list all drugs in a specific therapeutic class
    - Similarity Checking: find clinically similar drugs
    - Spelling Suggestions: autocomplete for drug and class names
    - Class Types: available classification systems (ATC, MEDRT, etc.)
    - Relationship Sources: different relationship data sources
"""

import requests
import sys
from typing import Optional, Dict, Any, List, Union
from rich.console import Console
from rich.panel import Panel
from utils.output_formatter import print_result

class RxClassClient:
    BASE_URL = "https://rxnav.nlm.nih.gov/REST/rxclass"

    def __init__(self, timeout: float = 10.0):
        self.session = requests.Session()
        self.timeout = timeout

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{path}"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def find_class_by_name(self, class_name: str) -> Dict[str, Any]:
        """/class/byName — Drug classes with a specified class name."""
        return self._get("/class/byName.json", params={"className": class_name})

    def find_classes_by_id(self, class_id: str) -> Dict[str, Any]:
        """/class/byId — Drug classes with a specified class identifier."""
        return self._get("/class/byId.json", params={"classId": class_id})

    def find_similar_classes_by_class(self, class_id: str) -> Dict[str, Any]:
        """/class/similar — Classes with similar clinically-significant RxNorm ingredients."""
        return self._get("/class/similar.json", params={"classId": class_id})

    def find_similar_classes_by_drug_list(self, rxcuis: List[str]) -> Dict[str, Any]:
        """/class/similarByRxcuis — Classes with clinically-significant ingredients similar to a list of RXCUIs."""
        rxcui_param = ",".join(rxcuis)
        return self._get("/class/similarByRxcuis.json", params={"rxcuis": rxcui_param})

    def get_all_classes(self, class_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """/allClasses — Retrieve all classes (optionally filtered by class type)."""
        params: Dict[str, Any] = {}
        if class_types:
            # API expects space-separated list
            params["classTypes"] = " ".join(class_types)
        return self._get("/allClasses.json", params=params)

    def get_class_by_rxcui(self, rxcui: str) -> Dict[str, Any]:
        """/class/byRxcui — Classes containing a specified drug RXCUI."""
        return self._get("/class/byRxcui.json", params={"rxcui": rxcui})

    def get_class_by_drug_name(self, drug_name: str) -> Dict[str, Any]:
        """/class/byDrugName — Classes containing a drug of the specified name (generic or brand)."""
        return self._get("/class/byDrugName.json", params={"drugName": drug_name})

    def get_class_contexts(self, class_id: str) -> Dict[str, Any]:
        """/classContext — Paths from the specified class to the root of its class hierarchies."""
        return self._get("/classContext.json", params={"classId": class_id})

    def get_class_graph_by_source(self, class_id: str, source: Optional[str] = None) -> Dict[str, Any]:
        """/classGraph — Classes along the path from a specified class to the root of a class hierarchy (by source)."""
        params: Dict[str, Any] = {"classId": class_id}
        if source:
            params["source"] = source
        return self._get("/classGraph.json", params=params)

    def get_class_members(
        self,
        class_id: str,
        rela_source: str,
        rela: Optional[str] = None,
        ttys: Optional[str] = None,
        trans: Optional[Union[int, str]] = None
    ) -> Dict[str, Any]:
        """
        /classMembers — Drug members of a specified class.
        Note: `relaSource` is required per documentation. :contentReference[oaicite:1]{index=1}
        """
        params: Dict[str, Any] = {"classId": class_id, "relaSource": rela_source}
        if rela:
            params["rela"] = rela
        if ttys:
            params["ttys"] = ttys
        if trans is not None:
            params["trans"] = str(trans)
        return self._get("/classMembers.json", params=params)

    def get_class_tree(self, class_id: str) -> Dict[str, Any]:
        """/classTree — Subclasses or descendants of the specified class."""
        return self._get("/classTree.json", params={"classId": class_id})

    def get_class_types(self) -> Dict[str, Any]:
        """/classTypes — List of available class types."""
        return self._get("/classTypes.json")

    def get_rela_source_version(self, rela_source: str) -> Dict[str, Any]:
        """/version/relaSource — Version of dataset from which RxClass draws drug-class relations."""
        return self._get("/version/relaSource.json", params={"relaSource": rela_source})

    def get_relas(self, rela_source: str, rela: Optional[str] = None) -> Dict[str, Any]:
        """/relas — Relationships expressed by a source of drug-class relations."""
        params: Dict[str, Any] = {"relaSource": rela_source}
        if rela:
            params["rela"] = rela
        return self._get("/relas.json", params=params)

    def get_similarity_information(self, class1: str, class2: str) -> Dict[str, Any]:
        """/class/similarInfo — Similarity of the clinically-significant membership of two classes."""
        return self._get("/class/similarInfo.json", params={"class1": class1, "class2": class2})

    def get_sources_of_drug_class_relations(self) -> Dict[str, Any]:
        """/relaSources — Sources of drug-class relations."""
        return self._get("/relaSources.json")

    def get_spelling_suggestions(self, term: str, type_: str = "CLASS") -> Dict[str, Any]:
        """/spellingsuggestions — Drug or class names similar to a given string."""
        params: Dict[str, Any] = {
            "term": term,
            "type": type_.upper()
        }
        return self._get("/spellingsuggestions.json", params=params)




def main():
    """CLI function for RxClassClient examples."""
    import argparse
    parser = argparse.ArgumentParser(description="RxClass API client for drug classification and relationships.")
    parser.add_argument("--json-output", "-j", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    client = RxClassClient()

    results = {}
    try:
        results["find_class_by_name"] = client.find_class_by_name("Beta blocking agents")
    except Exception as e:
        results["find_class_by_name_error"] = str(e)

    try:
        results["get_class_by_drug_name"] = client.get_class_by_drug_name("Lipitor")
    except Exception as e:
        results["get_class_by_drug_name_error"] = str(e)

    try:
        results["get_class_members"] = client.get_class_members(class_id="A12CA", rela_source="ATC")
    except Exception as e:
        results["get_class_members_error"] = str(e)

    try:
        results["get_class_types"] = client.get_class_types()
    except Exception as e:
        results["get_class_types_error"] = str(e)

    try:
        results["get_spelling_suggestions"] = client.get_spelling_suggestions("betablocking", type_="CLASS")
    except Exception as e:
        results["get_spelling_suggestions_error"] = str(e)

    if args.json_output:
        print(json.dumps(results, indent=2))
        return

    for key, val in results.items():
        print(f"{key} ->")
        print_result(val, title=key.replace('_', ' ').title())


if __name__ == "__main__":
    sys.exit(main() or 0)
