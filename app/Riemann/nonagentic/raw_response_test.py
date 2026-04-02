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

print("Testing raw response from Ollama...")
model = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3:12b")
print(f"Using model: {model}")

model_config = ModelConfig(model=model, temperature=0.3)
client = LiteClient(model_config)

# Test with just text response (no structured output)
model_input = ModelInput(
    system_prompt="You are a helpful mathematician.",
    user_prompt="Tell me about the Riemann Hypothesis in a few sentences.",
)

try:
    print("Making raw text call...")
    result = client.generate_text(model_input)
    print(f"Raw text result: {result}")
    print(f"Raw text result type: {type(result)}")
except Exception as e:
    print(f"Raw text test failed: {e}")
    import traceback

    traceback.print_exc()

# Now test with response_format but see what we get
from Riemann.nonagentic.riemann_problems_prompts import PromptBuilder
from Riemann.nonagentic.riemann_problems_models import RiemannTheoryModel

model_input2 = ModelInput(
    system_prompt=PromptBuilder.get_system_prompt(),
    user_prompt=PromptBuilder.get_user_prompt("Riemann Hypothesis"),
    response_format=RiemannTheoryModel,
)

try:
    print("\nMaking structured call...")
    result2 = client.generate_text(model_input2)
    print(f"Structured result: {result2}")
    print(f"Structured result type: {type(result2)}")

    # Let's also see what the raw response looks like before parsing
    # We'll temporarily bypass the JSON parsing
    import json
    from lite.utils.json_cleaner import JSONCleaner

    messages = client.create_message(model_input2)
    print(f"Messages: {messages}")

    from litellm import completion

    response = completion(
        model=model_config.model,
        messages=messages,
        temperature=model_config.temperature,
        response_format=RiemannTheoryModel,
    )

    response_content = response.choices[0].message.content
    print(f"\nRaw response content: {response_content}")
    print(f"Raw response content type: {type(response_content)}")

    # Try to clean and parse it
    cleaned_json = JSONCleaner.extract_json(response_content)
    print(f"Cleaned JSON: {cleaned_json}")

    parsed_response = RiemannTheoryModel.model_validate_json(cleaned_json)
    print(f"Parsed response: {parsed_response}")

except Exception as e:
    print(f"Structured test failed: {e}")
    import traceback

    traceback.print_exc()
