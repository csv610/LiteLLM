"""
liteagents.py - Unified LiteClient-based agents for ScholarWork.
"""

from . import scholar_work_prompts as prompts
from app.ScholarWork.shared.models import *
from app.ScholarWork.shared.models import ResearchBrief, SynthesizedReport, ScholarMajorWork, ModelOutput
from app.ScholarWork.shared.prompts import PromptBuilder
from app.ScholarWork.shared.utils import *
from lite.config import ModelConfig
from lite.lite_client import LiteClient
from typing import Callable, Optional
import logging

"""
scholar_work_generator.py - Multi-agent orchestration engine for scholar work

Orchestrates a 3-agent pipeline (Researcher -> Synthesizer -> Editor) using 
specialized prompts to produce high-quality contribution lists.
"""

logger = logging.getLogger(__name__)

class ScholarWorkGenerator:
    """Multi-agent generator class for creating structured lists of a scholar's major work."""
    
    def __init__(self, model_name: str = "ollama/gemma3", temperature: float = 0.0):
        """Initialize the generator with specified model configuration."""
        self.model_name = model_name
        self.model_config = ModelConfig(model=model_name, temperature=temperature)
        self.client = LiteClient(model_config=self.model_config)
    
    def generate_text(self, scholar_name: str, major_contribution: str = "their most significant work", progress_callback: Optional[Callable[[int, str], None]] = None) -> ModelOutput:
        """Execute the 3-agent pipeline to generate a ModelOutput artifact.

        Args:
            scholar_name: The name of the scholar.
            major_contribution: (Optional) A specific contribution to focus on.
            progress_callback: Optional callback receiving (step_number, message).

        Returns:
            ModelOutput: The final standardized artifact.
        """
        
        # --- AGENT 1: THE RESEARCHER (Tier 1 Specialist) ---
        if progress_callback:
            progress_callback(1, f"Researching major contributions of {scholar_name}...")
        brief_res = self.client.generate_text(
            model_input=prompts.get_researcher_input(scholar_name)
        )
        brief: ResearchBrief = brief_res.data

        # --- AGENT 2: THE SYNTHESIZER (Tier 1 Specialist) ---
        if progress_callback:
            progress_callback(2, "Synthesizing research into a comprehensive list...")
        synth_res = self.client.generate_text(
            model_input=prompts.get_journalist_input(brief)
        )
        synthesized_report: SynthesizedReport = synth_res.data

        # --- AGENT 3: THE EDITOR (Tier 3 Closer) ---
        if progress_callback:
            progress_callback(3, "Polishing and packaging the contribution report...")
        final_markdown_res = self.client.generate_text(
            model_input=prompts.get_editor_input(scholar_name, synthesized_report)
        )
        final_markdown = final_markdown_res.markdown

        # Create structured data for the .data member
        final_data = ScholarMajorWork(
            scholar_name=scholar_name,
            title=f"Major Works of {scholar_name}",
            subtitle="Synthesized Research Report",
            contribution_list="\n".join(synthesized_report.contributions),
            key_terms=brief.scientific_core,
            impact_summary=brief.revolutionary_impact,
            discussion_questions=[]
        )

        return ModelOutput(
            data=final_data,
            markdown=final_markdown,
            metadata={
                "research_brief": brief.model_dump() if hasattr(brief, 'model_dump') else {},
                "technical_report": synthesized_report.model_dump() if hasattr(synthesized_report, 'model_dump') else {}
            }
        )
    
    def update_model(self, model_name: str, temperature: float = 0.7) -> None:
        """Update the model configuration."""
        self.model_name = model_name
        self.model_config = ModelConfig(model=model_name, temperature=temperature)
        self.client = LiteClient(model_config=self.model_config)

    def get_model_info(self) -> dict:
        """Get information about the current model configuration.
        
        Returns:
            dict: Dictionary containing model information
        """
        return {
            "model_name": self.model_name,
            "temperature": self.model_config.temperature
        }

