from lite import LiteClient, ModelConfig
from lite.config import ModelInput
from ArticleReviewer.agentic.article_reviewer_models import ArticleReviewModel
import os
import json

def test():
    model = "ollama/gemma3:12b-cloud"
    config = ModelConfig(model=model, temperature=0.3)
    client = LiteClient(model_config=config)
    
    schema = ArticleReviewModel.model_json_schema()
    
    prompt = f"""Review the following article: 'The quick brown fox jumps over the lazy dog. This is a redundant sentence.'
    
Return the review ONLY in JSON format following this schema:
{json.dumps(schema, indent=2)}
"""
    
    model_input = ModelInput(
        user_prompt=prompt,
        response_format=ArticleReviewModel
    )
    
    print(f"Testing model: {model}")
    try:
        from litellm import completion
        messages = client.create_message(model_input)
        response = completion(
            model=model,
            messages=messages,
            temperature=0.3,
        )
        raw_content = response.choices[0].message.content
        print(f"RAW CONTENT:\n{raw_content}")
        
        from lite.utils.json_cleaner import JSONCleaner
        cleaned = JSONCleaner.extract_json(raw_content)
        print(f"CLEANED JSON:\n{cleaned}")
        
        parsed = ArticleReviewModel.model_validate_json(cleaned)
        print("SUCCESSFULLY PARSED")
        print(parsed.model_dump_json(indent=2))
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test()
