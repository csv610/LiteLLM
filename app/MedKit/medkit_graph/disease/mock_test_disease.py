import json

import pytest
from disease_models import DiseaseKnowledgeGraphBuilder, Triple


def test_triple_normalization():
    # Test relation normalization
    t1 = Triple(source="Malaria", relation="symptom", target="Fever")
    assert t1.relation == "has_symptom"

    t2 = Triple(source="Malaria", relation="treated by", target="ACT")
    assert t2.relation == "treated_with"

    t3 = Triple(source="Obesity", relation="risk factor", target="Diabetes")
    assert t3.relation == "risk_factor_for"

    # Test node type normalization
    t4 = Triple(
        source="Malaria",
        relation="has_symptom",
        target="Fever",
        source_type="disease",
        target_type="sign",
    )
    assert t4.source_type == "Disease"
    assert t4.target_type == "Symptom"


def test_graph_builder():
    builder = DiseaseKnowledgeGraphBuilder()
    triples = [
        Triple(
            source="Malaria",
            relation="has_symptom",
            target="Fever",
            source_type="Disease",
            target_type="Symptom",
        ),
        Triple(
            source="Malaria",
            relation="has_symptom",
            target="Chills",
            source_type="Disease",
            target_type="Symptom",
        ),
        Triple(
            source="Malaria",
            relation="treated_with",
            target="ACT",
            source_type="Disease",
            target_type="Treatment",
        ),
        Triple(
            source="Malaria",
            relation="affects_organ",
            target="Liver",
            source_type="Disease",
            target_type="Organ",
        ),
    ]
    builder.add_triples(triples)

    symptoms = builder.query_symptoms("Malaria")
    assert "Fever" in symptoms
    assert "Chills" in symptoms
    assert len(symptoms) == 2

    treatments = builder.query_treatments("Malaria")
    assert "ACT" in treatments

    # Check nodes and edges
    assert builder.nodes["Malaria"] == "Disease"
    assert builder.nodes["Liver"] == "Organ"
    assert len(builder.edges) == 4


def test_graph_export(tmp_path):
    builder = DiseaseKnowledgeGraphBuilder()
    triple = Triple(source="Malaria", relation="has_symptom", target="Fever")
    builder.add_triples([triple])

    export_path = tmp_path / "test_graph.json"
    builder.export_json(str(export_path))

    assert export_path.exists()
    with open(export_path, "r") as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["source"] == "Malaria"
        assert data[0]["relation"] == "has_symptom"


if __name__ == "__main__":
    # If run directly, just use pytest
    pytest.main([__file__])
