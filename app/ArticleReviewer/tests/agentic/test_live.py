import pytest
import os
import sys
import json
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).parent.parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from lite.config import ModelConfig  # noqa: E402
from ArticleReviewer.agentic.article_reviewer_agents import MultiAgentReviewer  # noqa: E402
from ArticleReviewer.agentic.article_reviewer_models import ArticleReviewModel  # noqa: E402

@pytest.mark.anyio
async def test_live_agentic():
    print("\nStarting live test for ArticleReviewer (agentic)...")
    model = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3:12b-cloud")
    model_config = ModelConfig(model=model, temperature=0.3)
    instance = MultiAgentReviewer(model_config)
    
    schema = ArticleReviewModel.model_json_schema()
    input_data = 'Test article content.'
    if isinstance(input_data, str):
        input_data += f"\n\nReturn ONLY JSON following this schema:\n{json.dumps(schema, indent=2)}"
    
    result = await instance.review(input_data)
    
    assert result is not None
    print("\nLive test for ArticleReviewer (agentic) completed successfully.")
