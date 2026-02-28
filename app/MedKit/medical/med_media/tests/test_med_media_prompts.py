import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from medical.med_media.med_media_prompts import PromptBuilder

def test_create_system_prompt():
    prompt = PromptBuilder.create_system_prompt()
    assert "medical media specialist" in prompt
    assert "professional captions" in prompt

def test_create_caption_prompt():
    topic = "chest X-ray"
    prompt = PromptBuilder.create_caption_prompt(topic, "image")
    assert topic in prompt
    assert "image" in prompt
    assert "medical caption" in prompt

def test_create_summary_prompt():
    topic = "diabetes mellitus"
    prompt = PromptBuilder.create_summary_prompt(topic, "video")
    assert topic in prompt
    assert "video" in prompt
    assert "medical summary" in prompt
