import streamlit as st
from litellm import completion
import base64
from PIL import Image
import time

class ModelConfig:
      OPENAI_MODELS = ["openai/gpt-4o", "openai/gpt-4o-mini"]
      OLLAMA_MODELS = ["ollama/llava", "ollama/llava-llama3", "ollama/bakllava"]
      GEMINI_MODELS = ["gemini/gemini-2.0-flash", "gemini/gemini-2.0-flash-lite-preview-02-05", "gemini/gemini-2.0-pro-exp-02-05", "gemini/gemini-2.0-flash-thinking-exp-01-21"]

      MODELS = OPENAI_MODELS + OLLAMA_MODELS + GEMINI_MODELS

class LiteVision:
    @staticmethod
    def image_url(image):
        with open(image, "rb") as file:
            file_data = file.read()
            encoded_file = base64.b64encode(file_data).decode("utf-8")
            base64_url = f"data:image/jpeg;base64,{encoded_file}"
        return base64_url

    @staticmethod
    def get_response(prompt, image_file, model):
        try:
            start_time = time.time()
            base64_url = LiteVision.image_url(image_file)
            image_content = [{"type": "text", "text": prompt},
                             {"type": "image_url", "image_url": {"url": base64_url}}]
            response = completion(model=model, messages=[{"role": "user", "content": image_content}], temperature=0.2, max_tokens=1000)
            response_text = response.choices[0].message.content
            end_time = time.time()
            response_time = end_time - start_time
            word_count = len(response_text.split())
            return {"text": response_text, "response_time": response_time, "word_count": word_count}
        except FileNotFoundError:
            return {"error": f"File '{image_file}' not found", "response_time": 0, "word_count": 0}
        except Exception as e:
            return {"error": str(e), "response_time": 0, "word_count": 0}

def streamlit_app():
    st.set_page_config(layout="wide")
    st.title("Litellm Vision")

    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
    model_index = st.sidebar.selectbox("Select a model", range(len(ModelConfig.MODELS)), format_func=lambda i: ModelConfig.MODELS[i])
    fit_image   = st.sidebar.checkbox("Fit image", False)

    if uploaded_file:
        image_path = f"temp_{uploaded_file.name}"
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        image = Image.open(image_path)
        width, height = image.size
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=fit_image)
        st.write(f"**Image Size:** {width} x {height} pixels")
        
        prompt = st.text_input("Ask Question", "Describe the image")
        if st.button("Get Answer"):
            with st.spinner("Processing... Please wait."):
                model  = ModelConfig.MODELS[model_index]
                result = LiteVision.get_response(prompt, image_path, model)
            st.write(result.get("text", "Error occurred"))
            st.write(f"**Response Time:** {result.get('response_time', 0):.2f} seconds")
            st.write(f"**Word Count:** {result.get('word_count', 0)}")

if __name__ == "__main__":
    streamlit_app()

