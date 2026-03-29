import pytest
import os
from pathlib import Path
from studyguide_models import BookInput
from studyguide_generator import StudyGuideGenerator
from lite.config import ModelConfig

@pytest.mark.skipif(os.environ.get("LIVE_TEST") != "true", reason="Skipping live test. Set LIVE_TEST=true to run.")
def test_generate_and_save_live():
    """Live test using a real LLM. Use a small book to save tokens."""
    model_name = os.environ.get("TEST_MODEL", "ollama/gemma3")
    config = ModelConfig(model=model_name, temperature=0.2)
    generator = StudyGuideGenerator(config)
    
    # Using a very simple, short book to minimize costs/time
    book_input = BookInput(title="The Cat in the Hat", author="Dr. Seuss")
    
    output_file_str = generator.generate_and_save(book_input)
    output_file = Path(output_file_str)
    
    assert output_file.exists()
    content = output_file.read_text()
    
    assert "The Cat in the Hat" in content
    assert "Dr. Seuss" in content
    assert "## IV. Chapter-by-Chapter Deep Deconstruction" in content
    
    print(f"\nLive test output saved to: {output_file_str}")
