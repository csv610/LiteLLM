"""
liteagents.py - Unified for drugs_comparision
"""
from lite.utils import save_model_response\nfrom lite.config import ModelConfig\nfrom typing import Optional, Union\nfrom dataclasses import dataclass\nimport logging\nfrom lite.lite_client import LiteClient\nfrom app.MedKit.drug.drugs_comparision.shared.models import *\nfrom pathlib import Path\nfrom .drugs_comparison import DrugsComparison, DrugsComparisonInput\nimport argparse\nfrom .drugs_comparison_models import (\nfrom unittest.mock import MagicMock, patch\nfrom lite.config import ModelConfig, ModelInput\nfrom lite.logging_config import configure_logging\n\n#!/usr/bin/env python3
"""
Drugs Comparison module.

This module provides the core DrugsComparison class for comparing two medicines
across clinical, regulatory, and practical metrics.
"""



try:
    from .drugs_comparison_models import MedicinesComparisonResult
    from .drugs_comparison_prompts import PromptBuilder
except ImportError:
    from drugs_comparison_models import MedicinesComparisonResult
    from drugs_comparison_prompts import PromptBuilder

logger = logging.getLogger(__name__)


@dataclass
class DrugsComparisonInput:
    """Configuration and input for medicines comparison."""

    medicine1: str
    medicine2: str
    use_case: Optional[str] = None
    patient_age: Optional[int] = None
    patient_conditions: Optional[str] = None
    prompt_style: str = "detailed"


class DrugsComparison:
    """Compares two medicines using a multi-agent architecture."""

    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)
        self.config = None
        logger.debug("Initialized Multi-Agent DrugsComparison")

    def generate_text(
        self, config: DrugsComparisonInput, structured: bool = False
    ) -> Union[MedicinesComparisonResult, str]:
        """Compares two medicines using a 3-tier multi-agent system."""
        self.config = config
        self._validate_input(config)

        logger.info(f"Starting 3-tier analysis: {config.medicine1} vs {config.medicine2}")
        context = self._prepare_context(config)

        # 1. Tier 1: Specialist Agents (Parallelizable JSON)
        logger.debug("Tier 1: Running specialist agents...")
        pharmacology_report = self._run_agent(
            PromptBuilder.create_pharmacology_system_prompt(), config, context
        )
        regulatory_report = self._run_agent(
            PromptBuilder.create_regulatory_system_prompt(), config, context
        )
        market_report = self._run_agent(
            PromptBuilder.create_market_access_system_prompt(), config, context
        )
        context_report = self._run_agent(
            PromptBuilder.create_clinical_context_system_prompt(), config, context
        )
        compliance_report = self._run_agent(
            PromptBuilder.create_compliance_system_prompt(), config, context
        )

        specialist_data = f"""
        - Pharmacology: {pharmacology_report}
        - Regulatory: {regulatory_report}
        - Market Access: {market_report}
        - Clinical Context: {context_report}
        - Compliance: {compliance_report}
        """

        # 2. Tier 2: Safety Auditor (JSON Audit)
        logger.debug("Tier 2: Running safety auditor...")
        safety_report = self._run_agent(
            PromptBuilder.create_safety_auditor_system_prompt(), config, specialist_data
        )

        # 3. Tier 3: Final Output Synthesis (Markdown Closer)
        logger.debug("Tier 3: Output synthesis starting...")
        out_sys, out_usr = PromptBuilder.create_output_synthesis_prompts(
            config.medicine1, config.medicine2, specialist_data, safety_report
        )

        model_input = ModelInput(
            system_prompt=out_sys,
            user_prompt=out_usr,
            response_format=None,
        )

        final_res = self._ask_llm(model_input)
        
        # Assemble data if structured requested
        if structured:
            # We need to run the original synthesis agent if we want a structured model return
            # For now, let's assume we return the synthesized markdown as requested.
            pass

        logger.debug("✓ 3-tier Multi-agent synthesis complete")
        return ModelOutput(
            data=None, # Tier 1 data is complex here, can be added if needed
            markdown=final_res.markdown,
            metadata={"audit": safety_report}
        )

    def _run_agent(self, system_prompt: str, config: DrugsComparisonInput, context: str) -> str:
        """Helper to run a specific agent and get its narrative report."""
        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=PromptBuilder.create_user_prompt(
                config.medicine1, config.medicine2, context
            ),
        )
        # Specialist agents always return text reports for the synthesis orchestrator
        return self._ask_llm(model_input)

    def _validate_input(self, config: DrugsComparisonInput) -> None:
        """Validate input parameters."""
        if not config.medicine1 or not config.medicine1.strip():
            raise ValueError("Medicine 1 name cannot be empty")
        if not config.medicine2 or not config.medicine2.strip():
            raise ValueError("Medicine 2 name cannot be empty")
        if config.patient_age is not None and (
            config.patient_age < 0 or config.patient_age > 150
        ):
            raise ValueError("Age must be between 0 and 150 years")

    def _prepare_context(self, config: DrugsComparisonInput) -> str:
        """Build the analysis context string from input parameters."""
        context_parts = [f"Comparing {config.medicine1} and {config.medicine2}"]
        if config.use_case:
            context_parts.append(f"Use case: {config.use_case}")
            logger.debug(f"Use case: {config.use_case}")
        if config.patient_age is not None:
            context_parts.append(f"Patient age: {config.patient_age} years")
            logger.debug(f"Patient age: {config.patient_age}")
        if config.patient_conditions:
            context_parts.append(f"Patient conditions: {config.patient_conditions}")
            logger.debug(f"Patient conditions: {config.patient_conditions}")
        return ". ".join(context_parts) + "."

    def _ask_llm(
        self, model_input: ModelInput
    ) -> Union[MedicinesComparisonResult, str]:
        """Helper to call LiteClient with error handling."""
        logger.debug("Calling LiteClient.generate_text()...")
        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"✗ Error during LLM analysis: {e}")
            logger.exception("Full exception details:")
            raise

    def save(
        self, result: Union[MedicinesComparisonResult, str], output_dir: Path
    ) -> Path:
        """Saves the drugs comparison analysis to a file."""
        if self.config is None:
            raise ValueError(
                "No configuration information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        medicine1_safe = self.config.medicine1.lower().replace(" ", "_")
        medicine2_safe = self.config.medicine2.lower().replace(" ", "_")
        base_filename = f"{medicine1_safe}_vs_{medicine2_safe}_comparison"

        return save_model_response(result, output_dir / base_filename)

    MedicinesComparisonResult, ClinicalMetrics, RegulatoryMetrics, 
    PracticalMetrics, ComplianceMetrics, ComparisonSummary, RecommendationContext,
    SafetyAudit, EffectivenessRating, SafetyRating, AvailabilityStatus
)

# Configure logging to see the agent flow
logging.basicConfig(level=logging.DEBUG)

def mock_ask_llm(model_input):
    system_prompt = model_input.system_prompt
    
    if "pharmacology expert" in system_prompt:
        return "PHARMACOLOGY REPORT: Ibuprofen is an NSAID. Acetaminophen is an antipyretic/analgesic. Ibuprofen has higher GI risk."
    
    elif "regulatory expert" in system_prompt:
        return "REGULATORY REPORT: Both are FDA approved and available OTC. Patents expired decades ago."
    
    elif "market access specialist" in system_prompt:
        return "MARKET ACCESS REPORT: Both are very affordable (<$10 for bottle). Widely available in pharmacies and grocery stores."
    
    elif "clinical practitioner" in system_prompt:
        return "CLINICAL CONTEXT REPORT: Ibuprofen better for inflammation. Acetaminophen safer for elderly and those with kidney issues."
    
    elif "compliance and patient safety" in system_prompt:
        return "COMPLIANCE REPORT: Both are non-controlled. No major prescribing restrictions. High adherence for both as they are OTC."
    
    elif "Senior Medical Safety Auditor" in system_prompt:
        return "SAFETY AUDIT: Black box warnings verified for both. Pharmacology cites FDA Label 2023. Regulatory cites FDA approval database. Evidence quality: High."
    
    elif "senior medical editor" in system_prompt:
        # Return a structured result for the synthesis agent
        return MedicinesComparisonResult(
            medicine1_clinical=ClinicalMetrics(
                medicine_name="Ibuprofen",
                effectiveness_rating=EffectivenessRating.HIGH,
                efficacy_rate="85%",
                onset_of_action="30-60 mins",
                duration_of_effect="4-6 hours",
                safety_rating=SafetyRating.MODERATE_RISK,
                common_side_effects="Stomach upset",
                serious_side_effects="GI bleeding",
                contraindications="NSAID allergy, ulcers"
            ),
            medicine2_clinical=ClinicalMetrics(
                medicine_name="Acetaminophen",
                effectiveness_rating=EffectivenessRating.HIGH,
                efficacy_rate="80%",
                onset_of_action="30-60 mins",
                duration_of_effect="4-6 hours",
                safety_rating=SafetyRating.LOW_RISK,
                common_side_effects="Nausea",
                serious_side_effects="Liver toxicity",
                contraindications="Severe liver disease"
            ),
            medicine1_regulatory=RegulatoryMetrics(
                medicine_name="Ibuprofen",
                fda_approval_status="Approved",
                approval_date="1974",
                approval_type="Standard",
                has_black_box_warning=True,
                fda_alerts="CV risk",
                generic_available=True
            ),
            medicine2_regulatory=RegulatoryMetrics(
                medicine_name="Acetaminophen",
                fda_approval_status="Approved",
                approval_date="1955",
                approval_type="Standard",
                has_black_box_warning=False,
                fda_alerts="Liver warning",
                generic_available=True
            ),
            medicine1_practical=PracticalMetrics(
                medicine_name="Ibuprofen",
                availability_status=AvailabilityStatus.OVER_THE_COUNTER,
                typical_cost_range="$5-15",
                insurance_coverage="Standard",
                available_formulations="Tablet, Gel, Liquid",
                dosage_strengths="200mg, 400mg",
                patient_assistance_programs="N/A"
            ),
            medicine2_practical=PracticalMetrics(
                medicine_name="Acetaminophen",
                availability_status=AvailabilityStatus.OVER_THE_COUNTER,
                typical_cost_range="$5-15",
                insurance_coverage="Standard",
                available_formulations="Tablet, Liquid",
                dosage_strengths="325mg, 500mg",
                patient_assistance_programs="N/A"
            ),
            medicine1_compliance=ComplianceMetrics(
                medicine_name="Ibuprofen",
                controlled_substance_schedule="Non-controlled",
                prescribing_restrictions="None (OTC)",
                monitoring_requirements="Renal function for long-term use",
                patient_adherence_risk="Low",
                guideline_alignment="First-line for inflammatory pain"
            ),
            medicine2_compliance=ComplianceMetrics(
                medicine_name="Acetaminophen",
                controlled_substance_schedule="Non-controlled",
                prescribing_restrictions="None (OTC)",
                monitoring_requirements="None (Routine)",
                patient_adherence_risk="Low",
                guideline_alignment="First-line for mild-to-moderate pain"
            ),
            comparison_summary=ComparisonSummary(
                more_effective="Context dependent",
                safer_option="Acetaminophen (lower GI risk)",
                more_affordable="Equivalent",
                easier_access="Equivalent",
                key_differences="Anti-inflammatory properties, GI vs Liver risk profile"
            ),
            recommendations=RecommendationContext(
                for_acute_conditions="Both effective",
                for_elderly_patients="Acetaminophen preferred",
                overall_recommendation="Use Ibuprofen for inflammation, Acetaminophen for simple pain/fever."
            ),
            safety_audit=SafetyAudit(
                black_box_warning_verified=True,
                evidence_citations="FDA Label 2023, DailyMed Ibuprofen, FDA Acetaminophen Consumer Guide",
                recommendation_safety_level="Conservative"
            ),
            narrative_analysis="Synthesized analysis of 6 specialist reports audited for safety...",
            evidence_quality="High",
            limitations="General OTC guidance only"
        )
    
    return "Unknown agent"

def run_mock_test():
    print("\n--- Starting Mock Multi-Agent Test ---\n")
    
    model_config = ModelConfig(model="mock-model")
    analyzer = DrugsComparison(model_config)
    
    # Patch the internal _ask_llm method
    with patch.object(DrugsComparison, '_ask_llm', side_effect=mock_ask_llm):
        config = DrugsComparisonInput(
            medicine1="Ibuprofen",
            medicine2="Acetaminophen",
            use_case="General Pain",
            patient_age=65
        )
        
        result = analyzer.generate_text(config, structured=True)
        
        print("\n--- Final Synthesized Result ---")
        print(f"Medicine 1: {result.medicine1_clinical.medicine_name}")
        print(f"Medicine 2: {result.medicine2_clinical.medicine_name}")
        print(f"Summary: {result.comparison_summary.key_differences}")
        print(f"Recommendation for Elderly: {result.recommendations.for_elderly_patients}")
        print("\nTest completed successfully!")

if __name__ == "__main__":
    run_mock_test()

"""Module docstring - Medicines Comparison Tool.

Compare medicines side-by-side across clinical, regulatory, and practical metrics to help
healthcare professionals and patients make informed treatment decisions.
"""



logger = logging.getLogger(__name__)


def get_user_arguments():
    """Create and configure the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Medicines Comparison Tool - Compare two medicines side-by-side",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Required arguments
    parser.add_argument(
        "medicine1",
        type=str,
        help="Name of the first medicine to compare",
    )

    parser.add_argument(
        "medicine2",
        type=str,
        help="Name of the second medicine to compare",
    )

    # Optional arguments
    parser.add_argument(
        "--use-case",
        "-u",
        type=str,
        default=None,
        help="Use case or indication for the comparison (e.g., 'pain relief', 'hypertension')",
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
        "--model",
        "-m",
        type=str,
        default="ollama/gemma2",
        help="Model ID to use for the comparison (e.g., 'ollama/llama3', 'openai/gpt-4o')",
    )

    parser.add_argument(
        "--json-output",
        "-j",
        action="store_true",
        default=False,
        help="Output results as JSON to stdout",
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


def create_drugs_comparision_report(args) -> int:

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "drugs_comparison.log"),
        verbosity=args.verbosity,
        enable_console=True,
    )
    logger.debug("CLI Arguments:")
    logger.debug(f"  Medicine 1: {args.medicine1}")
    logger.debug(f"  Medicine 2: {args.medicine2}")
    logger.debug(f"  Use Case: {args.use_case}")
    logger.debug(f"  Age: {args.age}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Create configuration
        config = DrugsComparisonInput(
            medicine1=args.medicine1,
            medicine2=args.medicine2,
            use_case=args.use_case,
            patient_age=args.age,
            patient_conditions=args.conditions,
            prompt_style=args.prompt_style,
        )

        # Run analysis
        model_config = ModelConfig(model=args.model, temperature=0.7)
        analyzer = DrugsComparison(model_config)
        result = analyzer.generate_text(config, structured=args.structured)

        if result is None:
            logger.error("✗ Failed to generate drugs comparison information.")
            return 1

        # Save result to output directory
        analyzer.save(result, output_dir)

        logger.debug("✓ Drugs comparison generation completed successfully")
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
    args = get_user_arguments()
    create_drugs_comparision_report(args)

