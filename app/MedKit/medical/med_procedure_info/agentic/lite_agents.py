"""
liteagents.py - Unified for med_procedure_info
"""
from .medical_procedure_info_prompts import (
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
import sys
from unittest.mock import patch
from .eval_medical_procedure_models import MedicalProcedureEvaluationModel, ModelOutput
from typing import Optional, Union
from .medical_procedure_info_models import (
from tqdm import tqdm
import pytest
from .eval_medical_procedure_prompts import PromptBuilder
import logging
from pathlib import Path
from lite.utils import save_model_response
from lite.lite_client import LiteClient
from app.MedKit.medical.med_procedure_info.shared.models import *
import concurrent.futures
import argparse

#!/usr/bin/env python3
"""
Standalone module for creating medical procedure info prompts.

This module provides a builder class for generating system and user prompts
for structured, evidence-based medical procedure documentation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical procedure documentation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for medical procedure documentation."""
        return (
            "You are an expert medical documentation specialist. "
            "Generate structured, clinically accurate, evidence-based medical procedure information. "
            "Use precise medical terminology. Avoid vague language. "
            "Do not include legal disclaimers or advice to consult doctors."
        )

    @staticmethod
    def create_user_prompt(procedure: str) -> str:
        """Create the user prompt for procedure information."""
        return f"""
Generate comprehensive, evidence-based information for the medical procedure or surgery: "{procedure}"

Organize the output under the following sections:

1. Definition and Purpose
2. Indications
3. Contraindications
4. Patient Preparation
5. Required Instruments and Equipment
6. Anesthesia or Analgesia Used
7. Step-by-Step Procedure Technique
8. Duration of Procedure
9. Intraoperative Monitoring
10. Possible Complications
11. Post-procedure Care
12. Recovery and Follow-up
13. Outcomes and Success Rates (if known)
14. Alternatives

Requirements:
- Use medically accurate terminology
- Be clinically precise and complete
- Do not use conversational tone
- Do not add unnecessary commentary
- Do not assume the procedure is surgical unless it truly is
- Clearly state whether it is minimally invasive or surgical when relevant
"""


# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))



try:
    from medical.med_procedure_info.agentic.medical_procedure_info import (
        MedicalProcedureInfoGenerator,
    )
    from medical.med_procedure_info.agentic.medical_procedure_info_models import (
        AdminAgentOutput,
        Alternatives,
        ClinicalAgentOutput,
        ComplianceReport,
        CostAndInsurance,
        DiscomfortAndRisks,
        FollowUpCare,
        MedicalProcedureInfoModel,
        ModelOutput,
        OutcomesAndEffectiveness,
        PreparationRequirements,
        ProcedureDetails,
        ProcedureEducation,
        ProcedureEvidence,
        ProcedureIndications,
        ProcedureLimitations,
        ProcedureMetadata,
        ProcedurePurpose,
        RecoveryAgentOutput,
        RecoveryInformation,
        RiskAgentOutput,
        TechnicalAgentOutput,
        TechnicalDetails,
    )
except ImportError:
    from medical_procedure_info import MedicalProcedureInfoGenerator
    from medical_procedure_info_models import (
        AdminAgentOutput,
        Alternatives,
        ClinicalAgentOutput,
        ComplianceReport,
        CostAndInsurance,
        DiscomfortAndRisks,
        FollowUpCare,
        MedicalProcedureInfoModel,
        ModelOutput,
        OutcomesAndEffectiveness,
        PreparationRequirements,
        ProcedureDetails,
        ProcedureEducation,
        ProcedureEvidence,
        ProcedureIndications,
        ProcedureLimitations,
        ProcedureMetadata,
        ProcedurePurpose,
        RecoveryAgentOutput,
        RecoveryInformation,
        RiskAgentOutput,
        TechnicalAgentOutput,
        TechnicalDetails,
    )


@pytest.fixture
def mock_lite_client():
    # Use absolute path for mocking to be safe
    mock_path = "medical.med_procedure_info.agentic.medical_procedure_info.LiteClient"
    with patch(mock_path) as mock:
        yield mock


def test_generator_init():
    config = ModelConfig(model="test-model")
    generator = MedicalProcedureInfoGenerator(config)
    assert generator.model_config == config


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalProcedureInfoGenerator(config)
    mock_output = ModelOutput(markdown="Appendectomy info", data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Appendectomy")
    assert "Appendectomy info" in result.markdown
    assert generator.procedure_name == "Appendectomy"


def test_generate_text_empty():
    config = ModelConfig(model="test-model")
    generator = MedicalProcedureInfoGenerator(config)
    with pytest.raises(ValueError, match="Procedure name cannot be empty"):
        generator.generate_text("")


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalProcedureInfoGenerator(config)

    # Mock side_effect to handle multiple agent calls
    def side_effect(model_input):
        sys_prompt = str(model_input.system_prompt).lower()
        if "compliance" in sys_prompt:
            return ModelOutput(data=ComplianceReport(is_compliant=True, safety_concerns=[], readability_issues=[], tone_violations=[], suggestions=[]))
        elif "clinical diagnostician" in sys_prompt:
            return ModelOutput(data=ClinicalAgentOutput(
                metadata=ProcedureMetadata(procedure_name="Appendectomy", alternative_names="", procedure_category="", medical_specialty=""),
                purpose=ProcedurePurpose(primary_purpose="", therapeutic_uses="", diagnostic_uses="", preventive_uses=""),
                indications=ProcedureIndications(when_recommended="", symptoms_requiring_procedure="", conditions_treated="", contraindications=""),
                alternatives=Alternatives(alternative_procedures="", non_surgical_alternatives="", advantages_over_alternatives="", when_alternatives_preferred="")
            ))
        elif "procedure specialist" in sys_prompt:
            return ModelOutput(data=TechnicalAgentOutput(
                details=ProcedureDetails(procedure_type="", anesthesia_type="", step_by_step_process="", duration="", location="", equipment_used="", hospital_stay=""),
                technical=TechnicalDetails(surgical_approach="", technology_used="", procedure_variations="", surgeon_qualifications="", facility_requirements=""),
                evidence=ProcedureEvidence(evidence_summary="", procedure_limitations=ProcedureLimitations(not_suitable_for="", age_limitations="", medical_conditions_precluding="", anatomical_limitations=""))
            ))
        elif "risk analyst" in sys_prompt:
            return ModelOutput(data=RiskAgentOutput(
                risks=DiscomfortAndRisks(discomfort_level="", common_sensations="", common_side_effects="", serious_risks="", complication_rates="", mortality_risk="")
            ))
        elif "care coordinator" in sys_prompt:
            return ModelOutput(data=RecoveryAgentOutput(
                preparation=PreparationRequirements(fasting_required="", medication_adjustments="", dietary_restrictions="", pre_procedure_tests="", items_to_bring="", lifestyle_modifications=""),
                recovery=RecoveryInformation(immediate_recovery="", recovery_timeline="", pain_management="", activity_restrictions="", return_to_work="", return_to_normal_activities="", warning_signs=""),
                outcomes=OutcomesAndEffectiveness(success_rate="", expected_benefits="", symptom_improvement="", long_term_outcomes="", factors_affecting_outcomes=""),
                follow_up=FollowUpCare(follow_up_schedule="", monitoring_required="", lifestyle_changes="", medications_after="", physical_therapy="")
            ))
        elif "patient liaison" in sys_prompt:
            return ModelOutput(data=AdminAgentOutput(
                cost_and_insurance=CostAndInsurance(typical_cost_range="", insurance_coverage="", prior_authorization="", medicare_coverage="", medicaid_coverage="", financial_assistance_programs="", cpt_codes=""),
                education=ProcedureEducation(plain_language_explanation="", key_takeaways="", common_misconceptions="")
            ))
        return ModelOutput()

    mock_lite_client.return_value.generate_text.side_effect = side_effect

    result = generator.generate_text("Appendectomy", structured=True)
    assert result.data.metadata.procedure_name == "Appendectomy"
    assert result.compliance_report.is_compliant is True


@patch("medical.med_procedure_info.agentic.medical_procedure_info.save_model_response")
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalProcedureInfoGenerator(config)
    mock_output = ModelOutput(markdown="Info")
    mock_lite_client.return_value.generate_text.return_value = mock_output

    generator.generate_text("Appendectomy")
    generator.save(mock_output, Path("/tmp"))

    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("appendectomy")

#!/usr/bin/env python3
"""
Medical Procedure Information module.

This module provides the core MedicalProcedureInfoGenerator class for generating
comprehensive medical procedure information based on provided configuration using
a multi-agent approach, including parallel domain agents and a sequential compliance auditor.
"""



    AdminAgentOutput,
    ClinicalAgentOutput,
    ComplianceReport,
    MedicalProcedureInfoModel,
    ModelOutput,
    RecoveryAgentOutput,
    RiskAgentOutput,
    TechnicalAgentOutput,
)
    AdminPromptBuilder,
    ClinicalPromptBuilder,
    CompliancePromptBuilder,
    OutputPromptBuilder,
    RecoveryPromptBuilder,
    RiskPromptBuilder,
    TechnicalPromptBuilder,
)

logger = logging.getLogger(__name__)


class MedicalProcedureInfoGenerator:
    """Generate comprehensive information for medical procedures using a 3-tier multi-agent approach."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.procedure_name: Optional[str] = None
        logger.debug("Initialized 3-tier MedicalProcedureInfoGenerator")

    def generate_text(self, procedure: str, structured: bool = False) -> ModelOutput:
        """Generate and retrieve comprehensive medical procedure information."""
        if not procedure or not procedure.strip():
            raise ValueError("Procedure name cannot be empty")

        # Store the procedure for later use in save
        self.procedure_name = procedure
        logger.debug(
            f"Starting 3-tier multi-agent medical procedure information generation for: {procedure}"
        )

        # Step 1: Parallel Domain Agents (Scatter - JSON Specialists)
        agents = [
            ("Clinical", ClinicalPromptBuilder, ClinicalAgentOutput),
            ("Technical", TechnicalPromptBuilder, TechnicalAgentOutput),
            ("Risk", RiskPromptBuilder, RiskAgentOutput),
            ("Recovery", RecoveryPromptBuilder, RecoveryAgentOutput),
            ("Admin", AdminPromptBuilder, AdminAgentOutput),
        ]

        def call_agent(agent_name, prompt_builder, output_model) -> ModelOutput:
            sys_prompt = prompt_builder.create_system_prompt()
            usr_prompt = prompt_builder.create_user_prompt(procedure)
            
            response_format = output_model if structured else None
            
            model_input = ModelInput(
                system_prompt=sys_prompt,
                user_prompt=usr_prompt,
                response_format=response_format,
            )
            
            try:
                result = self.client.generate_text(model_input=model_input)
                return result
            except Exception as e:
                logger.error(f"[{agent_name} Agent] ✗ Error generating information: {e}")
                raise

        futures = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            for name, builder, model in agents:
                futures[name] = executor.submit(call_agent, name, builder, model)
            
            concurrent.futures.wait(futures.values())

        # Step 2: Gather Results
        final_data = None
        content_for_review = ""

        if not structured:
            content_for_review = "

".join(
                [f.result().markdown or "" for name, f in futures.items() if not f.exception()]
            )
        else:
            # Merge structured results
            try:
                clinical_data = futures["Clinical"].result().data
                technical_data = futures["Technical"].result().data
                risk_data = futures["Risk"].result().data
                recovery_data = futures["Recovery"].result().data
                admin_data = futures["Admin"].result().data
                
                final_data = MedicalProcedureInfoModel(
                    metadata=clinical_data.metadata,
                    purpose=clinical_data.purpose,
                    indications=clinical_data.indications,
                    preparation=recovery_data.preparation,
                    details=technical_data.details,
                    risks=risk_data.risks,
                    recovery=recovery_data.recovery,
                    outcomes=recovery_data.outcomes,
                    follow_up=recovery_data.follow_up,
                    alternatives=clinical_data.alternatives,
                    technical=technical_data.technical,
                    evidence=technical_data.evidence,
                    cost_and_insurance=admin_data.cost_and_insurance,
                    education=admin_data.education,
                )
                content_for_review = final_data.model_dump_json(indent=2)
            except Exception as e:
                logger.error(f"✗ Error merging multi-agent results: {e}")
                raise

        # Step 3: Compliance Audit (Sequential - JSON Auditor)
        logger.debug(f"Starting compliance audit for: {procedure}")
        
        audit_sys_prompt = CompliancePromptBuilder.create_system_prompt()
        audit_usr_prompt = CompliancePromptBuilder.create_user_prompt(procedure, content_for_review)
        
        audit_input = ModelInput(
            system_prompt=audit_sys_prompt,
            user_prompt=audit_usr_prompt,
            response_format=ComplianceReport,
        )
        
        try:
            audit_result = self.client.generate_text(model_input=audit_input)
            compliance_report_json = audit_result.data.model_dump_json(indent=2)
            logger.debug("✓ Compliance audit completed (JSON)")
        except Exception as e:
            logger.error(f"✗ Compliance audit failed: {e}")
            compliance_report_json = "{}"
        
        # Step 4: Final Synthesis (Sequential - Markdown Closer)
        logger.debug(f"Starting final synthesis for: {procedure}")
        output_sys_prompt = OutputPromptBuilder.create_system_prompt()
        output_usr_prompt = OutputPromptBuilder.create_user_prompt(
            procedure, content_for_review, compliance_report_json
        )
        
        output_input = ModelInput(
            system_prompt=output_sys_prompt,
            user_prompt=output_usr_prompt,
            response_format=None,
        )
        
        try:
            final_markdown_res = self.client.generate_text(model_input=output_input)
            final_markdown = final_markdown_res.markdown if hasattr(final_markdown_res, 'markdown') else str(final_markdown_res)
            logger.debug("✓ Final synthesis completed (Markdown)")
            
            # Tier 2: Process/Audit metadata
            metadata = {}
            try:
                if 'audit_result' in locals() and audit_result and hasattr(audit_result, 'data'):
                    metadata["audit"] = audit_result.data
            except Exception as e:
                logger.debug(f"Could not attach audit metadata: {e}")

            return ModelOutput(
                data=final_data, 
                markdown=final_markdown,
                metadata=metadata
            )
        except Exception as e:
            logger.error(f"✗ Final synthesis failed: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical procedure information to a file."""
        if self.procedure_name is None:
            raise ValueError(
                "No procedure information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.procedure_name.lower().replace(' ', '_')}"

        return save_model_response(result, output_dir / base_filename)

#!/usr/bin/env python3
"""
Medical Procedure Output Evaluation module.

This module provides the MedicalProcedureEvaluator class for critically reviewing
generated medical procedure information against high medical standards.
"""




logger = logging.getLogger(__name__)


class MedicalProcedureEvaluator:
    """Evaluate medical procedure information using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the evaluator."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.procedure_name: Optional[str] = None
        logger.debug("Initialized MedicalProcedureEvaluator")

    def generate_text(
        self, file_path: Union[str, Path], structured: bool = True
    ) -> ModelOutput:
        """Read content from a file and evaluate it."""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise

        # Infer procedure name from filename
        procedure_name = file_path.stem.replace("_", " ").title()
        self.procedure_name = procedure_name
        logger.info(f"Inferred procedure name from filename: {procedure_name}")

        if not content or not content.strip():
            raise ValueError("Content to evaluate cannot be empty")

        logger.debug(f"Starting evaluation for procedure: {procedure_name}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(procedure_name, content)

        response_format = None
        if structured:
            response_format = MedicalProcedureEvaluationModel

        logger.debug(f"System Prompt: {system_prompt}")

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text() for evaluation...")
        try:
            result = self.client.generate_text(model_input=model_input)

            if structured:
                logger.debug("✓ Successfully generated structured evaluation")
                return ModelOutput(data=result.data, markdown=result.markdown)

            logger.debug(
                "✓ Successfully evaluated medical procedure information (unstructured)"
            )
            return ModelOutput(markdown=result.markdown)
        except Exception as e:
            logger.error(f"✗ Error evaluating medical procedure information: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the evaluation report to a file."""
        if self.procedure_name is None:
            raise ValueError(
                "No procedure evaluated. Call evaluate_text or evaluate_file first."
            )

        base_filename = f"{self.procedure_name.lower().replace(' ', '_')}_eval"

        return save_model_response(result, output_dir / base_filename)

"""eval_medical_procedure_output - Critically review medical procedure documentation."""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))




# Ensure we can import from the current directory
sys.path.append(str(Path(__file__).parent))


try:
    from .eval_medical_procedure_output import MedicalProcedureEvaluator
except (ImportError, ValueError):
    try:
        from eval_medical_procedure_output import MedicalProcedureEvaluator
    except ImportError:
        from medical.med_procedure_info.agentic.eval_medical_procedure_output import (
            MedicalProcedureEvaluator,
        )

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Critically evaluate medical procedure information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "file",
        help="Path to the file containing the medical procedure information to evaluate, or a file path containing paths.",
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
        default="ollama/gemma3:27b-cloud",
        help="Model to use (default: gemma3:27b-cloud)",
    )
    parser.add_argument(
        "-s",
        "--structured",
        action="store_true",
        default=True,
        help="Use structured output (Pydantic model) for the evaluation (default: True).",
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2).",
    )

    return parser.parse_args()


def evaluate_medical_procedure_report(args) -> int:

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "eval_medical_procedure.log"),
        verbosity=args.verbosity,
        enable_console=True,
    )

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Handle input - check if it's a file or direct term
    input_path = Path(args.file)
    if input_path.is_file():
        # Check if it's a markdown or text file which IS the target, OR a file list
        if input_path.suffix in [".md", ".txt", ".json"]:
            input_files = [str(input_path)]
        else:
            with open(input_path, "r", encoding="utf-8") as f:
                input_files = [line.strip() for line in f if line.strip()]
        logger.debug(f"Read {len(input_files)} files to evaluate from: {input_path}")
    else:
        input_files = [args.file]

    try:
        model_config = ModelConfig(
            model=args.model, temperature=0.1
        )  # Low temp for evaluation
        evaluator = MedicalProcedureEvaluator(model_config=model_config)

        for file_path in tqdm(input_files, desc="Evaluating procedure reports"):
            result = evaluator.generate_text(file_path=file_path)

            if result is None:
                logger.error(
                    f"✗ Failed to evaluate procedure information for: {file_path}"
                )
                continue

            # Save result to output directory
            saved_path = evaluator.save(result, output_dir)
            logger.info(f"Evaluation report saved to: {saved_path}")

        logger.debug("✓ Procedure evaluations completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Procedure evaluation failed: {e}")
        logger.exception("Full exception details:")
        return 1


def main():
    args = get_user_arguments()
    evaluate_medical_procedure_report(args)


if __name__ == "__main__":
    main()

"""Medical Procedure Information Generator CLI."""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))




try:
    from .medical_procedure_info import MedicalProcedureInfoGenerator
except (ImportError, ValueError):
    try:
    except ImportError:
            MedicalProcedureInfoGenerator,
        )

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate comprehensive medical procedure documentation."
    )
    parser.add_argument(
        "procedure", help="Procedure name or file path containing names."
    )
    parser.add_argument(
        "-d", "--output-dir", default="outputs", help="Output directory."
    )
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use.")
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Verbosity level.",
    )
    parser.add_argument(
        "-s", "--structured", action="store_true", help="Use structured output."
    )
    return parser.parse_args()


def main():
    args = get_user_arguments()
    configure_logging(
        log_file="medical_procedure_info.log",
        verbosity=args.verbosity,
        enable_console=True,
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.procedure)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.procedure]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MedicalProcedureInfoGenerator(model_config)

        for item in tqdm(items, desc="Generating"):
            result = generator.generate_text(procedure=item, structured=args.structured)
            if result:
                generator.save(result, output_dir)

        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())