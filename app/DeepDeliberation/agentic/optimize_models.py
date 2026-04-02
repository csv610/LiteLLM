"""
optimize_models.py - Script to optimize Pydantic models for DeepDeliberation using DSPydantic with Ollama.
"""

import dspy
from deep_deliberation_models import (
    DiscoveryFAQ,
    InitialKnowledgeMap,
    DiscoveryInsight,
    DiscoveryCheck,
    VerificationResult,
    SummaryResponse,
    KnowledgeSynthesis,
)

# Configure DSPy to use Ollama
ollama_lm = dspy.Ollama(
    model="llama3",  # Change to your preferred Ollama model
    max_tokens=2000,
    temperature=0.7,  # Higher temperature for more creative discovery
)
dspy.settings.configure(lm=ollama_lm)


def knowledge_synthesis_metric(example, pred, trace=None):
    """
    Validation metric for KnowledgeSynthesis model.
    """
    # Check required fields
    if not isinstance(pred.topic, str) or not pred.topic.strip():
        return False

    if (
        not isinstance(pred.executive_summary, str)
        or len(pred.executive_summary.strip()) < 20
    ):
        return False

    if not isinstance(pred.hidden_connections, list):
        return False
    if not isinstance(pred.research_frontiers, list):
        return False

    # Check that lists have reasonable content
    if len(pred.hidden_connections) == 0:
        return False
    if len(pred.research_frontiers) == 0:
        return False

    # Check that connections and frontiers are strings
    for conn in pred.hidden_connections:
        if not isinstance(conn, str) or not conn.strip():
            return False

    for frontier in pred.research_frontiers:
        if not isinstance(frontier, str) or not frontier.strip():
            return False

    return True


# Example training data - REPLACE WITH YOUR HIGH-QUALITY EXAMPLES
trainset = [
    dspy.Example(
        topic="Quantum Computing Applications",
        executive_summary="While quantum computing shows promise for specific applications like cryptography and simulation, practical limitations in error correction and qubit stability restrict near-term utility to specialized niches rather than general-purpose computing.",
        hidden_connections=[
            "Quantum error correction challenges resemble classical fault-tolerant systems in distributed computing",
            "Qubit decoherence times parallel limitations in analog signal processing bandwidth",
        ],
        research_frontiers=[
            "Topological qubit approaches for inherent error resistance",
            "Hybrid quantum-classical algorithms for near-term advantage",
            "Quantum-inspired optimization techniques for classical hardware",
        ],
    ).with_inputs("topic"),
    dspy.Example(
        topic="Remote Work Productivity",
        executive_summary="Remote work productivity depends less on individual discipline and more on organizational communication structures, asynchronous collaboration tools, and clear outcome-based metrics rather than activity monitoring.",
        hidden_connections=[
            "Async communication patterns mirror open-source software development workflows",
            "Outcome-based evaluation aligns with agile methodology principles",
        ],
        research_frontiers=[
            "AI-mediated conflict resolution in distributed teams",
            "Virtual presence technologies that replicate spontaneous office interactions",
            "Asynchronous decision-making frameworks for global teams",
        ],
    ).with_inputs("topic"),
    # Add more examples as needed
]

# Optimize using BootstrapFewShot
from dspy.teleprompt import BootstrapFewShot

print("Optimizing KnowledgeSynthesis model with Ollama...")
optimizer = BootstrapFewShot(
    metric=knowledge_synthesis_metric, max_bootstrapped_demos=3, max_labeled_demos=5
)

optimized_knowledge_synthesis = optimizer.compile(KnowledgeSynthesis, trainset=trainset)

print("Optimization complete!")

# Test the optimized model
test_topic = "Artificial Intelligence Ethics"
try:
    result = optimized_knowledge_synthesis(topic=test_topic)
    print("\n=== Test Result ===")
    print(f"Topic: {result.topic}")
    print(f"Executive Summary: {result.executive_summary[:100]}...")
    print(f"Number of Hidden Connections: {len(result.hidden_connections)}")
    print(f"Number of Research Frontiers: {len(result.research_frontiers)}")
    if result.hidden_connections:
        print(f"Sample Connection: {result.hidden_connections[0]}")
    if result.research_frontiers:
        print(f"Sample Frontier: {result.research_frontiers[0]}")
except Exception as e:
    print(f"Error during prediction: {e}")

# Optional: Save the optimized model
# import pickle
# with open('optimized_knowledge_synthesis.pkl', 'wb') as f:
#     pickle.dump(optimized_knowledge_synthesis, f)


from typing import Any

class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)
