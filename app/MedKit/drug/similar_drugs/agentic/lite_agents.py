"""
liteagents.py - Unified for similar_drugs
"""
from typing import Type, TypeVar\nfrom pydantic import BaseModel\nfrom typing import Optional, Union\nfrom lite.lite_client import LiteClient\nimport logging\nfrom pathlib import Path\nimport argparse\nfrom lite.config import ModelConfig\nfrom lite.config import ModelConfig, ModelInput\nfrom lite.logging_config import configure_logging\nimport sys\nfrom app.MedKit.drug.similar_drugs.shared.models import *\n\n"""
similar_drugs_agents.py - Specialized agents for finding similar medicines.
"""



try:
    from .similar_drugs_prompts import PromptBuilder
except ImportError:
    from similar_drugs_prompts import PromptBuilder

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class BaseAgent:
    """Base class for specialized similar medicine search agents."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)

    def run(self, medicine_name: str, context: str, response_format: Type[T]) -> T:
        """Run the agent with the given input and expected response format."""
        system_prompt = self.get_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(medicine_name, context)

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug(f"Running {self.__class__.__name__}...")
        return self.client.generate_text(model_input=model_input)

    async def run_async(
        self,
        medicine_name: str,
        context: str,
        response_format: Type[T],
        custom_user_prompt: str | None = None,
    ) -> T:
        """Run the agent asynchronously with the given input."""
        system_prompt = self.get_system_prompt()
        user_prompt = (
            custom_user_prompt
            if custom_user_prompt
            else PromptBuilder.create_user_prompt(medicine_name, context)
        )

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug(f"Running {self.__class__.__name__} (async)...")
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
    """Agent specializing in initial triage of medicines."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_triage_system_prompt()


class ResearchAgent(BaseAgent):
    """Agent specializing in medical research and comparison."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_research_system_prompt()


class ComplianceAgent(BaseAgent):
    """Agent specializing in medical compliance and safety review."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_compliance_system_prompt()

"""Similar Drugs Finder.

This module contains the core logic for finding similar medicines based on
active ingredients, therapeutic classes, and mechanisms of action.
"""



try:
    from .similar_drugs_agents import ComplianceAgent, ResearchAgent, TriageAgent
    from .similar_drugs_models import (
        AuditLogModel,
        ComplianceInfoModel,
        SimilarDrugsConfig,
        SimilarMedicinesModel,
        SimilarMedicinesResult,
        TriageResultModel,
    )
    from .similar_drugs_prompts import PromptBuilder
except ImportError:
    from similar_drugs_agents import ComplianceAgent, ResearchAgent, TriageAgent
    from similar_drugs_models import (
        AuditLogModel,
        ComplianceInfoModel,
        SimilarDrugsConfig,
        SimilarMedicinesModel,
        SimilarMedicinesResult,
        TriageResultModel,
    )
    from similar_drugs_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class SimilarDrugsOrchestrator:
    """Orchestrates multiple agents to find similar medicines."""

    def __init__(self, model_config: ModelConfig):
        self.triage_agent = TriageAgent(model_config)
        self.research_agent = ResearchAgent(model_config)
        self.compliance_agent = ComplianceAgent(model_config)

    async def orchestrate_async(
        self,
        medicine_name: str,
        context: str,
    ) -> ModelOutput:
        """Run the 3-tier multi-agent orchestration flow (Specialists -> Auditor -> Closer)."""
        logger.info(f"Starting 3-tier orchestrated search for medicines similar to {medicine_name}")

        # Tier 1: Specialists (JSON)
        # 1.1 Triage
        triage_data = await self.triage_agent.run_async(
            medicine_name, context, response_format=TriageResultModel
        )

        if not triage_data.is_real_medicine:
            logger.warning(f"Triage determined '{medicine_name}' may not be a valid medicine.")

        # 1.2 Research
        research_data = await self.research_agent.run_async(
            medicine_name, context, response_format=SimilarMedicinesResult
        )
        spec_json = research_data.model_dump_json(indent=2)

        # Tier 2: Compliance Auditor (JSON Audit)
        compliance_user_prompt = PromptBuilder.create_compliance_review_user_prompt(
            medicine_name, spec_json
        )
        compliance_data = await self.compliance_agent.run_async(
            medicine_name,
            context,
            response_format=ComplianceInfoModel,
            custom_user_prompt=compliance_user_prompt,
        )
        audit_json = compliance_data.model_dump_json(indent=2)

        # Tier 3: Final Output Synthesis (Markdown Closer)
        logger.info("Tier 3: Output synthesis starting...")
        out_sys, out_usr = PromptBuilder.create_output_synthesis_prompts(
            medicine_name, spec_json, audit_json
        )
        
        final_markdown = await self.research_agent.client.generate_text_async(ModelInput(
            system_prompt=out_sys,
            user_prompt=out_usr,
            response_format=None
        ))

        logger.info("✓ Successfully generated 3-tier similar medicines report")
        return ModelOutput(
            data=research_data, 
            markdown=final_markdown.markdown,
            metadata={"audit": audit_json}
        )


class SimilarDrugs:
    """Finds similar drugs based on provided configuration."""

    def __init__(self, config: "SimilarDrugsConfig", model_config: ModelConfig):
        self.config = config
        self.orchestrator = SimilarDrugsOrchestrator(model_config)

        # Apply verbosity level using centralized logging configuration
        configure_logging(
            log_file=str(Path(__file__).parent / "logs" / "similar_drugs.log"),
            verbosity=self.config.verbosity,
            enable_console=True,
        )

    def find(
        self,
        medicine_name: str,
        include_generics: bool = True,
        patient_age: Optional[int] = None,
        patient_conditions: Optional[str] = None,
        structured: bool = False,
    ) -> Union[SimilarMedicinesResult, SimilarMedicinesModel, str]:
        """
        Finds top 10-15 medicines similar to a given medicine.
        """
        # Validate inputs
        if not medicine_name or not medicine_name.strip():
            raise ValueError("Medicine name cannot be empty")
        if patient_age is not None and (patient_age < 0 or patient_age > 150):
            raise ValueError("Age must be between 0 and 150 years")

        context_parts = []
        if include_generics:
            context_parts.append("Include generic formulations")
        if patient_age is not None:
            context_parts.append(f"Patient age: {patient_age} years")
        if patient_conditions:
            context_parts.append(f"Patient conditions: {patient_conditions}")

        context = ". ".join(context_parts) + "." if context_parts else ""

        import asyncio

        try:
            result = asyncio.run(self.orchestrator.orchestrate_async(medicine_name, context))
            if structured:
                return result
            return result.main_result.model_dump_json(indent=2)
        except Exception as e:
            logger.error(f"Error in multi-agent orchestration: {e}")
            raise

"""Module docstring - Similar Medicines Finder and Comparator.

Find alternative medicines with similar active ingredients, therapeutic classes, and
mechanisms of action. Provides detailed comparisons to help identify suitable substitutes.
"""



logger = logging.getLogger(__name__)


def get_similar_medicines(
    medicine_name: str,
    config: SimilarDrugsConfig,
    model_config: ModelConfig,
    include_generics: bool = True,
    patient_age: Optional[int] = None,
    patient_conditions: Optional[str] = None,
    structured: bool = False,
) -> Union[SimilarMedicinesResult, str]:
    """
    Get similar medicines.

    This is a convenience function that instantiates and runs the
    SimilarDrugs finder.

    Args:
        medicine_name: Name of the medicine to find alternatives for
        config: Configuration object for the analysis
        model_config: ModelConfig object containing model settings
        include_generics: Whether to include generic formulations (default: True)
        patient_age: Patient's age in years (optional)
        patient_conditions: Patient's medical conditions (optional)

    Returns:
        SimilarMedicinesResult: The result of the analysis
    """
    finder = SimilarDrugs(config, model_config)
    return finder.find(
        medicine_name=medicine_name,
        include_generics=include_generics,
        patient_age=patient_age,
        patient_conditions=patient_conditions,
        structured=structured,
    )


def create_cli_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser for the CLI.

    Returns:
        argparse.ArgumentParser: Configured parser for command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Similar Drugs Finder - Find alternative medicines and similar drug options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Required arguments
    parser.add_argument(
        "medicine_name",
        type=str,
        help="Name of the medicine to find similar alternatives for",
    )

    # Optional arguments
    parser.add_argument(
        "--include-generics",
        action="store_true",
        default=True,
        help="Include generic formulations (default: True)",
    )

    parser.add_argument(
        "--no-generics",
        dest="include_generics",
        action="store_false",
        help="Exclude generic formulations",
    )

    parser.add_argument(
        "--age",
        "-a",
        type=int,
        default=None,
        help="Patient's age in years (0-150)",
    )

    parser.add_argument(
        "--conditions",
        "-c",
        type=str,
        default=None,
        help="Patient's medical conditions (comma-separated)",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Output file path for results (default: outputs/{medicine}_similar_medicines.json)",
    )

    parser.add_argument(
        "--prompt-style",
        "-p",
        type=str,
        choices=["detailed", "concise", "balanced"],
        default="detailed",
        help="Prompt style for analysis (default: detailed)",
    )

    parser.add_argument(
        "--verbosity",
        "-v",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2).",
    )

    parser.add_argument(
        "--json-output",
        "-j",
        action="store_true",
        default=False,
        help="Output results as JSON to stdout (in addition to file)",
    )

    parser.add_argument(
        "-s",
        "--structured",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response.",
    )

    return parser


def main() -> int:
    """
    Main entry point for the similar drugs CLI.

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    parser = create_cli_parser()
    args = parser.parse_args()

    try:
        # Create configuration
        config = SimilarDrugsConfig(
            output_path=args.output if hasattr(args, "output") else None,
            verbosity=args.verbosity,
        )

        logger.debug("Configuration created successfully")

        # Run analysis
        model_config = ModelConfig(model="ollama/gemma2", temperature=0.7)
        analyzer = SimilarDrugs(config, model_config)
        result = analyzer.find(
            medicine_name=args.medicine_name,
            include_generics=args.include_generics
            if hasattr(args, "include_generics")
            else True,
            patient_age=args.age if hasattr(args, "age") else None,
            patient_conditions=args.conditions if hasattr(args, "conditions") else None,
            structured=args.structured,
        )

        # Save results to file
        if args.output:
            output_path = args.output
        else:
            medicine_clean = args.medicine_name.lower().replace(" ", "_")
            suffix = ".json"
            if isinstance(result, str):
                suffix = ".md"
            output_path = (
                Path("outputs") / f"{medicine_clean}_similar_medicines{suffix}"
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(result, str) and output_path.suffix == ".json":
            output_path = output_path.with_suffix(".md")

        with open(output_path, "w") as f:
            if isinstance(result, str):
                f.write(result)
            else:
                f.write(result.model_dump_json(indent=2))

        logger.debug(f"✓ Results saved to {output_path}")
        print(f"\n✓ Results saved to: {output_path}")

        # Output JSON to stdout if requested
        if args.json_output:
            print(f"\n{result.model_dump_json(indent=2)}")

        return 0

    except ValueError as e:
        print(f"\n❌ Invalid input: {e}", file=sys.stderr)
        logger.error(f"Invalid input: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

