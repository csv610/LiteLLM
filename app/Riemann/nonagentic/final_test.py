#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).parent.parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from lite.config import ModelConfig
from Riemann.nonagentic.riemann_problems import RiemannTheoryGuide

print("Starting final test...")
model = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3:12b")
print(f"Using model: {model}")

model_config = ModelConfig(model=model, temperature=0.3)
instance = RiemannTheoryGuide(model_config)

input_data = "Riemann Hypothesis"

try:
    print(f"Generating text for: {input_data}")
    result = instance.generate_text(input_data)

    if result is not None:
        print("SUCCESS: Got a result")
        print(f"Result name: {result.name}")
        print(f"Result definition: {result.definition[:100]}...")
        print(f"Result layperson_explanation: {result.layperson_explanation[:100]}...")
    else:
        print("FAILED: Result is None")

except Exception as e:
    print(f"EXCEPTION: {e}")
    import traceback

    traceback.print_exc()
