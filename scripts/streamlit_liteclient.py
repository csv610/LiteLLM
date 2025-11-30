#!/usr/bin/env python3
"""Unified Streamlit web interface for LiteClient."""

import logging
import os
import sys
from pathlib import Path

import streamlit as st
from PIL import Image

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lite.lite_client import LiteClient
from lite.config import ModelConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def streamlit_app() -> None:
    """Unified Streamlit app for LiteClient - Text and Vision."""
    st.set_page_config(page_title="LiteClient", layout="wide")
    st.title("LiteClient - Unified Text and Vision Interface")

    # Mode selection
    mode = st.radio("Select Mode", ["Text Generation", "Image Analysis"], horizontal=True)

    with st.sidebar:
        st.header("Settings")

        # Get models based on mode
        if mode == "Text Generation":
            models = ModelConfig.get_models("text")
        else:
            models = ModelConfig.get_models("vision")

        model_index = st.selectbox(
            "Select a model",
            range(len(models)),
            format_func=lambda i: models[i],
        )
        temperature = st.slider(
            "Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.1
        )

    client = LiteClient()

    if mode == "Text Generation":
        st.subheader("Text Generation")
        prompt = st.text_area(
            "Enter your prompt",
            value="What are blackholes and their future?",
            height=100,
        )

        if st.button("Generate", type="primary"):
            model = models[model_index]
            with st.spinner("Processing... Please wait."):
                result = client.generate_text(
                    prompt=prompt,
                    model=model,
                    temperature=temperature,
                )

            if isinstance(result, dict) and "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.subheader("Response")
                st.write(result)

    else:  # Image Analysis
        st.subheader("Image Analysis")
        uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

        if uploaded_file:
            # Save temporary file
            image_path = f"temp_{uploaded_file.name}"
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Display image info
            image = Image.open(image_path)
            width, height = image.size

            col1, col2 = st.columns(2)
            with col1:
                st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            with col2:
                st.write(f"**Image Size:** {width} x {height} pixels")

            # Prompt input
            prompt = st.text_area(
                "Enter your question about the image",
                value="Describe the image",
                height=100,
            )

            if st.button("Analyze", type="primary"):
                model = models[model_index]
                with st.spinner("Analyzing image... Please wait."):
                    result = client.generate_text(
                        prompt=prompt,
                        image_path=image_path,
                        model=model,
                        temperature=temperature,
                    )

                if isinstance(result, dict) and "error" in result:
                    st.error(f"Error: {result['error']}")
                else:
                    st.subheader("Response")
                    st.write(result)

            # Clean up temporary file
            if os.path.exists(image_path):
                os.remove(image_path)


if __name__ == "__main__":
    streamlit_app()
