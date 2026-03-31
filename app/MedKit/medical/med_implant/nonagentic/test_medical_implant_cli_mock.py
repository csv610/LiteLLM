import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import MagicMock, patch

import pytest

from medical.med_implant.agentic.medical_implant_cli import get_user_arguments, main


def test_get_user_arguments():
    # Test valid arguments
    with patch.object(
        sys, "argv", ["medical_implant_cli.py", "-i", "Pacemaker", "-m", "test-model"]
    ):
        args = get_user_arguments()
        assert args.implant == "Pacemaker"
        assert args.model == "test-model"
        assert args.output_dir == "outputs"
        assert not args.structured


def test_get_user_arguments_required():
    # Test missing required argument
    with patch.object(sys, "argv", ["medical_implant_cli.py"]):
        with pytest.raises(SystemExit):
            get_user_arguments()


@patch("medical.med_implant.agentic.medical_implant_cli.MedicalImplantGenerator")
@patch("medical.med_implant.agentic.medical_implant_cli.configure_logging")
@patch("medical.med_implant.agentic.medical_implant_cli.Path.mkdir")
def test_main_success(mock_mkdir, mock_configure_logging, mock_generator_class):
    # Setup mocks
    mock_generator = mock_generator_class.return_value
    mock_generator.generate_text.return_value = MagicMock()

    with patch.object(sys, "argv", ["medical_implant_cli.py", "-i", "Pacemaker"]):
        exit_code = main()
        assert exit_code == 0
        mock_generator.generate_text.assert_called_once_with(
            implant="Pacemaker", structured=False
        )
        mock_generator.save.assert_called_once()


@patch("medical.med_implant.agentic.medical_implant_cli.MedicalImplantGenerator")
@patch("medical.med_implant.agentic.medical_implant_cli.configure_logging")
def test_main_failure(mock_configure_logging, mock_generator_class):
    # Setup mocks
    mock_generator = mock_generator_class.return_value
    mock_generator.generate_text.side_effect = Exception("Generation failed")

    with patch.object(sys, "argv", ["medical_implant_cli.py", "-i", "Pacemaker"]):
        exit_code = main()
        assert exit_code == 1
