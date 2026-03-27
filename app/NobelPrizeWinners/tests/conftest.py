import sys
from pathlib import Path


AGENTIC_DIR = Path(__file__).resolve().parent.parent / "agentic"

if str(AGENTIC_DIR) not in sys.path:
    sys.path.insert(0, str(AGENTIC_DIR))
