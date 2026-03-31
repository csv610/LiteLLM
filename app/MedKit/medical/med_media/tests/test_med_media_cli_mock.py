import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import MagicMock, patch

from medical.med_media.agentic.med_media_cli import main


@patch("medical.med_media.agentic.med_media_cli.argparse.ArgumentParser.parse_args")
@patch("medical.med_media.agentic.med_media_cli.MedicalMediaGenerator")
@patch("medical.med_media.agentic.med_media_cli.configure_logging")
@patch("medical.med_media.agentic.med_media_cli.Path.mkdir")
def test_cli_images(mock_mkdir, mock_logging, mock_generator, mock_parse_args):
    # Setup mock arguments
    args = MagicMock()
    args.command = "images"
    args.query = "heart anatomy"
    args.num = 3
    args.size = "Medium"
    args.model = "test-model"
    args.output_dir = "outputs/media"
    args.verbosity = 2
    args.structured = False
    mock_parse_args.return_value = args

    # Setup mock generator
    generator_instance = mock_generator.return_value
    generator_instance.download_images.return_value = ["path/1.jpg"]

    with patch("builtins.print") as mock_print:
        main()

    generator_instance.download_images.assert_called_once()
    mock_print.assert_any_call("✓ Saved: path/1.jpg")


@patch("medical.med_media.agentic.med_media_cli.argparse.ArgumentParser.parse_args")
@patch("medical.med_media.agentic.med_media_cli.MedicalMediaGenerator")
@patch("medical.med_media.agentic.med_media_cli.configure_logging")
@patch("medical.med_media.agentic.med_media_cli.Path.mkdir")
def test_cli_videos(mock_mkdir, mock_logging, mock_generator, mock_parse_args):
    args = MagicMock()
    args.command = "videos"
    args.query = "surgery"
    args.num = 5
    args.model = "test-model"
    args.output_dir = "outputs/media"
    args.verbosity = 2
    mock_parse_args.return_value = args

    generator_instance = mock_generator.return_value
    generator_instance.search_videos.return_value = [
        {"title": "Video 1", "duration": "10:00", "url": "http://v1"}
    ]

    with patch("builtins.print") as mock_print:
        main()

    generator_instance.search_videos.assert_called_once_with("surgery", 5)
    mock_print.assert_any_call("- Video 1 (10:00): http://v1")


@patch("medical.med_media.agentic.med_media_cli.argparse.ArgumentParser.parse_args")
@patch("medical.med_media.agentic.med_media_cli.MedicalMediaGenerator")
@patch("medical.med_media.agentic.med_media_cli.configure_logging")
@patch("medical.med_media.agentic.med_media_cli.Path.mkdir")
def test_cli_caption(mock_mkdir, mock_logging, mock_generator, mock_parse_args):
    args = MagicMock()
    args.command = "caption"
    args.topic = "X-ray"
    args.type = "x-ray"
    args.model = "test-model"
    args.output_dir = "outputs/media"
    args.verbosity = 2
    args.structured = True
    mock_parse_args.return_value = args

    generator_instance = mock_generator.return_value
    generator_instance.generate_caption.return_value = "Result"
    generator_instance.save.return_value = "saved_path"

    with patch("builtins.print"):
        main()

    generator_instance.generate_caption.assert_called_once_with(
        "X-ray", "x-ray", structured=True
    )
    generator_instance.save.assert_called_once()


@patch("medical.med_media.agentic.med_media_cli.argparse.ArgumentParser.parse_args")
@patch("medical.med_media.agentic.med_media_cli.MedicalMediaGenerator")
@patch("medical.med_media.agentic.med_media_cli.configure_logging")
@patch("medical.med_media.agentic.med_media_cli.Path.mkdir")
def test_cli_summary(mock_mkdir, mock_logging, mock_generator, mock_parse_args):
    args = MagicMock()
    args.command = "summary"
    args.topic = "Diabetes"
    args.type = "video"
    args.model = "test-model"
    args.output_dir = "outputs/media"
    args.verbosity = 2
    args.structured = False
    mock_parse_args.return_value = args

    generator_instance = mock_generator.return_value
    generator_instance.generate_summary.return_value = "Result"
    generator_instance.save.return_value = "saved_path"

    with patch("builtins.print"):
        main()

    generator_instance.generate_summary.assert_called_once_with(
        "Diabetes", "video", structured=False
    )
    generator_instance.save.assert_called_once()
