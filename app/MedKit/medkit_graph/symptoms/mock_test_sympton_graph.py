import os
import subprocess
import shutil

def test_generate_graph():
    symptom = "Cough"
    output_dot = os.path.join("outputs", f"{symptom}.dot")
    
    # Remove outputs directory if it exists to start fresh
    if os.path.exists("outputs"):
        shutil.rmtree("outputs")
        
    print(f"🧪 Testing graph generation for: {symptom}")
    
    # Run the script
    result = subprocess.run(["python3", "sympton_graph.py", symptom], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Script failed with error: {result.stderr}")
        return False
    
    print(f"✅ Script output: {result.stdout.strip()}")
    
    # Check if the output file exists
    if os.path.exists(output_dot):
        print(f"✅ Output file created: {output_dot}")
        
        # Check content
        with open(output_dot, "r") as f:
            content = f.read()
            if "digraph SymptomGraph {" in content and symptom in content:
                print(f"✅ DOT file content is valid.")
                return True
            else:
                print(f"❌ DOT file content is invalid.")
                return False
    else:
        print(f"❌ Output file NOT found: {output_dot}")
        return False

if __name__ == "__main__":
    if test_generate_graph():
        print("🎉 Test PASSED!")
    else:
        print("😢 Test FAILED!")
        exit(1)
