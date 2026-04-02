"""
liteagents.py - Unified LiteClient-based agents for DeepDeliberation.
"""

from app.DeepDeliberation.shared.models import (
from app.DeepDeliberation.shared.models import *
from app.DeepDeliberation.shared.prompts import PromptBuilder
from app.DeepDeliberation.shared.utils import *
from deep_deliberation_models import (
from dspy.teleprompt import BootstrapFewShot
from lite import LiteClient
from lite import LiteClient, ModelConfig
from lite.config import ModelInput
from pathlib import Path
from typing import Any
from typing import List, Optional, Any
from typing import List, Optional, Dict
import concurrent.futures
import dspy
import json
import logging

"""
deep_deliberation_agents.py - Reusable Discovery Agents

Encapsulates the specialized LLM logic for Inquiry, Analysis, and Verification.
"""

    DiscoveryFAQ, DiscoveryInsight, DiscoveryCheck, VerificationResult, SummaryResponse
)

class DiscoveryAgent:
    """Agent responsible for processing a single knowledge probe."""

    def __init__(self, client: LiteClient):
        self.client = client

    def analyze(self, topic: str, faq: DiscoveryFAQ, context_history: str) -> DiscoveryInsight:
        """Step 1: Perform adversarial analysis of a probe."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_iteration_prompt(topic, faq.question, faq.rationale, context_history),
            response_format=DiscoveryInsight
        )
        return self.client.generate_text(model_input)

    def check_novelty(self, topic: str, analysis: str) -> DiscoveryCheck:
        """Step 2: Adversarial Novelty Gate."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_discovery_check_prompt(topic, analysis),
            response_format=DiscoveryCheck
        )
        return self.client.generate_text(model_input)

    def verify(self, topic: str, insight: DiscoveryInsight) -> VerificationResult:
        """Step 3: Adversarial Skeptic Verifier."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_verification_prompt(topic, insight.analysis, insight.evidence),
            response_format=VerificationResult
        )
        return self.client.generate_text(model_input)

    def summarize(self, topic: str, analysis: str) -> str:
        """Step 4: Contextual Distillation."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_summary_prompt(topic, analysis),
            response_format=SummaryResponse
        )
        try:
            result = self.client.generate_text(model_input)
            return result.summary
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to summarize: {e}")
            return analysis[:200] + "..."

"""
deep_deliberation_archive.py - Persistence Component

Handles incremental saving and retrieval of mission discovery data.
"""

class MissionArchive:
    """Persistence manager for Knowledge Discovery Missions."""

    def __init__(self, topic: str, output_path: Optional[str] = None):
        self.topic = topic
        self.output_path = output_path
        self.history: List[dict] = []
        self.final_map: Optional[dict] = None

        if self.output_path:
            Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)

    def record_step(self, wave: int, query: str, analysis: str, evidence: List[str]):
        """Save a single discovery step to the archive."""
        record = {
            "wave": wave,
            "query": query,
            "analysis": analysis,
            "evidence": evidence
        }
        self.history.append(record)
        self._flush()

    def set_final_map(self, final_map: Any):
        """Save the synthesized Strategic Knowledge Map (Markdown)."""
        self.final_map = final_map
        self._flush()

    def _flush(self):
        """Write the current state to disk."""
        if not self.output_path:
            return

        is_markdown = isinstance(self.final_map, str)
        
        # Save JSON history/archive
        archive_path = Path(self.output_path)
        if archive_path.suffix != ".json":
            archive_path = archive_path.with_suffix(".json")

        data = {
            "topic": self.topic,
            "discovery_history": self.history,
            "strategic_knowledge_map": self.final_map if not is_markdown else "See associated .md file"
        }
        with open(archive_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        # Save separate Markdown report
        if is_markdown:
            report_path = archive_path.with_suffix(".md")
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(self.final_map)

"""
optimize_models.py - Script to optimize Pydantic models for DeepDeliberation using DSPydantic with Ollama.
"""

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

class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)

"""
deep_deliberation.py - The Knowledge Discovery Engine (Orchestrator)

Orchestrates the Discovery Swarm by coordinating Agents and Persistence.
"""

    DiscoveryFAQ, InitialKnowledgeMap, KnowledgeSynthesis
)

logger = logging.getLogger(__name__)

class DeepDeliberation:
    """The Swarm-based Knowledge Discovery Orchestrator."""

    def __init__(self, model_config: ModelConfig):
        """Initialize discovery engine with model configuration."""
        self.client = LiteClient(model_config=model_config)
        self.agent = DiscoveryAgent(self.client)

    def _execute_single_probe(self, topic: str, faq: DiscoveryFAQ, summary_history: List[str]) -> Optional[Dict]:
        """Worker to process a single probe using the DiscoveryAgent."""
        try:
            context_history = "\n".join(summary_history)
            
            # 1. Analyze
            insight = self.agent.analyze(topic, faq, context_history)

            # 2. Novelty Gate
            check = self.agent.check_novelty(topic, insight.analysis)
            if not check.is_novel:
                return {"faq": faq, "rejected": True, "reason": f"Low Novelty: {check.reasoning}"}

            # 3. Verification Gate
            verification = self.agent.verify(topic, insight)
            if not verification.is_verified:
                return {"faq": faq, "rejected": True, "reason": f"Verification Failed: {verification.critique}"}

            # 4. Contextual Summarization
            summary = self.agent.summarize(topic, insight.analysis)
            
            return {
                "faq": faq,
                "insight": insight,
                "check": check,
                "verification": verification,
                "summary": summary
            }
        except Exception as e:
            logger.error(f"Error executing probe '{faq.question}': {e}")
            return None

    def run(self, topic: str, num_rounds: int, num_faqs: int = 5, output_path: Optional[str] = None) -> ModelOutput:
        """Run the multi-wave discovery mission and return a ModelOutput artifact."""
        archive = MissionArchive(topic, output_path)
        analysis_list: List[str] = []
        summary_history: List[str] = []

        # Wave 0: Initialization
        print(f"\n[1/3] Initiating Mission: Mapping pillars for '{topic}'...")
        init_input = ModelInput(
            user_prompt=PromptBuilder.get_initial_prompt(topic, num_faqs),
            response_format=InitialKnowledgeMap
        )
        initial_map: InitialKnowledgeMap = self.client.generate_text(init_input).data
        
        base_analysis = f"Core Pillars: {', '.join(initial_map.core_pillars)}"
        archive.record_step(0, "Base Knowledge Map", base_analysis, initial_map.core_pillars)
        analysis_list.append(base_analysis)
        summary_history.append(self.agent.summarize(topic, base_analysis))

        current_faqs: List[DiscoveryFAQ] = list(initial_map.discovery_faqs)
        print(f"✅ Mission seeded with {len(current_faqs)} discovery probes.")

        # Iterative Swarm Waves
        print("\n[2/3] Launching Parallel Waves...")
        for wave in range(num_rounds):
            if not current_faqs:
                break
            
            print(f"\n--- Wave {wave+1} (Processing {len(current_faqs)} Probes) ---")
            new_faqs = []

            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                futures = [executor.submit(self._execute_single_probe, topic, faq, summary_history) for faq in current_faqs]
                
                for idx, future in enumerate(concurrent.futures.as_completed(futures)):
                    res = future.result()
                    if not res or res.get("rejected"):
                        if res: print(f"  ❌ Probe {idx+1} Rejected: {res['reason'][:80]}...")
                        continue
                    
                    faq, insight, check, verification = res["faq"], res["insight"], res["check"], res["verification"]
                    print(f"  ✅ Novel Discovery: {faq.question[:50]}... [Novelty: {check.discovery_score} | Cred: {verification.credibility_score}]")
                    
                    archive.record_step(wave + 1, faq.question, insight.analysis, insight.evidence)
                    analysis_list.append(f"Analysis: {insight.analysis}\nEvidence: {insight.evidence}")
                    new_faqs.append(insight.new_discovery_faq)
                    summary_history.append(res["summary"])

            current_faqs = new_faqs

        # Synthesis
        print("\n[3/3] Synthesizing Final Strategic Map (Markdown)...")
        synthesis_input = ModelInput(
            user_prompt=PromptBuilder.get_synthesis_prompt(topic, analysis_list) + "\n\nFINAL INSTRUCTION: Output the final strategic knowledge map in a comprehensive Markdown format for human readers. Include an Executive Summary, Hidden Connections, and Research Frontiers.",
            response_format=None # Final output is Markdown
        )
        final_markdown = self.client.generate_text(synthesis_input).markdown
        archive.set_final_map(final_markdown)

        # Create structured data for the .data member
        final_data = KnowledgeSynthesis(
            topic=topic,
            executive_summary="See markdown for full details",
            hidden_connections=[],
            research_frontiers=[]
        )

        return ModelOutput(
            data=final_data,
            markdown=final_markdown,
            metadata={"mission_history": archive.history}
        )

