import unittest
import json
import os
from DeepDeliberation.noagentic.deep_deliberation_archive import MissionArchive
from DeepDeliberation.noagentic.deep_deliberation_models import KnowledgeSynthesis

class TestMissionArchive(unittest.TestCase):
    def setUp(self):
        self.topic = "test_topic"
        self.output_path = "tests/test_output.json"
        self.archive = MissionArchive(self.topic, self.output_path)

    def tearDown(self):
        if os.path.exists(self.output_path):
            os.remove(self.output_path)
        if os.path.exists("tests/test_output.json"):
             # In case it was created elsewhere
             pass

    def test_record_step(self):
        self.archive.record_step(1, "query", "analysis", ["evidence1"])
        self.assertEqual(len(self.archive.history), 1)
        self.assertEqual(self.archive.history[0]["wave"], 1)
        
        # Check if it flushed to disk
        with open(self.output_path, 'r') as f:
            data = json.load(f)
            self.assertEqual(data["topic"], self.topic)
            self.assertEqual(len(data["discovery_history"]), 1)
            self.assertEqual(data["discovery_history"][0]["query"], "query")

    def test_set_final_map_with_model(self):
        final_map = KnowledgeSynthesis(
            topic=self.topic,
            executive_summary="summary",
            hidden_connections=["conn1"],
            research_frontiers=["front1"]
        )
        self.archive.set_final_map(final_map)
        self.assertIsNotNone(self.archive.final_map)
        
        with open(self.output_path, 'r') as f:
            data = json.load(f)
            self.assertEqual(data["strategic_knowledge_map"]["topic"], self.topic)
            self.assertEqual(data["strategic_knowledge_map"]["executive_summary"], "summary")

    def test_set_final_map_with_dict(self):
        final_map_dict = {"topic": self.topic, "summary": "dict_summary"}
        self.archive.set_final_map(final_map_dict)
        self.assertEqual(self.archive.final_map["summary"], "dict_summary")

if __name__ == "__main__":
    unittest.main()
