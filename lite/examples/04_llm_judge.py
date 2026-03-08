"""Example showing how to use the LLM-as-a-judge for evaluating model responses."""

from lite import ResponseJudge, ModelConfig, UserInput

# 1. Initialize the Judge
# By default, uses gemini-2.5-flash
judge_config = ModelConfig(model="gemini/gemini-2.5-flash")
judge = ResponseJudge(model_config=judge_config)

# 2. Evaluate a response against a prompt and ground truth
print("--- LLM Judge Evaluation ---")
user_input = UserInput(
    user_prompt="Who wrote the play Romeo and Juliet?",
    model_response="William Shakespeare is the author.",
    ground_truth="William Shakespeare"
)

# 3. Perform evaluation
evaluation = judge.evaluate(user_input)

# 4. Access evaluation scores and reasoning
print(f"Overall Score: {evaluation.overall_score:.2f}")
print(f"Is Correct:    {evaluation.is_correct}")
print(f"Reasoning:     {evaluation.reasoning}")
print("\nCriteria Scores:")
print(f"  Accuracy:     {evaluation.criteria.accuracy:.2f}")
print(f"  Completeness: {evaluation.criteria.completeness:.2f}")
print(f"  Relevance:    {evaluation.criteria.relevance:.2f}")
print(f"  Clarity:      {evaluation.criteria.clarity:.2f}")

print("\nExample complete!")
