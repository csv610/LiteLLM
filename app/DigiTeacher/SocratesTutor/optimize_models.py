"""
optimize_models.py - Script to optimize Pydantic models for SocratesTutor using DSPydantic with Ollama.
"""

import dspy
from socrates_tutor import SocratesTutor, ModelConfig

# Configure DSPy to use Ollama
ollama_lm = dspy.Ollama(
    model="llama3",  # Change to your preferred Ollama model
    max_tokens=2000,
    temperature=0.7,
)
dspy.settings.configure(lm=ollama_lm)


def socrates_response_metric(example, pred, trace=None):
    """
    Validation metric for Socrates tutor responses.
    Checks that the response follows the Socratic method (asking probing questions) and is helpful.
    """
    if not isinstance(pred, str) or not pred.strip():
        return False

    # Basic quality checks
    if len(pred.strip()) < 10:
        return False

    # Check for Socratic method elements (asking questions, encouraging critical thinking)
    socratic_elements = [
        "what",
        "how",
        "why",
        "question",
        "consider",
        "examine",
        "explore",
        "assume",
        "suppose",
        "imagine",
        "what if",
        "however",
        "but",
        "although",
        "evidence",
        "reason",
        "logic",
        "think",
        "believe",
        "know",
        "understand",
    ]

    # At least some Socratic-like elements should be present
    pred_lower = pred.lower()
    matches = sum(1 for element in socratic_elements if element in pred_lower)

    # Require at least 3 Socratic method elements in reasonable length responses
    if len(pred) > 50 and matches < 3:
        return False

    # Should not be just giving answers without questioning
    answer_indicators = [
        "therefore",
        "thus",
        "the answer is",
        "it is clear that",
        "we can conclude",
    ]
    answer_count = sum(1 for indicator in answer_indicators if indicator in pred_lower)

    # If too many conclusive statements without questioning, it's not following the method
    if answer_count > 2 and matches < 2:
        return False

    return True


# Example training data - REPLACE WITH YOUR HIGH-QUALITY EXAMPLES
trainset = [
    dspy.Example(
        topic="What is justice?",
        # This simulates what the tutor would generate - a good Socratic-style response
        response="That's an interesting question about justice. Let's explore it together. What does justice mean to you personally? When you think of a just society, what specific characteristics come to mind? How might your definition of justice apply to situations where resources are limited? Have you considered how different cultures throughout history have defined justice differently? What assumptions might we be making when we talk about justice being universal?",
    ).with_inputs("topic"),
    dspy.Example(
        topic="Is artificial intelligence conscious?",
        response="This is a fascinating question about AI consciousness. To begin, how would you define consciousness in a way that we could potentially measure or observe in an AI system? What specific behaviors or capabilities would lead you to conclude that an AI is truly conscious rather than just simulating consciousness? Have you considered the philosophical challenge of knowing whether any entity besides yourself is truly conscious? What evidence would convince you that an AI has subjective experiences rather than just complex information processing?",
    ).with_inputs("topic"),
    # Add more examples as needed
]

# Optimize using BootstrapFewShot
from dspy.teleprompt import BootstrapFewShot

print("Optimizing SocratesTutor responses with Ollama...")
optimizer = BootstrapFewShot(
    metric=socrates_response_metric, max_bootstrapped_demos=3, max_labeled_demos=5
)


# We'll create a wrapper class/function to optimize
class SocratesResponseOptimizer:
    def __init__(self, topic: str):
        self.topic = topic

    def __call__(self):
        # This is a simplified version - in practice you'd integrate with the actual tutor
        # For demonstration, we're optimizing the response generation
        pass


# Since SocratesTutor is more complex, we'll show how to optimize specific aspects
# For now, we'll demonstrate the concept with a simple response generator
from dspy import Predict, Signature


class SocraticExplain(Signature):
    topic = dspy.InputField(desc="The topic to explore using the Socratic method")
    response = dspy.OutputField(
        desc="A response that asks probing questions to encourage critical thinking"
    )


socratic_predict = Predict(SocraticExplain)
optimizer = BootstrapFewShot(metric=socrates_response_metric, max_bootstrapped_demos=3)
optimized_socratic_predict = optimizer.compile(socratic_predict, trainset=trainset)

print("Optimization complete!")

# Test the optimized predictor
test_topic = "What is the meaning of life?"
try:
    result = optimized_socratic_predict(topic=test_topic)
    print("\n=== Test Result ===")
    print(f"Topic: {result.topic}")
    print(f"Response: {result.response}")
except Exception as e:
    print(f"Error during prediction: {e}")

# Optional: Save the optimized model
# import pickle
# with open('optimized_socratic_tutor.pkl', 'wb') as f:
#     pickle.dump(optimized_socratic_predict, f)
