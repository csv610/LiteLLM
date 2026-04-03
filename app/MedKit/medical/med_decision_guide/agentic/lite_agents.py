"""
liteagents.py - Unified for med_decision_guide
"""
from typing import List, Literal, Optional
from .medical_decision_guide_models import MedicalDecisionGuideModel, ModelOutput
from .medical_decision_guide_prompts import PromptBuilder
from lite.config import ModelConfig, ModelInput
from medkit.diagnostics.medical_decision_guide import MedicalDecisionGuide
import json
from unittest.mock import patch, MagicMock
from lite.logging_config import configure_logging
import sys
from .medical_decision_guide_multi_agent_prompts import MultiAgentPrompts
from tqdm import tqdm
import pytest
from .medical_decision_guide_models import (
import logging
from pathlib import Path
from app.MedKit.medical.med_decision_guide.shared.models import *
from lite.utils import save_model_response
from lite.lite_client import LiteClient
import argparse


# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))



    MedicalDecisionGuideGenerator,
)
    DecisionNode,
    MedicalDecisionGuideModel,
    ModelOutput,
    Outcome,
)


@pytest.fixture
def mock_lite_client():
    with patch("medical.med_decision_guide.agentic.medical_decision_guide.LiteClient") as mock:
        yield mock


def test_medical_decision_guide_generator_init():
    config = ModelConfig(model="test-model")
    generator = MedicalDecisionGuideGenerator(config)
    assert generator.model_config == config


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalDecisionGuideGenerator(config)
    mock_output = ModelOutput(markdown="Chest pain guide", data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Chest pain")
    assert result.markdown == "Chest pain guide"
    assert generator.symptom == "Chest pain"


def test_generate_text_empty_symptom():
    config = ModelConfig(model="test-model")
    generator = MedicalDecisionGuideGenerator(config)
    with pytest.raises(ValueError, match="Symptom name cannot be empty"):
        generator.generate_text("")


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalDecisionGuideGenerator(config)

    mock_data = MedicalDecisionGuideModel(
        guide_name="Chest Pain Assessment",
        primary_symptom="Chest Pain",
        secondary_symptoms="Shortness of breath, sweating",
        age_groups_covered="Adults, Elderly",
        scope="Emergency assessment of chest pain",
        start_node_id="q1",
        decision_nodes=[
            DecisionNode(
                node_id="q1",
                question="Is it crushing pain?",
                yes_node_id="out_emergency",
                no_node_id="q2",
            ),
            DecisionNode(
                node_id="q2",
                question="Is it sharp?",
                yes_node_id="out_mild",
                no_node_id="out_moderate",
            ),
        ],
        outcomes=[
            Outcome(
                outcome_id="out_emergency",
                severity_level="Emergency",
                urgency="Emergency",
                recommendation="Call 911",
                possible_diagnoses="MI",
                home_care_advice="None",
                warning_signs="Crushing pain",
            ),
            Outcome(
                outcome_id="out_mild",
                severity_level="Mild",
                urgency="Self-care",
                recommendation="Rest",
                possible_diagnoses="Pleurisy",
                home_care_advice="OTC pain relief",
                warning_signs="Worsening pain",
            ),
            Outcome(
                outcome_id="out_moderate",
                severity_level="Moderate",
                urgency="Urgent-care",
                recommendation="See doctor",
                possible_diagnoses="GERD",
                home_care_advice="Antacids",
                warning_signs="Pain after eating",
            ),
        ],
        warning_signs="Shortness of breath",
        emergency_indicators="Crushing pain",
    )

    mock_output = ModelOutput(data=mock_data, markdown=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Chest pain", structured=True)
    assert result.data.guide_name == "Chest Pain Assessment"


def test_save_error():
    config = ModelConfig(model="test-model")
    generator = MedicalDecisionGuideGenerator(config)
    with pytest.raises(ValueError, match="No symptom information available"):
        generator.save(ModelOutput(), Path("/tmp"))


@patch("medical.med_decision_guide.agentic.medical_decision_guide.save_model_response")
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalDecisionGuideGenerator(config)
    mock_output = ModelOutput(markdown="Chest pain guide")
    mock_lite_client.return_value.generate_text.return_value = mock_output

    generator.generate_text("Chest pain")
    generator.save(mock_output, Path("/tmp"))

    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("chest_pain_decision_guide")


"""Medical Decision Guide Generator CLI."""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))




try:
    from .medical_decision_guide import MedicalDecisionGuideGenerator
except (ImportError, ValueError):
    from medical.med_decision_guide.agentic.medical_decision_guide import (
        MedicalDecisionGuideGenerator,
    )

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate medical decision trees for symptom assessment."
    )
    parser.add_argument(
        "symptom", help="Symptom name or file path containing symptoms."
    )
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
        log_file="medical_decision_guide.log",
        verbosity=args.verbosity,
        enable_console=True,
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.symptom)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.symptom]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MedicalDecisionGuideGenerator(model_config)

        for item in tqdm(items, desc="Generating"):
            result = generator.generate_text(symptom=item, structured=args.structured)
            if result:
                path = output_dir / f"{item.lower().replace(' ', '_')}_decision.json"
                generator.save(result, path)

        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())

#!/usr/bin/env python3
"""
Medical Decision Guide Analysis module.

This module provides the core MedicalDecisionGuideGenerator class for generating
medical decision guides for symptom assessment.
"""




logger = logging.getLogger(__name__)


class MedicalDecisionGuideGenerator:
    """Generates medical decision guides based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the medical decision guide generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.symptom = None  # Store the symptom for later use in save
        logger.debug("Initialized MedicalDecisionGuideGenerator")

    def generate_text(self, symptom: str, structured: bool = False) -> ModelOutput:
        """Generates a medical decision guide for symptom assessment."""
        # Store the symptom for later use in save
        self.symptom = symptom

        if not symptom or not str(symptom).strip():
            raise ValueError("Symptom name cannot be empty")

        logger.debug(f"Starting decision guide generation for: {symptom}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(symptom)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = MedicalDecisionGuideModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated medical decision guide")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating medical decision guide: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical decision guide information to a file."""
        if self.symptom is None:
            raise ValueError(
                "No symptom information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.symptom.lower().replace(' ', '_')}_decision_guide"

        return save_model_response(result, output_dir / base_filename)

#!/usr/bin/env python3
"""
Multi-agent Medical Decision Guide Analysis module.
"""



    MedicalDecisionGuideModel,
    ModelOutput,
    SymptomMetadataModel,
    EmergencyTriageModel,
    DecisionLogicModel,
    OutcomeListModel,
    ComplianceReportModel,
    DecisionNode,
    Outcome
)

logger = logging.getLogger(__name__)


class Agent:
    """Base class for specialized medical agents."""

    def __init__(self, client: LiteClient, name: str):
        self.client = client
        self.name = name

    def run(self, system_prompt: str, user_prompt: str, response_format) -> any:
        logger.info(f"[{self.name}] Running...")
        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )
        result = self.client.generate_text(model_input=model_input)
        return result.data


class MultiAgentMedicalDecisionGuideGenerator:
    """Orchestrates multiple agents to generate a medical decision guide."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        
        # Initialize agents
        self.analyzer = Agent(self.client, "SymptomAnalyzer")
        self.triage = Agent(self.client, "EmergencyTriage")
        self.architect = Agent(self.client, "LogicArchitect")
        self.outcomes = Agent(self.client, "OutcomeSpecialist")
        self.synthesizer = Agent(self.client, "SynthesisCoordinator")
        self.compliance_officer = Agent(self.client, "ComplianceOfficer")

    def generate(self, symptom: str) -> ModelOutput:
        """Orchestrates the 3-tier multi-agent generation process."""
        logger.info(f"Starting 3-tier multi-agent generation for: {symptom}")

        # --- Tier 1: Specialist Stages (JSON) ---
        # Step 1: Analyze symptom metadata
        metadata: SymptomMetadataModel = self.analyzer.run(
            MultiAgentPrompts.get_analyzer_system_prompt(),
            MultiAgentPrompts.get_analyzer_user_prompt(symptom),
            SymptomMetadataModel
        )

        # Step 2: Identify emergency triage indicators
        triage_info: EmergencyTriageModel = self.triage.run(
            MultiAgentPrompts.get_triage_system_prompt(),
            MultiAgentPrompts.get_triage_user_prompt(symptom),
            EmergencyTriageModel
        )

        # Step 3: Design decision tree logic
        logic_context = f"Symptom: {metadata.primary_symptom}, Scope: {metadata.scope}"
        tree_logic: DecisionLogicModel = self.architect.run(
            MultiAgentPrompts.get_logic_architect_system_prompt(),
            MultiAgentPrompts.get_logic_architect_user_prompt(symptom, logic_context),
            DecisionLogicModel
        )

        # Step 4: Define outcomes for the logic
        tree_summary = f"Nodes: {[n.node_id for n in tree_logic.decision_nodes]}"
        outcomes_info: OutcomeListModel = self.outcomes.run(
            MultiAgentPrompts.get_outcome_specialist_system_prompt(),
            MultiAgentPrompts.get_outcome_specialist_user_prompt(symptom, tree_summary),
            OutcomeListModel
        )

        final_guide = MedicalDecisionGuideModel(
            guide_name=metadata.guide_name,
            primary_symptom=metadata.primary_symptom,
            secondary_symptoms=metadata.secondary_symptoms,
            age_groups_covered=metadata.age_groups_covered,
            scope=metadata.scope,
            start_node_id=tree_logic.start_node_id,
            decision_nodes=tree_logic.decision_nodes,
            outcomes=outcomes_info.outcomes,
            warning_signs=triage_info.warning_signs,
            emergency_indicators=triage_info.emergency_indicators
        )
        specialist_json = final_guide.model_dump_json(indent=2)

        # --- Tier 2: Compliance Audit Stage (JSON Audit) ---
        audit_report: ComplianceReportModel = self.compliance_officer.run(
            MultiAgentPrompts.get_compliance_system_prompt(),
            MultiAgentPrompts.get_compliance_user_prompt(specialist_json),
            ComplianceReportModel
        )
        compliance_json = audit_report.model_dump_json(indent=2)

        # --- Tier 3: Final Output Synthesis (Markdown Closer) ---
        logger.info("Agent: Output synthesis starting...")
        out_sys, out_usr = MultiAgentPrompts.get_output_synthesis_prompts(
            symptom, specialist_json, compliance_json
        )
        
        output_input = ModelInput(
            system_prompt=out_sys,
            user_prompt=out_usr,
            response_format=None,
        )
        final_markdown = self.client.generate_text(model_input=output_input).markdown

        logger.info("✓ 3-tier multi-agent generation complete")
        return ModelOutput(
            data=final_guide, 
            markdown=final_markdown,
            metadata={"audit": compliance_json}
        )

    def save(self, result: ModelOutput, output_path: Path) -> Path:
        """Saves the final guide."""
        return save_model_response(result, output_path)

"""visualize_decision_guide - Visualize Medical Decision Trees.

This module provides functionality to visualize medical decision trees generated
by the medical_decision_guide module. It converts the structured decision tree
data into graph formats (DOT, Mermaid) for clear, intuitive representation.

Supports rendering decision nodes, outcomes, and connections, making complex
medical logic easily understandable for clinicians and patients.

QUICK START:
    Visualize a decision tree from a JSON file:

    >>> from visualize_decision_guide import visualize_guide
    >>> dot_graph = visualize_guide("path/to/fever_decision_tree.json", format="dot")
    >>> print(dot_graph)

COMMON USES:
    - Visualizing clinical decision protocols for training and education
    - Debugging and validating AI-generated decision logic
    - Creating patient-friendly visual aids for shared decision-making
    - Integrating decision trees into documentation or presentations

KEY FEATURES:
    - Converts MedicalDecisionGuide Pydantic model to graph formats
    - Supports DOT language for Graphviz rendering
    - Supports Mermaid syntax for web-based diagramming
    - Clearly labels decision nodes, questions, and outcomes
    - Highlights severity levels and urgency in outcomes
"""




def visualize_guide(
    decision_guide_path: str,
    format: Literal["dot", "mermaid"] = "dot",
    output_file: Optional[str] = None,
) -> str:
    """
    Visualize a medical decision guide from a JSON file.

    Args:
        decision_guide_path: Path to the JSON file containing the MedicalDecisionGuide.
        format: Output format for the visualization ("dot" or "mermaid").
        output_file: Optional path to save the visualization output.

    Returns:
        The generated graph visualization string (DOT or Mermaid syntax).

    Raises:
        FileNotFoundError: If the decision guide JSON file does not exist.
        ValueError: If the format is unsupported or JSON parsing fails.
    """
    guide_path = Path(decision_guide_path)
    if not guide_path.exists():
        raise FileNotFoundError(f"Decision guide file not found: {decision_guide_path}")

    try:
        with open(guide_path, "r", encoding="utf-8") as f:
            guide_data = json.load(f)
        decision_guide = MedicalDecisionGuide(**guide_data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse decision guide JSON: {e}")
    except Exception as e:
        raise ValueError(f"Failed to load MedicalDecisionGuide: {e}")

    if format == "dot":
        graph_string = _generate_dot_graph(decision_guide)
    elif format == "mermaid":
        graph_string = _generate_mermaid_graph(decision_guide)
    else:
        raise ValueError(f"Unsupported format: {format}. Choose 'dot' or 'mermaid'.")

    if output_file:
        Path(output_file).write_text(graph_string, encoding="utf-8")

    return graph_string


def _generate_dot_graph(guide: MedicalDecisionGuide) -> str:
    """Generate DOT graph syntax from a MedicalDecisionGuide."""
    dot_nodes = []
    dot_edges = []

    # Add decision nodes
    for node in guide.decision_nodes:
        dot_nodes.append(f'  "{node.node_id}" [label="{node.question}", shape=box];')
        dot_edges.append(f'  "{node.node_id}" -> "{node.yes_node_id}" [label="Yes"];')
        dot_edges.append(f'  "{node.node_id}" -> "{node.no_node_id}" [label="No"];')
        if node.uncertain_node_id:
            dot_edges.append(
                f'  "{node.node_id}" -> "{node.uncertain_node_id}" [label="Uncertain"];'
            )

    # Add outcome nodes
    for outcome in guide.outcomes:
        color = (
            "red"
            if "emergency" in outcome.severity_level.lower()
            else "orange"
            if "severe" in outcome.severity_level.lower()
            else "green"
        )
        dot_nodes.append(
            f'  "{outcome.outcome_id}" [label="Outcome: {outcome.severity_level}
{outcome.recommendation}", shape=oval, style=filled, fillcolor={color}];'
        )

    return (
        "digraph MedicalDecisionTree {
  rankdir=TB;
"
        + "
".join(dot_nodes + dot_edges)
        + "
}"
    )


def _generate_mermaid_graph(guide: MedicalDecisionGuide) -> str:
    """Generate Mermaid graph syntax from a MedicalDecisionGuide."""
    mermaid_nodes = []
    mermaid_edges = []

    # Add decision nodes
    for node in guide.decision_nodes:
        mermaid_nodes.append(f"  {node.node_id}[{node.question}]")
        mermaid_edges.append(f"  {node.node_id} -- Yes --> {node.yes_node_id}")
        mermaid_edges.append(f"  {node.node_id} -- No --> {node.no_node_id}")
        if node.uncertain_node_id:
            mermaid_edges.append(
                f"  {node.node_id} -- Uncertain --> {node.uncertain_node_id}"
            )

    # Add outcome nodes
    for outcome in guide.outcomes:
        mermaid_nodes.append(
            f"  {outcome.outcome_id}((Outcome: {outcome.severity_level}
{outcome.recommendation}))"
        )

    return "graph TD
" + "
".join(mermaid_nodes + mermaid_edges)



# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

    MultiAgentMedicalDecisionGuideGenerator,
)
    SymptomMetadataModel,
    EmergencyTriageModel,
    DecisionLogicModel,
    OutcomeListModel,
    ComplianceReportModel,
    DecisionNode,
    Outcome,
    ModelOutput
)

@pytest.fixture
def mock_lite_client():
    with patch("medical.med_decision_guide.agentic.multi_agent_decision_guide.LiteClient") as mock:
        yield mock

def test_multi_agent_generator_init():
    config = ModelConfig(model="test-model")
    generator = MultiAgentMedicalDecisionGuideGenerator(config)
    assert generator.model_config == config
    assert generator.analyzer.name == "SymptomAnalyzer"
    assert generator.compliance_officer.name == "ComplianceOfficer"

def test_multi_agent_generate(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MultiAgentMedicalDecisionGuideGenerator(config)
    
    # Mock return values for each agent call
    mock_metadata = SymptomMetadataModel(
        guide_name="Test Guide",
        primary_symptom="Test Symptom",
        secondary_symptoms="s1, s2",
        age_groups_covered="All",
        scope="Test Scope"
    )
    
    mock_triage = EmergencyTriageModel(
        warning_signs="w1, w2",
        emergency_indicators="e1, e2"
    )
    
    mock_logic = DecisionLogicModel(
        start_node_id="q1",
        decision_nodes=[
            DecisionNode(node_id="q1", question="Q1?", yes_node_id="o1", no_node_id="o2")
        ]
    )
    
    mock_outcomes = OutcomeListModel(
        outcomes=[
            Outcome(
                outcome_id="o1", severity_level="s", urgency="u", 
                recommendation="r", possible_diagnoses="d", 
                home_care_advice="h", warning_signs="w"
            ),
            Outcome(
                outcome_id="o2", severity_level="s", urgency="u", 
                recommendation="r", possible_diagnoses="d", 
                home_care_advice="h", warning_signs="w"
            )
        ]
    )

    mock_audit = ComplianceReportModel(
        is_safe=True,
        safety_concerns="None",
        guideline_adherence="High",
        required_corrections="None",
        compliance_score=100
    )

    # Configure the mock to return these in order
    mock_lite_client.return_value.generate_text.side_effect = [
        ModelOutput(data=mock_metadata),
        ModelOutput(data=mock_triage),
        ModelOutput(data=mock_logic),
        ModelOutput(data=mock_outcomes),
        ModelOutput(data=mock_audit)
    ]

    result = generator.generate("Test Symptom")
    
    assert result.guide_name == "Test Guide"
    assert result.primary_symptom == "Test Symptom"
    assert len(result.decision_nodes) == 1
    assert len(result.outcomes) == 2
    assert result.warning_signs == "w1, w2"
    assert result.emergency_indicators == "e1, e2"
    assert mock_lite_client.return_value.generate_text.call_count == 5

"""Multi-Agent Medical Decision Guide Generator CLI."""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


try:
    from .multi_agent_decision_guide import MultiAgentMedicalDecisionGuideGenerator
except (ImportError, ValueError):
    from multi_agent_decision_guide import MultiAgentMedicalDecisionGuideGenerator

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate multi-agent medical decision trees for symptom assessment."
    )
    parser.add_argument(
        "symptom", help="Symptom name or file path containing symptoms."
    )
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
    return parser.parse_args()


def main():
    args = get_user_arguments()
    configure_logging(
        log_file="multi_agent_medical_decision_guide.log",
        verbosity=args.verbosity,
        enable_console=True,
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.symptom)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.symptom]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MultiAgentMedicalDecisionGuideGenerator(model_config)

        for item in tqdm(items, desc="Multi-Agent Generation"):
            result = generator.generate(symptom=item)
            if result:
                path = output_dir / f"{item.lower().replace(' ', '_')}_multiagent_decision.json"
                generator.save(result, path)

        logger.info("✓ Multi-agent generation completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())