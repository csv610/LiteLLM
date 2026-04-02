"""
deep_deliberation_archive.py - Persistence Component

Handles incremental saving and retrieval of mission discovery data.
"""

import json
from pathlib import Path
from typing import List, Optional, Any


class MissionArchive:
    """Persistence manager for Knowledge Discovery Missions."""

    def __init__(self, topic: str, output_path: Optional[str] = None):
        self.topic = topic
        self.output_path = output_path
        self.history: List[dict] = []
        self.final_map: Optional[dict] = None

        if self.output_path:
            Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)

    def record_step(self, wave: int, query: str, analysis: str, evidence: List[str]):
        """Save a single discovery step to the archive."""
        record = {
            "wave": wave,
            "query": query,
            "analysis": analysis,
            "evidence": evidence
        }
        self.history.append(record)
        self._flush()

    def set_final_map(self, final_map: Any):
        """Save the synthesized Strategic Knowledge Map (Markdown)."""
        self.final_map = final_map
        self._flush()

    def _flush(self):
        """Write the current state to disk."""
        if not self.output_path:
            return

        is_markdown = isinstance(self.final_map, str)
        
        # Save JSON history/archive
        archive_path = Path(self.output_path)
        if archive_path.suffix != ".json":
            archive_path = archive_path.with_suffix(".json")

        data = {
            "topic": self.topic,
            "discovery_history": self.history,
            "strategic_knowledge_map": self.final_map if not is_markdown else "See associated .md file"
        }
        with open(archive_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        # Save separate Markdown report
        if is_markdown:
            report_path = archive_path.with_suffix(".md")
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(self.final_map)
