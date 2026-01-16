import streamlit as st
from ddg_videos import DuckDuckVideos

class StVideoSearch:
    def __init__(self):
        self.video_searcher = DuckDuckVideos()
        st.session_state.setdefault("videos", [])
        st.session_state.setdefault("selected_title", "")
        st.session_state.setdefault("max_results", 10)

    def search_videos(self, title, max_results):
        if title.strip():
            st.session_state.selected_title = title.strip()
            st.session_state.max_results = max_results
            with st.spinner("Searching for videos..."):
                st.session_state.videos = self.video_searcher.get_urls(st.session_state.selected_title, max_results=st.session_state.max_results)
            if not st.session_state.videos:
                st.info("No videos found for your search. Try a different query.")
        else:
            st.warning("Please enter a valid search query.")

    def show_videos(self):
        if st.session_state.videos:
            for i, video in enumerate(st.session_state.videos):
                if i >= st.session_state.max_results:
                    break
                with st.container():
                    st.markdown(f"### VideoID: {i}")
                    st.markdown(f"### Title: {video['title']}")
                    st.markdown(f"### Duration: {video['duration']}")
                    try:
                        st.video(video['url'])
                    except Exception:
                        st.warning("This video cannot be embedded. Please use the link above.")

                    st.divider()

                    if st.button(f"Remove Video {i}", key=f"remove_video_{i}"):
                        st.session_state.videos.pop(i)
                        st.rerun()

class UIVideoApp:
    def __init__(self):
        self.app = StVideoSearch()

    def run(self):
        st.title("🔎 DuckDuckGo Video Finder")

        # Step 1: Input title
        title = st.text_input("Enter a video title to search:", value=st.session_state.selected_title)

        # Step 2: Select number of results
        max_results = st.slider("Select number of videos to retrieve:", min_value=1, max_value=50, value=st.session_state.max_results)

        # Step 3: Search for videos
        if st.button("Search"):
           self.app.search_videos(title, max_results)

        self.app.show_videos()

if __name__ == "__main__":
    app = UIVideoApp()
    app.run()
