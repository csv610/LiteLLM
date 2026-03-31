import sys
from pathlib import Path
import argparse
from unittest.mock import MagicMock, patch

import pytest

# Add the project root to sys.path
try:
    from . import surgical_tool_info_cli
    from .surgical_tool_info_cli import (
        get_user_arguments,
        main,
    )
except (ImportError, ValueError):
    try:
        import surgical_tool_info_cli
        from surgical_tool_info_cli import (
            get_user_arguments,
            main,
        )
    except (ImportError, ValueError):
        # Add the project root to sys.path
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        
        from medical.surgical_tool_info.agentic.agentic import surgical_tool_info_cli
        from medical.surgical_tool_info.agentic.surgical_tool_info_cli import (
            get_user_arguments,
            main,
        )

def test_get_user_arguments():
    test_args = ["scalpel", "-d", "test_outputs", "-m", "test-model", "-v", "3", "-s", "-a"]
    with patch("sys.argv", ["surgical_tool_info_cli.py"] + test_args):
        args = get_user_arguments()
        assert args.tool == "scalpel"
        assert args.output_dir == "test_outputs"
        assert args.model == "test-model"
        assert args.verbosity == 3
        assert args.structured is True
        assert args.agentic is True


def test_main_with_args_single_tool():
    with patch.object(surgical_tool_info_cli, "SurgicalToolInfoGenerator") as mock_gen_class:
        with patch.object(surgical_tool_info_cli, "configure_logging"):
            mock_generator = mock_gen_class.return_value
            mock_result = MagicMock()
            mock_generator.generate_text.return_value = mock_result
        
            args = argparse.Namespace(
                tool="scalpel",
                output_dir="test_outputs",
                model="test-model",
                verbosity=2,
                structured=False,
                agentic=False,
            )
        
            with patch("pathlib.Path.mkdir"):
                with patch.object(surgical_tool_info_cli, "get_user_arguments", return_value=args):
                    result = main()
        
            assert result == 0
            mock_generator.generate_text.assert_called_once_with(
                tool="scalpel", structured=False
            )
            mock_generator.save.assert_called_once_with(mock_result, Path("test_outputs"))


def test_main_with_agentic_flag():
    with patch.object(surgical_tool_info_cli, "MultiAgentSurgicalToolInfoGenerator") as mock_multi_gen_class:
        with patch.object(surgical_tool_info_cli, "configure_logging"):
            mock_generator = mock_multi_gen_class.return_value
            mock_result = MagicMock()
            mock_generator.generate_text.return_value = mock_result
        
            args = argparse.Namespace(
                tool="scalpel",
                output_dir="test_outputs",
                model="test-model",
                verbosity=2,
                structured=True,
                agentic=True,
            )
        
            with patch("pathlib.Path.mkdir"):
                with patch.object(surgical_tool_info_cli, "get_user_arguments", return_value=args):
                    result = main()
        
            assert result == 0
            mock_generator.generate_text.assert_called_once_with(
                tool="scalpel", structured=True
            )
            mock_generator.save.assert_called_once_with(mock_result, Path("test_outputs"))


def test_main_with_args_file_input(tmp_path):
    with patch.object(surgical_tool_info_cli, "SurgicalToolInfoGenerator") as mock_gen_class:
        with patch.object(surgical_tool_info_cli, "configure_logging"):
            mock_generator = mock_gen_class.return_value
            mock_result = MagicMock()
            mock_generator.generate_text.return_value = mock_result
        
            tool_file = tmp_path / "tools.txt"
            tool_file.write_text("""scalpel\nforceps""")
        
            args = argparse.Namespace(
                tool=str(tool_file),
                output_dir=str(tmp_path / "outputs"),
                model="test-model",
                verbosity=2,
                structured=True,
                agentic=False,
            )
        
            with patch.object(surgical_tool_info_cli, "get_user_arguments", return_value=args):
                result = main()
        
            assert result == 0
            assert mock_generator.generate_text.call_count == 2
            mock_generator.generate_text.assert_any_call(tool="scalpel", structured=True)
            mock_generator.generate_text.assert_any_call(tool="forceps", structured=True)
