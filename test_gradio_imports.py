#!/usr/bin/env python3
"""Test script to verify Gradio imports work with proper path adjustments."""

import sys
import os

# Add the project root to the path
sys.path.insert(0, "/Users/csv610/Projects/LiteLLM")


# Mock gradio since it's not installed
class MockGradio:
    class Blocks:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    class Textbox:
        def __init__(self, *args, **kwargs):
            pass

    class Dropdown:
        def __init__(self, *args, **kwargs):
            pass

    class Button:
        def __init__(self, *args, **kwargs):
            pass

    class Markdown:
        def __init__(self, *args, **kwargs):
            pass

    @staticmethod
    def fn(*args, **kwargs):
        def decorator(func):
            return func

        return decorator


# Replace the gradio module
sys.modules["gradio"] = MockGradio()

# Test importing a few Gradio files
test_files = [
    "app/ArticleReviewer/agentic/article_reviewer_gradio.py",
    "app/DeepIntuition/agentic/deep_intuition_gradio.py",
    "app/DigiTeacher/FeynmanTutor/feynman_tutor_gradio.py",
]

for file_path in test_files:
    full_path = os.path.join("/Users/csv610/Projects/LiteLLM", file_path)
    try:
        with open(full_path, "r") as f:
            content = f.read()
        # Execute the content up to the main block
        main_split = content.split('if __name__ == "__main__":')
        if len(main_split) > 0:
            exec(main_split[0], {"__file__": full_path})
            print(f"✓ {file_path} - Import successful")
        else:
            print(f"✗ {file_path} - No content before main block")
    except Exception as e:
        print(f"✗ {file_path} - Import failed: {e}")

print("Done testing Gradio imports")
