#!/usr/bin/env python3
"""
Comprehensive Test Runner for All Recognizer Modules.

This script runs tests for all recognizer modules without using mock libraries.
"""

import sys
import os
import subprocess
from pathlib import Path


def run_test_script(test_script_path):
    """Run a single test script and return the result."""
    try:
        result = subprocess.run(
            [sys.executable, str(test_script_path)],
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout per test
        )
        
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'stdout': '',
            'stderr': 'Test timed out after 30 seconds',
            'returncode': -1
        }
    except Exception as e:
        return {
            'success': False,
            'stdout': '',
            'stderr': str(e),
            'returncode': -2
        }


def main():
    """Run all recognizer module tests."""
    print("=" * 80)
    print("COMPREHENSIVE RECOGNIZER MODULE TESTS")
    print("=" * 80)
    
    # Get the recognizers directory
    recognizers_dir = Path(__file__).parent
    test_results = {}
    
    # List of modules to test
    modules = [
        "disease",
        "medical_symptom", 
        "medical_test",
        "medical_specialty",
        "medical_supplement",
        "medical_vaccine",
        "medical_procedure",
        "medical_pathogen",
        "medical_device",
        "medical_condition",
        "medical_coding",
        "medical_abbreviation",
        "imaging_finding",
        "genetic_variant",
        "lab_unit",
        "clinical_sign",
        "medication_class"
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for module in modules:
        module_dir = recognizers_dir / module
        test_script = module_dir / f"test_{module}_identifier.py"
        
        print(f"\n{'='*60}")
        print(f"TESTING MODULE: {module.upper()}")
        print(f"{'='*60}")
        
        if test_script.exists():
            print(f"Running test script: {test_script}")
            result = run_test_script(test_script)
            test_results[module] = result
            total_tests += 1
            
            if result['success']:
                passed_tests += 1
                print(f"✅ {module}: PASSED")
                if result['stdout']:
                    print("Output:")
                    print(result['stdout'])
            else:
                failed_tests += 1
                print(f"❌ {module}: FAILED")
                if result['stderr']:
                    print("Error:")
                    print(result['stderr'])
                if result['stdout']:
                    print("Output:")
                    print(result['stdout'])
        else:
            print(f"⚠️  {module}: Test script not found at {test_script}")
            test_results[module] = {
                'success': False,
                'stdout': '',
                'stderr': 'Test script not found',
                'returncode': -3
            }
            failed_tests += 1
    
    # Print summary
    print(f"\n{'='*80}")
    print("TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Total modules tested: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "N/A")
    
    # Print detailed results
    print(f"\n{'='*80}")
    print("DETAILED RESULTS")
    print(f"{'='*80}")
    
    for module, result in test_results.items():
        status = "✅ PASSED" if result['success'] else "❌ FAILED"
        print(f"{module:20} {status}")
    
    # Exit with appropriate code
    if failed_tests > 0:
        print(f"\n❌ {failed_tests} test(s) failed")
        sys.exit(1)
    else:
        print(f"\n✅ All {passed_tests} tests passed successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
