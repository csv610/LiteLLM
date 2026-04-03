"""
liteagents.py - Unified for drug_food
"""
from functools import partial\nfrom typing import Type, TypeVar\nfrom lite.utils import save_model_response\nimport asyncio\nfrom pydantic import BaseModel\nimport logging\nfrom lite.lite_client import LiteClient\nfrom app.MedKit.drug.drug_food.shared.models import *\nfrom pathlib import Path\nimport argparse\nfrom lite.config import ModelConfig\nfrom lite.config import ModelConfig, ModelInput\nfrom lite.logging_config import configure_logging\n\n

logger = logging.getLogger(__name__)


def get_user_arguments():
    """Create and configure the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Drug-Food Interaction Checker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "medicine_name", type=str, help="Name of the medicine to analyze"
    )
    parser.add_argument(
        "--diet-type", type=str, default=None, help="Patient's diet type"
    )
    parser.add_argument(
        "--age", "-a", type=int, default=None, help="Patient's age in years (0-150)"
    )
    parser.add_argument(
        "--conditions",
        "-c",
        type=str,
        default=None,
        help="Patient's medical conditions",
    )
    parser.add_argument(
        "--prompt-style",
        "-p",
        type=str,
        choices=["detailed", "concise", "balanced"],
        default="detailed",
        help="Prompt style",
    )
    parser.add_argument(
        "--no-schema",
        action="store_true",
        help="Disable schema-based prompt generation",
    )
    parser.add_argument(
        "--verbosity",
        "-v",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Logging verbosity level",
    )
    parser.add_argument(
        "--model", "-m", type=str, default="ollama/gemma3", help="Model ID"
    )
    parser.add_argument(
        "--json-output", action="store_true", help="Output results as JSON to stdout"
    )
    parser.add_argument(
        "-s",
        "--structured",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response.",
    )
    parser.add_argument(
        "-d",
        "--output-dir",
        default="outputs",
        help="Directory for output files (default: outputs).",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point for the drug-food interaction CLI."""
    args = get_user_arguments()

    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "drug_food_interaction.log"),
        verbosity=args.verbosity,
        enable_console=True,
    )

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        user_input = DrugFoodInput(
            medicine_name=args.medicine_name,
            diet_type=args.diet_type,
            medical_conditions=args.conditions,
            age=args.age,
            specific_food=None,
            prompt_style=args.prompt_style,
        )

        # Validate the input
        user_input.validate()

        logger.info("Configuration created successfully")

        model_config = ModelConfig(model=args.model, temperature=0.2)
        analyzer = DrugFoodInteraction(model_config)
        result = analyzer.generate_text(user_input, structured=args.structured)

        if result is None:
            logger.error("✗ Failed to generate drug-food interaction information.")
            return 1

        # Save result to output directory
        analyzer.save(result, output_dir)

        logger.debug("✓ Drug-food interaction generation completed successfully")
        return 0

    except ValueError as e:
        print(f"\n❌ Invalid input: {e}")
        logger.error(f"Invalid input: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.error(f"Unexpected error: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == "__main__":
    main()

"""
drug_food_agents.py - Specialized agents for drug-food interaction analysis.
"""



try:
    from .drug_food_interaction_models import (
        DrugFoodInteractionDetailsModel,
        PatientFriendlySummaryModel,
    )
    from .drug_food_interaction_prompts import DrugFoodInput, PromptBuilder
except ImportError:
    from drug_food_interaction_models import (
        DrugFoodInteractionDetailsModel,
        PatientFriendlySummaryModel,
    )
    from drug_food_interaction_prompts import DrugFoodInput, PromptBuilder

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class BaseAgent:
    """Base class for specialized drug-food interaction agents."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)

    def run(self, user_input: DrugFoodInput, response_format: Type[T]) -> T:
        """Run the agent with the given input and expected response format."""
        system_prompt = self.get_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(user_input)

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug(f"Running {self.__class__.__name__}...")
        return self.client.generate_text(model_input=model_input)

    async def run_async(
        self,
        user_input: DrugFoodInput,
        response_format: Type[T],
        custom_user_prompt: str | None = None,
    ) -> T:
        """Run the agent asynchronously with the given input."""
        system_prompt = self.get_system_prompt()
        user_prompt = (
            custom_user_prompt
            if custom_user_prompt
            else PromptBuilder.create_user_prompt(user_input)
        )

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug(f"Running {self.__class__.__name__} (async)...")
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
        return PromptBuilder.create_triage_system_prompt()


class PharmacologyAgent(BaseAgent):
    """Agent specializing in pharmacological mechanisms."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_pharmacology_system_prompt()


class RiskAssessmentAgent(BaseAgent):
    """Agent specializing in clinical risk assessment."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_risk_assessment_system_prompt()


class ManagementAgent(BaseAgent):
    """Agent specializing in clinical management recommendations."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_management_system_prompt()


class PatientEducationAgent(BaseAgent):
    """Agent specializing in patient-friendly communication."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_patient_education_system_prompt()


class SearchAgent(BaseAgent):
    """Agent specializing in medical evidence research."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_search_agent_system_prompt()


class ComplianceAgent(BaseAgent):
    """Agent specializing in medical compliance and safety review."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_compliance_system_prompt()

#!/usr/bin/env python3
"""
Drug-Food Interaction Analysis module.

This module provides the core DrugFoodInteraction class for analyzing
how food and beverages interact with medicines using a multi-agent orchestrated approach.
"""



try:
    from .drug_food_agents import (
        ComplianceAgent,
        ManagementAgent,
        PatientEducationAgent,
        PharmacologyAgent,
        RiskAssessmentAgent,
        SearchAgent,
        TriageAgent,
    )
    from .drug_food_interaction_models import (
        AuditLogModel,
        ComplianceInfoModel,
        DataAvailabilityInfoModel,
        DrugFoodInteractionDetailsModel,
        DrugFoodInteractionModel,
        ModelOutput,
        PatientFriendlySummaryModel,
        TriageResultModel,
    )
    from .drug_food_interaction_prompts import DrugFoodInput, PromptBuilder
except ImportError:
    from drug_food_agents import (
        ComplianceAgent,
        ManagementAgent,
        PatientEducationAgent,
        PharmacologyAgent,
        RiskAssessmentAgent,
        SearchAgent,
        TriageAgent,
    )
    from drug_food_interaction_models import (
        AuditLogModel,
        ComplianceInfoModel,
        DataAvailabilityInfoModel,
        DrugFoodInteractionDetailsModel,
        DrugFoodInteractionModel,
        ModelOutput,
        PatientFriendlySummaryModel,
        TriageResultModel,
    )
    from drug_food_interaction_prompts import DrugFoodInput, PromptBuilder

logger = logging.getLogger(__name__)


class DrugFoodOrchestrator:
    """Orchestrates multiple agents to perform drug-food interaction analysis."""

    def __init__(self, model_config: ModelConfig):
        self.triage_agent = TriageAgent(model_config)
        self.pharmacology_agent = PharmacologyAgent(model_config)
        self.risk_agent = RiskAssessmentAgent(model_config)
        self.management_agent = ManagementAgent(model_config)
        self.patient_agent = PatientEducationAgent(model_config)
        self.search_agent = SearchAgent(model_config)
        self.compliance_agent = ComplianceAgent(model_config)

    async def orchestrate_async(self, user_input: DrugFoodInput) -> ModelOutput:
        """Run the 3-tier multi-agent orchestration flow (Specialists -> Auditor -> Closer)."""
        logger.info(f"Starting 3-tier food interaction analysis for {user_input.medicine_name}")

        # Tier 1: Specialists (JSON)
        # 1.1 Triage
        triage_data = await self.triage_agent.run_async(
            user_input, response_format=TriageResultModel
        )

        if not triage_data.interaction_exists:
            logger.info("✓ Triage determined no clinically significant food interactions.")
            return ModelOutput(markdown=f"No clinically significant food interactions found for {user_input.medicine_name}. {triage_data.initial_reasoning}")

        # 1.2 Parallel Specialists
        logger.debug("Tier 1: Running Specialists in parallel...")
        tasks = [
            self.pharmacology_agent.run_async(user_input, DrugFoodInteractionDetailsModel),
            self.risk_agent.run_async(user_input, DrugFoodInteractionDetailsModel),
            self.management_agent.run_async(user_input, DrugFoodInteractionDetailsModel),
            self.patient_agent.run_async(user_input, PatientFriendlySummaryModel),
            self.search_agent.run_async(user_input, DrugFoodInteractionDetailsModel),
        ]
        spec_results = await asyncio.gather(*tasks)
        
        spec_data_json = "\n\n".join([
            f"SPECIALIST {i}: {res.model_dump_json(indent=2) if hasattr(res, 'model_dump_json') else str(res)}"
            for i, res in enumerate(spec_results)
        ])

        # Tier 2: Compliance Auditor (JSON Audit)
        logger.debug("Tier 2: Compliance Auditor performing safety review...")
        compliance_user_prompt = PromptBuilder.create_compliance_review_user_prompt(
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
        out_sys, out_usr = PromptBuilder.create_output_synthesis_prompts(
            user_input, spec_data_json, audit_json
        )
        
        final_markdown = await self.pharmacology_agent.client.generate_text_async(ModelInput(
            system_prompt=out_sys,
            user_prompt=out_usr,
            response_format=None
        ))

        logger.info("✓ Successfully generated 3-tier orchestrated drug-food report")
        return ModelOutput(
            data=spec_results[0] if structured else None, 
            markdown=final_markdown.markdown,
            metadata={"audit": audit_json}
        )


class DrugFoodInteraction:
    """Analyzes drug-food interactions using multi-agent orchestration."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the drug-food interaction analyzer."""
        self.model_config = model_config
        self.orchestrator = DrugFoodOrchestrator(model_config)
        self.user_input = None  # Store the configuration for later use in save
        logger.debug("Initialized DrugFoodInteraction with Orchestrator")

    def generate_text(
        self, user_input: DrugFoodInput, structured: bool = True
    ) -> ModelOutput:
        """Analyzes how food and beverages interact with a medicine (sync wrapper)."""
        self.user_input = user_input
        logger.debug(f"Starting drug-food interaction analysis for {user_input.medicine_name}")

        try:
            # Wrap the async orchestration for the existing sync API
            result = asyncio.run(self.orchestrator.orchestrate_async(user_input))
            logger.debug("✓ Successfully analyzed food interactions via orchestration")
            return ModelOutput(data=result)
        except Exception as e:
            logger.error(f"✗ Error in multi-agent orchestration: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the drug-food interaction information to a file."""
        if self.user_input is None:
            raise ValueError("No configuration available. Call generate_text first.")

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.user_input.medicine_name.lower().replace(' ', '_')}_food_interaction"

        return save_model_response(result, output_dir / base_filename)

