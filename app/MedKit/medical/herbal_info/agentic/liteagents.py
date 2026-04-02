"""
liteagents.py - Unified for herbal_info
"""
from app.MedKit.medical.herbal_info.shared.models import *\nfrom typing import Optional, Type, Dict, Any\nfrom lite.utils import save_model_response\nfrom concurrent.futures import ThreadPoolExecutor\nfrom tqdm import tqdm\nfrom lite.lite_client import LiteClient\nimport logging\nimport pytest\nfrom pathlib import Path\nfrom pydantic import BaseModel, Field\nimport argparse\nfrom lite.config import ModelConfig\nfrom unittest.mock import patch, MagicMock\nfrom lite.config import ModelConfig, ModelInput\nfrom lite.logging_config import configure_logging\nimport sys\n\n#!/usr/bin/env python3
"""
Herbal Information module.

This module provides the core HerbalInfoGenerator class for generating
comprehensive herbal remedy information based on provided configuration.
"""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


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


# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))



    AdministrationGuidanceModel,
    AlternativesModel,
    CostAndAvailabilityModel,
    DosageModel,
    EfficacyModel,
    HerbalBackgroundModel,
    HerbalClassificationModel,
    HerbalEducationModel,
    HerbalEvidenceModel,
    HerbalInfoModel,
    HerbalInteractionsModel,
    HerbalMechanismModel,
    HerbalMetadataModel,
    HerbalResearchModel,
    ModelOutput,
    SafetyInformationModel,
    SpecialInstructionsModel,
    SpecialPopulationsModel,
    UsageAndAdministrationModel,
)


@pytest.fixture
def mock_lite_client():
    with patch("medical.herbal_info.agentic.herbal_info.LiteClient") as mock:
        yield mock


def test_herbal_info_generator_init():
    config = ModelConfig(model="test-model")
    generator = HerbalInfoGenerator(config)
    assert generator.model_config == config
    assert len(generator.agents) == 5


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = HerbalInfoGenerator(config)
    
    # Each agent returns the same markdown in this simple test
    mock_output = ModelOutput(markdown="Agent info", data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Ashwagandha")
    # 5 agents, so "Agent info" repeated 5 times with separators
    assert "Agent info" in result.markdown
    assert generator.herb == "Ashwagandha"
    assert mock_lite_client.return_value.generate_text.call_count == 5


def test_generate_text_empty_herb():
    config = ModelConfig(model="test-model")
    generator = HerbalInfoGenerator(config)
    with pytest.raises(ValueError, match="Herb name cannot be empty"):
        generator.generate_text("")


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = HerbalInfoGenerator(config)

    # Mock different data for different agents would be better, 
    # but for simplicity let's mock one that has all fields needed.
    # We need to return specific output models for each agent.
    
    from medical.herbal_info.agentic.herbal_info_agents import (
        BotanicalOutput,
        PharmacologicalOutput,
        SafetyOutput,
        ClinicalOutput,
        EducatorOutput,
    )
    # Create dummy data for each agent's expected output format
    def side_effect(model_input):
        if model_input.response_format == BotanicalOutput:
            return ModelOutput(data=BotanicalOutput(
                metadata=HerbalMetadataModel(
                    common_name="Ashwagandha",
                    botanical_name="Withania somnifera",
                    other_names="Winter cherry",
                    plant_family="Solanaceae",
                    active_constituents="Withanolides",
                    forms_available="Powder, Capsule",
                ),
                classification=HerbalClassificationModel(
                    traditional_system="Ayurveda",
                    primary_uses="Adaptogen",
                    energetics="Warming",
                    taste_profile="Bitter",
                ),
                background=HerbalBackgroundModel(
                    origin_and_habitat="India",
                    history_and_traditional_use="Ancient",
                    botanical_description="Shrub",
                )
            ))
        elif model_input.response_format == PharmacologicalOutput:
            return ModelOutput(data=PharmacologicalOutput(
                mechanism=HerbalMechanismModel(
                    mechanism_of_action="HPA axis modulation",
                    active_constituents_effects="Anti-stress",
                    body_systems_affected="Endocrine",
                ),
                evidence=HerbalEvidenceModel(
                    evidence_level="Moderate",
                    clinical_studies="Multiple RCTs",
                    regulatory_status="Dietary supplement",
                ),
                research=HerbalResearchModel(
                    recent_research="Sleep studies",
                    ongoing_studies="Cognition",
                    future_applications="Neuroprotection",
                )
            ))
        elif model_input.response_format == SafetyOutput:
            return ModelOutput(data=SafetyOutput(
                safety=SafetyInformationModel(
                    common_side_effects="Drowsiness",
                    serious_adverse_effects="None",
                    interactions=HerbalInteractionsModel(
                        drug_interactions="Sedatives",
                        herb_interactions="None",
                        food_interactions="None",
                        caffeine_interactions="None",
                        alcohol_interactions="Increased sedation",
                    ),
                    contraindications="Pregnancy",
                    precautions="Thyroid conditions",
                ),
                special_instructions=SpecialInstructionsModel(
                    discontinuation_guidance="None",
                    overdose_information="Gastrointestinal upset",
                    quality_concerns="Heavy metals",
                ),
                special_populations=SpecialPopulationsModel(
                    pregnancy_use="Avoid",
                    breastfeeding_use="Consult doctor",
                    pediatric_use="Consult doctor",
                )
            ))
        elif model_input.response_format == ClinicalOutput:
            return ModelOutput(data=ClinicalOutput(
                usage_and_administration=UsageAndAdministrationModel(
                    suitable_conditions="Stress",
                    preparation_methods="Tea",
                    age_specific_dosage=DosageModel(
                        children_dosage="N/A", adult_dosage="500mg", elderly_dosage="500mg"
                    ),
                    administration_guidance=AdministrationGuidanceModel(
                        tea_infusion="Steep 5 mins"
                    ),
                    storage_instruction="Cool dry place",
                    quality_indicators="Standardized extract",
                ),
                efficacy=EfficacyModel(
                    traditional_efficacy_claims="Strong",
                    clinical_evidence="Promising",
                    onset_of_action="2-4 weeks",
                    duration_of_effect="Hours",
                    expected_outcomes="Reduced stress",
                ),
                alternatives=AlternativesModel(
                    similar_herbs="Ginseng",
                    complementary_herbs="Rhodiola",
                    non_herbal_alternatives="Meditation",
                    when_to_seek_conventional_care="Severe anxiety",
                )
            ))
        elif model_input.response_format == EducatorOutput:
            return ModelOutput(data=EducatorOutput(
                education=HerbalEducationModel(
                    plain_language_explanation="Helps with stress",
                    key_takeaways="Adaptogen",
                    common_misconceptions="Instant results",
                    sustainability_notes="Eco-friendly",
                ),
                cost_and_availability=CostAndAvailabilityModel(
                    typical_cost_range="$15-30",
                    availability="OTC",
                    quality_considerations="Look for withanolide content",
                    organic_availability="Widely available",
                    sourcing_information="Ethical sources",
                )
            ))
        return ModelOutput(data=None)

    mock_lite_client.return_value.generate_text.side_effect = side_effect

    result = generator.generate_text("Ashwagandha", structured=True)
    assert result.data.metadata.common_name == "Ashwagandha"
    assert result.data.mechanism.mechanism_of_action == "HPA axis modulation"
    assert result.data.safety.common_side_effects == "Drowsiness"
    assert result.data.usage_and_administration.suitable_conditions == "Stress"
    assert result.data.education.key_takeaways == "Adaptogen"


def test_save_error():
    config = ModelConfig(model="test-model")
    generator = HerbalInfoGenerator(config)
    with pytest.raises(ValueError, match="No herb information available"):
        generator.save(ModelOutput(), Path("/tmp"))


@patch("medical.herbal_info.agentic.herbal_info.save_model_response")
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = HerbalInfoGenerator(config)
    mock_output = ModelOutput(markdown="Ashwagandha info")
    mock_lite_client.return_value.generate_text.return_value = mock_output

    generator.generate_text("Ashwagandha")
    generator.save(mock_output, Path("/tmp"))

    mock_save.assert_called_once()
    # Check if it was called with something like Path('/tmp/ashwagandha')
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("ashwagandha")

"""Herbal Information Generator CLI."""



# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


try:
    from .herbal_info import HerbalInfoGenerator
except (ImportError, ValueError):
    from medical.herbal_info.agentic.herbal_info import HerbalInfoGenerator

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate comprehensive herbal information."
    )
    parser.add_argument("herb", help="Herb name or file path containing names.")
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
        log_file="herbal_info.log", verbosity=args.verbosity, enable_console=True
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.herb)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.herb]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = HerbalInfoGenerator(model_config)

        for item in tqdm(items, desc="Generating"):
            result = generator.generate_text(herb=item, structured=args.structured)
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

"""
Specialized agents for herbal information generation.
"""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


try:
    from .herbal_info_models import (
        HerbalMetadataModel,
        HerbalClassificationModel,
        HerbalBackgroundModel,
        HerbalMechanismModel,
        HerbalEvidenceModel,
        HerbalResearchModel,
        UsageAndAdministrationModel,
        EfficacyModel,
        AlternativesModel,
        SafetyInformationModel,
        SpecialInstructionsModel,
        SpecialPopulationsModel,
        HerbalEducationModel,
        CostAndAvailabilityModel,
        ModelOutput,
    )
except (ImportError, ValueError):
    try:
        from herbal_info_models import (
            HerbalMetadataModel,
            HerbalClassificationModel,
            HerbalBackgroundModel,
            HerbalMechanismModel,
            HerbalEvidenceModel,
            HerbalResearchModel,
            UsageAndAdministrationModel,
            EfficacyModel,
            AlternativesModel,
            SafetyInformationModel,
            SpecialInstructionsModel,
            SpecialPopulationsModel,
            HerbalEducationModel,
            CostAndAvailabilityModel,
            ModelOutput,
        )
    except ImportError:
        from medical.herbal_info.agentic.herbal_info_models import (
            HerbalMetadataModel,
            HerbalClassificationModel,
            HerbalBackgroundModel,
            HerbalMechanismModel,
            HerbalEvidenceModel,
            HerbalResearchModel,
            UsageAndAdministrationModel,
            EfficacyModel,
            AlternativesModel,
            SafetyInformationModel,
            SpecialInstructionsModel,
            SpecialPopulationsModel,
            HerbalEducationModel,
            CostAndAvailabilityModel,
            ModelOutput,
        )

logger = logging.getLogger(__name__)

# Define output models for each agent
class BotanicalOutput(BaseModel):
    metadata: HerbalMetadataModel
    classification: HerbalClassificationModel
    background: HerbalBackgroundModel

class PharmacologicalOutput(BaseModel):
    mechanism: HerbalMechanismModel
    evidence: HerbalEvidenceModel
    research: HerbalResearchModel

class ClinicalOutput(BaseModel):
    usage_and_administration: UsageAndAdministrationModel
    efficacy: EfficacyModel
    alternatives: AlternativesModel

class SafetyOutput(BaseModel):
    safety: SafetyInformationModel
    special_instructions: SpecialInstructionsModel
    special_populations: SpecialPopulationsModel

class EducatorOutput(BaseModel):
    education: HerbalEducationModel
    cost_and_availability: CostAndAvailabilityModel

class BaseAgent:
    """Base class for specialized herbal agents."""
    
    def __init__(self, model_config: ModelConfig, client: LiteClient):
        self.model_config = model_config
        self.client = client
        self.agent_name = self.__class__.__name__

    def get_system_prompt(self) -> str:
        raise NotImplementedError

    def get_user_prompt(self, herb: str) -> str:
        raise NotImplementedError

    def get_response_format(self, structured: bool = False) -> Optional[Type[BaseModel]]:
        if structured:
            return self._get_response_format()
        return None

    def _get_response_format(self) -> Type[BaseModel]:
        raise NotImplementedError

    def generate(self, herb: str, structured: bool = False) -> ModelOutput:
        """Generates agent-specific herbal information."""
        logger.debug(f"{self.agent_name} starting for: {herb}")
        
        model_input = ModelInput(
            system_prompt=self.get_system_prompt(),
            user_prompt=self.get_user_prompt(herb),
            response_format=self.get_response_format(structured),
        )
        
        return self.client.generate_text(model_input=model_input)

class BotanicalAgent(BaseAgent):
    """Specializes in botanical classification and history."""
    
    def get_system_prompt(self) -> str:
        return """You are an expert Botanist and Ethnobotanist. 
Focus exclusively on botanical identification, classification, origin, and historical context of herbs.
Be precise with scientific names and plant families."""

    def get_user_prompt(self, herb: str) -> str:
        return f"Provide botanical metadata, classification, and background for: {herb}"

    def _get_response_format(self) -> Type[BaseModel]:
        return BotanicalOutput

class PharmacologicalAgent(BaseAgent):
    """Specializes in mechanisms and research."""
    
    def get_system_prompt(self) -> str:
        return """You are an expert Pharmacognosist and Clinical Researcher. 
Focus on chemical mechanisms of action, active constituents, and modern clinical evidence."""

    def get_user_prompt(self, herb: str) -> str:
        return f"Provide pharmacological mechanism, evidence-based data, and current research for: {herb}"

    def _get_response_format(self) -> Type[BaseModel]:
        return PharmacologicalOutput

class SafetyAgent(BaseAgent):
    """Specializes in safety and toxicology."""
    
    def get_system_prompt(self) -> str:
        return """You are a specialized Herbal Safety and Toxicology Expert. 
Focus strictly on contraindications, drug interactions, and safety considerations for special populations."""

    def get_user_prompt(self, herb: str) -> str:
        return f"Provide comprehensive safety information, special population guidance, and toxicology warnings for: {herb}"

    def _get_response_format(self) -> Type[BaseModel]:
        return SafetyOutput

class ClinicalAgent(BaseAgent):
    """Specializes in usage and efficacy."""
    
    def get_system_prompt(self) -> str:
        return """You are an experienced Clinical Herbalist. 
Focus on practical administration, dosage, clinical efficacy, and herbal/non-herbal alternatives."""

    def get_user_prompt(self, herb: str) -> str:
        return f"Provide clinical usage, administration guidance, efficacy outcomes, and alternatives for: {herb}"

    def _get_response_format(self) -> Type[BaseModel]:
        return ClinicalOutput

class EducatorAgent(BaseAgent):
    """Specializes in patient communication."""
    
    def get_system_prompt(self) -> str:
        return """You are a Health Educator and Consumer Advocate. 
Focus on explaining concepts in plain language, key takeaways, sustainability, and market availability."""

    def get_user_prompt(self, herb: str) -> str:
        return f"Provide patient education content, cost, and availability information for: {herb}"

    def _get_response_format(self) -> Type[BaseModel]:
        return EducatorOutput

