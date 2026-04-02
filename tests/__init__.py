"""Tests for LiteLLM Tools."""

import importlib
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
app_root = project_root / "app"
if str(app_root) not in sys.path:
    sys.path.insert(0, str(app_root))

sys.modules.setdefault(
    "tests.test_periodic_table_mock",
    importlib.import_module("app.PeriodicTable.tests.test_periodic_table_mock"),
)
