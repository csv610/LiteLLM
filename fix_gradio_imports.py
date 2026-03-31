#!/usr/bin/env python3
import sys
from pathlib import Path
import glob

# Define the robust path adjustment code
robust_code = """# Add the project root to sys.path
path = Path(__file__).parent
while path.name != "app" and path.parent != path:
    path = path.parent
if path.name == "app":
    root = path.parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
"""

# Find all _gradio.py files
gradio_files = glob.glob("**/*_gradio.py", recursive=True)
print(f"Found {len(gradio_files)} Gradio files")

for file_path in gradio_files:
    print(f"Processing {file_path}")
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Check if the robust code is already present
    if 'while path.name != "app" and path.parent != path:' in "".join(lines):
        print(f"  Robust code already present in {file_path}")
        continue

    # Look for the old pattern to replace
    old_pattern = "# Add parent directory to path for imports\nsys.path.insert(0, str(Path(__file__).parent.parent.parent))"
    old_pattern_lines = [
        "# Add parent directory to path for imports\n",
        "sys.path.insert(0, str(Path(__file__).parent.parent.parent))\n",
    ]

    # Check if the old pattern exists consecutively
    found_old = False
    for i in range(len(lines) - 1):
        if lines[i] == old_pattern_lines[0] and lines[i + 1] == old_pattern_lines[1]:
            # Replace the two lines with the robust code
            lines[i] = robust_code + "\n"
            del lines[i + 1]  # Remove the second line of the old pattern
            found_old = True
            print(f"  Replaced old path adjustment in {file_path}")
            break

    if not found_old:
        # If we didn't find the old pattern, we need to insert the robust code
        # We'll insert it after the last standard import (before any project imports)
        # We'll look for the first import that seems to be from the project
        # Project imports start with: from lite, from app, or from . (relative)
        insert_index = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if (
                stripped.startswith("from lite")
                or stripped.startswith("from app")
                or stripped.startswith("from .")
            ):
                insert_index = i
                break
            # Also skip blank lines and comments at the top
            if stripped and not stripped.startswith("#"):
                # This is likely a standard import or third-party import
                pass
        # Insert the robust code at the insert_index position
        lines.insert(insert_index, robust_code + "\n")
        print(f"  Inserted robust code at position {insert_index} in {file_path}")

    # Write the file back
    with open(file_path, "w") as f:
        f.writelines(lines)

print("Done")
