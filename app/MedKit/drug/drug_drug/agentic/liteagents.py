"""
liteagents.py - Unified for drug_drug
"""
from typing import Type, TypeVar\nfrom lite.utils import save_model_response\nfrom pydantic import BaseModel\nfrom lite.lite_client import LiteClient\nimport logging\nfrom pathlib import Path\nimport argparse\nfrom lite.config import ModelConfig\nfrom app.MedKit.drug.drug_drug.shared.models import *\nfrom lite.config import ModelConfig, ModelInput\nfrom lite.logging_config import configure_logging\n\n#!/usr/bin/env python3
"""
Drug-Drug Interaction Analysis module.

This module provides the core DrugDrugInteractionGenerator class for analyzing
interactions between two medicines.
"""



try:
    from .drug_drug_agents import (
        ComplianceAgent,
        ManagementAgent,
        PatientEducationAgent,
        PharmacologyAgent,
        RiskAssessmentAgent,
        SearchAgent,
        TriageAgent,
    )
    from .drug_drug_interaction_models import (
        AuditLogModel,
        ComplianceInfoModel,
        DataAvailabilityInfoModel,
        DrugInteractionDetailsModel,
        DrugInteractionModel,
        ModelOutput,
        PatientFriendlySummaryModel,
        TriageResultModel,
    )
    from .drug_drug_interaction_prompts import DrugDrugInput, DrugDrugPromptBuilder
except ImportError:
    from drug_drug_agents import (
        ComplianceAgent,
        ManagementAgent,
        PatientEducationAgent,
        PharmacologyAgent,
        RiskAssessmentAgent,
        SearchAgent,
        TriageAgent,
    )
    from drug_drug_interaction_models import (
        AuditLogModel,
        ComplianceInfoModel,
        DataAvailabilityInfoModel,
        DrugInteractionDetailsModel,
        DrugInteractionModel,
        ModelOutput,
        PatientFriendlySummaryModel,
        TriageResultModel,
    )
    from drug_drug_interaction_prompts import DrugDrugInput, DrugDrugPromptBuilder

logger = logging.getLogger(__name__)


class DrugDrugOrchestrator:
    """Orchestrates multiple agents to perform drug-drug interaction analysis."""

    def __init__(self, model_config: ModelConfig):
        self.triage_agent = TriageAgent(model_config)
        self.pharmacology_agent = PharmacologyAgent(model_config)
        self.risk_agent = RiskAssessmentAgent(model_config)
        self.management_agent = ManagementAgent(model_config)
        self.patient_agent = PatientEducationAgent(model_config)
        self.search_agent = SearchAgent(model_config)
        self.compliance_agent = ComplianceAgent(model_config)

    async def orchestrate_async(self, user_input: DrugDrugInput) -> ModelOutput:
        """Run the 3-tier multi-agent orchestration flow (Specialists -> Auditor -> Closer)."""
        logger.info(f"Starting 3-tier analysis for {user_input.medicine1} + {user_input.medicine2}")

        # Tier 1: Triage
        triage_data = await self.triage_agent.run_async(
            user_input, response_format=TriageResultModel
        )

        if not triage_data.interaction_exists:
            logger.info("✓ Triage determined no clinically significant interaction.")
            return ModelOutput(markdown=f"No clinically significant interaction found between {user_input.medicine1} and {user_input.medicine2}. {triage_data.initial_reasoning}")

        # Tier 1: Parallel Specialists
        import asyncio
        logger.debug("Tier 1: Running Specialists in parallel...")
        tasks = [
            self.pharmacology_agent.run_async(user_input, DrugInteractionDetailsModel),
            self.risk_agent.run_async(user_input, DrugInteractionDetailsModel),
            self.management_agent.run_async(user_input, DrugInteractionDetailsModel),
            self.patient_agent.run_async(user_input, PatientFriendlySummaryModel),
            self.search_agent.run_async(user_input, DrugInteractionDetailsModel),
        ]
        spec_results = await asyncio.gather(*tasks)
        
        spec_data_json = "\n\n".join([
            f"SPECIALIST {i}: {res.model_dump_json(indent=2) if hasattr(res, 'model_dump_json') else str(res)}"
            for i, res in enumerate(spec_results)
        ])

        # Tier 2: Compliance Auditor (JSON Audit)
        logger.debug("Tier 2: Compliance Auditor performing safety review...")
        compliance_user_prompt = DrugDrugPromptBuilder.create_compliance_review_user_prompt(
            user_input, spec_data_json
        )
        compliance_data = await self.compliance_agent.run_async(
            user_input,
            response_format=ComplianceInfoModel,
            custom_user_prompt=compliance_user_prompt,
        )
        audit_json = compliance_data.model_dump_json(indent=2)

        # Tier 3: Final Output Synthesis (Markdown Closer)
        logger.debug("Tier 3: Output Agent synthesizing final report...")
        out_sys, out_usr = DrugDrugPromptBuilder.create_output_synthesis_prompts(
            user_input, spec_data_json, audit_json
        )
        
        final_markdown = await self.pharmacology_agent.client.generate_text_async(ModelInput(
            system_prompt=out_sys,
            user_prompt=out_usr,
            response_format=None
        ))

        logger.info("✓ Successfully generated 3-tier orchestrated drug-drug report")
        return ModelOutput(
            data=spec_results[0] if structured else None, 
            markdown=final_markdown.markdown,
            metadata={"audit": audit_json}
        )


class DrugDrugInteractionGenerator:
    """Generates drug-drug interaction analysis using multi-agent orchestration."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator with an orchestrator."""
        self.model_config = model_config
        self.orchestrator = DrugDrugOrchestrator(model_config)
        self.user_input = None
        logger.debug("Initialized DrugDrugInteractionGenerator with Orchestrator")

    def generate_text(
        self, user_input: DrugDrugInput, structured: bool = True
    ) -> ModelOutput:
        """Generate drug-drug interaction analysis through orchestration (sync wrapper)."""
        import asyncio

        try:
            # Wrap the async orchestration for the existing sync API
            result = asyncio.run(self.orchestrator.orchestrate_async(user_input))
            logger.debug("✓ Successfully analyzed drug-drug interaction via async orchestration")
            return ModelOutput(data=result)
        except Exception as e:
            logger.error(f"✗ Error in multi-agent orchestration: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the drug-drug interaction information to a file."""
        if self.user_input is None:
            raise ValueError("No configuration available. Call generate_text first.")

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.user_input.medicine1.lower().replace(' ', '_')}_{self.user_input.medicine2.lower().replace(' ', '_')}_interaction"

        return save_model_response(result, output_dir / base_filename)



logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Drug-Drug Interaction Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("medicine1", type=str, help="Name of the first medicine")
    parser.add_argument("medicine2", type=str, help="Name of the second medicine")
    parser.add_argument(
        "--age", "-a", type=int, default=None, help="Patient's age in years (0-150)"
    )
    parser.add_argument(
        "--dosage1",
        "-d1",
        type=str,
        default=None,
        help="Dosage information for first medicine",
    )
    parser.add_argument(
        "--dosage2",
        "-d2",
        type=str,
        default=None,
        help="Dosage information for second medicine",
    )
    parser.add_argument(
        "--conditions",
        "-c",
        type=str,
        default=None,
        help="Patient's medical conditions (comma-separated)",
    )
    parser.add_argument(
        "--style",
        "-s",
        type=str,
        choices=["detailed", "concise", "balanced"],
        default="detailed",
        help="Prompt style for analysis (default: detailed)",
    )
    parser.add_argument(
        "-d",
        "--output-dir",
        default="outputs",
        help="Directory for output files (default: outputs).",
    )
    parser.add_argument(
        "-m",
        "--model",
        default="ollama/gemma3",
        help="Model to use for generation (default: ollama/gemma3).",
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2).",
    )
    parser.add_argument(
        "-t",
        "--structured",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response.",
    )

    return parser.parse_args()


def create_drug_drug_interaction_report(args) -> int:
    """Generate drug-drug interaction report."""
    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "drug_drug_interaction.log"),
        verbosity=args.verbosity,
        enable_console=True,
    )
    logger.debug("CLI Arguments:")
    logger.debug(f"  Medicine 1: {args.medicine1}")
    logger.debug(f"  Medicine 2: {args.medicine2}")
    logger.debug(f"  Age: {args.age}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = DrugDrugInteractionGenerator(model_config)

        # Create input configuration
        user_input = DrugDrugInput(
            medicine1=args.medicine1,
            medicine2=args.medicine2,
            age=args.age,
            dosage1=args.dosage1,
            dosage2=args.dosage2,
            medical_conditions=args.conditions,
            prompt_style=PromptStyle(args.style),
        )

        result = generator.generate_text(user_input=user_input, structured=args.structured)

        if result is None:
            logger.error("✗ Failed to generate drug-drug interaction information.")
            return 1

        # Save result to output directory
        generator.save(result, output_dir)

        logger.debug("✓ Drug-drug interaction generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Drug-drug interaction generation failed: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == "__main__":
    args = get_user_arguments()
    create_drug_drug_interaction_report(args)

"""
drug_drug_agents.py - Specialized agents for drug-drug interaction analysis.
"""



try:
    from .drug_drug_interaction_models import (
        DrugInteractionDetailsModel,
        PatientFriendlySummaryModel,
    )
    from .drug_drug_interaction_prompts import DrugDrugInput, DrugDrugPromptBuilder
except ImportError:
    from drug_drug_interaction_models import (
        DrugInteractionDetailsModel,
        PatientFriendlySummaryModel,
    )
    from drug_drug_interaction_prompts import DrugDrugInput, DrugDrugPromptBuilder

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class BaseAgent:
    """Base class for specialized drug-drug interaction agents."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)

    def run(self, user_input: DrugDrugInput, response_format: Type[T]) -> T:
        """Run the agent with the given input and expected response format."""
        system_prompt = self.get_system_prompt()
        user_prompt = DrugDrugPromptBuilder.create_user_prompt(user_input)

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug(f"Running {self.__class__.__name__}...")
        return self.client.generate_text(model_input=model_input)

    async def run_async(
        self,
        user_input: DrugDrugInput,
        response_format: Type[T],
        custom_user_prompt: str | None = None,
    ) -> T:
        """Run the agent asynchronously with the given input."""
        system_prompt = self.get_system_prompt()
        user_prompt = (
            custom_user_prompt
            if custom_user_prompt
            else DrugDrugPromptBuilder.create_user_prompt(user_input)
        )

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug(f"Running {self.__class__.__name__} (async)...")
        # Assuming LiteClient.generate_text has an async version or can be run in a thread
        # For now, we'll wrap it in a thread if no async version exists
        import asyncio
        from functools import partial

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, partial(self.client.generate_text, model_input=model_input)
        )

    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent. Must be overridden."""
        raise NotImplementedError


class TriageAgent(BaseAgent):
    """Agent specializing in initial triage of interactions."""

    def get_system_prompt(self) -> str:
        return DrugDrugPromptBuilder.create_triage_system_prompt()


class PharmacologyAgent(BaseAgent):
    """Agent specializing in pharmacological mechanisms."""

    def get_system_prompt(self) -> str:
        return DrugDrugPromptBuilder.create_pharmacology_system_prompt()


class RiskAssessmentAgent(BaseAgent):
    """Agent specializing in clinical risk assessment."""

    def get_system_prompt(self) -> str:
        return DrugDrugPromptBuilder.create_risk_assessment_system_prompt()


class ManagementAgent(BaseAgent):
    """Agent specializing in clinical management recommendations."""

    def get_system_prompt(self) -> str:
        return DrugDrugPromptBuilder.create_management_system_prompt()


class PatientEducationAgent(BaseAgent):
    """Agent specializing in patient-friendly communication."""

    def get_system_prompt(self) -> str:
        return DrugDrugPromptBuilder.create_patient_education_system_prompt()


class SearchAgent(BaseAgent):
    """Agent specializing in medical evidence research."""

    def get_system_prompt(self) -> str:
        return DrugDrugPromptBuilder.create_search_agent_system_prompt()


class ComplianceAgent(BaseAgent):
    """Agent specializing in medical compliance and safety review."""

    def get_system_prompt(self) -> str:
        return DrugDrugPromptBuilder.create_compliance_system_prompt()

