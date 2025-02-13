from litellm import completion
import os
import asyncio
import sys

OPENAI_MODELS = [ "gpt-4o", "gpt-4o-mini"]
OLLAMA_MODELS = [ "ollama/llama3.2", "ollama/phi4", "ollama/deepseek-r1"]
GROQ_MODELS   = [ "groq/llama3-8b-8192"]
GEMINI_MODEL  = [ "gemini/gemini-2.0-flash", 
                  "gemini/gemini-2.0-flash-lite-preview-02-05", 
                  "gemini/gemini-2.0-pro-exp-02-05",
                  "gemini/gemini-2.0-flash-thinking-exp-01-21"
                ]
    
MODELS = OPENAI_MODELS + OLLAMA_MODELS + GROQ_MODELS + GEMINI_MODEL

def process_response(response, stream):
    answer = ""
    if stream:
       for part in response:
           answer += part.choices[0].delta.content or ""
    else:
       answer = response.choices[0].message.content

    return answer

def get_response(question, model, stream=True):
    messages=[{ "content": f"{question}", "role": "user"}]
    response = completion( model= model, messages=messages, stream = stream)
    answer = process_response(response, stream)
    return answer

question = sys.argv[1]
mid      = int(sys.argv[2] )

response = get_response(question, MODELS[mid] )
print( response)




