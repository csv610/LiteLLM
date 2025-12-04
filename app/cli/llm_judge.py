import argparse
import json
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any, List

from pydantic import BaseModel, Field, ValidationError

# Internal imports
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput


# ============================================================
# ======================  Criteria Enum  ======================
# ============================================================

class JudgingCriteria(str, Enum):
    HELPFULNESS = "helpfulness"
    ACCURACY = "accuracy"
    RELEVANCE = "relevance"
    SAFETY = "safety"
    CLARITY = "clarity"
    COMPLETENESS = "completeness"
    COHERENCE = "coherence"
    FACTUAL_CORRECTNESS = "factual_correctness"
    BIAS_DETECTION = "bias_detection"
    TOXICITY = "toxicity"
    REASONING_QUALITY = "reasoning_quality"
    INSTRUCTION_ADHERENCE = "instruction_adherence"
    CONCISENESS = "conciseness"

    @classmethod
    def list(cls) -> List[str]:
        return [c.value for c in cls]


# ============================================================
# ======================  Config Models  ======================
# ============================================================

class JudgeConfig(BaseModel):
    model: str = Field(default="gemini/gemini-2.5-flash")
    temperature: float = Field(default=0.1, ge=0, le=2)


# ============================================================
# ====================== Output Models ========================
# ============================================================

class CriterionEvaluation(BaseModel):
    """Single criterion score and explanation."""
    score: float = Field(default=0.0, ge=0.0, le=10.0, description="Score (0-10)")
    explanation: str = Field(default="", description="Explanation of the score")


class EvalScores(BaseModel):
    """All criteria scores and explanations."""
    helpfulness: CriterionEvaluation = Field(default_factory=CriterionEvaluation)
    accuracy: CriterionEvaluation = Field(default_factory=CriterionEvaluation)
    relevance: CriterionEvaluation = Field(default_factory=CriterionEvaluation)
    safety: CriterionEvaluation = Field(default_factory=CriterionEvaluation)
    clarity: CriterionEvaluation = Field(default_factory=CriterionEvaluation)
    completeness: CriterionEvaluation = Field(default_factory=CriterionEvaluation)
    coherence: CriterionEvaluation = Field(default_factory=CriterionEvaluation)
    factual_correctness: CriterionEvaluation = Field(default_factory=CriterionEvaluation)
    bias_detection: CriterionEvaluation = Field(default_factory=CriterionEvaluation)
    toxicity: CriterionEvaluation = Field(default_factory=CriterionEvaluation)
    reasoning_quality: CriterionEvaluation = Field(default_factory=CriterionEvaluation)
    instruction_adherence: CriterionEvaluation = Field(default_factory=CriterionEvaluation)
    conciseness: CriterionEvaluation = Field(default_factory=CriterionEvaluation)


class JudgmentResult(BaseModel):
    """Final judgment result."""
    criteria: EvalScores = Field(default_factory=EvalScores)
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Confidence in evaluation (0-1)")

    def format_output(self) -> Dict[str, Any]:
        """Format result as nested criteria structure."""
        return {
            "criteria": self.criteria.model_dump(),
            "confidence": self.confidence,
        }


class ComparisonResult(BaseModel):
    """Result of comparing two responses."""
    response1: EvalScores = Field(default_factory=EvalScores)
    response2: EvalScores = Field(default_factory=EvalScores)
    winner: Optional[int] = Field(default=None, description="Winner: 0 for response1, 1 for response2, null for tie")
    explanation: str = Field(default="", description="Explanation of comparison results")
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Confidence in comparison (0-1)")

    def format_output(self) -> Dict[str, Any]:
        """Format result as nested criteria structure for both responses."""
        return {
            "response1": self.response1.model_dump(),
            "response2": self.response2.model_dump(),
            "winner": self.winner,
            "explanation": self.explanation,
            "confidence": self.confidence,
        }


# ============================================================
# ==================== Prompt Builder =========================
# ============================================================

class PromptBuilder:
    """Generates evaluation prompts with audience-awareness and fairness."""

    @staticmethod
    def single_evaluation_prompt(content: str, context: Optional[str] = None) -> str:
        ctx = f"Context: {context}\n" if context else ""

        return f"""
You are a professional evaluator trained to assess content quality across multiple criteria.
Your evaluations must be FAIR, CONSISTENT, and AUDIENCE-AWARE.

Before scoring, determine the **intended audience**:
- If the writing is for a general audience, score according to consumer-information standards.
- If it is technical, score according to expert-level expectations.
Do NOT penalize the response for excluding details that would be unsafe or inappropriate for laypersons.

Evaluate the content using the following criteria: {", ".join(JudgingCriteria.list())}.

SCORING SCALE:
9-10: Exceptional — accurate, thorough, audience-appropriate.
7-8: Strong — high quality with minor issues.
5-6: Adequate — understandable but missing notable elements.
3-4: Weak — significant omissions or unclear.
0-2: Very poor — incorrect, unsafe, incoherent, or severely lacking.

GUIDELINES:
- Helpfulness: practical usefulness for the intended audience.
- Accuracy: factual correctness.
- Relevance: stays on topic.
- Safety: absence of harmful advice; appropriate level of medical detail.
- Clarity: readability & structure.
- Completeness: adequate depth relative to audience expectations.
- Coherence: logical flow.
- Factual correctness: alignment with established scientific knowledge.
- Bias detection: neutrality.
- Toxicity: absence of harmful tone.
- Reasoning quality: logical soundness of arguments and explanations.
- Instruction adherence: how well the response follows given instructions.
- Conciseness: efficiency and brevity without sacrificing clarity.

{ctx}
Content to evaluate:
\"\"\"{content}\"\"\"

For each criterion:
1. Provide a score (0–10).
2. Provide a concise explanation identifying strengths AND weaknesses.

Return JSON with:
- scores: {{criterion: number}}
- explanations: {{criterion: string}}
- confidence: 0–1
"""

    @staticmethod
    def comparison_prompt(response1: str, response2: str, context: Optional[str] = None) -> str:
        ctx = f"Context: {context}\n" if context else ""

        return f"""
You are a professional evaluator comparing two responses.
Your evaluations must be FAIR, CONSISTENT, and AUDIENCE-AWARE.

Before scoring, infer the intended audience and adjust expectations accordingly.

CRITERIA: {", ".join(JudgingCriteria.list())}

For each criterion:
1. Score Response 1 (0–10)
2. Score Response 2 (0–10)
3. Identify strengths and weaknesses of each

Winner rules:
- Declare a winner (0 or 1) ONLY if one response is clearly superior.
- If quality is comparable, mark winner = null.

{ctx}

Response 1:
\"\"\"{response1}\"\"\"

Response 2:
\"\"\"{response2}\"\"\"

Return JSON:
- response1_scores
- response2_scores
- winner
- explanation (why)
- confidence
"""


# ============================================================
# ====================== LLM Judge ===========================
# ============================================================

class LLMJudge:
    def __init__(self, config: JudgeConfig):
        self.config = config
        self.model_config = ModelConfig(
            model=config.model,
            temperature=config.temperature
        )
        self.client = LiteClient(model_config=self.model_config)

    @staticmethod
    def _transform_to_criteria_scores(data: Dict[str, Any], prefix: str = "") -> EvalScores:
        """Transform flat response data into nested EvalScores structure."""
        criteria_names = [
            "helpfulness", "accuracy", "relevance", "safety", "clarity",
            "completeness", "coherence", "factual_correctness", "bias_detection", "toxicity",
            "reasoning_quality", "instruction_adherence", "conciseness"
        ]
        criteria = {}

        for name in criteria_names:
            score_key = f"{prefix}{name}" if prefix else name
            explanation_key = f"{prefix}{name}_explanation" if prefix else f"{name}_explanation"

            score = data.get(score_key, 0.0)
            explanation = data.get(explanation_key, "")
            criteria[name] = CriterionEvaluation(score=score, explanation=explanation)

        return EvalScores(**criteria)

    def evaluate(self, content: str, context: Optional[str] = None) -> Dict[str, Any]:
        prompt = PromptBuilder.single_evaluation_prompt(content, context)
        try:
            model_input = ModelInput(user_prompt=prompt, response_format=JudgmentResult)
            output = self.client.generate_text(model_input=model_input)

            if isinstance(output, str):
                data = json.loads(output)
            else:
                data = output

            criteria = self._transform_to_criteria_scores(data)
            confidence = data.get("confidence")
            result = JudgmentResult(criteria=criteria, confidence=confidence)
            return result.format_output()

        except Exception as e:
            result = JudgmentResult(confidence=0.0)
            return result.format_output()

    def compare(self, r1: str, r2: str, context: Optional[str] = None) -> Dict[str, Any]:
        prompt = PromptBuilder.comparison_prompt(r1, r2, context)
        try:
            model_input = ModelInput(user_prompt=prompt, response_format=ComparisonResult)
            output = self.client.generate_text(model_input=model_input)

            if isinstance(output, str):
                data = json.loads(output)
            else:
                data = output

            response1 = self._transform_to_criteria_scores(data, prefix="response1_")
            response2 = self._transform_to_criteria_scores(data, prefix="response2_")
            winner = data.get("winner")
            explanation = data.get("explanation", "")
            confidence = data.get("confidence")

            result = ComparisonResult(
                response1=response1,
                response2=response2,
                winner=winner,
                explanation=explanation,
                confidence=confidence
            )
            return result.format_output()

        except Exception as e:
            result = ComparisonResult(
                winner=None,
                explanation=f"Error: {str(e)}",
                confidence=0.0
            )
            return result.format_output()


# ============================================================
# ========================= Utilities =========================
# ============================================================

def load_input(item: str) -> str:
    path = Path(item)
    if path.is_file():
        text = path.read_text()
        try:
            if path.suffix.lower() == ".json":
                return json.dumps(json.loads(text), indent=2)
        except Exception:
            pass
        return text
    return item


# ============================================================
# ========================= CLI Runner ========================
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="LLM Judge Framework")
    parser.add_argument("-c", "--content", help="Optional context or reference text")
    parser.add_argument("-r", "--responses", nargs="+", required=True)
    parser.add_argument("-m", "--model", default="gemini/gemini-2.5-flash")
    parser.add_argument("-t", "--temperature", type=float, default=0.1)
    parser.add_argument("-o", "--output", help="Output JSON file")

    args = parser.parse_args()

    config = JudgeConfig(model=args.model, temperature=args.temperature)
    judge = LLMJudge(config=config)

    context = load_input(args.content) if args.content else None

    if len(args.responses) == 1:
        content = load_input(args.responses[0])
        output = judge.evaluate(content=content, context=context)
    else:
        r1 = load_input(args.responses[0])
        r2 = load_input(args.responses[1])
        output = judge.compare(r1=r1, r2=r2, context=context)

    if args.output:
        Path(args.output).write_text(json.dumps(output, indent=2))
        print(f"Saved to {args.output}")
    else:
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

