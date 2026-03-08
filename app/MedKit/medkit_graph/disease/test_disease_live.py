import pytest
from disease_models import DiseaseKnowledgeGraphBuilder, LiteClient


@pytest.mark.skipif(
    LiteClient is None, reason="lite package is not installed; cannot run live test."
)
def test_live_build_from_name():
    """Live test that calls the LLM to generate disease triples."""
    from lite.config import ModelConfig

    # Use the requested model
    config = ModelConfig(model="ollama/gemma3")
    builder = DiseaseKnowledgeGraphBuilder(model_config=config)

    disease_name = "Malaria"

    triples = builder.build_from_name(disease_name)

    # Basic assertions to ensure we got a valid response
    assert len(triples) > 0, "No triples generated from live model."

    # The source disease should be present in the generated nodes
    nodes_lower = [str(n).lower() for n in builder.nodes.keys()]
    assert any(disease_name.lower() in n for n in nodes_lower), (
        f"Expected '{disease_name}' to be present in graph nodes."
    )

    # Verify that relations are valid (Pydantic already validates, but let's double check basic structure)
    for triple in triples:
        assert triple.relation is not None
        assert triple.source is not None
        assert triple.target is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
