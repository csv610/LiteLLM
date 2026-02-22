"""Example showing how to extract structured data using Pydantic models."""

from pydantic import BaseModel, Field
from typing import List
from lite import LiteClient, ModelConfig, ModelInput

# 1. Define your output schema using Pydantic
class Ingredient(BaseModel):
    name: str
    amount: str
    unit: str

class Recipe(BaseModel):
    title: str
    prep_time: int = Field(description="Preparation time in minutes")
    ingredients: List[Ingredient]

# 2. Initialize the client
client = LiteClient(ModelConfig(model="gemini/gemini-2.5-flash"))

# 3. Request structured completion
print("--- Extracting Structured Data ---")
prompt = "Extract recipe info: Tomato Soup. 10 mins prep. 2 tomatoes, 500ml water, salt to taste."

user_input = ModelInput(
    user_prompt=prompt,
    response_format=Recipe # Pass the class here!
)

recipe = client.generate_text(user_input)

# Now 'recipe' is a validated Recipe object!
print(f"Recipe Title: {recipe.title}")
print(f"Prep Time: {recipe.prep_time} minutes")
print("Ingredients:")
for ing in recipe.ingredients:
    print(f"  - {ing.name}: {ing.amount} {ing.unit}")

print("Example complete!")
