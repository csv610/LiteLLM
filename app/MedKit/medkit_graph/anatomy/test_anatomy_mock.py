import pytest
from anatomy_models import AnatomyKnowledgeGraph, Triple


def test_triple_validation():
    """Test Triple model validation and normalization."""
    t = Triple(
        source="heart ",
        relation="is_part_of",
        target=" Circulatory system",
    )
    assert t.source == "heart"
    assert t.relation == "part_of"
    assert t.target == "Circulatory system"


def test_graph_builder():
    """Test adding triples and querying the graph."""
    builder = AnatomyKnowledgeGraph()
    triples = [
        Triple(
            source="Heart",
            relation="part_of",
            target="Circulatory System",
        ),
        Triple(
            source="Heart",
            relation="adjacent_to",
            target="Lungs",
        ),
    ]
    builder.add_triples(triples)

    assert "Heart" in builder.G.nodes
    assert "Lungs" in builder.G.nodes
    assert builder.query_part_of("Heart") == ["Circulatory System"]
    assert builder.query_connections("Heart") == ["Lungs"]


def test_build_from_name():
    """Test building graph directly from anatomy name (simulation)."""
    builder = AnatomyKnowledgeGraph()
    # Simulation should work for "Heart"
    triples = builder.build_from_name("Heart")
    assert len(triples) > 0
    assert "Heart" in builder.G.nodes
    assert any(t.source == "Heart" for t in triples)
    assert any(t.relation == "part_of" for t in triples)
    assert any(
        t.target in ["Circulatory System", "Cardiovascular System"] for t in triples
    )


if __name__ == "__main__":
    pytest.main([__file__])
