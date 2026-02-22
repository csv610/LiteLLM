"""Basic usage example for LiteClient with text and vision support."""

from lite import LiteClient, ModelConfig, ModelInput

# 1. Initialize the client
# By default, uses gemini-2.5-flash
client = LiteClient(ModelConfig(model="gemini/gemini-2.5-flash"))

# 2. Simple text completion
print("--- Text Completion ---")
text_input = ModelInput(user_prompt="Explain what a Large Language Model is in one sentence.")
response = client.generate_text(text_input)
print(f"Response: {response}
")

# 3. Vision analysis (Image understanding)
# Note: Provide a valid image path or URL
print("--- Vision Analysis ---")
vision_input = ModelInput(
    user_prompt="What are the main colors in this image?",
    image_path="https://raw.githubusercontent.com/python-pillow/Pillow/main/docs/conf.py" # Just a placeholder, use real image path
)
# vision_response = client.generate_text(vision_input)
# print(f"Vision Response: {vision_response}")

print("Example complete!")
