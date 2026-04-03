"""
liteagents.py - Unified for disease_info
"""
from app.MedKit.medical.disease_info.shared.models import *
from unittest.mock import patch
from lite.utils import save_model_response
from tqdm import tqdm
import logging
import pytest
from lite.lite_client import LiteClient
from pathlib import Path
import argparse
from lite.config import ModelConfig, ModelInput
import subprocess
from lite.logging_config import configure_logging
import sys
import shutil

"""Disease Information Generator CLI."""



# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


try:
    from .disease_info import DiseaseInfoGenerator
except (ImportError, ValueError):
    from medical.disease_info.agentic.disease_info import DiseaseInfoGenerator

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate comprehensive disease information."
    )
    parser.add_argument("disease", help="Disease name or file path containing names.")
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
        log_file="disease_info.log", verbosity=args.verbosity, enable_console=True
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.disease)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.disease]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = DiseaseInfoGenerator(model_config)

        for item in tqdm(items, desc="Generating"):
            result = generator.generate_text(disease=item, structured=args.structured)
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

#!/usr/bin/env python3
"""
Live test for Disease Information CLI.
This test runs the actual CLI app without mocking.
"""


# Paths
CUR_DIR = Path(__file__).parent
CLI_PATH = CUR_DIR / "disease_info_cli.py"
TEST_OUTPUT_DIR = CUR_DIR / "test_outputs"
DISEASE_UNSTRUCTURED = "flu"
DISEASE_STRUCTURED = "malaria"
EXPECTED_UNSTRUCTURED_FILE = TEST_OUTPUT_DIR / f"{DISEASE_UNSTRUCTURED}.md"
EXPECTED_STRUCTURED_FILE = TEST_OUTPUT_DIR / f"{DISEASE_STRUCTURED}.json"


def run_live_test():
    """Runs the live test by calling the CLI with real LLM."""
    print("--- Starting Live Test ---")

    # Cleanup previous test outputs
    if TEST_OUTPUT_DIR.exists():
        shutil.rmtree(TEST_OUTPUT_DIR)
    TEST_OUTPUT_DIR.mkdir(exist_ok=True)

    # --- Test Case 1: Unstructured Output ---
    print(f"
1. Testing Unstructured Output for: {DISEASE_UNSTRUCTURED}")
    cmd_u = [
        "python3",
        str(CLI_PATH),
        DISEASE_UNSTRUCTURED,
        "--output-dir",
        str(TEST_OUTPUT_DIR),
        "--verbosity",
        "2",
    ]

    try:
        subprocess.run(cmd_u, capture_output=True, text=True, check=True)
        if EXPECTED_UNSTRUCTURED_FILE.exists():
            print(f"✓ Success: Output file generated at {EXPECTED_UNSTRUCTURED_FILE}")
            content = EXPECTED_UNSTRUCTURED_FILE.read_text()
            if len(content) > 100:
                print(f"✓ Success: Content found ({len(content)} chars).")
            else:
                print("✗ Failure: Output file is too small.")
                return False
        else:
            print(f"✗ Failure: Output file {EXPECTED_UNSTRUCTURED_FILE} not created.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"✗ Failure: {e}")
        return False

    # --- Test Case 2: Structured Output ---
    print(f"
2. Testing Structured Output for: {DISEASE_STRUCTURED}")
    cmd_s = [
        "python3",
        str(CLI_PATH),
        DISEASE_STRUCTURED,
        "--output-dir",
        str(TEST_OUTPUT_DIR),
        "--structured",
        "--verbosity",
        "2",
    ]

    try:
        subprocess.run(cmd_s, capture_output=True, text=True, check=True)
        # Note: save_model_response should add .json extension if it's structured
        # Let's check what it actually produces.
        if EXPECTED_STRUCTURED_FILE.exists():
            print(f"✓ Success: Output file generated at {EXPECTED_STRUCTURED_FILE}")
            import json

            with open(EXPECTED_STRUCTURED_FILE) as f:
                data = json.load(f)
                if "identity" in data and "name" in data["identity"]:
                    print(
                        f"✓ Success: Found structured data for {data['identity']['name']}"
                    )
                else:
                    print("✗ Failure: JSON structure missing expected keys.")
                    return False
        else:
            print(f"✗ Failure: Output file {EXPECTED_STRUCTURED_FILE} not created.")
            print("Files in test_outputs:", list(TEST_OUTPUT_DIR.glob("*")))
            return False
    except subprocess.CalledProcessError as e:
        print(f"✗ Failure: {e}")
        return False

    print("
--- All Live Tests Completed Successfully ---")
    return True


if __name__ == "__main__":
    success = run_live_test()
    exit(0 if success else 1)


sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))



    DiagnosticCriteriaModel,
    DiseaseBackgroundModel,
    DiseaseClinicalPresentationModel,
    DiseaseDiagnosisModel,
    DiseaseEpidemiologyModel,
    DiseaseIdentityModel,
    DiseaseInfoModel,
    DiseaseLivingWithModel,
    DiseaseManagementModel,
    DiseaseResearchModel,
    DiseaseSpecialPopulationsModel,
    ModelOutput,
    RiskFactorsModel,
)


@pytest.fixture
def mock_lite_client():
    with patch("medical.disease_info.agentic.disease_info.LiteClient") as mock:
        yield mock


def test_disease_info_generator_init():
    config = ModelConfig(model="test-model")
    generator = DiseaseInfoGenerator(config)
    assert generator.model_config == config
    assert generator.client is not None


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = DiseaseInfoGenerator(config)
    mock_output = ModelOutput(
        markdown="Disease information in markdown", data_available=True
    )
    mock_lite_client.return_value.generate_text.return_value = mock_output
    result = generator.generate_text("Diabetes")
    assert result.markdown == "Disease information in markdown"


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = DiseaseInfoGenerator(config)

    mock_data = DiseaseInfoModel(
        identity=DiseaseIdentityModel(
            name="Diabetes",
            disease_name="Diabetes",
            icd_10_code="E11",
            icd10_code="E11",
            icd11_code="5A11",
            synonyms=[],
        ),
        background=DiseaseBackgroundModel(
            definition="Chronic", pathophysiology="Insulin", etiology="Multiple factors"
        ),
        epidemiology=DiseaseEpidemiologyModel(
            prevalence="High",
            incidence="Rising",
            risk_factors=RiskFactorsModel(
                lifestyle=[],
                genetic=[],
                environmental=[],
                modifiable=[],
                non_modifiable=[],
            ),
        ),
        clinical_presentation=DiseaseClinicalPresentationModel(
            symptoms=[], complications=[], signs=[], natural_history="Progressive"
        ),
        diagnosis=DiseaseDiagnosisModel(
            criteria=[],
            tests=[],
            diagnostic_criteria=DiagnosticCriteriaModel(
                primary=[],
                secondary=[],
                exclusion=[],
                symptoms=[],
                physical_exam=[],
                laboratory_tests=[],
                imaging_studies=[],
            ),
            differential_diagnosis=[],
        ),
        management=DiseaseManagementModel(
            treatments=[],
            medications=[],
            lifestyle=[],
            treatment_options=[],
            prevention=[],
            prognosis="Variable",
        ),
        research=DiseaseResearchModel(
            current_research="None",
            recent_advancements="None",
            future_outlooks=[],
            current_trends=[],
        ),
        special_populations=DiseaseSpecialPopulationsModel(
            pediatric="None", geriatric="None", pregnancy="None"
        ),
        living_with=DiseaseLivingWithModel(
            quality_of_life="None", support_resources=[]
        ),
        summary="A chronic disease",
    )
    mock_output = ModelOutput(data=mock_data, data_available=True)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Diabetes", structured=True)
    assert result.data.identity.name == "Diabetes"

#!/usr/bin/env python3
"""
Disease Information module.

This module provides the core DiseaseInfoGenerator class for generating
comprehensive disease information based on provided configuration.
"""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


try:
    from .disease_info_models import DiseaseInfoModel, ModelOutput
    from .disease_info_prompts import PromptBuilder
except (ImportError, ValueError):
    from medical.disease_info.agentic.disease_info_models import DiseaseInfoModel, ModelOutput
    from medical.disease_info.agentic.disease_info_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class DiseaseInfoGenerator:
    """Generates comprehensive disease information."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.disease = None  # Store the disease being analyzed
        logger.debug("Initialized DiseaseInfoGenerator")

    def generate_text(self, disease: str, structured: bool = False) -> ModelOutput:
        """Generate 3-tier comprehensive disease information."""
        if not disease or not str(disease).strip():
            raise ValueError("Disease name cannot be empty")

        self.disease = disease
        logger.info(f"Starting 3-tier disease information generation for: {disease}")

        try:
            # 1. Specialist Stage (JSON)
            logger.debug(f"[Specialist] Generating content for: {disease}")
            system_prompt = PromptBuilder.create_system_prompt()
            user_prompt = PromptBuilder.create_user_prompt(disease)
            
            spec_input = ModelInput(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_format=DiseaseInfoModel if structured else None,
            )
            spec_res = self.ask_llm(spec_input)
            
            if structured:
                spec_json = spec_res.data.model_dump_json(indent=2)
            else:
                spec_json = spec_res.markdown

            # 2. Auditor Stage (JSON Audit)
            logger.debug(f"[Auditor] Auditing content for: {disease}")
            audit_sys, audit_usr = PromptBuilder.get_disease_auditor_prompts(disease, spec_json)
            audit_input = ModelInput(
                system_prompt=audit_sys,
                user_prompt=audit_usr,
                response_format=None # Audit result
            )
            audit_res = self.ask_llm(audit_input)
            audit_json = audit_res.markdown

            # 3. Final Synthesis Stage (Markdown Closer)
            logger.debug(f"[Output] Synthesizing final report for: {disease}")
            out_sys, out_usr = PromptBuilder.get_output_synthesis_prompts(disease, spec_json, audit_json)
            out_input = ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None,
            )
            final_res = self.ask_llm(out_input)

            logger.info("✓ Successfully generated 3-tier disease information")
            return ModelOutput(
                data=spec_res.data if structured else None, 
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier disease generation failed: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the disease information to a file."""
        if self.disease is None:
            raise ValueError(
                "No disease information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.disease.lower().replace(' ', '_')}"

        return save_model_response(result, output_dir / base_filename)