"""rxnorm_client_cli - RxNorm Drug Database CLI tool.
"""

import argparse
import json
from rxnorm_client import RxNormClient

def main():
    """
    Command-line interface for RxNorm client.
    """
    parser = argparse.ArgumentParser(description="RxNorm Drug Database Client")
    parser.add_argument("drug_name", help="Name of the drug to look up")
    parser.add_argument("--json-output", "-j", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    drug_name = args.drug_name

    with RxNormClient() as client:
        if args.json_output:
            if client.check_valid_drug(drug_name):
                identifier = client.get_identifier(drug_name)
                props = client.get_properties(identifier)
                print(json.dumps(props, indent=2))
            else:
                print(json.dumps({"error": f"Drug '{drug_name}' not found"}, indent=2))
            return

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
    main()