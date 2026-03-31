"""
deep_deliberation.py - The Knowledge Discovery Engine (Orchestrator)

Orchestrates the Discovery Swarm by coordinating Agents and Persistence.
"""

import logging
import concurrent.futures
from typing import List, Optional, Dict

from lite import LiteClient, ModelConfig
from lite.config import ModelInput

from .deep_deliberation_models import (
    DiscoveryFAQ, InitialKnowledgeMap, KnowledgeSynthesis
)
from .deep_deliberation_prompts import PromptBuilder
from .deep_deliberation_agents import DiscoveryAgent
from .deep_deliberation_archive import MissionArchive

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

    def run(self, topic: str, num_rounds: int, num_faqs: int = 5, output_path: Optional[str] = None) -> KnowledgeSynthesis:
        """Run the multi-wave discovery mission."""
        archive = MissionArchive(topic, output_path)
        analysis_list: List[str] = []
        summary_history: List[str] = []

        # Wave 0: Initialization
        print(f"\n[1/3] Initiating Mission: Mapping pillars for '{topic}'...")
        init_input = ModelInput(
            user_prompt=PromptBuilder.get_initial_prompt(topic, num_faqs),
            response_format=InitialKnowledgeMap
        )
        initial_map: InitialKnowledgeMap = self.client.generate_text(init_input)
        
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
        print("\n[3/3] Synthesizing Final Strategic Map...")
        synthesis_input = ModelInput(
            user_prompt=PromptBuilder.get_synthesis_prompt(topic, analysis_list),
            response_format=KnowledgeSynthesis
        )
        final_map = self.client.generate_text(synthesis_input)
        archive.set_final_map(final_map)

        return final_map
