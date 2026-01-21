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

import json
from pathlib import Path
from typing import Literal, Optional

from medkit.diagnostics.medical_decision_guide import MedicalDecisionGuide, DecisionNode, Outcome


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
            dot_edges.append(f'  "{node.node_id}" -> "{node.uncertain_node_id}" [label="Uncertain"];')

    # Add outcome nodes
    for outcome in guide.outcomes:
        color = "red" if "emergency" in outcome.severity_level.lower() else "orange" if "severe" in outcome.severity_level.lower() else "green"
        dot_nodes.append(f'  "{outcome.outcome_id}" [label="Outcome: {outcome.severity_level}\n{outcome.recommendation}", shape=oval, style=filled, fillcolor={color}];')

    return "digraph MedicalDecisionTree {\n  rankdir=TB;\n" + "\n".join(dot_nodes + dot_edges) + "\n}"


def _generate_mermaid_graph(guide: MedicalDecisionGuide) -> str:
    """Generate Mermaid graph syntax from a MedicalDecisionGuide."""
    mermaid_nodes = []
    mermaid_edges = []

    # Add decision nodes
    for node in guide.decision_nodes:
        mermaid_nodes.append(f'  {node.node_id}[{node.question}]')
        mermaid_edges.append(f'  {node.node_id} -- Yes --> {node.yes_node_id}')
        mermaid_edges.append(f'  {node.node_id} -- No --> {node.no_node_id}')
        if node.uncertain_node_id:
            mermaid_edges.append(f'  {node.node_id} -- Uncertain --> {node.uncertain_node_id}')

    # Add outcome nodes
    for outcome in guide.outcomes:
        mermaid_nodes.append(f'  {outcome.outcome_id}((Outcome: {outcome.severity_level}\n{outcome.recommendation}))')

    return "graph TD\n" + "\n".join(mermaid_nodes + mermaid_edges)
