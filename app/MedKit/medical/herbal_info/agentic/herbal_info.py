#!/usr/bin/env python3
"""
Herbal Information module.

This module provides the core HerbalInfoGenerator class for generating
comprehensive herbal remedy information based on provided configuration.
"""

import logging
import sys
from pathlib import Path

# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response

try:
    from .herbal_info_models import HerbalInfoModel, ModelOutput
    from .herbal_info_agents import (
        BotanicalAgent,
        PharmacologicalAgent,
        SafetyAgent,
        ClinicalAgent,
        EducatorAgent,
    )
except (ImportError, ValueError):
    try:
        from herbal_info_models import HerbalInfoModel, ModelOutput
        from herbal_info_agents import (
            BotanicalAgent,
            PharmacologicalAgent,
            SafetyAgent,
            ClinicalAgent,
            EducatorAgent,
        )
    except ImportError:
        from medical.herbal_info.agentic.herbal_info_models import HerbalInfoModel, ModelOutput
        from medical.herbal_info.agentic.herbal_info_agents import (
            BotanicalAgent,
            PharmacologicalAgent,
            SafetyAgent,
            ClinicalAgent,
            EducatorAgent,
        )

logger = logging.getLogger(__name__)


from concurrent.futures import ThreadPoolExecutor

class HerbalInfoGenerator:
    """Generates comprehensive herbal remedy information using a multi-agent approach."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.herb = None  # Store the herb being analyzed
        
        # Initialize specialized agents
        self.agents = [
            BotanicalAgent(model_config, self.client),
            PharmacologicalAgent(model_config, self.client),
            SafetyAgent(model_config, self.client),
            ClinicalAgent(model_config, self.client),
            EducatorAgent(model_config, self.client),
        ]
        logger.debug(f"Initialized HerbalInfoGenerator with {len(self.agents)} agents")

    def generate_text(self, herb: str, structured: bool = False) -> ModelOutput:
        """Generates 3-tier comprehensive herbal information."""
        if not herb or not str(herb).strip():
            raise ValueError("Herb name cannot be empty")

        self.herb = herb
        logger.info(f"Starting 3-tier herbal generation for: {herb}")

        try:
            # 1. Specialist Stage (JSON - Parallel)
            logger.debug("Tier 1: Specialists generating herbal data...")
            with ThreadPoolExecutor(max_workers=len(self.agents)) as executor:
                future_to_agent = {
                    executor.submit(agent.generate, herb, structured=structured): agent
                    for agent in self.agents
                }
                spec_results = [f.result() for f in future_to_agent]

            if structured:
                spec_data = self._combine_structured_results(spec_results).data
                spec_json = spec_data.model_dump_json(indent=2)
            else:
                spec_json = self._combine_markdown_results(spec_results).markdown

            # 2. Auditor Stage (JSON Audit)
            logger.debug("Tier 2: Auditor performing safety check...")
            from .herbal_info_prompts import PromptBuilder as PB
            audit_sys, audit_usr = PB.create_compliance_auditor_prompts(herb, spec_json)
            audit_input = ModelInput(
                system_prompt=audit_sys,
                user_prompt=audit_usr,
                response_format=None # Audit result
            )
            audit_res = self.client.generate_text(model_input=audit_input)
            audit_json = audit_res.markdown

            # 3. Final Synthesis Stage (Markdown Closer)
            logger.debug("Tier 3: Output Agent synthesizing final monograph...")
            out_sys, out_usr = PB.create_output_synthesis_prompts(herb, spec_json, audit_json)
            out_input = ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None,
            )
            final_res = self.client.generate_text(model_input=out_input)

            logger.info("✓ Successfully generated 3-tier herbal monograph")
            return ModelOutput(
                data=spec_data if structured else None,
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier Herbal generation failed: {e}")
            raise

    def _combine_structured_results(self, results: list[ModelOutput]) -> ModelOutput:
        """Combines structured data from multiple agents into a single HerbalInfoModel."""
        combined_data = {}
        for res in results:
            if res.data:
                # Support both pydantic v1 and v2
                if hasattr(res.data, "model_dump"):
                    combined_data.update(res.data.model_dump())
                else:
                    combined_data.update(res.data.dict())
        
        try:
            final_model = HerbalInfoModel(**combined_data)
            # Optionally generate markdown from the combined data if needed
            # For now, we'll just return the combined data
            return ModelOutput(data=final_model)
        except Exception as e:
            logger.error(f"Error combining structured results: {e}")
            raise

    def _combine_markdown_results(self, results: list[ModelOutput]) -> ModelOutput:
        """Combines markdown output from multiple agents."""
        combined_markdown = ""
        for res in results:
            if res.markdown:
                combined_markdown += res.markdown + "\n\n---\n\n"
        
        return ModelOutput(markdown=combined_markdown.strip())

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate content (backward compatibility)."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the herbal information to a file."""
        if self.herb is None:
            raise ValueError("No herb information available. Call generate_text first.")

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.herb.lower().replace(' ', '_')}"

        return save_model_response(result, output_dir / base_filename)
