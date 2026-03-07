import unittest
import os
import shutil
from surgery_models import SurgeryTripletExtractor, SurgeryGraphBuilder, Triple

class TestSurgeryGraph(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Ensure outputs directory is clean for tests."""
        if os.path.exists("outputs"):
            shutil.rmtree("outputs")

    def test_triplet_normalization(self):
        """Test if Triple model correctly normalizes relation and node types."""
        t = Triple(
            source="CABG",
            relation="treats",
            target="CAD",
            source_type="surgery",
            target_type="disease"
        )
        self.assertEqual(t.relation, "treats_disease")
        self.assertEqual(t.source_type, "Surgery")
        self.assertEqual(t.target_type, "Disease")

    def test_graph_builder_and_dot_export(self):
        """Test building a graph and exporting to .dot file."""
        builder = SurgeryGraphBuilder()
        triples = [
            Triple(source="Surgical Procedure", relation="treats_disease", target="Ailment", source_type="Surgery", target_type="Disease")
        ]
        builder.add_triples(triples)
        
        surgery_name = "Test Surgery"
        builder.export_dot(surgery_name, output_dir="outputs")
        
        expected_path = "outputs/test_surgery.dot"
        self.assertTrue(os.path.exists(expected_path), f".dot file not found at {expected_path}")
        
        with open(expected_path, "r") as f:
            content = f.read()
            self.assertIn('digraph "Test Surgery"', content)
            self.assertIn('"Surgical Procedure" -> "Ailment"', content)

    def test_offline_simulation(self):
        """Test extraction using the offline simulation mode."""
        extractor = SurgeryTripletExtractor()
        # Mocking offline mode by ensuring LiteClient is treated as None if needed, 
        # but the class already handles this if import fails or we can test the _simulate method directly.
        triples = extractor.extract("Coronary Artery Bypass Surgery")
        self.assertGreater(len(triples), 0)
        self.assertEqual(triples[0].source, "Coronary Artery Bypass Surgery")

if __name__ == "__main__":
    unittest.main()
