"""
liteagents.py - Unified LiteClient-based agents for DeepDeliberation.
"""

from lite import LiteClient
from lite.config import ModelInput, ModelConfig
from pathlib import Path
from typing import List, Optional, Dict, Any
import concurrent.futures
import json
import logging

from app.DeepDeliberation.shared.models import (
    DiscoveryFAQ,
    DiscoveryInsight,
    DiscoveryCheck,
    VerificationResult,
    SummaryResponse,
    InitialKnowledgeMap,
    KnowledgeSynthesis,
    ModelOutput,
)
from app.DeepDeliberation.shared.prompts import PromptBuilder
from app.DeepDeliberation.shared.utils import save_result, print_result


logger = logging.getLogger(__name__)


class DiscoveryAgent:
    """Agent responsible for processing a single knowledge probe."""

    def __init__(self, client: LiteClient):
        self.client = client

    def analyze(
        self, topic: str, faq: DiscoveryFAQ, context_history: str
    ) -> DiscoveryInsight:
        """Step 1: Perform adversarial analysis of a probe."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_iteration_prompt(
                topic, faq.question, faq.rationale, context_history
            ),
            response_format=DiscoveryInsight,
        )
        return self.client.generate_text(model_input)

    def check_novelty(self, topic: str, analysis: str) -> DiscoveryCheck:
        """Step 2: Adversarial Novelty Gate."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_discovery_check_prompt(topic, analysis),
            response_format=DiscoveryCheck,
        )
        return self.client.generate_text(model_input)

    def verify(self, topic: str, insight: DiscoveryInsight) -> VerificationResult:
        """Step 3: Adversarial Skeptic Verifier."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_verification_prompt(
                topic, insight.analysis, insight.evidence
            ),
            response_format=VerificationResult,
        )
        return self.client.generate_text(model_input)

    def summarize(self, topic: str, analysis: str) -> str:
        """Step 4: Contextual Distillation."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_summary_prompt(topic, analysis),
            response_format=SummaryResponse,
        )
        try:
            result = self.client.generate_text(model_input)
            return result.summary
        except Exception as e:
            logger.error(f"Failed to summarize: {e}")
            return analysis[:200] + "..."


class MissionArchive:
    """Persistence manager for Knowledge Discovery Missions."""

    def __init__(self, topic: str, output_path: Optional[str] = None):
        self.topic = topic
        self.output_path = output_path
        self.history: List[dict] = []
        self.final_map: Optional[Any] = None

        if self.output_path:
            Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)

    def record_step(self, wave: int, query: str, analysis: str, evidence: List[str]):
        """Save a single discovery step to the archive."""
        record = {
            "wave": wave,
            "query": query,
            "analysis": analysis,
            "evidence": evidence,
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

        archive_path = Path(self.output_path)
        if archive_path.suffix != ".json":
            archive_path = archive_path.with_suffix(".json")

        data = {
            "topic": self.topic,
            "discovery_history": self.history,
            "strategic_knowledge_map": self.final_map
            if not is_markdown
            else "See associated .md file",
        }
        with open(archive_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        if is_markdown:
            report_path = archive_path.with_suffix(".md")
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(self.final_map)


class DeepDeliberation:
    """The Swarm-based Knowledge Discovery Orchestrator."""

    def __init__(self, model_config: ModelConfig):
        """Initialize discovery engine with model configuration."""
        self.client = LiteClient(model_config=model_config)
        self.agent = DiscoveryAgent(self.client)

    def _execute_single_probe(
        self, topic: str, faq: DiscoveryFAQ, summary_history: List[str]
    ) -> Optional[Dict]:
        """Worker to process a single probe using the DiscoveryAgent."""
        try:
            context_history = "\n".join(summary_history)

            insight = self.agent.analyze(topic, faq, context_history)

            check = self.agent.check_novelty(topic, insight.analysis)
            if not check.is_novel:
                return {
                    "faq": faq,
                    "rejected": True,
                    "reason": f"Low Novelty: {check.reasoning}",
                }

            verification = self.agent.verify(topic, insight)
            if not verification.is_verified:
                return {
                    "faq": faq,
                    "rejected": True,
                    "reason": f"Verification Failed: {verification.critique}",
                }

            summary = self.agent.summarize(topic, insight.analysis)

            return {
                "faq": faq,
                "insight": insight,
                "check": check,
                "verification": verification,
                "summary": summary,
            }
        except Exception as e:
            logger.error(f"Error executing probe '{faq.question}': {e}")
            return None

    def run(
        self,
        topic: str,
        num_rounds: int,
        num_faqs: int = 5,
        output_path: Optional[str] = None,
    ) -> ModelOutput:
        """Run the multi-wave discovery mission and return a ModelOutput artifact."""
        archive = MissionArchive(topic, output_path)
        analysis_list: List[str] = []
        summary_history: List[str] = []

        print(f"\n[1/3] Initiating Mission: Mapping pillars for '{topic}'...")
        init_input = ModelInput(
            user_prompt=PromptBuilder.get_initial_prompt(topic, num_faqs),
            response_format=InitialKnowledgeMap,
        )
        initial_map: InitialKnowledgeMap = self.client.generate_text(init_input).data

        base_analysis = f"Core Pillars: {', '.join(initial_map.core_pillars)}"
        archive.record_step(
            0, "Base Knowledge Map", base_analysis, initial_map.core_pillars
        )
        analysis_list.append(base_analysis)
        summary_history.append(self.agent.summarize(topic, base_analysis))

        current_faqs: List[DiscoveryFAQ] = list(initial_map.discovery_faqs)
        print(f"✅ Mission seeded with {len(current_faqs)} discovery probes.")

        print("\n[2/3] Launching Parallel Waves...")
        for wave in range(num_rounds):
            if not current_faqs:
                break

            print(f"\n--- Wave {wave + 1} (Processing {len(current_faqs)} Probes) ---")
            new_faqs = []

            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                futures = [
                    executor.submit(
                        self._execute_single_probe, topic, faq, summary_history
                    )
                    for faq in current_faqs
                ]

                for idx, future in enumerate(concurrent.futures.as_completed(futures)):
                    res = future.result()
                    if not res or res.get("rejected"):
                        if res:
                            print(
                                f"  ❌ Probe {idx + 1} Rejected: {res['reason'][:80]}..."
                            )
                        continue

                    faq, insight, check, verification = (
                        res["faq"],
                        res["insight"],
                        res["check"],
                        res["verification"],
                    )
                    print(
                        f"  ✅ Novel Discovery: {faq.question[:50]}... [Novelty: {check.discovery_score} | Cred: {verification.credibility_score}]"
                    )

                    archive.record_step(
                        wave + 1, faq.question, insight.analysis, insight.evidence
                    )
                    analysis_list.append(
                        f"Analysis: {insight.analysis}\nEvidence: {insight.evidence}"
                    )
                    new_faqs.append(insight.new_discovery_faq)
                    summary_history.append(res["summary"])

            current_faqs = new_faqs

        print("\n[3/3] Synthesizing Final Strategic Map (Markdown)...")
        synthesis_input = ModelInput(
            user_prompt=PromptBuilder.get_synthesis_prompt(topic, analysis_list)
            + "\n\nFINAL INSTRUCTION: Output the final strategic knowledge map in a comprehensive Markdown format for human readers. Include an Executive Summary, Hidden Connections, and Research Frontiers.",
            response_format=None,
        )
        final_markdown = self.client.generate_text(synthesis_input).markdown
        archive.set_final_map(final_markdown)

        final_data = KnowledgeSynthesis(
            topic=topic,
            executive_summary="See markdown for full details",
            hidden_connections=[],
            research_frontiers=[],
        )

        return ModelOutput(
            data=final_data,
            markdown=final_markdown,
            metadata={"mission_history": archive.history},
        )
