import logging
from ddgs import DDGS
import re

logger = logging.getLogger(__name__)

class DuckDuckVideos:
    def get_urls(self, query, max_results=10): 
        video_urls = []
        try:
            with DDGS() as ddgs:
                for result in ddgs.videos(query, max_results=max_results):
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
        if duration_str == 'N/A' or not duration_str:
            return float('inf')
        
        parts = duration_str.split(':')
        try:
            parts = [int(p) for p in parts]
            if len(parts) == 3: # HH:MM:SS
                return parts[0] * 3600 + parts[1] * 60 + parts[2]
            elif len(parts) == 2: # MM:SS
                return parts[0] * 60 + parts[1]
            elif len(parts) == 1: # SS
                return parts[0]
        except (ValueError, TypeError):
            return float('inf')
        return float('inf')

    def sort_by_duration(self, videos):
        return sorted(videos, key=lambda x: self._duration_to_seconds(x['duration']))

