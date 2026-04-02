"""
liteagents.py - Unified for med_speciality
"""
from typing import Union\nfrom lite.utils import save_model_response\nfrom lite.lite_client import LiteClient\nimport logging\nimport pytest\nimport sys\nfrom pathlib import Path\nfrom .medical_speciality_models import CategoryList, MedicalSpecialistDatabase\nimport argparse\nfrom lite.config import ModelConfig\nfrom unittest.mock import patch, MagicMock\nfrom lite.config import ModelConfig, ModelInput\nfrom lite.logging_config import configure_logging\nfrom .medical_speciality_prompts import PromptBuilder\nfrom app.MedKit.medical.med_speciality.shared.models import *\n\n#!/usr/bin/env python3
"""
Medical Speciality Analysis module.

This module provides the core MedicalSpecialityGenerator class for generating
a comprehensive database of medical specialities using LiteClient.
"""




logger = logging.getLogger(__name__)


class MedicalSpecialityGenerator:
    """Generate a comprehensive database of medical specialities using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        logger.debug("Initialized MedicalSpecialityGenerator")

    def generate_text(
        self, structured: bool = False
    ) -> Union[MedicalSpecialistDatabase, str]:
        """Generate a comprehensive medical specialists database using a 3-tier system."""
        logger.debug("Starting 3-tier medical speciality database generation")

        try:
            # --- Tier 1: Specialist Stages (JSON) ---
            logger.info("Agent 1 (Planner): Identifying major specialty categories")
            planner_input = ModelInput(
                system_prompt=PromptBuilder.create_planner_system_prompt(),
                user_prompt=PromptBuilder.create_planner_user_prompt(),
                response_format=CategoryList if structured else None,
            )
            categories_result = self.ask_llm(planner_input)
            
            categories = []
            if structured:
                categories = categories_result.data.categories
            else:
                raw_lines = str(categories_result.markdown).split('\n')
                for line in raw_lines:
                    cleaned = line.strip().strip('-* ')
                    if cleaned and len(cleaned) < 100:
                        categories.append(cleaned)
                if not categories:
                    categories = ["Internal Medicine", "Surgery", "Pediatrics", "Diagnostic", "Psychiatry"]

            all_specialists = []
            for category in categories:
                logger.info(f"Agent 2 (Researcher): Investigating category '{category}'")
                researcher_input = ModelInput(
                    system_prompt=PromptBuilder.create_researcher_system_prompt(),
                    user_prompt=PromptBuilder.create_researcher_user_prompt(category),
                    response_format=MedicalSpecialistDatabase if structured else None,
                )
                res_result = self.ask_llm(researcher_input)
                if structured:
                    all_specialists.extend(res_result.data.specialists)
                else:
                    all_specialists.append(f"Category: {category}\n{res_result.markdown}")

            specialist_data_json = ""
            if structured:
                spec_db = MedicalSpecialistDatabase(specialists=all_specialists)
                specialist_data_json = spec_db.model_dump_json(indent=2)
            else:
                specialist_data_json = "\n\n".join(all_specialists)

            # --- Tier 2: Compliance Auditor Stage (JSON Audit) ---
            logger.info("Agent 3 (Auditor): Auditing specialty data")
            reviewer_input = ModelInput(
                system_prompt=PromptBuilder.create_reviewer_system_prompt(),
                user_prompt=PromptBuilder.create_reviewer_user_prompt(specialist_data_json),
                response_format=None # Audit result
            )
            audit_result = self.ask_llm(reviewer_input)
            audit_json = audit_result.markdown

            # --- Tier 3: Final Output Synthesis (Markdown Closer) ---
            logger.info("Agent 4 (Output): Synthesizing final database")
            out_sys, out_usr = PromptBuilder.create_output_synthesis_prompts(
                specialist_data_json, audit_json
            )
            output_input = ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None,
            )
            final_res = self.ask_llm(output_input)

            logger.info("✓ Successfully generated 3-tier medical specialty database")
            return ModelOutput(
                data=MedicalSpecialistDatabase(specialists=all_specialists) if structured else None,
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ Error in 3-tier generation workflow: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> Union[MedicalSpecialistDatabase, str]:
        """Internal helper to call the LLM client."""
        return self.client.generate_text(model_input=model_input)

    def save(
        self, result: Union[MedicalSpecialistDatabase, str], output_dir: Path
    ) -> Path:
        """Saves the medical speciality database information to a file."""
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = "medical_specialities_database"

        return save_model_response(result, output_dir / base_filename)


# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))



    CategoryList,
    MedicalSpecialist,
    MedicalSpecialistDatabase,
    SpecialtyCategory,
)


@pytest.fixture
def mock_lite_client():
    with patch("medical.med_speciality.agentic.medical_speciality.LiteClient") as mock:
        yield mock


def test_generator_init():
    config = ModelConfig(model="test-model")
    generator = MedicalSpecialityGenerator(config)
    assert generator.model_config == config


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalSpecialityGenerator(config)
    
    mock_lite_client.return_value.generate_text.side_effect = [
        "Cardiology\nNeurology",
        "Cardiologist details...",
        "Neurologist details...",
        "Specialists list"
    ]

    result = generator.generate_text()
    assert result == "Specialists list"
    assert mock_lite_client.return_value.generate_text.call_count == 4


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalSpecialityGenerator(config)

    cat = SpecialtyCategory(name="Cardiovascular", description="Heart and vessels")
    
    mock_categories = CategoryList(categories=["Cardiovascular"])
    
    mock_data = MedicalSpecialistDatabase(
        specialists=[
            MedicalSpecialist(
                specialty_name="Cardiologist",
                category=cat,
                description="Heart doctor",
                treats=["Heart failure", "Arrhythmia"],
                common_referral_reasons=["Chest pain"],
                is_surgical=False,
            ),
            MedicalSpecialist(
                specialty_name="Cardiac Surgeon",
                category=cat,
                description="Heart surgeon",
                treats=["Valve disease"],
                common_referral_reasons=["Surgery needed"],
                is_surgical=True,
            ),
        ]
    )

    mock_lite_client.return_value.generate_text.side_effect = [
        mock_categories,
        mock_data
    ]

    result = generator.generate_text(structured=True)
    assert len(result.specialists) == 2
    assert len(result.get_surgical_specialists()) == 1
    assert result.get_by_category("Cardiovascular")[0].specialty_name == "Cardiologist"
    assert mock_lite_client.return_value.generate_text.call_count == 2


@patch("medical.med_speciality.agentic.medical_speciality.save_model_response")
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalSpecialityGenerator(config)
    
    mock_lite_client.return_value.generate_text.side_effect = [
        "Cardiology\nNeurology",
        "Cardiologist details...",
        "Neurologist details...",
        "Specialists list"
    ]

    result = generator.generate_text()
    generator.save(result, Path("/tmp"))

    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == "Specialists list"
    assert str(args[1]).endswith("medical_specialities_database")

"""Medical Specialist Database Generator CLI."""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))




try:
    from .medical_speciality import MedicalSpecialityGenerator
except (ImportError, ValueError):
    from medical.med_speciality.agentic.medical_speciality import MedicalSpecialityGenerator

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate comprehensive medical specialist database."
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
        log_file="medical_speciality.log", verbosity=args.verbosity, enable_console=True
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.3)
        generator = MedicalSpecialityGenerator(model_config)

        logger.info("Generating medical speciality database...")
        result = generator.generate_text(structured=args.structured)
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

