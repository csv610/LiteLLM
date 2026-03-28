#!/usr/bin/env python3
"""
Live test for Disease Information CLI.
This test runs the actual CLI app without mocking.
"""

import shutil
import subprocess
from pathlib import Path

# Paths
CUR_DIR = Path(__file__).parent
CLI_PATH = CUR_DIR / "disease_info_cli.py"
TEST_OUTPUT_DIR = CUR_DIR / "test_outputs"
DISEASE_UNSTRUCTURED = "flu"
DISEASE_STRUCTURED = "malaria"
EXPECTED_UNSTRUCTURED_FILE = TEST_OUTPUT_DIR / f"{DISEASE_UNSTRUCTURED}.md"
EXPECTED_STRUCTURED_FILE = TEST_OUTPUT_DIR / f"{DISEASE_STRUCTURED}.json"


def run_live_test():
    """Runs the live test by calling the CLI with real LLM."""
    print("--- Starting Live Test ---")

    # Cleanup previous test outputs
    if TEST_OUTPUT_DIR.exists():
        shutil.rmtree(TEST_OUTPUT_DIR)
    TEST_OUTPUT_DIR.mkdir(exist_ok=True)

    # --- Test Case 1: Unstructured Output ---
    print(f"\n1. Testing Unstructured Output for: {DISEASE_UNSTRUCTURED}")
    cmd_u = [
        "python3",
        str(CLI_PATH),
        DISEASE_UNSTRUCTURED,
        "--output-dir",
        str(TEST_OUTPUT_DIR),
        "--verbosity",
        "2",
    ]

    try:
        subprocess.run(cmd_u, capture_output=True, text=True, check=True)
        if EXPECTED_UNSTRUCTURED_FILE.exists():
            print(f"✓ Success: Output file generated at {EXPECTED_UNSTRUCTURED_FILE}")
            content = EXPECTED_UNSTRUCTURED_FILE.read_text()
            if len(content) > 100:
                print(f"✓ Success: Content found ({len(content)} chars).")
            else:
                print("✗ Failure: Output file is too small.")
                return False
        else:
            print(f"✗ Failure: Output file {EXPECTED_UNSTRUCTURED_FILE} not created.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"✗ Failure: {e}")
        return False

    # --- Test Case 2: Structured Output ---
    print(f"\n2. Testing Structured Output for: {DISEASE_STRUCTURED}")
    cmd_s = [
        "python3",
        str(CLI_PATH),
        DISEASE_STRUCTURED,
        "--output-dir",
        str(TEST_OUTPUT_DIR),
        "--structured",
        "--verbosity",
        "2",
    ]

    try:
        subprocess.run(cmd_s, capture_output=True, text=True, check=True)
        # Note: save_model_response should add .json extension if it's structured
        # Let's check what it actually produces.
        if EXPECTED_STRUCTURED_FILE.exists():
            print(f"✓ Success: Output file generated at {EXPECTED_STRUCTURED_FILE}")
            import json

            with open(EXPECTED_STRUCTURED_FILE) as f:
                data = json.load(f)
                if "identity" in data and "name" in data["identity"]:
                    print(
                        f"✓ Success: Found structured data for {data['identity']['name']}"
                    )
                else:
                    print("✗ Failure: JSON structure missing expected keys.")
                    return False
        else:
            print(f"✗ Failure: Output file {EXPECTED_STRUCTURED_FILE} not created.")
            print("Files in test_outputs:", list(TEST_OUTPUT_DIR.glob("*")))
            return False
    except subprocess.CalledProcessError as e:
        print(f"✗ Failure: {e}")
        return False

    print("\n--- All Live Tests Completed Successfully ---")
    return True


if __name__ == "__main__":
    success = run_live_test()
    exit(0 if success else 1)
