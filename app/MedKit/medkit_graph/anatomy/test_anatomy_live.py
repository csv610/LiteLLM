import pytest
import networkx as nx
from anatomy_models import AnatomyKnowledgeGraph

try:
    from lite import LiteClient
except ImportError:
    LiteClient = None

@pytest.mark.skipif(LiteClient is None, reason="lite package is not installed; cannot run live test.")
def test_live_build_from_name():
    """Live test that calls the LLM to generate anatomical triples."""
    from lite.config import ModelConfig
    # Ensure we use a live model
    config = ModelConfig(model="ollama/gemma3:27b-cloud")
    builder = AnatomyKnowledgeGraph(model_config=config)

    anatomy_name = "Liver"

    triples = builder.build_from_name(anatomy_name)
    
    # Basic assertions to ensure we got a valid response
    assert len(triples) > 0, "No triples generated from live model."
    
    # The source anatomy should be present in the generated nodes
    nodes_lower = [str(n).lower() for n in builder.G.nodes]
    assert any(anatomy_name.lower() in n for n in nodes_lower), f"Expected '{anatomy_name}' to be present in graph nodes."
    
    # Verify that relations are valid (they should have been validated by the Pydantic model)
    for triple in triples:
        assert triple.relation is not None
        assert triple.source is not None
        assert triple.target is not None

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
