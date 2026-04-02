"""
liteagents.py - Unified for med_speciality_roles
"""
from typing import Any, Callable, Type\nfrom app.MedKit.medical.med_speciality_roles.shared.models import *\nfrom tqdm import tqdm\nimport logging\nfrom lite.lite_client import LiteClient\nimport pytest\nfrom pathlib import Path\nimport argparse\nfrom lite.config import ModelConfig\nfrom unittest.mock import patch, MagicMock\nfrom lite.config import ModelConfig, ModelInput\nfrom lite.logging_config import configure_logging\nimport sys\n\n"""Medical Speciality Roles CLI."""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))




try:
    from .med_speciality_roles import MedSpecialityRoles
except (ImportError, ValueError):
    from medical.med_speciality_roles.agentic.med_speciality_roles import MedSpecialityRoles

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Get roles and responsibilities of a medical specialist."
    )
    parser.add_argument(
        "speciality", help="Speciality or file path containing specialities."
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
    return parser.parse_args()


def main():
    args = get_user_arguments()
    configure_logging(
        log_file="med_speciality_roles.log",
        verbosity=args.verbosity,
        enable_console=True,
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.speciality)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.speciality]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.0)
        med_roles = MedSpecialityRoles(model_config)

        for item in tqdm(items, desc="Retrieving Roles"):
            result = med_roles.generate_text(item)
            if result and not result.startswith("Error"):
                fname = "".join([c if c.isalnum() else "_" for c in item.lower()])[:50]
                with open(output_dir / f"{fname}.md", "w") as f:
                    f.write(result)

        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())

"""Specialized agents for medical speciality roles generation."""



    ModelOutput,
    SpecialityRoleInfo,
    ComplianceReviewModel,
)

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for specialized medical agents."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the agent with a model configuration."""
        self.model_config = model_config
        self.client = LiteClient(model_config)

    def generate(
        self,
        topic: str,
        structured: bool,
        response_format: Type[Any],
        prompts_fn: Callable[[str], tuple[str, str]],
    ) -> ModelOutput:
        """Execute the agent's task for the given topic."""
        system_prompt, user_prompt = prompts_fn(topic)
        logger.debug(f"Agent {self.__class__.__name__} starting generation.")

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format if structured else None,
        )

        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {e}")
            raise


class SpecialityAgent(BaseAgent):
    """Agent for medical speciality roles and responsibilities."""

    def run(self, speciality: str, structured: bool) -> ModelOutput:
        return self.generate(
            speciality,
            structured,
            SpecialityRoleInfo,
            PromptBuilder.create_speciality_agent_prompts,
        )


class ComplianceAgent(BaseAgent):
    """Agent for final compliance and regulatory review (Outputs JSON)."""

    def run(self, speciality: str, content: str, structured: bool) -> ModelOutput:
        """Run the compliance review on the provided content and return structured JSON."""
        system_prompt, user_prompt = PromptBuilder.create_compliance_agent_prompts(
            speciality, content
        )
        logger.debug("ComplianceAgent starting validation (JSON output).")

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=ComplianceReviewModel if structured else None,
        )

        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"Error in ComplianceAgent: {e}")
            raise


class OutputAgent(BaseAgent):
    """The Final Closer Agent. Synthesizes all specialists and compliance data into Markdown."""

    def run(self, speciality: str, specialist_data: str, compliance_data: str) -> str:
        """Synthesize all inputs into a final, polished Markdown report."""
        system_prompt, user_prompt = PromptBuilder.create_output_agent_prompts(
            speciality, specialist_data, compliance_data
        )
        logger.debug("OutputAgent starting final synthesis (Markdown).")

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=None, # Always Markdown
        )

        try:
            res = self.client.generate_text(model_input=model_input)
            return res.markdown
        except Exception as e:
            logger.error(f"Error in OutputAgent: {e}")
            raise


# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


    ModelOutput,
    SpecialityRoleInfo,
    ComplianceReviewModel,
    MedicalSpecialityRolesModel
)


@pytest.fixture
def mock_lite_client():
    # Mock the LiteClient in the agents module
    with patch("medical.med_speciality_roles.agentic.med_speciality_roles_agents.LiteClient") as mock:
        yield mock


def test_med_speciality_roles_init():
    config = ModelConfig(model="test-model")
    roles = MedSpecialityRoles(config)
    assert roles.config == config


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    roles = MedSpecialityRoles(config)

    mock_instance = mock_lite_client.return_value
    mock_instance.generate_text.side_effect = [
        ModelOutput(markdown="Specialist info"),
        ModelOutput(markdown="Compliance: All clear."),
        ModelOutput(markdown="Final Markdown Report"),
    ]

    result = roles.generate_text("Cardiologist", structured=False)
    assert result.markdown == "Final Markdown Report"


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    roles = MedSpecialityRoles(config)

    mock_instance = mock_lite_client.return_value

    # 1. SpecialityAgent
    spec_info = SpecialityRoleInfo(
        speciality_name="Cardiologist",
        primary_focus="Heart",
        key_responsibilities=["Treat heart"],
        common_procedures=["EKG"]
    )
    # 2. ComplianceAgent
    compliance_info = ComplianceReviewModel(
        is_compliant=True,
        issues_found=[],
        required_disclaimers=["Disclaimer"],
        suggested_edits=None
    )
    # 3. OutputAgent (Always returns markdown)
    output_res = ModelOutput(markdown="# Final Report\n\nSome content.")

    mock_instance.generate_text.side_effect = [
        ModelOutput(data=spec_info),
        ModelOutput(data=compliance_info),
        output_res,
    ]

    result = roles.generate_text("Cardiologist", structured=True)
    assert result.data.speciality_name == "Cardiologist"
    assert result.data.roles_info.primary_focus == "Heart"
    assert result.data.compliance_review.is_compliant is True
    assert result.markdown == "# Final Report\n\nSome content."


def test_generate_text_error(mock_lite_client):
    config = ModelConfig(model="test-model")
    roles = MedSpecialityRoles(config)

    mock_lite_client.return_value.generate_text.side_effect = Exception("API Error")

    with pytest.raises(Exception) as excinfo:
        roles.generate_text("Cardiologist")
    assert "API Error" in str(excinfo.value)



logger = logging.getLogger(__name__)


class MedSpecialityRoles:
    """
    A class for determining the roles and responsibilities of a medical specialist.
    Using a 3-tier multi-agent approach.
    """

    def __init__(self, config: ModelConfig):
        self.config = config
        self.speciality_agent = SpecialityAgent(config)
        self.compliance_agent = ComplianceAgent(config)
        self.output_agent = OutputAgent(config)

    def generate_text(self, speciality: str, structured: bool = False) -> ModelOutput:
        """
        Generates comprehensive specialist roles info using a 3-tier agent system.
        """
        if not speciality or not speciality.strip():
            raise ValueError("Speciality name cannot be empty")

        logger.info(f"Starting 3-tier specialist roles generation for: {speciality}")

        try:
            # 1. Run Specialist agent
            logger.debug("Running Specialist agent...")
            spec_res = self.speciality_agent.run(speciality, structured)
            
            if structured:
                spec_content = spec_res.data.model_dump_json(indent=2)
                roles_info = spec_res.data
            else:
                spec_content = spec_res.markdown
                roles_info = None

            # 2. Compliance Audit Stage (JSON/Audit)
            logger.debug("Running ComplianceAgent audit...")
            compliance_res = self.compliance_agent.run(
                speciality, spec_content, structured
            )
            
            comp_content = (
                compliance_res.data.model_dump_json(indent=2)
                if structured and compliance_res.data
                else str(compliance_res.markdown)
            )

            # 3. Final Synthesis Stage (Markdown/Refinement)
            logger.debug("Running OutputAgent final synthesis...")
            final_markdown = self.output_agent.run(
                speciality, spec_content, comp_content
            )

            # Aggregate data
            aggregated_data = None
            if structured:
                aggregated_data = MedicalSpecialityRolesModel(
                    speciality_name=speciality,
                    roles_info=roles_info,
                    compliance_review=compliance_res.data
                )

            return ModelOutput(markdown=final_markdown, data=aggregated_data)

        except Exception as e:
            logger.error(f"✗ 3-tier generation failed: {e}")
            raise

