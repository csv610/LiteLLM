import re
import time
from pathlib import Path

# Configuration
LOG_DIRS = [
    "logs",
    "drug/logs",
    "medical/logs",
    "medkit_diagnose/logs",
    "med_dictionary/logs",
    "med_legal/logs",
    "medkit_article/article_summary/logs",
    "medkit_article/article_comparison/logs",
    "medkit_article/article_keywords/logs",
    "medkit_article/article_review/logs",
]

CHECK_INTERVAL = 60  # seconds
ERROR_PATTERNS = [r"ERROR", r"CRITICAL", r"Exception"]


def find_all_log_files():
    log_files = []
    project_root = Path(__file__).parent.parent
    for log_dir in LOG_DIRS:
        dir_path = project_root / log_dir
        if dir_path.exists():
            log_files.extend(list(dir_path.glob("*.log")))

    # Also find any directory named 'logs' recursively
    for p in project_root.rglob("**/logs/*.log"):
        if p not in log_files:
            log_files.append(p)

    return log_files


def get_last_line_count(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def check_for_errors(file_path, last_line_count):
    new_errors = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            new_lines = lines[last_line_count:]
            for i, line in enumerate(new_lines):
                if any(re.search(pattern, line) for pattern in ERROR_PATTERNS):
                    # Capture some context
                    context = "".join(
                        new_lines[max(0, i - 5) : min(len(new_lines), i + 10)]
                    )
                    new_errors.append(
                        {
                            "file": str(file_path),
                            "line": line.strip(),
                            "context": context,
                        }
                    )
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return new_errors


def trigger_gemini_fix(error_info):
    print(f"\n[!] New error detected in {error_info['file']}:")
    print(f"    {error_info['line']}")

    prompt = f"""
I found an error in the logs of the MedKit project. 
File: {error_info["file"]}
Error: {error_info["line"]}
Context:
{error_info["context"]}

Please analyze this error, find the root cause in the codebase, and provide a fix.
"""

    # We use 'gemini' command if available, or just output instructions for the user.
    # Since this script runs in the background, it can't easily "talk" to the current session.
    # But it can write a "FIX_ME.md" or similar, or try to invoke gemini cli if configured.

    fix_request_file = Path(__file__).parent.parent / "PENDING_FIX.md"
    with open(fix_request_file, "a", encoding="utf-8") as f:
        f.write(f"\n--- ERROR DETECTED AT {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        f.write(prompt)
        f.write("\n-----------------------------------------------------------\n")

    print(f"[*] Fix request appended to {fix_request_file}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="MedKit Log Error Scanner")
    parser.add_argument(
        "-n",
        "--lines",
        type=int,
        default=50,
        help="Number of lines to scan from the end of each log file",
    )
    parser.add_argument(
        "-f",
        "--fix",
        action="store_true",
        help="Automatically append fix requests to PENDING_FIX.md",
    )
    args = parser.parse_args()

    print("[*] Scanning MedKit log files for recent errors...")
    log_files = find_all_log_files()

    total_errors = 0
    for log_file in log_files:
        try:
            with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                # Scan only the last N lines
                scan_start = max(0, len(lines) - args.lines)
                recent_lines = lines[scan_start:]

                errors_in_file = []
                for i, line in enumerate(recent_lines):
                    if any(re.search(pattern, line) for pattern in ERROR_PATTERNS):
                        context = "".join(
                            recent_lines[max(0, i - 3) : min(len(recent_lines), i + 7)]
                        )
                        errors_in_file.append(
                            {
                                "file": str(log_file),
                                "line": line.strip(),
                                "context": context,
                            }
                        )

                if errors_in_file:
                    print(f"\n[!] Found {len(errors_in_file)} errors in {log_file}")
                    for err in errors_in_file:
                        print(f"    - {err['line']}")
                        if args.fix:
                            trigger_gemini_fix(err)
                        total_errors += 1
        except Exception as e:
            print(f"Error scanning {log_file}: {e}")

    if total_errors == 0:
        print("[+] No recent errors found in the last scan.")
    else:
        print(f"\n[*] Total errors found: {total_errors}")
        if args.fix:
            print("[*] Fix requests have been added to PENDING_FIX.md")
        else:
            print("[*] Run with --fix to generate fix requests in PENDING_FIX.md")


if __name__ == "__main__":
    main()
