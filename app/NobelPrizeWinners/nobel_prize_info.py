import argparse
import logging
import json
import sys
import os
from pathlib import Path
from typing import Optional

# Add project root directory to path to import lite module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from lite.config import ModelConfig
# from lite import logging_config
from nobel_prize_models import PrizeWinner
from nobel_prize_explorer import NobelPrizeWinnerInfo

# logger = logging_config.setup_logging(str(Path(__file__).parent / "logs" / "nobel_prize_info.log"))

# Setup standard logging
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=str(log_dir / "nobel_prize_info.log")
)
logger = logging.getLogger(__name__)

# ==============================================================================
# Core Functions
# ==============================================================================

def fetch_nobel_winners(
    category: str,
    year: str,
    model: Optional[str] = None
) -> list[PrizeWinner]:
    """
    Fetch Nobel Prize winners for a specific field and year.

    Args:
        category: Nobel Prize category (Physics, Chemistry, Medicine, Literature, Peace, Economics)
        year: Year of the prize
        model: LLM model to use (defaults to environment variable or gemini/gemini-2.5-flash)

    Returns:
        List of PrizeWinner instances

    Raises:
        ValueError: If API response is invalid or model response doesn't match schema
        RuntimeError: If API call fails or required credentials are missing
    """
    if model is None:
        model = os.getenv("NOBEL_PRIZE_MODEL", "gemini/gemini-2.5-flash")

    # Create ModelConfig and NobelPrizeWinnerInfo
    model_config = ModelConfig(model=model, temperature=0.2)
    explorer = NobelPrizeWinnerInfo(model_config)

    # Fetch winners using the explorer
    return explorer.fetch_winners(category, year, model)
