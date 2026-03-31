"""
optimize_models.py - Script to optimize Pydantic models for DeepIntuition using DSPydantic with Ollama.
"""

import dspy
from deep_intuition_models import IntuitionResponse  # Assuming this is the main model

# Configure DSPy to use Ollama
ollama_lm = dspy.Ollama(
    model="llama3",  # Change to your preferred Ollama model
    max_tokens=2000,
    temperature=0.7,  # Higher temperature for more creative intuition
)
dspy.settings.configure(lm=ollama_lm)


def intuition_response_metric(example, pred, trace=None):
    """
    Validation metric for IntuitionResponse model.
    """
    # Check required fields exist
    if not isinstance(pred.topic, str) or not pred.topic.strip():
        return False

    if (
        not isinstance(pred.executive_summary, str)
        or len(pred.executive_summary.strip()) < 20
    ):
        return False

    if not isinstance(pred.key_insights, list):
        return False
    if not isinstance(pred.reasoning_chain, list):
        return False

    # Check that lists have reasonable content
    if len(pred.key_insights) == 0:
        return False
    if len(pred.reasoning_chain) == 0:
        return False

    # Check that insights and reasoning steps are strings
    for insight in pred.key_insights:
        if not isinstance(insight, str) or not insight.strip():
            return False

    for step in pred.reasoning_chain:
        if not isinstance(step, str) or not step.strip():
            return False

    # Optional: Check alternative perspectives if present
    if (
        hasattr(pred, "alternative_perspectives")
        and pred.alternative_perspectives is not None
    ):
        if not isinstance(pred.alternative_perspectives, list):
            return False
        for perspective in pred.alternative_perspectives:
            if not isinstance(perspective, str) or not perspective.strip():
                return False

    return True


# Example training data - REPLACE WITH YOUR HIGH-QUALITY EXAMPLES
trainset = [
    dspy.Example(
        problem_statement="How can we reduce plastic waste in oceans?",
        executive_summary="Reducing ocean plastic requires a multi-faceted approach combining improved waste management systems, biodegradable material alternatives, and economic incentives for recycling and cleanup efforts.",
        key_insights=[
            "Most ocean plastic originates from just 10 river systems, primarily in Asia and Africa",
            "Economic incentives for recycling can be more effective than regulatory approaches in developing countries",
            "Microplastics from synthetic textiles represent a significant but often overlooked source",
        ],
        reasoning_chain=[
            "Identified primary sources of ocean plastic through watershed analysis",
            "Evaluated effectiveness of different intervention strategies based on case studies",
            "Synthesized findings into a comprehensive reduction strategy",
        ],
        alternative_perspectives=[
            "Some argue that cleanup efforts should focus on gyres rather than river sources",
            "Others believe technological solutions like autonomous cleanup vessels are most promising",
        ],
    ).with_inputs("problem_statement"),
    dspy.Example(
        problem_statement="What makes a successful startup team?",
        executive_summary="Successful startup teams combine complementary skill sets, shared vision, and psychological safety that allows for rapid iteration and learning from failure.",
        key_insights=[
            "Technical founders benefit significantly from having a co-founder with strong business and customer development skills",
            "Teams that establish psychological safety early show faster iteration and better problem-solving",
            "Shared vision acts as a stabilizing force during the inevitable challenges of early-stage startups",
        ],
        reasoning_chain=[
            "Analyzed characteristics of successful vs unsuccessful startup teams from case studies",
            "Identified common patterns in team composition and dynamics",
            "Synthesized findings into key factors for startup team success",
        ],
        alternative_perspectives=[
            "Some investors prioritize domain expertise over complementary skills in early teams",
            "Others argue that single-founder teams can be more effective due to clearer decision-making",
        ],
    ).with_inputs("problem_statement"),
    # Add more examples as needed
]

# Optimize using BootstrapFewShot
from dspy.teleprompt import BootstrapFewShot

print("Optimizing IntuitionResponse model with Ollama...")
optimizer = BootstrapFewShot(
    metric=intuition_response_metric, max_bootstrapped_demos=3, max_labeled_demos=5
)

optimized_intuition_response = optimizer.compile(IntuitionResponse, trainset=trainset)

print("Optimization complete!")

# Test the optimized model
test_problem = "How can cities reduce traffic congestion while improving air quality?"
try:
    result = optimized_intuition_response(problem_statement=test_problem)
    print("\n=== Test Result ===")
    print(f"Problem: {result.problem_statement}")
    print(f"Executive Summary: {result.executive_summary[:100]}...")
    print(f"Number of Key Insights: {len(result.key_insights)}")
    print(f"Number of Reasoning Steps: {len(result.reasoning_chain)}")
    if result.key_insights:
        print(f"Sample Insight: {result.key_insights[0]}")
    if result.reasoning_chain:
        print(f"Sample Reasoning: {result.reasoning_chain[0]}")
    if hasattr(result, "alternative_perspectives") and result.alternative_perspectives:
        print(
            f"Number of Alternative Perspectives: {len(result.alternative_perspectives)}"
        )
        if result.alternative_perspectives:
            print(f"Sample Alternative: {result.alternative_perspectives[0]}")
except Exception as e:
    print(f"Error during prediction: {e}")

# Optional: Save the optimized model
# import pickle
# with open('optimized_intuition_response.pkl', 'wb') as f:
#     pickle.dump(optimized_intuition_response, f)
