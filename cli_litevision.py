from litellm import completion
import base64
import argparse

OPENAI_MODELS = ["openai/gpt-4o", 
                 "openai/gpt-4o-mini"
                ]
OLLAMA_MODELS = [ "ollama/llava",
                  "ollama/llava-llama3",
                  "ollama/bakllava"
                ]
GEMINI_MODELS = [ "gemini/gemini-2.0-flash", 
                  "gemini/gemini-2.0-flash-lite-preview-02-05", 
                  "gemini/gemini-2.0-pro-exp-02-05", 
                  "gemini/gemini-2.0-flash-thinking-exp-01-21"
                ]

MODELS = OPENAI_MODELS + OLLAMA_MODELS + GEMINI_MODELS

def image_url(image):
    with open(image, "rb") as file:
         file_data = file.read()
         encoded_file = base64.b64encode(file_data).decode("utf-8")
         base64_url = f"data:image/jpeg;base64,{encoded_file}"
    return base64_url

def get_response(prompt, image_file, model):
    try:
        base64_url = image_url(image_file)
      
        image_content = [
            {"type": "text", 
             "text": prompt
            },
            {
                "type": "image_url",
                "image_url": { "url": base64_url }
            }
        ]
        response = completion(
            model=model,
            messages=[{"role": "user", "content": image_content}],
            temperature = 0.2,
            max_tokens  = 1000
        )
        return response.choices[0].message.content
    except FileNotFoundError:
        return f"Error: File '{image}' not found"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Analyze an image using AI models.")
    parser.add_argument("-i", "--image", required=True, help="Path to the image file (PDF, PNG, or JPG)")
    parser.add_argument("-p", "--prompt", default="Describe the image", help="Prompt to analyze the image")
    parser.add_argument("-m", "--model", type=int, choices=range(len(MODELS)), default=0, help="Index of the AI model to use (0-{})".format(len(MODELS)-1))
    args = parser.parse_args()

    model = MODELS[args.model]

    response = get_response(args.prompt, args.image, model)

    print(response)

if __name__ == "__main__":
    main()

