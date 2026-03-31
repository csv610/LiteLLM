"""
optimize_models.py - Script to optimize Pydantic models for HadamardTutor using DSPydantic with Ollama.
"""

import dspy
from hadamard_tutor import HadamardTutorQuestionGenerator, ModelConfig

# Configure DSPy to use Ollama
ollama_lm = dspy.Ollama(
    model="llama3",  # Change to your preferred Ollama model
    max_tokens=2000,
    temperature=0.7,
)
dspy.settings.configure(lm=ollama_lm)


def hadamard_response_metric(example, pred, trace=None):
    """
    Validation metric for Hadamard tutor responses.
    Checks that the response follows the four phases of discovery and is helpful.
    """
    if not isinstance(pred, str) or not pred.strip():
        return False

    # Basic quality checks
    if len(pred.strip()) < 10:
        return False

    # Check for Hadamard phase elements (Preparation, Incubation, Illumination, Verification)
    hadamard_phases = [
        "preparation",
        "incubation",
        "illumination",
        "verification",
        "prepare",
        "incubate",
        "illuminate",
        "verify",
        "gather",
        "explore",
        "simmer",
        "insight",
        "aha",
        "test",
        "refine",
    ]

    # At least some Hadamard-like elements should be present
    pred_lower = pred.lower()
    matches = sum(1 for phase in hadamard_phases if phase in pred_lower)

    # Require at least 2 Hadamard phase elements in reasonable length responses
    if len(pred) > 30 and matches < 2:
        return False

    # Should not be too generic or lacking in structure
    generic_phrases = ["i think", "maybe", "perhaps", "it seems"]
    generic_count = sum(1 for phrase in generic_phrases if phrase in pred_lower)

    # If too many hesitant phrases without substantive content, it's not following the method well
    if generic_count > 3 and len(pred) < 100:
        return False

    return True


# Example training data - REPLACE WITH YOUR HIGH-QUALITY EXAMPLES
trainset = [
    dspy.Example(
        topic="How to improve public speaking skills",
        # This simulates what the tutor would generate - a good Hadamard-style response covering the phases
        response="**Preparation**: To improve public speaking, start by researching effective techniques, studying great speakers, and understanding the fundamentals of vocal variety, body language, and speech structure. **Incubation**: Let these ideas sit in your mind while you engage in other activities - take a walk, do some chores, or sleep on it. Often your subconscious will make connections you didn't see consciously. **Illumination**: You might suddenly realize that the key is not perfection but authentic connection with your audience, or that practicing in front of a mirror helps build confidence. **Verification**: Test your improved speaking by giving short presentations to friends or joining a group like Toastmasters, then refine based on feedback.",
    ).with_inputs("topic"),
    dspy.Example(
        topic="Learning a new programming language",
        response="**Preparation**: Begin by studying the language syntax, data structures, and common idioms. Read tutorials and documentation to build a foundation. **Incubation**: While working on other tasks or taking breaks, let your mind process how the language features relate to concepts you already know. **Illumination**: You might have an 'aha!' moment when you see how a particular feature solves a problem you've struggled with before, or realize that the language's approach to error handling is actually simpler than you thought. **Verification**: Build a small project using the language, then refine your approach based on what worked and what didn't.",
    ).with_inputs("topic"),
    # Add more examples as needed
]

# Optimize using BootstrapFewShot
from dspy.teleprompt import BootstrapFewShot

print("Optimizing HadamardTutor responses with Ollama...")
optimizer = BootstrapFewShot(
    metric=hadamard_response_metric, max_bootstrapped_demos=3, max_labeled_demos=5
)


# We'll create a wrapper class/function to optimize
class HadamardResponseOptimizer:
    def __init__(self, topic: str):
        self.topic = topic

    def __call__(self):
        # This is a simplified version - in practice you'd integrate with the actual tutor
        # For demonstration, we're optimizing the response generation
        pass


# Since HadamardTutor is more complex, we'll show how to optimize specific aspects
# For now, we'll demonstrate the concept with a simple response generator
from dspy import Predict, Signature


class HadamardExplain(Signature):
    topic = dspy.InputField(desc="The topic to explore using the Hadamard method")
    response = dspy.OutputField(
        desc="A response that covers the Preparation, Incubation, Illumination, and Verification phases"
    )


hadamard_predict = Predict(HadamardExplain)
optimizer = BootstrapFewShot(metric=hadamard_response_metric, max_bootstrapped_demos=3)
optimized_hadamard_predict = optimizer.compile(hadamard_predict, trainset=trainset)

print("Optimization complete!")

# Test the optimized predictor
test_topic = "How to learn a new skill"
try:
    result = optimized_hadamard_predict(topic=test_topic)
    print("\n=== Test Result ===")
    print(f"Topic: {result.topic}")
    print(f"Response: {result.response}")
except Exception as e:
    print(f"Error during prediction: {e}")

# Optional: Save the optimized model
# import pickle
# with open('optimized_hadamard_tutor.pkl', 'wb') as f:
#     pickle.dump(optimized_hadamard_predict, f)
