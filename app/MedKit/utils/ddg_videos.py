import logging
from duckduckgo_search import DDGS
import re

logger = logging.getLogger(__name__)

class DuckDuckVideos:
    def get_urls(self, query, max_results=10): 
        video_urls = []
        try:
            with DDGS() as ddgs:
                for result in ddgs.videos(keywords=query, max_results=max_results):
                    url = result.get('url') or result.get('content') or result.get('image')
                    if not url:
                        continue
                    video_urls.append({
                        'url': url,
                        'title': result.get('title', 'No title'),
                        'duration': result.get('duration', 'N/A')
                    })
                    if len(video_urls) >= max_results:
                        break
        except Exception as e:
            try:
                import streamlit as st
                st.error(f"Error during video search: {e}")
            except (ImportError, RuntimeError):
                logger.error(f"Error during video search: {e}")
        return self.sort_by_duration(video_urls)

    def _duration_to_seconds(self, duration_str):
        if duration_str == 'N/A':
            return float('inf')
        match = re.match(r'(?:(\d+):)?(\d+):?(\d+)?', duration_str)
        if not match:
            return float('inf')
        parts = [int(p) if p else 0 for p in match.groups()]
        if len(parts) == 3:
            return parts[0] * 3600 + parts[1] * 60 + parts[2]
        elif len(parts) == 2:
            return parts[0] * 60 + parts[1]
        return float('inf')

    def sort_by_duration(self, videos):
        return sorted(videos, key=lambda x: self._duration_to_seconds(x['duration']))

