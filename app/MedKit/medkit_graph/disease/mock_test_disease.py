import json

import pytest
from disease_models import DiseaseGraphBuilder, DiseaseTripletExtractor, Triple


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
    builder = DiseaseGraphBuilder()
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


def test_extractor_simulation():
    extractor = DiseaseTripletExtractor()
    # Test simulation for Malaria from text
    triples = extractor._simulate_as_triples("This is about Malaria")

    assert len(triples) > 0
    malaria_triples = [t for t in triples if t.source == "Malaria"]
    assert len(malaria_triples) > 0

    # Check for specific simulated edges
    has_fever = any(
        t.target == "Fever" and t.relation == "has_symptom" for t in triples
    )
    assert has_fever

    has_liver = any(
        t.target == "Liver" and t.relation == "affects_organ" for t in triples
    )
    assert has_liver


def test_extract_by_name():
    extractor = DiseaseTripletExtractor()
    # Test extraction by name for Diabetes (simulated)
    triples = extractor.extract_by_name("Diabetes")

    assert len(triples) > 0
    diabetes_triples = [t for t in triples if t.source == "Diabetes Mellitus"]
    assert len(diabetes_triples) > 0

    # Check for specific simulated edges
    has_thirst = any(
        t.target == "Increased thirst" and t.relation == "has_symptom" for t in triples
    )
    assert has_thirst


def test_graph_export(tmp_path):
    builder = DiseaseGraphBuilder()
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
