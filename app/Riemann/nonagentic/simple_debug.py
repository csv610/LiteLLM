#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).parent.parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from Riemann.nonagentic.riemann_problems_models import RiemannTheoryModel

print("Starting simple debug test...")
model = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3:12b")
print(f"Using model: {model}")

model_config = ModelConfig(model=model, temperature=0.3)
print("Created model config")

client = LiteClient(model_config)
print("Created LiteClient instance")

# Test direct call without response_format first
model_input = ModelInput(
    system_prompt="You are a helpful assistant.", user_prompt="What is 2+2?"
)

try:
    print("Making simple test call...")
    result = client.generate_text(model_input)
    print(f"Simple test result: {result}")
except Exception as e:
    print(f"Simple test failed: {e}")
    import traceback

    traceback.print_exc()

# Now test with response_format
model_input2 = ModelInput(
    system_prompt="You are a helpful assistant that outputs JSON.",
    user_prompt='{"answer": 4}',
    response_format=RiemannTheoryModel,
)

try:
    print("\nMaking structured test call...")
    result2 = client.generate_text(model_input2)
    print(f"Structured test result: {result2}")
    print(f"Structured test result type: {type(result2)}")
except Exception as e:
    print(f"Structured test failed: {e}")
    import traceback

    traceback.print_exc()
