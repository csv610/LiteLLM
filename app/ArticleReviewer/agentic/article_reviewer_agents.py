"""
article_reviewer_agents.py - Multi-agent implementation of the article reviewer using Pydantic AI.
"""

import json
from datetime import datetime, timezone
from typing import List, Optional, Any, Sequence
import anyio

from pydantic_ai import Agent, RunContext
from pydantic_ai.models import Model, ModelRequestParameters, ModelResponse
from pydantic_ai.messages import ModelMessage, TextPart, ModelRequest, ModelResponse as ModelResponseMsg
from pydantic_ai.settings import ModelSettings

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

from .article_reviewer_models import (
    DeleteModel, ModifyModel, InsertModel, ArticleReviewModel
)


class LiteModel(Model):
    """Custom Model implementation for Pydantic AI using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        self.lite_client = LiteClient(model_config=model_config)
        self.model_config = model_config
        super().__init__()

    async def request(
        self,
        messages: List[ModelMessage],
        model_settings: Optional[ModelSettings],
        model_request_parameters: ModelRequestParameters,
    ) -> ModelResponse:
        # Convert messages to a single prompt for LiteClient
        prompt_parts = []
        for msg in messages:
            role = "user"
            if isinstance(msg, ModelRequest):
                role = "user"
            elif isinstance(msg, ModelResponseMsg):
                role = "assistant"
            
            if hasattr(msg, 'parts'):
                for part in msg.parts:
                    if isinstance(part, TextPart):
                        prompt_parts.append(f"{role.upper()}: {part.content}")
                    elif hasattr(part, 'content') and part.content:
                        prompt_parts.append(f"{role.upper()}: {part.content}")
                    elif hasattr(part, 'tool_name'):
                        if role == 'assistant':
                            prompt_parts.append(f"CALL TOOL: {part.tool_name} with {part.args}")
                        else:
                            prompt_parts.append(f"TOOL RETURN: {part.tool_name} -> {part.content}")
        
        prompt = "\n".join(prompt_parts)
        
        # Inject JSON schema for structured output if applicable
        if model_request_parameters.output_object:
            schema = model_request_parameters.output_object.json_schema
            prompt += f"\n\nIMPORTANT: Return ONLY a JSON object matching this schema:\n{json.dumps(schema, indent=2)}"

        model_input = ModelInput(user_prompt=prompt)
        
        # Run sync LiteClient call in a thread
        response_content = await anyio.to_thread.run_sync(
            self.lite_client.generate_text, model_input
        )
        
        if not isinstance(response_content, str):
            if hasattr(response_content, "model_dump_json"):
                text_content = response_content.model_dump_json()
            else:
                text_content = json.dumps(response_content) if isinstance(response_content, (dict, list)) else str(response_content)
        else:
            text_content = response_content

        response = ModelResponse(
            parts=[TextPart(content=text_content)],
            model_name=self.model_config.model,
            timestamp=datetime.now(timezone.utc)
        )
        return response

    def name(self) -> str:
        return f"lite:{self.model_config.model}"
    
    @property
    def model_name(self) -> str:
        return self.model_config.model
    
    @property
    def system(self) -> str:
        return "lite"


class MultiAgentReviewer:
    """Orchestrator for the Multi-Agent Article Reviewer system."""

    def __init__(self, model_config: ModelConfig = None):
        """Initialize the multi-agent system with a model configuration."""
        if model_config is None:
            model_config = ModelConfig(model="ollama/gemma3", temperature=0.3)
            
        self.model = LiteModel(model_config)
        self._setup_agents()

    def _setup_agents(self):
        """Initialize and configure all specialized agents."""
        
        # 1. Deletions Agent
        self.deletions_agent = Agent(
            self.model,
            output_type=List[DeleteModel],
            system_prompt=(
                "You are an expert article reviewer specializing in deletions. "
                "Identify redundant, unnecessary, or irrelevant content. "
                "Do NOT include empty lines or whitespace issues. "
                "Return a JSON list of DeleteModel objects."
            )
        )

        # 2. Modifications Agent
        self.modifications_agent = Agent(
            self.model,
            output_type=List[ModifyModel],
            system_prompt=(
                "You are an expert article reviewer specializing in modifications. "
                "Improve clarity, grammar, and style. "
                "Return a JSON list of ModifyModel objects."
            )
        )

        # 3. Insertions Agent
        self.insertions_agent = Agent(
            self.model,
            output_type=List[InsertModel],
            system_prompt=(
                "You are an expert article reviewer specializing in insertions. "
                "Identify missing context, explanations, or structural elements. "
                "Return a JSON list of InsertModel objects."
            )
        )

        # 4. Manager Agent
        self.manager_agent = Agent(
            self.model,
            output_type=ArticleReviewModel,
            deps_type=str, # deps will be the article_text
            system_prompt=(
                "You are the Lead Article Reviewer. Orchestrate specialized reviewers "
                "(Deletions, Modifications, and Insertions) to provide a final report. "
                "Use your tools to gather feedback on the article provided in dependencies. "
                "Provide an overall quality score (0-100) and a brief summary."
            )
        )

        # Register tools to the manager instance
        @self.manager_agent.tool
        async def get_deletions(ctx: RunContext[str]) -> List[DeleteModel]:
            """Get specialized feedback on content that should be deleted."""
            result = await self.deletions_agent.run(ctx.deps)
            return result.output

        @self.manager_agent.tool
        async def get_modifications(ctx: RunContext[str]) -> List[ModifyModel]:
            """Get specialized feedback on content that should be modified."""
            result = await self.modifications_agent.run(ctx.deps)
            return result.output

        @self.manager_agent.tool
        async def get_insertions(ctx: RunContext[str]) -> List[InsertModel]:
            """Get specialized feedback on content that should be inserted."""
            result = await self.insertions_agent.run(ctx.deps)
            return result.output

    async def review(self, article_text: str) -> ArticleReviewModel:
        """Review an article using the Multi-Agent system."""
        prompt = f"Please review this article: \n\n{article_text[:500]}..." # Brief preview in prompt
        
        # Run manager with article_text as dependencies
        result = await self.manager_agent.run(prompt, deps=article_text)
        
        review = result.output
        # Ensure total_issues is accurate
        review.total_issues = len(review.deletions) + len(review.modifications) + len(review.insertions)
        
        return review


if __name__ == "__main__":
    async def test():
        reviewer = MultiAgentReviewer()
        article = "This is a test article. It is redundant. It is redundant."
        try:
            review = await reviewer.review(article)
            print("Review successful!")
            print(f"Score: {review.score}")
            print(f"Issues: {review.total_issues}")
        except Exception as e:
            print(f"Review failed: {e}")

    import asyncio
    asyncio.run(test())
