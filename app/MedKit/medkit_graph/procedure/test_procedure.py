import unittest
from procedure_models import Triple, ProcedureGraphBuilder, ProcedureTripletExtractor, ModelConfig

class TestProcedureKnowledgeGraph(unittest.TestCase):

    def setUp(self):
        self.model_config = ModelConfig(model="ollama/gemma3")

    def test_triple_validation(self):
        """Test Pydantic model validation and normalization."""
        # Test alias normalization
        t = Triple(
            source="Appendectomy",
            relation="treats",
            target="Appendicitis",
            source_type="surgery",
            target_type="disease"
        )
        self.assertEqual(t.relation, "treats_disease")
        self.assertEqual(t.source_type, "Procedure")
        self.assertEqual(t.target_type, "Disease")

        # Test default normalization
        t2 = Triple(source="X", relation="unknown", target="Y")
        self.assertEqual(t2.relation, "other")
        self.assertEqual(t2.source_type, "Other")

    def test_graph_builder(self):
        """Test building and querying the graph."""
        builder = ProcedureGraphBuilder(model_config=self.model_config)
        triples = [
            Triple(source="Appendectomy", relation="treats_disease", target="Appendicitis", source_type="Procedure", target_type="Disease"),
            Triple(source="Cholecystectomy", relation="treats_disease", target="Gallstones", source_type="Procedure", target_type="Disease")
        ]
        builder.add_triples(triples)
        
        # Test nodes
        self.assertIn("Appendectomy", builder.G.nodes)
        self.assertEqual(builder.G.nodes["Appendectomy"]["type"], "Procedure")
        
        # Test query
        results = builder.query_treats("Appendicitis")
        self.assertIn("Appendectomy", results)
        self.assertNotIn("Cholecystectomy", results)

    def test_graph_builder_build(self):
        """Test the new build method of GraphBuilder."""
        builder = ProcedureGraphBuilder(model_config=self.model_config)
        triples = builder.build("Appendectomy")
        self.assertTrue(len(triples) > 0)
        self.assertIn("Appendectomy", builder.G.nodes)

    def test_extractor_offline_mode(self):
        """Test the extractor's fallback mechanism."""
        extractor = ProcedureTripletExtractor(model_config=self.model_config)
        # By providing text that triggers simulation, we can test without API keys if needed
        triples = extractor.extract("Appendectomy for appendicitis")
        self.assertTrue(len(triples) > 0)
        self.assertEqual(triples[0].source, "Appendectomy")

    def test_extract_from_text_offline(self):
        """Test extraction directly from text using the extractor."""
        extractor = ProcedureTripletExtractor(model_config=self.model_config)
        triples = extractor.extract("Colonoscopy is performed on the colon.")
        self.assertTrue(len(triples) >= 1)
        self.assertEqual(triples[0].source, "Colonoscopy")

    def test_graph_builder_extractor_separation(self):
        """Test that extractor-based building is separated into its own class."""
        from procedure_models import ProcedureExtractorGraphBuilder
        builder = ProcedureExtractorGraphBuilder(model_config=self.model_config)
        triples = builder.build_from_text("Appendectomy is for appendicitis.")
        self.assertTrue(len(triples) > 0)
        self.assertIn("Appendectomy", builder.G.nodes)

if __name__ == "__main__":
    unittest.main()
