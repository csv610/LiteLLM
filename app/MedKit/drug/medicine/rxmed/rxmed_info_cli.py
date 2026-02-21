"""rx_med_info_cli - CLI for drug classification and relationships.
"""

import json
import sys
from typing import Any
from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty

from rxclass_client import RxClassClient

def print_result(data: Any, title: str = ""):
    """Prints data using Rich."""
    console = Console()
    console.print(Panel(Pretty(data), title=title))

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