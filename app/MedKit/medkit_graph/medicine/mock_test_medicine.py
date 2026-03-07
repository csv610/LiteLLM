import json
import os
import tempfile
import unittest

from medicine_models import (
    MedicineGraphBuilder,
    MedicineTripletExtractor,
    Triple,
)
from pydantic import ValidationError


class TestMedicineModels(unittest.TestCase):
    def test_triple_validation_valid(self):
        t = Triple(source="DrugA", relation="treats", target="DiseaseB")
        self.assertEqual(t.source, "DrugA")
        self.assertEqual(t.relation, "treats")
        self.assertEqual(t.target, "DiseaseB")
        self.assertEqual(t.source_type, "Other")
        self.assertEqual(t.target_type, "Other")

    def test_triple_validation_relation_alias(self):
        t = Triple(source="DrugA", relation="treat", target="DiseaseB")
        self.assertEqual(t.relation, "treats")

        t2 = Triple(source="DrugA", relation="adverse_effect", target="SymptomC")
        self.assertEqual(t2.relation, "has_side_effect")

    def test_triple_validation_node_type_alias(self):
        t = Triple(
            source="DrugA",
            relation="treats",
            target="DiseaseB",
            source_type="drug",
            target_type="disorder",
        )
        self.assertEqual(t.source_type, "Drug")
        self.assertEqual(t.target_type, "Disease")

    def test_triple_validation_invalid_entity(self):
        with self.assertRaises(ValidationError):
            Triple(source="", relation="treats", target="DiseaseB")

    def test_medicine_triplet_extractor_simulate(self):
        extractor = MedicineTripletExtractor()
        triples = extractor._simulate("Paracetamol is good")
        self.assertEqual(len(triples), 5)
        self.assertEqual(triples[0]["source"], "Paracetamol")
        self.assertEqual(triples[0]["relation"], "treats")

        triples_empty = extractor._simulate("Unknown drug")
        self.assertEqual(len(triples_empty), 0)

    def test_medicine_graph_builder_add_and_query(self):
        builder = MedicineGraphBuilder()
        triples = [
            Triple(
                source="Paracetamol",
                relation="treats",
                target="Fever",
                source_type="Drug",
                target_type="Disease",
            ),
            Triple(
                source="Paracetamol",
                relation="has_side_effect",
                target="Nausea",
                source_type="Drug",
                target_type="SideEffect",
            ),
        ]
        builder.add_triples(triples)

        self.assertIn("Paracetamol", builder.G.nodes)
        self.assertIn("Fever", builder.G.nodes)
        self.assertIn("Nausea", builder.G.nodes)

        treats = builder.query_treats("Fever")
        self.assertIn("Paracetamol", treats)

        side_effects = builder.query_side_effects("Paracetamol")
        self.assertIn("Nausea", side_effects)

    def test_medicine_graph_builder_export(self):
        builder = MedicineGraphBuilder()
        triples = [
            Triple(
                source="Paracetamol",
                relation="treats",
                target="Fever",
                source_type="Drug",
                target_type="Disease",
            )
        ]
        builder.add_triples(triples)

        with tempfile.TemporaryDirectory() as tmpdir:
            json_path = os.path.join(tmpdir, "graph.json")
            builder.export_json(json_path)
            self.assertTrue(os.path.exists(json_path))

            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertEqual(len(data), 1)
                self.assertEqual(data[0]["source"], "Paracetamol")

            dot_path = os.path.join(tmpdir, "graph.dot")
            builder.export_dot(dot_path)
            self.assertTrue(os.path.exists(dot_path))


if __name__ == "__main__":
    unittest.main()
