#!/usr/bin/env python3
"""Streamlit web interface for LiteText."""

import logging
import sys

import streamlit as st

# Add lite to path for imports
sys.path.insert(0, "/Users/csv610/Projects/LiteLLM")

from lite.litellm_tools import LiteText, ModelConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def streamlit_app() -> None:
    """Streamlit app for LiteText."""
    st.set_page_config(page_title="LiteText", layout="wide")
    st.title("LiteText - Language Model Interface")

    models = ModelConfig.get_models("text")

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

    st.subheader("Query")
    prompt = st.text_area(
        "Enter your prompt",
        value="What are blackholes and their future?",
        height=100,
    )

    if st.button("Get Answer", type="primary"):
        model = models[model_index]
        with st.spinner("Processing... Please wait."):
            result = LiteText.get_response(
                prompt, model, temperature=temperature, max_tokens=max_tokens
            )

        if result.is_success():
            st.subheader("Response")
            st.write(result.response)

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Response Time", f"{result.response_time:.2f}s")
            with col2:
                st.metric("Word Count", result.word_count)
        else:
            st.error(f"Error: {result.error}")


if __name__ == "__main__":
    streamlit_app()
