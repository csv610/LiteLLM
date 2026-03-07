
import os
import pytest
from deep_intuition import DeepIntuition
from lite import ModelConfig
from deep_intuition_models import DeepIntuitionStory

@pytest.mark.live
def test_live_story_generation():
    """Live test for the story generation engine using a real LLM."""
    
    # Use a faster/cheaper model for testing if not specified in environment
    model_name = os.getenv("TEST_LLM_MODEL", "openai/gpt-4o-mini")
    
    # Check if API key for the chosen model is available
    if "openai" in model_name and not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set, skipping live test")
    
    model_config = ModelConfig(model=model_name, temperature=0.7)
    engine = DeepIntuition(model_config=model_config)
    
    topic = "The Pythagorean Theorem"
    
    print(f"\n🚀 Running live test for topic: '{topic}' using model: '{model_name}'")
    
    try:
        story = engine.generate_story(topic)
        
        # Validation
        assert isinstance(story, DeepIntuitionStory)
        assert story.topic == topic
        assert len(story.the_human_struggle) > 200
        assert len(story.the_aha_moment) > 100
        assert len(story.human_triumph_rationale) > 100
        assert len(story.counterfactual_world) > 100
        assert len(story.modern_resonance) > 100
        assert len(story.key_historical_anchors) >= 1
        
        print(f"\n✅ Live test passed! Story generated successfully with {len(story.the_human_struggle)} chars in struggle.")
        
    except Exception as e:
        pytest.fail(f"Live story generation failed: {e}")

if __name__ == "__main__":
    # If run directly, run the test
    pytest.main([__file__, "-v", "-s", "-m", "live"])
