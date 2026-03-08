import json
import os
import tempfile
import unittest

from medicine_models import (
    MedicineKnowledgeGraph,
    MedicineReport,
    Triple,
)
from pydantic import ValidationError


class TestMedicineModels(unittest.TestCase):
    def test_triple_validation_valid(self):
        t = Triple(subject="DrugA", predicate="treats", object="DiseaseB")
        self.assertEqual(t.source, "DrugA")
        self.assertEqual(t.relation, "treats")
        self.assertEqual(t.target, "DiseaseB")
        self.assertEqual(t.source_type, "Other")
        self.assertEqual(t.target_type, "Other")

    def test_triple_validation_relation_alias(self):
        t = Triple(subject="DrugA", predicate="treat", object="DiseaseB")
        self.assertEqual(t.relation, "treats")

        t2 = Triple(subject="DrugA", predicate="adverse_effect", object="SymptomC")
        self.assertEqual(t2.relation, "has_side_effect")

    def test_triple_validation_node_type_alias(self):
        t = Triple(
            subject="DrugA",
            predicate="treats",
            object="DiseaseB",
            subject_type="drug",
            object_type="disorder",
        )
        self.assertEqual(t.source_type, "Drug")
        self.assertEqual(t.target_type, "Disease")

    def test_triple_validation_invalid_entity(self):
        with self.assertRaises(ValidationError):
            Triple(subject="", predicate="treats", object="DiseaseB")

    def test_medicine_graph_builder_add_and_query(self):
        builder = MedicineKnowledgeGraph()
        triples = [
            Triple(
                subject="Paracetamol",
                predicate="treats",
                object="Fever",
                subject_type="Drug",
                object_type="Disease",
            ),
            Triple(
                subject="Paracetamol",
                predicate="has_side_effect",
                object="Nausea",
                subject_type="Drug",
                object_type="SideEffect",
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
        builder = MedicineKnowledgeGraph()
        report = MedicineReport(
            name="Paracetamol",
            therapeutic_class="Analgesic",
            description="Treats fever and pain",
            triples=[
                Triple(
                    subject="Paracetamol",
                    predicate="treats",
                    object="Fever",
                    subject_type="Drug",
                    object_type="Disease",
                )
            ],
        )
        builder.last_report = report
        builder.add_triples(report.triples)

        with tempfile.TemporaryDirectory() as tmpdir:
            json_path = os.path.join(tmpdir, "graph.json")
            builder.export_json(json_path)
            self.assertTrue(os.path.exists(json_path))

            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertEqual(data["name"], "Paracetamol")
                self.assertEqual(len(data["triples"]), 1)
                self.assertEqual(data["triples"][0]["subject"], "Paracetamol")

            # Test dot export (dot export uses hardcoded 'outputs' directory in model,
            # so we might need to be careful, but we can call it and see)
            # However, for mock test, we can just verify it works.
            # I updated export_dot to use 'outputs' directory.
            # Let's mock os.makedirs to avoid side effects if possible, or just let it run.
            builder.export_dot("TestDrug")
            expected_dot = os.path.join("outputs", "testdrug.dot")
            self.assertTrue(os.path.exists(expected_dot))
            if os.path.exists(expected_dot):
                os.remove(expected_dot)


if __name__ == "__main__":
    unittest.main()
