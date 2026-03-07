import argparse
import json
import logging
from typing import Any, Dict, List

from lite.config import ModelConfig

# External dependencies
from litellm import completion
from pydantic import BaseModel

# Internal MedKit Tools
from drug.medicine_explainer import explain_medicine
from recognizers.recognizer_factory import RecognizerFactory

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ToolOutput(BaseModel):
    tool_name: str
    result: Any
    status: str = "success"


class MedKitOrchestrator:
    """
    A professional agentic layer that coordinates specialized medical tools.
    Implements a ReAct (Reason-Act) loop for multi-step reasoning.
    """

    def __init__(
        self, model: str = "ollama/gemma3", temperature: float = 0.2, max_steps: int = 5
    ):
        self.model = model
        self.temperature = temperature
        self.max_steps = max_steps
        self.history = []
        self.tools = self._register_tools()

        self.system_prompt = """You are the MedKit Orchestrator, a high-reasoning medical agent.
Your goal is to assist clinicians by coordinating specialized medical tools.

### Operational Protocol:
1. **Analyze**: Break down complex queries into logical steps.
2. **Execute**: Use the appropriate tools to gather evidence.
3. **Reason**: After each tool call, analyze the observation and decide if more data is needed.
4. **Synthesize**: Provide a professional, structured clinical response.

### Available Tools:
- get_medicine_info: Explains a drug's mechanism, use, and side effects.
- identify_medical_entity: Identifies a specific medical entity (disease, sign, pathogen, etc.).
- search_icd11: Searches the official WHO ICD-11 database for codes (Requires credentials).
- anatomical_lookup: Provides detailed info on body parts and structures.

### Guidelines:
- If a tool returns an error, explain why and try an alternative if possible.
- If the query is ambiguous, ask the user for clarification before taking significant actions.
- Always include a medical disclaimer in your final answer.
"""

    def _register_tools(self) -> List[Dict]:
        return [
            {
                "name": "get_medicine_info",
                "description": "Explains a medication in simple, compassionate terms.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "medicine_name": {
                            "type": "string",
                            "description": "Generic name of the drug",
                        }
                    },
                    "required": ["medicine_name"],
                },
            },
            {
                "name": "identify_medical_entity",
                "description": "Identifies a medical entity (drug, disease, pathogen, clinical_sign, etc.).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "enum": [
                                "drug",
                                "disease",
                                "pathogen",
                                "clinical_sign",
                                "medical_symptom",
                                "medical_test",
                            ],
                        },
                        "entity_name": {"type": "string"},
                    },
                    "required": ["entity_type", "entity_name"],
                },
            },
            {
                "name": "search_icd11",
                "description": "Searches for ICD-11 codes for a given condition.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The medical condition to search for",
                        }
                    },
                    "required": ["query"],
                },
            },
        ]

    def call_tool(self, tool_name: str, args: Dict) -> ToolOutput:
        logger.info(f"🔧 Executing: {tool_name}({args})")

        try:
            if tool_name == "get_medicine_info":
                res = explain_medicine(args["medicine_name"])
                return ToolOutput(tool_name=tool_name, result=res)

            elif tool_name == "identify_medical_entity":
                config = ModelConfig(model=self.model)
                recognizer = RecognizerFactory.get(args["entity_type"], config)
                result = recognizer.identify(args["entity_name"])
                if hasattr(result, "markdown") and result.markdown:
                    return ToolOutput(tool_name=tool_name, result=result.markdown)
                return ToolOutput(tool_name=tool_name, result=str(result))

            elif tool_name == "search_icd11":
                import os

                from med_codes.get_icd11 import ICD11Client

                client_id = os.environ.get("ICD11_CLIENT_ID")
                client_secret = os.environ.get("ICD11_CLIENT_SECRET")
                if not client_id or not client_secret:
                    return ToolOutput(
                        tool_name=tool_name,
                        status="error",
                        result="ICD-11 API credentials missing in environment.",
                    )

                client = ICD11Client(client_id, client_secret)
                results = client.search(args["query"])
                if results and "destinationEntities" in results:
                    summary = []
                    for entity in results["destinationEntities"][:5]:
                        title = (
                            entity.get("title", "")
                            .replace("<em class='found'>", "")
                            .replace("</em>", "")
                        )
                        summary.append(
                            f"Code: {entity.get('theCode', 'N/A')} | {title}"
                        )
                    return ToolOutput(tool_name=tool_name, result="\n".join(summary))
                return ToolOutput(
                    tool_name=tool_name, result="No matching ICD-11 codes found."
                )

            return ToolOutput(
                tool_name=tool_name,
                result=f"Tool '{tool_name}' not implemented.",
                status="error",
            )
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return ToolOutput(tool_name=tool_name, result=str(e), status="error")

    def run(self, query: str):
        print(f"\n[USER]: {query}")
        self.history.append({"role": "user", "content": query})

        for step in range(self.max_steps):
            print(f"--- Step {step + 1} ---")

            response = completion(
                model=self.model,
                messages=[{"role": "system", "content": self.system_prompt}]
                + self.history,
                functions=self.tools,
                function_call="auto",
                temperature=self.temperature,
            )

            message = response.choices[0].message

            # Check for tool call
            function_call = (
                message.get("function_call")
                if isinstance(message, dict)
                else getattr(message, "function_call", None)
            )

            if function_call:
                tool_name = (
                    function_call["name"]
                    if isinstance(function_call, dict)
                    else function_call.name
                )
                args_str = (
                    function_call["arguments"]
                    if isinstance(function_call, dict)
                    else function_call.arguments
                )
                tool_args = json.loads(args_str)

                observation = self.call_tool(tool_name, tool_args)

                # Update history with tool call and result
                self.history.append(message)
                self.history.append(
                    {
                        "role": "function",
                        "name": tool_name,
                        "content": str(observation.result),
                    }
                )

                print(f"[OBSERVATION]: {str(observation.result)[:200]}...")

            else:
                # No more tools needed, this is the final answer
                content = (
                    message.get("content")
                    if isinstance(message, dict)
                    else getattr(message, "content", "")
                )
                print(f"\n[ORCHESTRATOR]: {content}")
                return content

        print(
            "\n[ORCHESTRATOR]: Max reasoning steps reached. Please refine your query."
        )
        return "Max steps reached."


def main():
    # Add the project root to sys.path to ensure modules are found
    import sys
    from pathlib import Path

    project_root = str(Path(__file__).parent.parent)
    if project_root not in sys.path:
        sys.path.append(project_root)

    parser = argparse.ArgumentParser(description="MedKit Orchestrator CLI")
    parser.add_argument("query", nargs="?", help="The medical query to solve")
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use")
    parser.add_argument(
        "-t", "--temperature", type=float, default=0.2, help="Temperature for the model"
    )
    parser.add_argument(
        "-s", "--steps", type=int, default=5, help="Max reasoning steps"
    )

    args = parser.parse_args()

    orchestrator = MedKitOrchestrator(
        model=args.model, temperature=args.temperature, max_steps=args.steps
    )

    if args.query:
        orchestrator.run(args.query)
    else:
        print("Welcome to MedKit Orchestrator. Type 'exit' to quit.")
        while True:
            try:
                user_input = input("\n> ").strip()
                if user_input.lower() in ["exit", "quit"]:
                    break
                if not user_input:
                    continue
                orchestrator.run(user_input)
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    main()
