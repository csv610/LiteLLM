#!/usr/bin/env python3
"""
Script to run all medical module tests using pytest.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_tests():
    # Get the absolute path of the current directory (medical)
    current_dir = Path(__file__).resolve().parent

    # Add the parent directory (MedKit) to PYTHONPATH so imports like 'medical.xxx' work
    project_root = current_dir.parent
    env = os.environ.copy()
    python_path = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{project_root}{os.pathsep}{python_path}"

    print(f"Running all tests in: {current_dir}")
    print(f"Project root added to PYTHONPATH: {project_root}")
    print("-" * 50)

    # Construct the pytest command
    # We use sys.executable -m pytest to ensure we use the same python environment
    cmd = [sys.executable, "-m", "pytest", str(current_dir), "-v"]

    try:
        # Run pytest
        result = subprocess.run(cmd, env=env)

        if result.returncode == 0:
            print("-" * 50)
            print("✅ All tests passed successfully!")
        else:
            print("-" * 50)
            print(f"❌ Some tests failed (exit code: {result.returncode})")

        sys.exit(result.returncode)

    except FileNotFoundError:
        print("Error: pytest not found. Please install it using 'pip install pytest'.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
