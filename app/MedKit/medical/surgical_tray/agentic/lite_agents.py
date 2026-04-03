"""
liteagents.py - Unified for surgical_tray
"""
from unittest.mock import patch
from lite.utils import save_model_response
from app.MedKit.medical.surgical_tray.shared.models import *
from tqdm import tqdm
import pytest
import logging
from lite.lite_client import LiteClient
from pathlib import Path
import argparse
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
import sys


# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))



    ModelOutput,
    SurgicalTrayModel,
    TrayInstrument,
)


@pytest.fixture
def mock_lite_client():
    with patch("medical.surgical_tray.agentic.surgical_tray_info.LiteClient") as mock:
        yield mock


def test_generator_init():
    config = ModelConfig(model="test-model")
    generator = SurgicalTrayGenerator(config)
    assert generator.model_config == config


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SurgicalTrayGenerator(config)
    mock_output = ModelOutput(markdown="Tray info", tray_data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Appendectomy")
    assert result.markdown == "Tray info"
    assert generator.target == "Appendectomy"


def test_generate_text_empty():
    config = ModelConfig(model="test-model")
    generator = SurgicalTrayGenerator(config)
    with pytest.raises(ValueError, match="Surgery name cannot be empty"):
        generator.generate_text("")


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SurgicalTrayGenerator(config)

    mock_data = SurgicalTrayModel(
        surgery_name="Appendectomy",
        specialty="General Surgery",
        instruments=[
            TrayInstrument(
                name="Scalpel", quantity=1, category="Cutting", reason="Incision"
            )
        ],
        sterilization_method="Autoclave",
        setup_instructions="Open tray on sterile field",
    )

    mock_output = ModelOutput(tray_data=mock_data, markdown=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Appendectomy", structured=True)
    assert result.tray_data.surgery_name == "Appendectomy"


@patch("medical.surgical_tray.agentic.surgical_tray_info.save_model_response")
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SurgicalTrayGenerator(config)
    mock_output = ModelOutput(markdown="Info")
    mock_lite_client.return_value.generate_text.return_value = mock_output

    generator.generate_text("Appendectomy")
    generator.save(mock_output, Path("/tmp"))

    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("appendectomy")

"""Surgical Tray Setup Information Generator CLI."""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))




try:
    try:
        from .surgical_tray_info import SurgicalTrayGenerator
    except (ImportError, ValueError):
        from medical.surgical_tray.agentic.surgical_tray_info import SurgicalTrayGenerator
except (ImportError, ValueError):
    from surgical_tray_info import SurgicalTrayGenerator

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate comprehensive surgical tray information."
    )
    parser.add_argument("surgery", help="Surgery name or file path containing names.")
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
        log_file="surgical_tray_info.log", verbosity=args.verbosity, enable_console=True
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.surgery)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.surgery]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = SurgicalTrayGenerator(model_config)

        for item in tqdm(items, desc="Generating"):
            result = generator.generate_text(surgery=item, structured=args.structured)
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



try:
    from .surgical_tray_info_models import ModelOutput, SurgicalTrayModel
    from .surgical_tray_info_prompts import PromptBuilder
except (ImportError, ValueError):
    from surgical_tray_info_models import ModelOutput, SurgicalTrayModel
    from surgical_tray_info_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class SurgicalTrayGenerator:
    """Generates comprehensive surgical tray information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.target = None
        logger.debug("Initialized SurgicalTrayGenerator")

    def generate_text(self, surgery: str, structured: bool = False) -> ModelOutput:
        """Generates surgical tray information using a 3-tier agent system."""
        if not surgery or not str(surgery).strip():
            raise ValueError("Surgery name cannot be empty")

        self.target = surgery
        logger.info(f"Starting 3-tier surgical tray generation for: {surgery}")

        try:
            # 1. Specialist Stage (JSON)
            logger.debug("[Specialist] Generating tray list...")
            spec_input = ModelInput(
                system_prompt=PromptBuilder.create_system_prompt(),
                user_prompt=PromptBuilder.create_user_prompt(surgery),
                response_format=SurgicalTrayModel if structured else None,
            )
            spec_res = self.client.generate_text(model_input=spec_input)
            
            if structured:
                spec_json = spec_res.data.model_dump_json(indent=2)
            else:
                spec_json = spec_res.markdown

            # 2. Auditor Stage (JSON Audit)
            logger.debug("[Auditor] Auditing tray accuracy...")
            audit_sys, audit_usr = PromptBuilder.create_tray_auditor_prompts(surgery, spec_json)
            audit_input = ModelInput(
                system_prompt=audit_sys,
                user_prompt=audit_usr,
                response_format=None # Audit result
            )
            audit_res = self.client.generate_text(model_input=audit_input)
            audit_json = audit_res.markdown

            # 3. Final Synthesis Stage (Markdown Closer)
            logger.debug("[Output] Synthesizing final tray report...")
            out_sys, out_usr = PromptBuilder.create_output_synthesis_prompts(surgery, spec_json, audit_json)
            out_input = ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None,
            )
            final_res = self.client.generate_text(model_input=out_input)

            logger.info("✓ Successfully generated 3-tier surgical tray information")
            return ModelOutput(
                data=spec_res.data, 
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier Surgical Tray generation failed: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        if self.target is None:
            raise ValueError("No information available. Call generate_text first.")
        base_filename = f"{self.target.lower().replace(' ', '_')}"
        return save_model_response(result, output_dir / base_filename)