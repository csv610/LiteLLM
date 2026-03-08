"""Example of using the LiteMCQClient to solve multiple-choice questions."""

from lite import LiteMCQClient, MCQInput

# 1. Initialize the MCQ Client
# It handles the specialized prompting for you
client = LiteMCQClient(model="gemini/gemini-2.5-flash")

# 2. Solve a simple question
print("--- Solving a Multiple-Choice Question ---")
question = MCQInput(
    question="Which of these is the capital of France?",
    options=["Berlin", "Paris", "London", "Rome"],
    context="The question is about major European capitals."
)

answer = client.solve(question)

# 3. Display the result
print(f"Question: {question.question}")
print(f"Options: {question.options}")
print(f"Correct Option: {answer.correct_options[0].key} - {answer.correct_options[0].value}")
print(f"Reasoning: {answer.reasoning}")

print("\nExample complete!")
