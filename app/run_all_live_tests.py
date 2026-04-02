import os
import subprocess

def run_tests():
    test_files = []
    # Only target nonagentic/noagentic live tests that match our new naming convention
    for root, dirs, files in os.walk("."):
        if "nonagentic" in root or "noagentic" in root:
            for file in files:
                if file.endswith("_live.py") and file.startswith("test_") and ("nonagentic" in file or "noagentic" in file):
                    test_files.append(os.path.join(root, file))
    
    # Also include the special MillenniumPrize test if it exists
    if os.path.exists("MillenniumPrize/nonagentic/test_millennium_prize_live.py"):
        test_files.append("MillenniumPrize/nonagentic/test_millennium_prize_live.py")

    test_files = list(set(test_files)) # Deduplicate
    test_files.sort()
    results = {}
    
    env = os.environ.copy()
    if "DEFAULT_LLM_MODEL" not in env:
        env["DEFAULT_LLM_MODEL"] = "ollama/gemma3:12b-cloud"
    
    print(f"Running {len(test_files)} nonagentic live tests...")
    
    for test_file in test_files:
        print(f"Running {test_file}...", end=" ", flush=True)
        try:
            # Using pytest for better handling
            result = subprocess.run(
                ["pytest", test_file, "-q", "--no-summary"],
                env=env,
                capture_output=True,
                text=True,
                timeout=180 # 3 minutes timeout
            )
            if result.returncode == 0:
                print("PASSED")
                results[test_file] = "PASSED"
            else:
                print("FAILED")
                results[test_file] = "FAILED"
                # print(result.stdout)
                # print(result.stderr)
        except subprocess.TimeoutExpired:
            print("TIMEOUT")
            results[test_file] = "TIMEOUT"
        except Exception as e:
            print(f"ERROR: {e}")
            results[test_file] = f"ERROR: {e}"
            
    print("\n--- Summary ---")
    passed = sum(1 for r in results.values() if r == "PASSED")
    failed = sum(1 for r in results.values() if r == "FAILED")
    timeout = sum(1 for r in results.values() if r == "TIMEOUT")
    
    for test, status in results.items():
        print(f"{test}: {status}")
        
    print(f"\nTotal: {len(results)}, Passed: {passed}, Failed: {failed}, Timeout: {timeout}")

if __name__ == "__main__":
    run_tests()
