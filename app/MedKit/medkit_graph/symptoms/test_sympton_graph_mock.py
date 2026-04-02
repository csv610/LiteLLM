import os
import shutil
import subprocess
from pathlib import Path


def test_generate_graph():
    symptom = "Cough"
    test_dir = Path(__file__).parent
    output_dir = test_dir / "outputs"
    output_dot = output_dir / f"{symptom}.dot"

    # Remove outputs directory if it exists to start fresh
    if output_dir.exists():
        shutil.rmtree(output_dir)

    print(f"🧪 Testing graph generation for: {symptom}")

    # Run the script
    result = subprocess.run(
        ["python3", "sympton_graph.py", symptom],
        capture_output=True,
        text=True,
        cwd=test_dir,
    )

    if result.returncode != 0:
        print(f"❌ Script failed with error: {result.stderr}")
    assert result.returncode == 0, result.stderr

    print(f"✅ Script output: {result.stdout.strip()}")

    # Check if the output file exists
    if output_dot.exists():
        print(f"✅ Output file created: {output_dot}")

        # Check content
        with open(output_dot, "r") as f:
            content = f.read()
            if "digraph SymptomGraph {" in content and symptom in content:
                print("✅ DOT file content is valid.")
            else:
                print("❌ DOT file content is invalid.")
            assert "digraph SymptomGraph {" in content and symptom in content
    else:
        print(f"❌ Output file NOT found: {output_dot}")
    assert output_dot.exists(), f"Expected output file not found: {output_dot}"


if __name__ == "__main__":
    if test_generate_graph():
        print("🎉 Test PASSED!")
    else:
        print("😢 Test FAILED!")
        exit(1)
