import pytest
import os
import networkx as nx
from anatomy_models import AnatomyTripletExtractor, AnatomyGraphBuilder, Triple

def test_triple_validation():
    """Test Triple model validation and normalization."""
    t = Triple(
        source="heart ",
        relation="is_part_of",
        target=" Circulatory system",
        source_type="organ",
        target_type="system"
    )
    assert t.source == "heart"
    assert t.relation == "part_of"
    assert t.target == "Circulatory system"
    assert t.source_type == "Organ"
    assert t.target_type == "BodySystem"

def test_graph_builder():
    """Test adding triples and querying the graph."""
    builder = AnatomyGraphBuilder()
    triples = [
        Triple(source="Heart", relation="part_of", target="Circulatory System", source_type="Organ", target_type="BodySystem"),
        Triple(source="Heart", relation="adjacent_to", target="Lungs", source_type="Organ", target_type="Organ")
    ]
    builder.add_triples(triples)
    
    assert "Heart" in builder.G.nodes
    assert "Lungs" in builder.G.nodes
    assert builder.query_part_of("Heart") == ["Circulatory System"]
    assert builder.query_connections("Heart") == ["Lungs"]

def test_export_dot(tmp_path):
    """Test DOT export functionality."""
    # Mocking os.makedirs and open is also possible, but tmp_path is cleaner
    # However, export_dot is hardcoded to use "outputs" directory.
    # We'll just verify it creates the file.
    builder = AnatomyGraphBuilder()
    builder.add_triples([Triple(source="A", relation="part_of", target="B")])
    
    # Ensure outputs directory exists (it should after running export_dot)
    builder.export_dot("test_anatomy")
    assert os.path.exists("outputs/test_anatomy.dot")
    
    with open("outputs/test_anatomy.dot", "r") as f:
        content = f.read()
        assert "digraph G {" in content
        assert '"A" -> "B" [label="part_of"];' in content

def test_extractor_simulation():
    """Test extractor in simulation mode."""
    extractor = AnatomyTripletExtractor(model_name="test-model")
    # Force simulation by ensuring client is None if 'lite' is missing
    # or just trust the _simulate logic for "heart"
    triples = extractor.extract("The heart is an organ.")
    assert len(triples) > 0
    assert any(t.source == "Heart" for t in triples)
    assert any(t.relation == "common_disease" for t in triples)

if __name__ == "__main__":
    pytest.main([__file__])
