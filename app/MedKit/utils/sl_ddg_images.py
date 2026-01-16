import os
import streamlit as st

from ddg_images import DuckDuckImages

class RenderImages:
    def __init__(self):
        self.image_searcher = DuckDuckImages()
        if "last_query" not in st.session_state:
            st.session_state.last_query = ""
        # Initialize object_images in session state
        if "object_images" not in st.session_state:
            st.session_state.object_images = {}

    def display_image(self, query, url):
        width, height = self.image_searcher.fetch_image_size(url)
        if width == 0 and height == 0:
            st.write(f"Could not retrieve image size for {url}.")
            return
        st.image(url, caption=f"Image - Size: {width}x{height}", width='stretch' if self.fit_image else 'content')
        if st.button(f"Remove Image", key=query+url):
            for query, urls in st.session_state.object_images.items():
                if url in urls:
                    st.session_state.object_images[query].remove(url)
            st.rerun()
        st.divider()
            
    def display_all_images(self):
        for query, urls in st.session_state.object_images.items():
            for url in urls:
                self.display_image(query, url)
            
    def fetch_object_images(self, query, image_size, num_images):
        st.write(f"Downloading images for {query} ")
        with st.spinner(f"Fetching images for '{query}'..."):
            new_urls = self.image_searcher.get_urls(query, image_size, num_images)
            for url in new_urls:
                self.display_image(query, url)
            st.session_state.object_images[query] = new_urls

    def fetch_all_images(self, query_input, image_size, num_images):
        queries = [q.strip() for q in query_input.split(",") if q.strip()]
        if query_input != st.session_state.last_query:
            st.session_state.last_query = query_input
            st.session_state.object_images = {}

        for q in queries:
            self.fetch_object_images(q, image_size, num_images)
        
        st.write("All images fetched")
        st.rerun()  

    def save_images(self):
        # Create directory for saving images
        os.makedirs("downloaded_images", exist_ok=True)

        # Check if there are any images to save
        if not st.session_state.object_images:
            st.write("No images to save.")
            return

        for query, urls in st.session_state.object_images.items():
            for i, url in enumerate(urls):
                filename = self.image_searcher.download_image(url, "downloaded_images", query, i)
                if filename:
                    st.write(f"Saved: {filename}")

    def get_sidebar_options(self):
        size = st.sidebar.selectbox(
            "Select image size:",
            options=["Large", "Medium", "Small",  "Wallpaper"],
            index=0
        )
        max_results = st.sidebar.number_input("images per item:", min_value=1, value=5, step=1)
        self.fit_image = st.sidebar.checkbox("Fit Image", value=False)

        # Store the selected size in session state
        st.session_state.image_size = size
        return size, max_results

    def render(self, med_image):
        image_size, max_images_per_item = self.get_sidebar_options()

        # Check if the image size has changed
        if 'image_size' not in st.session_state or st.session_state.image_size != image_size:
            st.session_state.object_images = {}  # Clear previous images if size changes
            st.session_state.image_size = image_size  # Update the stored image size

        #Image Search
        if st.button("Image Search"):
            st.session_state.query_input =  med_image
            self.fetch_all_images(med_image, image_size, max_images_per_item)
                    
        self.display_all_images()

        #Images download and save
        if st.session_state.object_images and st.sidebar.button("Save Images"):
            self.save_images()

if __name__ == "__main__":
    st.title("DuckDuckGo Image Search")
    med_image = st.text_input("Search Medical Images: ", "Give an image of lazy eye")
    app = RenderImages()
    app.render(med_image)
