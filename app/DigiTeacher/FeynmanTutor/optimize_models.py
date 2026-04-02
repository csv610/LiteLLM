"""
optimize_models.py - Script to optimize Pydantic models for FeynmanTutor using DSPydantic with Ollama.
"""

import dspy
from feynman_tutor import FeynmanTutorQuestionGenerator, ModelConfig

# Configure DSPy to use Ollama
ollama_lm = dspy.Ollama(
    model="llama3",  # Change to your preferred Ollama model
    max_tokens=2000,
    temperature=0.7,
)
dspy.settings.configure(lm=ollama_lm)


def feynman_response_metric(example, pred, trace=None):
    """
    Validation metric for Feynman tutor responses.
    Checks that the response is helpful, educational, and follows the Feynman technique principles.
    """
    if not isinstance(pred, str) or not pred.strip():
        return False

    # Basic quality checks
    if len(pred.strip()) < 10:
        return False

    # Check for Feynman technique elements (customize based on what you value)
    # These are examples - adjust based on your specific goals
    feynman_elements = [
        "simple",
        "simply",
        "easy",
        "basic",
        "fundamental",  # Simplicity focus
        "example",
        "analogy",
        "like",
        "imagine",  # Analogies/examples
        "why",
        "how",
        "what",  # Questioning approach
        "imagine",
        "picture",
        "visualize",  # Visualization
    ]

    # At least some Feynman-like elements should be present
    pred_lower = pred.lower()
    matches = sum(1 for element in feynman_elements if element in pred_lower)

    # Require at least 2 Feynman technique elements in reasonable length responses
    if len(pred) > 50 and matches < 2:
        return False

    # Should not be overly complex or jargon-heavy without explanation
    jargon_indicators = ["therefore", "thus", "consequently", "furthermore", "moreover"]
    jargon_count = sum(1 for indicator in jargon_indicators if indicator in pred_lower)

    # If too much formal jargon without balancing simple elements, it's not following Feynman
    if jargon_count > 3 and matches < 1:
        return False

    return True


# Example training data - REPLACE WITH YOUR HIGH-QUALITY EXAMPLES
# These should be examples of good Feynman-style explanations
trainset = [
    dspy.Example(
        topic="Photosynthesis",
        # This simulates what the tutor would generate - a good Feynman-style explanation
        explanation="Photosynthesis is how plants make their own food using sunlight. Imagine a plant as a solar-powered kitchen: it takes in water through its roots (like bringing in ingredients), carbon dioxide from the air (like grabbing more supplies), and uses sunlight as energy to cook sugar (glucose) and release oxygen as a byproduct. The chlorophyll in leaves is like the solar panels that catch the sunlight energy.",
    ).with_inputs("topic"),
    dspy.Example(
        topic="Vaccines",
        explanation="Think of a vaccine like a wanted poster for your immune system. It shows your body's defenses what a bad germ looks like without actually letting the bad germ in. Your immune system studies this poster, learns to recognize the germ, and builds up defenses. Then if the real germ ever shows up, your body already knows how to fight it off quickly.",
    ).with_inputs("topic"),
    dspy.Example(
        topic="How a refrigerator works",
        explanation="A refrigerator doesn't actually make things cold - it moves heat from inside to outside, like carrying heat out of a room. Inside, there's a special liquid that easily absorbs heat (like a sponge soaking up water). This liquid flows through pipes inside the fridge, picking up heat from your food. Then it goes outside where it releases that heat into the room (like wringing out the sponge outside). A pump keeps the liquid circulating to continuously move heat from inside to outside.",
    ).with_inputs("topic"),
    # Add more examples as needed
]

# Optimize using BootstrapFewShot
from dspy.teleprompt import BootstrapFewShot

print("Optimizing FeynmanTutor responses with Ollama...")
optimizer = BootstrapFewShot(
    metric=feynman_response_metric, max_bootstrapped_demos=3, max_labeled_demos=5
)


# We'll create a wrapper class/function to optimize
class FeynmanResponseOptimizer:
    def __init__(self, topic: str):
        self.topic = topic

    def __call__(self):
        # This is a simplified version - in practice you'd integrate with the actual tutor
        # For demonstration, we're optimizing the response generation
        pass


# Since FeynmanTutor is more complex, we'll show how to optimize specific aspects
# For now, we'll demonstrate the concept with a simple response generator
from dspy import Predict, Signature


class FeynmanExplain(Signature):
    topic = dspy.InputField(desc="The topic to explain")
    explanation = dspy.OutputField(
        desc="A clear, simple explanation using the Feynman technique"
    )


feynman_predict = Predict(FeynmanExplain)
optimizer = BootstrapFewShot(metric=feynman_response_metric, max_bootstrapped_demos=3)
optimized_feynman_predict = optimizer.compile(feynman_predict, trainset=trainset)

print("Optimization complete!")

# Test the optimized predictor
test_topic = "How vaccines work"
try:
    result = optimized_feynman_predict(topic=test_topic)
    print("\n=== Test Result ===")
    print(f"Topic: {result.topic}")
    print(f"Explanation: {result.explanation}")
except Exception as e:
    print(f"Error during prediction: {e}")

# Optional: Save the optimized model
# import pickle
# with open('optimized_feynman_tutor.pkl', 'wb') as f:
#     pickle.dump(optimized_feynman_predict, f)


class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)
