"""
liteagents.py - Unified LiteClient-based agents for DeepIntuition.
"""

from app.DeepIntuition.shared.models import (
from app.DeepIntuition.shared.models import *
from app.DeepIntuition.shared.prompts import AgentPrompts
from app.DeepIntuition.shared.prompts import PromptBuilder
from app.DeepIntuition.shared.utils import *
from deep_intuition_models import IntuitionResponse  # Assuming this is the main model
from dspy.teleprompt import BootstrapFewShot
from lite import LiteClient, ModelConfig
from lite.config import ModelInput
from pathlib import Path
from pydantic import BaseModel
from typing import Any
from typing import Optional, Any
from typing import Optional, Dict, Any, Type
import dspy
import json
import logging

"""
deep_intuition_archive.py - Persistence Component

Handles saving and retrieval of Deep Intuition stories.
"""

class MissionArchive:
    """Persistence manager for Deep Intuition Storytelling."""

    def __init__(self, topic: str, output_path: Optional[str] = None):
        self.topic = topic
        self.output_path = output_path
        self.story: Optional[dict] = None

        if self.output_path:
            Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)

    def set_final_story(self, story: Any):
        """Save the synthesized Deep Intuition story."""
        self.story = story.model_dump() if hasattr(story, 'model_dump') else story
        self._flush()

    def _flush(self):
        """Write the story to disk."""
        if not self.output_path:
            return

        path = Path(self.output_path)
        
        # If story is a string (Markdown), ensure extension is .md
        if isinstance(self.story, str):
            if path.suffix != '.md':
                path = path.with_suffix('.md')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.story)
        else:
            # Otherwise save as JSON
            if path.suffix != '.json':
                path = path.with_suffix('.json')
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.story, f, indent=4, ensure_ascii=False)

"""
deep_intuition.py - The 5-Agent Deep Intuition Storytelling Engine (Refactored)

Orchestrates multiple specialized agents with a DRY, declarative approach.
"""

    DeepIntuitionStory, 
    HistoricalResearch, 
    IntuitionInsight, 
    CounterfactualAnalysis, 
    StruggleNarrative,
    ModelOutput
)

logger = logging.getLogger(__name__)

class DeepIntuition:
    """The 5-Agent Deep Intuition Storytelling Engine."""

    def __init__(self, model_config: ModelConfig):
        """Initialize with a high-fidelity client."""
        self.client = LiteClient(model_config=model_config)

    def _execute_agent(self, 
                       name: str, 
                       prompt: str, 
                       response_model: Optional[Type[BaseModel]], 
                       emoji: str = "🤖") -> Any:
        """Helper to run a single agent and return its output (structured or string)."""
        print(f"{emoji} {name} working...")
        model_input = ModelInput(user_prompt=prompt, response_format=response_model)
        
        try:
            res = self.client.generate_text(model_input)
            if response_model:
                return res.data
            return res.markdown
        except Exception as e:
            logger.error(f"Agent '{name}' failed: {e}")
            raise RuntimeError(f"Mission failed during {name} phase: {e}") from e

    def generate_story(self, topic: str, output_path: Optional[str] = None) -> ModelOutput:
        """Uncover the human story through a 3-tier artifact-based pipeline."""
        archive = MissionArchive(topic, output_path)
        print(f"\n✨ Initiating Deep Intuition mission for '{topic}'...")

        # --- Tier 1: Specialists (JSON) ---
        # 1. Historical Researcher
        historical: HistoricalResearch = self._execute_agent(
            "Historical Researcher",
            AgentPrompts.build(AgentPrompts.HISTORICAL_RESEARCHER, topic=topic),
            HistoricalResearch,
            emoji="🔍"
        )

        # 2. Intuition Specialist
        intuition: IntuitionInsight = self._execute_agent(
            "Intuition Specialist",
            AgentPrompts.build(AgentPrompts.INTUITION_SPECIALIST, topic=topic),
            IntuitionInsight,
            emoji="💡"
        )

        # 3. Counterfactual Analyst
        counterfactual: CounterfactualAnalysis = self._execute_agent(
            "Counterfactual Analyst",
            AgentPrompts.build(AgentPrompts.COUNTERFACTUAL_ANALYST, topic=topic),
            CounterfactualAnalysis,
            emoji="🌍"
        )

        # 4. Human Struggle Narrator
        struggle: StruggleNarrative = self._execute_agent(
            "Human Struggle Narrator",
            AgentPrompts.build(
                AgentPrompts.HUMAN_STRUGGLE_NARRATOR, 
                topic=topic, 
                historical_data=historical.archive_of_failures_details
            ),
            StruggleNarrative,
            emoji="🎭"
        )

        # --- Tier 3: Lead Editor (Final Synthesis - Markdown Closer) ---
        story_markdown: str = self._execute_agent(
            "Lead Editor",
            AgentPrompts.build(
                AgentPrompts.LEAD_EDITOR_WEAVER,
                topic=topic,
                historical=historical.model_dump(),
                intuition=intuition.model_dump(),
                counterfactual=counterfactual.model_dump(),
                struggle=struggle.model_dump()
            ) + "\n\nFINAL INSTRUCTION: Weave these insights into a powerful Markdown story. Use headers, quotes, and emphasized key insights.",
            None,
            emoji="✍️"
        )

        # Create structured data for the .data member
        final_data = DeepIntuitionStory(
            topic=topic,
            the_human_struggle=struggle.the_human_struggle,
            the_aha_moment=intuition.the_aha_moment,
            human_triumph_rationale=struggle.human_triumph_rationale,
            counterfactual_world=counterfactual.counterfactual_world,
            modern_resonance=counterfactual.modern_resonance,
            key_historical_anchors=historical.key_historical_anchors
        )

        archive.set_final_story(story_markdown)
        
        return ModelOutput(
            data=final_data,
            markdown=story_markdown,
            metadata={
                "historical": historical.model_dump(),
                "intuition": intuition.model_dump(),
                "counterfactual": counterfactual.model_dump(),
                "struggle": struggle.model_dump()
            }
        )

"""
optimize_models.py - Script to optimize Pydantic models for DeepIntuition using DSPydantic with Ollama.
"""

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

class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)

