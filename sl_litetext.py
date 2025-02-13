import streamlit as st
from litellm import completion
import base64
from PIL import Image
import time

OPENAI_MODELS = ["openai/gpt-4o", "openai/gpt-4o-mini"]
OLLAMA_MODELS = ["ollama/llama3.2", "ollama/phi4"]
GEMINI_MODELS = ["gemini/gemini-2.0-flash", "gemini/gemini-2.0-flash-lite-preview-02-05", "gemini/gemini-2.0-pro-exp-02-05", "gemini/gemini-2.0-flash-thinking-exp-01-21"]

MODELS = OPENAI_MODELS + OLLAMA_MODELS + GEMINI_MODELS

class LiteText:
    @staticmethod
    def get_response(prompt, model):
        try:
            start_time = time.time()
            text_content = [{"type": "text", "text": prompt}]
            response = completion(model=model, messages=[{"role": "user", "content": text_content}], temperature=0.2, max_tokens=1000)
            response_text = response.choices[0].message.content
            end_time = time.time()
            response_time = end_time - start_time
            word_count = len(response_text.split())
            return {"response": response_text, "response_time": response_time, "word_count": word_count}
        except Exception as e:
            return {"error": str(e), "response_time": 0, "word_count": 0}

def streamlit_app():
    st.set_page_config(layout="wide")
    st.title("Litellm Text")

    model_index = st.sidebar.selectbox("Select a model", range(len(MODELS)), format_func=lambda i: MODELS[i])

    prompt = st.text_input("Ask Question", "What are blackhole and their future?")
    if st.button("Get Answer"):
       with st.spinner("Processing... Please wait."):
            result = LiteText.get_response(prompt, MODELS[model_index])
       st.write(result.get("response", "Error occurred"))
       st.write(f"**Response Time:** {result.get('response_time', 0):.2f} seconds")
       st.write(f"**Word Count:** {result.get('word_count', 0)}")

if __name__ == "__main__":
    streamlit_app()

