import os
from typing import Optional
import sys

# Add project root directory to path to import lite module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from lite.config import ModelConfig
from .nobel_prize_models import PrizeWinner
from .nobel_prize_explorer import NobelPrizeWinnerInfo

DEFAULT_MODEL = "gemini/gemini-2.5-flash"


def fetch_nobel_winners(
    category: str,
    year: str,
    model: Optional[str] = None
) -> list[PrizeWinner]:
    """
    Fetch Nobel Prize winners for a specific field and year using a two-agent workflow.

    Args:
        category: Nobel Prize category (Physics, Chemistry, Medicine, Literature, Peace, Economics)
        year: Year of the prize
        model: LLM model to use for both generation and validation

    Returns:
        List of PrizeWinner instances

    Raises:
        ValueError: If API response is invalid or model response doesn't match schema
        RuntimeError: If API call fails or required credentials are missing
    """
    resolved_model = model or os.getenv("NOBEL_PRIZE_MODEL", DEFAULT_MODEL)
    model_config = ModelConfig(model=resolved_model, temperature=0.2)
    explorer = NobelPrizeWinnerInfo(model_config)
    return explorer.fetch_winners(category, year, resolved_model)
