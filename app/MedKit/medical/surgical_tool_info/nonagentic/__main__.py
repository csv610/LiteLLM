"""Main entry point for surgical tool info package."""

import sys

try:
    from .surgical_tool_info_cli import main
except (ImportError, ValueError):
    from surgical_tool_info_cli import main

if __name__ == "__main__":
    sys.exit(main())
