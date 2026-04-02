"""
deep_intuition_archive.py - Persistence Component

Handles saving and retrieval of Deep Intuition stories.
"""

import json
from pathlib import Path
from typing import Optional, Any


class MissionArchive:
    """Persistence manager for Deep Intuition Storytelling."""

    def __init__(self, topic: str, output_path: Optional[str] = None):
        self.topic = topic
        self.output_path = output_path
        self.story: Optional[dict] = None

        if self.output_path:
            Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)

    def set_final_story(self, story: Any):
        """Save the synthesized Deep Intuition story."""
        self.story = story.model_dump() if hasattr(story, 'model_dump') else story
        self._flush()

    def _flush(self):
        """Write the story to disk."""
        if not self.output_path:
            return

        path = Path(self.output_path)
        
        # If story is a string (Markdown), ensure extension is .md
        if isinstance(self.story, str):
            if path.suffix != '.md':
                path = path.with_suffix('.md')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.story)
        else:
            # Otherwise save as JSON
            if path.suffix != '.json':
                path = path.with_suffix('.json')
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.story, f, indent=4, ensure_ascii=False)
