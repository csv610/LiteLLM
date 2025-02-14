import os
import asyncio
import sys
import argparse

from litellm import completion
import time

class ModelConfig:
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

def cli_interface():
    parser = argparse.ArgumentParser(description="CLI for LiteText API")
    parser.add_argument("-p", "--prompt", type=str, required=True, help="Input prompt for the model")
    parser.add_argument("-m", "--model", type=int, default=0, help="Index of the model to use")
    args = parser.parse_args()
    
    if args.model < 0 or args.model >= len(ModelConfig.MODELS):
        print("Invalid model index. Please select a valid index from:")
        for i, model in enumerate(ModelConfig.MODELS):
            print(f"{i}: {model}")
        return
    
    result = LiteText.get_response(args.prompt, ModelConfig.MODELS[args.model])
    print(f"Response: {result.get('response', 'Error occurred')}")
    print(f"Response Time: {result.get('response_time', 0):.2f} seconds")
    print(f"Word Count: {result.get('word_count', 0)}")

cli_interface()
