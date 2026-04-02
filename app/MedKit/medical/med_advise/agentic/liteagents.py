"""
liteagents.py - Unified for med_advise
"""
from typing import Any, Type\nimport gradio as gr\nfrom .primary_health_care_models import ModelOutput, PrimaryCareResponseModel\nfrom app.MedKit.medical.med_advise.shared.models import *\nfrom lite.config import ModelConfig\nfrom lite.logging_config import configure_logging\nimport sys\nfrom typing import Optional\nfrom tqdm import tqdm\nimport pytest\nfrom .primary_health_care_prompts import PromptBuilder\nfrom .primary_health_care_models import (\nfrom lite.config import ModelConfig, ModelInput\nfrom .primary_health_care_agents import (\nimport logging\nfrom pathlib import Path\nimport os\nfrom unittest.mock import MagicMock, patch\nfrom lite.utils import save_model_response\nfrom lite.lite_client import LiteClient\nimport argparse\n\n"""Specialized agents for primary health care."""



    TriageResponseModel,
    EducationResponseModel,
    SelfCareResponseModel,
    ClinicalResponseModel,
)

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for primary care agents."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)

    def _generate(
        self,
        query: str,
        system_prompt: str,
        response_format: Type[Any],
        context: str = "",
    ) -> Any:
        user_prompt = PromptBuilder.create_user_prompt(query, context)
        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )
        result = self.client.generate_text(model_input=model_input)
        return result.data


class TriageAgent(BaseAgent):
    """Agent specialized in understanding the user's health concern."""

    def process(self, query: str) -> TriageResponseModel:
        logger.debug("TriageAgent: Processing query...")
        return self._generate(
            query, PromptBuilder.create_triage_system_prompt(), TriageResponseModel
        )


class EducatorAgent(BaseAgent):
    """Agent specialized in providing medical explanations."""

    def process(self, query: str, context: str) -> EducationResponseModel:
        logger.debug("EducatorAgent: Providing medical background...")
        return self._generate(
            query,
            PromptBuilder.create_education_system_prompt(),
            EducationResponseModel,
            context,
        )


class AdvisorAgent(BaseAgent):
    """Agent specialized in practical self-care advice."""

    def process(self, query: str, context: str) -> SelfCareResponseModel:
        logger.debug("AdvisorAgent: Offering self-care advice...")
        return self._generate(
            query,
            PromptBuilder.create_advisor_system_prompt(),
            SelfCareResponseModel,
            context,
        )


class ClinicalAgent(BaseAgent):
    """Agent specialized in clinical guidance and red flags."""

    def process(self, query: str, context: str) -> ClinicalResponseModel:
        logger.debug("ClinicalAgent: Defining clinical red flags...")
        return self._generate(
            query,
            PromptBuilder.create_clinical_system_prompt(),
            ClinicalResponseModel,
            context,
        )

class PromptBuilder:
    """Builder class for creating prompts for a primary health care provider persona."""

    @staticmethod
    def create_system_prompt() -> str:
        """Creates the system prompt for a primary health care provider."""
        return """You are a knowledgeable primary health care provider. 
You have a broad understanding of the medical field but are not a specialist in any specific area.
Your goal is to provide clear, accessible, and helpful medical information to patients who may have general health questions or concerns.

Guidelines:
- Use clear, non-technical language where possible. Explain medical terms simply if you must use them.
- Focus on general health advice, common conditions, prevention, and wellness.
- Provide balanced information that helps the patient understand their situation from a generalist's perspective.
- If a situation sounds serious or outside the scope of primary care, advise the patient on when to seek urgent care or see a specialist.
- Be empathetic, professional, and supportive.
- Do NOT provide specific prescriptions or dosages.
- Do NOT claim to be a specialist.
- Base your information on established medical guidelines but keep it accessible for a general audience.
- Do not add any preamble and disclaimers in the output.

Structure your response using these sections:
- Understanding Your Concern: A brief summary of the issue.
- Common Symptoms and Observations: What these symptoms typically mean in a general context.
- General Advice and Self-Care: Practical steps the patient can take.
- When to Seek Medical Attention: Clear indicators for when to see a doctor or go to the ER.
- Next Steps: Recommended questions for their next appointment or further actions.
"""

    @staticmethod
    def create_user_prompt(query: str) -> str:
        """Creates the user prompt for a patient query.

        Args:
            query: The patient's question or topic of concern.

        Returns:
            A formatted user prompt string.
        """
        return f"As a primary health care provider, give medically accurate information on the question: {query}"

"""Primary Health Care Advice CLI."""



# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


try:
    from .primary_health_care import PrimaryHealthCareProvider
except (ImportError, ValueError):
    from medical.med_advise.agentic.primary_health_care import PrimaryHealthCareProvider

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Get primary health care advice.")
    parser.add_argument("query", help="Health concern or file path containing queries.")
    parser.add_argument(
        "-d", "--output-dir", default="outputs", help="Output directory."
    )
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use.")
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Verbosity level.",
    )
    parser.add_argument(
        "-s", "--structured", action="store_true", help="Use structured output."
    )
    return parser.parse_args()


def main():
    args = get_user_arguments()
    configure_logging(
        log_file="primary_health_care.log",
        verbosity=args.verbosity,
        enable_console=True,
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.query)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.query]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        provider = PrimaryHealthCareProvider(model_config)

        for item in tqdm(items, desc="Processing"):
            result = provider.generate_text(query=item, structured=args.structured)
            if result:
                provider.save(result, output_dir)

        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())

"""
primary_health_care_gradio.py - Gradio interface for the Primary Health Care Advisor application.
"""


# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Add the project root to sys.path
path = Path(__file__).parent
while path.name != "app" and path.parent != path:
    path = path.parent
if path.name == "app":
    root = path.parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))


try:
    from .primary_health_care import PrimaryHealthCareProvider
except (ImportError, ValueError):
    try:
        from medical.med_advise.agentic.primary_health_care import (
            PrimaryHealthCareProvider,
        )
    except (ImportError, ValueError):
        from medical.med_advise.agentic.primary_health_care import (
            PrimaryHealthCareProvider,
        )


def get_health_advice(query: str, model_name: str, structured: bool):
    """Get primary health care advice for a health concern."""
    if not query.strip():
        return "Please enter a health concern or question."

    try:
        model_config = ModelConfig(model=model_name, temperature=0.2)
        provider = PrimaryHealthCareProvider(model_config)
        result = provider.generate_text(query=query.strip(), structured=structured)

        if result:
            # Save result to outputs directory
            output_dir = Path("outputs")
            output_dir.mkdir(exist_ok=True)
            # Create a safe filename from the query
            safe_query = "".join(c if c.isalnum() else "_" for c in query.strip())[:50]
            output_file = output_dir / f"health_advice_{safe_query.lower()}.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result)

            return f"""## Primary Health Care Advice

**Your Question:** {query}

{result}

---
*Advice saved to: {output_file}*"""
        else:
            return f"Unable to generate advice for: {query}"

    except Exception as e:
        return f"Error generating health advice: {str(e)}"


def process_health_queries_file(file_path, model_name: str, structured: bool):
    """Process a file containing multiple health queries."""
    if not file_path:
        return "Please upload a file with health queries."

    if not os.path.exists(file_path.name):
        return f"File not found: {file_path.name}"

    try:
        # Read queries from file
        with open(file_path.name, "r", encoding="utf-8") as f:
            queries = [line.strip() for line in f if line.strip()]

        if not queries:
            return "The file is empty or contains no valid queries."

        model_config = ModelConfig(model=model_name, temperature=0.2)
        provider = PrimaryHealthCareProvider(model_config)

        results = []
        for query in queries:
            result = provider.generate_text(query=query, structured=structured)
            if result:
                results.append(f"**Query:** {query}\n\n{result}\n\n{'-' * 50}\n")

        if results:
            # Save combined results
            output_dir = Path("outputs")
            output_dir.mkdir(exist_ok=True)
            output_file = output_dir / "health_advice_batch.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n\n".join(results))

            return f"""## Batch Health Advice Results

Processed {len(queries)} health queries.

{chr(10).join(results)}

---
*All advice saved to: {output_file}*"""
        else:
            return "Unable to generate advice for any of the queries."

    except Exception as e:
        return f"Error processing health queries file: {str(e)}"


def create_gradio_interface():
    """Create and return the Gradio interface."""
    with gr.Blocks(title="Primary Health Care Advisor") as interface:
        gr.Markdown("# 🏥 Primary Health Care Advisor")
        gr.Markdown(
            "Get preliminary health information and advice for common health concerns."
        )

        with gr.Tabs():
            # Single Query Tab
            with gr.TabItem("💬 Single Health Query"):
                with gr.Row():
                    with gr.Column():
                        query_input = gr.Textbox(
                            label="Health Concern or Question",
                            placeholder="Describe your health concern or question (e.g., 'I have a headache and fever', 'What are symptoms of diabetes?')",
                            lines=3,
                        )
                        model_dropdown = gr.Dropdown(
                            label="LLM Model",
                            choices=[
                                "ollama/gemma3",
                                "ollama/llama3",
                                "ollama/mistral",
                                "gpt-3.5-turbo",
                                "gpt-4",
                                "claude-3-haiku-20240307",
                                "claude-3-sonnet-20240229",
                            ],
                            value="ollama/gemma3",
                        )
                        structured_checkbox = gr.Checkbox(
                            label="Structured Output", value=False
                        )
                        advice_btn = gr.Button("Get Health Advice", variant="primary")

                    with gr.Column():
                        advice_output = gr.Markdown(label="Health Advice")

                advice_btn.click(
                    fn=get_health_advice,
                    inputs=[query_input, model_dropdown, structured_checkbox],
                    outputs=advice_output,
                )

                gr.Markdown("""
                ### About Single Health Queries
                Enter a specific health concern or question to get preliminary information and advice.
                The advisor provides general health information but is not a substitute for professional medical consultation.
                """)

            # Batch Processing Tab
            with gr.TabItem("📄 Multiple Queries from File"):
                with gr.Row():
                    with gr.Column():
                        file_input = gr.File(
                            label="Upload File with Health Queries",
                            file_types=[".txt"],
                            type="filepath",
                        )
                        batch_model_dropdown = gr.Dropdown(
                            label="LLM Model",
                            choices=[
                                "ollama/gemma3",
                                "ollama/llama3",
                                "ollama/mistral",
                                "gpt-3.5-turbo",
                                "gpt-4",
                                "claude-3-haiku-20240307",
                                "claude-3-sonnet-20240229",
                            ],
                            value="ollama/gemma3",
                        )
                        batch_structured_checkbox = gr.Checkbox(
                            label="Structured Output", value=False
                        )
                        batch_btn = gr.Button(
                            "Process Health Queries", variant="primary"
                        )

                    with gr.Column():
                        batch_output = gr.Markdown(label="Batch Results")

                batch_btn.click(
                    fn=process_health_queries_file,
                    inputs=[
                        file_input,
                        batch_model_dropdown,
                        batch_structured_checkbox,
                    ],
                    outputs=batch_output,
                )

                gr.Markdown("""
                ### About Batch Processing
                Upload a text file containing multiple health queries (one per line) to get advice for all of them.
                Each query should be on a separate line in the file.
                """)

        gr.Markdown("""
        ### How to Use
        1. **Single Health Query**: Enter your health concern or question and click "Get Health Advice"
        2. **Multiple Queries**: Upload a text file with health queries (one per line) and click "Process Health Queries"
        3. Select your preferred LLM model
        4. Optionally enable structured output for formatted results
        5. Advice will be displayed and automatically saved to the `outputs` directory
        
        ### Important Disclaimer
        ⚠️ **This tool provides general health information only and is NOT a substitute for professional medical advice, diagnosis, or treatment.**
        - Always consult with a qualified healthcare provider for medical concerns
        - In case of emergency, call emergency services immediately
        - This advisor does not replace professional medical judgment
        """)

    return interface


if __name__ == "__main__":
    interface = create_gradio_interface()
    interface.launch(server_name="0.0.0.0", server_port=7869, share=False)


# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))



    ClinicalResponseModel,
    EducationResponseModel,
    ModelOutput,
    PrimaryCareResponseModel,
    SelfCareResponseModel,
    TriageResponseModel,
)


@pytest.fixture
def mock_lite_client():
    # Patch LiteClient in primary_health_care_agents
    with patch("medical.med_advise.agentic.primary_health_care_agents.LiteClient") as mock:
        yield mock


def test_primary_health_care_provider_init():
    config = ModelConfig(model="test-model")
    provider = PrimaryHealthCareProvider(config)
    assert provider.model_config == config
    assert provider.triage_agent is not None
    assert provider.educator_agent is not None
    assert provider.advisor_agent is not None
    assert provider.clinical_agent is not None


def test_generate_text_multi_agent(mock_lite_client):
    config = ModelConfig(model="test-model")
    provider = PrimaryHealthCareProvider(config)

    # Set up mock responses for each agent
    mock_triage_output = MagicMock()
    mock_triage_output.data = TriageResponseModel(
        understanding_concern="Cough", common_symptoms=["Cough", "Fever"]
    )

    mock_edu_output = MagicMock()
    mock_edu_output.data = EducationResponseModel(general_explanation="A chronic cough")

    mock_advisor_output = MagicMock()
    mock_advisor_output.data = SelfCareResponseModel(self_care_advice="Rest")

    mock_clinical_output = MagicMock()
    mock_clinical_output.data = ClinicalResponseModel(
        when_to_seek_care="Fever", next_steps=["See doctor"]
    )

    # Mock sequential calls to generate_text
    # Since all agents share the same LiteClient (mocked), we define side_effect
    mock_instance = mock_lite_client.return_value
    mock_instance.generate_text.side_effect = [
        mock_triage_output,
        mock_edu_output,
        mock_advisor_output,
        mock_clinical_output,
    ]

    result = provider.generate_text("I have a cough", structured=True)

    assert result.data.understanding_concern == "Cough"
    assert "Cough" in result.data.common_symptoms
    assert result.data.general_explanation == "A chronic cough"
    assert result.data.self_care_advice == "Rest"
    assert result.data.when_to_seek_care == "Fever"
    assert "See doctor" in result.data.next_steps

    # Verify markdown is generated
    assert "# Understanding Your Concern" in result.markdown
    assert "Cough" in result.markdown

#!/usr/bin/env python3
"""
Primary Health Care module.

This module provides the PrimaryHealthCareProvider class for addressing
patient questions with a multi-agentic perspective.
"""



    TriageAgent,
    EducatorAgent,
    AdvisorAgent,
    ClinicalAgent,
)

logger = logging.getLogger(__name__)


class PrimaryHealthCareProvider:
    """Orchestrates multiple agents to provide general medical information."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.triage_agent = TriageAgent(model_config)
        self.educator_agent = EducatorAgent(model_config)
        self.advisor_agent = AdvisorAgent(model_config)
        self.clinical_agent = ClinicalAgent(model_config)
        self.query = None
        logger.debug("Initialized Multi-Agent PrimaryHealthCareProvider")

    def generate_text(self, query: str, structured: bool = False) -> ModelOutput:
        """Addresses health concern using a 3-tier multi-agent system."""
        if not query or not str(query).strip():
            raise ValueError("Query cannot be empty")

        self.query = query
        logger.info(f"Addressing 3-tier health concern: {query}")

        try:
            # 1. Specialist Stage (JSON)
            logger.debug("Tier 1: Specialists processing concern...")
            triage_data = self.triage_agent.process(query)
            context = (
                f"Understanding Concern: {triage_data.understanding_concern}\n"
                f"Symptoms: {', '.join(triage_data.common_symptoms)}"
            )
            education_data = self.educator_agent.process(query, context)
            advisor_data = self.advisor_agent.process(query, context)
            clinical_data = self.clinical_agent.process(query, context)

            spec_data = PrimaryCareResponseModel(
                understanding_concern=triage_data.understanding_concern,
                common_symptoms=triage_data.common_symptoms,
                general_explanation=education_data.general_explanation,
                self_care_advice=advisor_data.self_care_advice,
                when_to_seek_care=clinical_data.when_to_seek_care,
                next_steps=clinical_data.next_steps,
            )
            spec_json = spec_data.model_dump_json(indent=2)

            # 2. Auditor Stage (JSON Audit)
            logger.debug("Tier 2: Auditor checking safety...")
            audit_sys, audit_usr = PromptBuilder.get_compliance_auditor_prompts(query, spec_json)
            audit_input = ModelInput(
                system_prompt=audit_sys,
                user_prompt=audit_usr,
                response_format=None # Audit result
            )
            audit_res = self.advisor_agent.client.generate_text(model_input=audit_input)
            audit_json = audit_res.markdown

            # 3. Final Synthesis Stage (Markdown)
            logger.debug("Tier 3: Output Agent synthesizing final response...")
            out_sys, out_usr = PromptBuilder.get_output_synthesis_prompts(query, spec_json, audit_json)
            out_input = ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None,
            )
            final_res = self.advisor_agent.client.generate_text(model_input=out_input)

            logger.info("✓ Successfully generated 3-tier health advice")
            return ModelOutput(
                data=spec_data if structured else None, 
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier advice generation failed: {e}")
            raise

    def _format_markdown(self, data: PrimaryCareResponseModel) -> str:
        """Formats the synthesized response into markdown."""
        sections = [
            f"# Understanding Your Concern\n{data.understanding_concern}",
            f"# Common Symptoms and Observations\n"
            + "\n".join([f"- {s}" for s in data.common_symptoms]),
            f"# General Explanation\n{data.general_explanation}",
            f"# General Advice and Self-Care\n{data.self_care_advice}",
            f"# When to Seek Medical Attention\n{data.when_to_seek_care}",
            f"# Next Steps\n" + "\n".join([f"- {s}" for s in data.next_steps]),
        ]
        return "\n\n".join(sections)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the provider's response to a file."""
        if self.query is None:
            raise ValueError("No query information available.")

        safe_query = "".join(
            [c if c.isalnum() else "_" for c in self.query[:30].lower()]
        ).strip("_")
        base_filename = f"response_{safe_query}"

        return save_model_response(result, output_dir / base_filename)

