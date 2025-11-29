#!/usr/bin/env python3
"""Streamlit web interface for LiteVision."""

import logging
import os
import sys

import streamlit as st
from PIL import Image

# Add lite to path for imports
sys.path.insert(0, "/Users/csv610/Projects/LiteLLM")

from lite.litellm_tools import LiteVision, ModelConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def streamlit_app() -> None:
    """Streamlit app for LiteVision."""
    st.set_page_config(page_title="LiteVision", layout="wide")
    st.title("LiteVision - Image Analysis Interface")

    models = ModelConfig.get_models("vision")

    with st.sidebar:
        st.header("Settings")
        model_index = st.selectbox(
            "Select a model",
            range(len(models)),
            format_func=lambda i: models[i],
        )
        temperature = st.slider(
            "Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.1
        )
        max_tokens = st.slider(
            "Max Tokens", min_value=100, max_value=4000, value=1000, step=100
        )
        fit_image = st.checkbox("Fit image to container", value=False)

    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        # Save temporary file
        image_path = f"temp_{uploaded_file.name}"
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Display image info
        image = Image.open(image_path)
        width, height = image.size
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=fit_image)
        st.write(f"**Image Size:** {width} x {height} pixels")

        # Prompt input
        prompt = st.text_area(
            "Enter your question about the image",
            value="Describe the image",
            height=100,
        )

        if st.button("Get Answer", type="primary"):
            model = models[model_index]
            with st.spinner("Analyzing image... Please wait."):
                result = LiteVision.get_response(
                    prompt,
                    image_path,
                    model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.subheader("Response")
                st.write(result.get("text", "N/A"))

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Response Time", f"{result.get('response_time', 0):.2f}s")
                with col2:
                    st.metric("Word Count", result.get("word_count", 0))

        # Clean up temporary file
        if os.path.exists(image_path):
            os.remove(image_path)


if __name__ == "__main__":
    streamlit_app()
