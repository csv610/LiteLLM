"""visualize_decision_guide - Tree Visualization for Medical Decision Guides.

Converts medical decision guide JSON files into publication-quality diagrams using
Graphviz and Mermaid visualization engines. This module generates multiple output
formats including DOT diagrams, PNG images, and Mermaid flowcharts suitable for
clinical documentation, training materials, and web integration.

Creates visually clear decision tree representations with color-coded severity
levels, branch labeling (YES/NO/UNCERTAIN), and formatted outcome boxes. Also
generates detailed text descriptions of all nodes and decision logic for
reference documentation.

QUICK START:
    Visualize a decision tree and generate PNG:

        python visualize_decision_guide.py -i outputs/fever_decision_tree.json -o outputs

    Generate Mermaid format for web embedding:

        python visualize_decision_guide.py -i outputs/fever_decision_tree.json -f mermaid -o outputs

    Use programmatically:

        from visualize_decision_guide import visualize_guide

        dot_output, descriptions = visualize_guide("fever_tree.json", output_format="dot")
        print(dot_output)

COMMON USES:
    - Creating clinical protocol diagrams for training
    - Generating publication-ready decision tree figures
    - Embedding interactive flowcharts in web applications
    - Creating patient education diagrams
    - Documenting triage and assessment workflows
    - Building clinical documentation supplements

KEY FEATURES:
    - Multiple visualization formats (DOT, PNG, Mermaid)
    - Color-coded severity levels (mild=green, moderate=orange, severe=red, emergency=darkred)
    - Auto-generation of PNG images from DOT format
    - Branch labeling with YES (green), NO (red), UNCERTAIN (orange)
    - Detailed node descriptions in text format
    - Integration with Graphviz and Mermaid CLI tools
    - Recursive tree traversal with cycle detection
    - Clean, professional diagram layout
"""

import json
from pathlib import Path
from medical_decision_guide import MedicalDecisionGuide


class GraphvizVisualizer:
    """Visualize decision guide as Graphviz DOT diagram."""

    def __init__(self, guide: MedicalDecisionGuide):
        """
        Initialize visualizer with a guide.

        Args:
            guide: MedicalDecisionGuide object to visualize
        """
        self.guide = guide
        self.visited = set()
        self.dot_lines = []
        # Create lookup dictionaries from lists
        self.decision_nodes_map = {node.node_id: node for node in guide.decision_nodes}
        self.outcomes_map = {outcome.outcome_id: outcome for outcome in guide.outcomes}

    def visualize_dot(self) -> str:
        """
        Generate Graphviz DOT format visualization.

        Format:
        - Decision nodes as diamonds
        - Outcomes as boxes with color based on severity
        - YES edges in green (left)
        - NO edges in red (right)

        Returns:
            String containing DOT diagram syntax
        """
        self.visited = set()
        self.dot_lines = []

        self.dot_lines.append("digraph DecisionTree {")
        self.dot_lines.append('    graph [rankdir=TB, bgcolor=white, splines=curved];')
        self.dot_lines.append('    node [shape=box, style=rounded, fontname=Arial];')
        self.dot_lines.append("")

        # Add title
        title = self.guide.guide_name.replace('"', '\\"')
        self.dot_lines.append(f'    labelloc="t";')
        self.dot_lines.append(f'    label="{title}";')
        self.dot_lines.append("")

        # Add nodes and edges
        self._add_nodes(self.guide.start_node_id)

        # Add styling
        self._add_styling()

        self.dot_lines.append("}")

        return "\n".join(self.dot_lines)

    def _add_nodes(self, node_id: str) -> None:
        """Recursively add nodes and edges to DOT."""
        if node_id in self.visited:
            return
        self.visited.add(node_id)

        # Check if outcome
        if node_id in self.outcomes_map:
            outcome = self.outcomes_map[node_id]
            self._add_outcome_node(outcome)
            return

        # Decision node
        if node_id not in self.decision_nodes_map:
            return

        node = self.decision_nodes_map[node_id]
        self._add_decision_node(node)

        # Add edges
        yes_node = node.yes_node_id
        no_node = node.no_node_id

        # YES edge (green)
        self.dot_lines.append(
            f'    "{node_id}" -> "{yes_node}" [xlabel="YES", color=green, fontcolor=green, penwidth=2];'
        )

        # NO edge (red)
        self.dot_lines.append(
            f'    "{node_id}" -> "{no_node}" [xlabel="NO", color=red, fontcolor=red, penwidth=2];'
        )

        # UNCERTAIN edge (orange/yellow) - only if present
        if node.uncertain_node_id:
            uncertain_node = node.uncertain_node_id
            self.dot_lines.append(
                f'    "{node_id}" -> "{uncertain_node}" [xlabel="UNCERTAIN", color=orange, fontcolor=orange, penwidth=2];'
            )
            self._add_nodes(uncertain_node)

        # Recurse
        self._add_nodes(yes_node)
        self._add_nodes(no_node)

    def _add_decision_node(self, node) -> None:
        """Add decision node to DOT."""
        self.dot_lines.append(
            f'    "{node.node_id}" [shape=diamond, label="{node.node_id}", '
            f'style=filled, fillcolor="#E3F2FD", fontname="Arial"];'
        )

    def _add_outcome_node(self, outcome) -> None:
        """Add outcome node to DOT with severity-based color."""
        # Color based on severity
        severity_colors = {
            "mild": "#C8E6C9",           # Light green
            "mild-moderate": "#BBDEFB",  # Light blue
            "moderate": "#FFE0B2",       # Light orange
            "severe": "#FFCCBC",         # Light red
            "emergency": "#EF9A9A",      # Red
        }

        severity = outcome.severity_level.lower()
        color = severity_colors.get(severity, "#F0F0F0")

        self.dot_lines.append(
            f'    "{outcome.outcome_id}" [shape=box, label="{outcome.outcome_id}", '
            f'style=filled, fillcolor="{color}", fontname="Arial", fontsize=10];'
        )

    def _add_styling(self) -> None:
        """Add node styling definitions."""
        self.dot_lines.append("")
        self.dot_lines.append("    // Legend")
        self.dot_lines.append('    legend [label="Severity Levels", shape=plaintext];')

    def generate_node_descriptions(self) -> str:
        """
        Generate a text file with descriptions of all nodes.

        Returns:
            String with formatted node descriptions
        """
        lines = []
        lines.append("=" * 80)
        lines.append(f"DECISION TREE NODE DESCRIPTIONS: {self.guide.guide_name}")
        lines.append("=" * 80)
        lines.append("")

        # Decision nodes
        lines.append("DECISION NODES:")
        lines.append("-" * 80)
        for node in self.guide.decision_nodes:
            lines.append(f"\n{node.node_id}:")
            lines.append(f"  Question: {node.question}")
            lines.append(f"  YES → {node.yes_node_id}")
            lines.append(f"  NO → {node.no_node_id}")
            if node.uncertain_node_id:
                lines.append(f"  UNCERTAIN → {node.uncertain_node_id}")

        lines.append("\n")
        lines.append("=" * 80)
        lines.append("OUTCOMES:")
        lines.append("-" * 80)
        for outcome in self.guide.outcomes:
            lines.append(f"\n{outcome.outcome_id}:")
            lines.append(f"  Severity: {outcome.severity_level}")
            lines.append(f"  Urgency: {outcome.urgency}")
            lines.append(f"  Recommendation: {outcome.recommendation}")
            lines.append(f"  Possible Diagnoses: {outcome.possible_diagnoses}")
            lines.append(f"  Home Care Advice: {outcome.home_care_advice}")
            lines.append(f"  Warning Signs: {outcome.warning_signs}")

        return "\n".join(lines)

    def visualize_mermaid(self) -> str:
        """
        Generate Mermaid diagram syntax.

        Can be visualized at https://mermaid.live/

        Returns:
            String with Mermaid flowchart syntax
        """
        lines = ["graph TD"]
        self.visited = set()

        # Create Mermaid nodes
        self._mermaid_add_nodes(self.guide.start_node_id, lines)

        # Add styling
        lines.append("    classDef question fill:#E3F2FD,stroke:#1976D2,stroke-width:2px,color:#000")
        lines.append("    classDef mild fill:#C8E6C9,stroke:#388E3C,stroke-width:2px,color:#000")
        lines.append("    classDef moderate fill:#FFE0B2,stroke:#F57C00,stroke-width:2px,color:#000")
        lines.append("    classDef severe fill:#FFCCBC,stroke:#D84315,stroke-width:2px,color:#000")
        lines.append("    classDef emergency fill:#EF9A9A,stroke:#C62828,stroke-width:2px,color:#000")

        return "\n".join(lines)

    def _mermaid_add_nodes(self, node_id: str, lines: list) -> None:
        """Recursively add nodes to Mermaid diagram."""
        if node_id in self.visited:
            return
        self.visited.add(node_id)

        # Check if outcome
        if node_id in self.outcomes_map:
            outcome = self.outcomes_map[node_id]
            label = f"{outcome.outcome_id}<br/>{outcome.severity_level}<br/>{outcome.urgency}"
            lines.append(f'    {node_id}["{label}"]')

            # Apply class based on severity
            severity = outcome.severity_level.lower()
            if severity == "emergency":
                lines.append(f'    class {node_id} emergency;')
            elif "severe" in severity:
                lines.append(f'    class {node_id} severe;')
            elif "moderate" in severity:
                lines.append(f'    class {node_id} moderate;')
            else:
                lines.append(f'    class {node_id} mild;')
            return

        # Decision node
        if node_id not in self.decision_nodes_map:
            return

        node = self.decision_nodes_map[node_id]
        question = node.question.replace('"', "'")[:45]
        lines.append(f'    {node_id}["{question}"]')
        lines.append(f'    class {node_id} question;')

        # Add edges
        yes_node = node.yes_node_id
        no_node = node.no_node_id

        lines.append(f'    {node_id} -->|YES| {yes_node}')
        lines.append(f'    {node_id} -->|NO| {no_node}')

        # UNCERTAIN edge - only if present
        if node.uncertain_node_id:
            uncertain_node = node.uncertain_node_id
            lines.append(f'    {node_id} -->|UNCERTAIN| {uncertain_node}')
            self._mermaid_add_nodes(uncertain_node, lines)

        # Recurse
        self._mermaid_add_nodes(yes_node, lines)
        self._mermaid_add_nodes(no_node, lines)


def visualize_guide(guide_path: Path, output_format: str = "dot") -> tuple:
    """
    Load guide and visualize it.

    Args:
        guide_path: Path to guide JSON file
        output_format: Format (dot, mermaid)

    Returns:
        Tuple of (visualization_string, node_descriptions_string)
    """
    with open(guide_path, 'r') as f:
        guide_data = json.load(f)

    guide = MedicalDecisionGuide(**guide_data)
    visualizer = GraphvizVisualizer(guide)

    if output_format == "mermaid":
        visualization = visualizer.visualize_mermaid()
    else:  # dot
        visualization = visualizer.visualize_dot()

    descriptions = visualizer.generate_node_descriptions()
    return visualization, descriptions


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Visualize medical decision guide trees with Graphviz",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Visualize and generate PNG (default)
  python visualize_decision_guide.py -i outputs/ankle_pain_decision_tree.json -o outputs

  # Generate Mermaid format instead of PNG
  python visualize_decision_guide.py -i outputs/fever_decision_tree.json -f mermaid -o outputs

  # Display to stdout (DOT format)
  python visualize_decision_guide.py -i outputs/headache_decision_tree.json
        """
    )

    parser.add_argument("-i", "--guide", type=Path, help="Path to guide JSON file")
    parser.add_argument(
        "-f", "--format",
        choices=["dot", "mermaid"],
        default="dot",
        help="Visualization format (default: dot) - PNG output is auto-generated from DOT"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=Path,
        help="Output directory for visualization files"
    )

    args = parser.parse_args()

    try:
        import subprocess

        visualization, descriptions = visualize_guide(args.guide, output_format=args.format)

        if args.output_dir:
            args.output_dir.mkdir(parents=True, exist_ok=True)

            # Generate filename from guide file
            guide_stem = args.guide.stem
            # Remove '_decision_tree' suffix if present
            if guide_stem.endswith('_decision_tree'):
                guide_stem = guide_stem[:-14]

            if args.format == "dot":
                # Save DOT file
                dot_path = args.output_dir / f"{guide_stem}.dot"
                with open(dot_path, 'w') as f:
                    f.write(visualization)
                print(f"✓ DOT file saved to: {dot_path}")

                # Auto-generate PNG from DOT
                png_path = args.output_dir / f"{guide_stem}.png"
                subprocess.run(['dot', '-Tpng', str(dot_path), '-o', str(png_path)], check=True)
                print(f"✓ PNG visualization saved to: {png_path}")
            else:  # mermaid
                # Save Mermaid file
                mermaid_path = args.output_dir / f"{guide_stem}.mmd"
                with open(mermaid_path, 'w') as f:
                    f.write(visualization)
                print(f"✓ Mermaid diagram saved to: {mermaid_path}")

                # Auto-generate PNG from Mermaid using mmdc (mermaid-cli)
                try:
                    png_path = args.output_dir / f"{guide_stem}.png"
                    subprocess.run(
                        ['mmdc', '-i', str(mermaid_path), '-o', str(png_path)],
                        check=True,
                        capture_output=True
                    )
                    print(f"✓ PNG visualization saved to: {png_path}")
                except FileNotFoundError:
                    print(f"⚠ Warning: mermaid-cli (mmdc) not found. PNG not generated.")
                    print(f"  Install with: npm install -g @mermaid-js/mermaid-cli")
                except subprocess.CalledProcessError as e:
                    print(f"⚠ Warning: Failed to generate PNG from Mermaid: {e}")

            # Save descriptions to a separate file
            desc_path = args.output_dir / f"{guide_stem}_descriptions.txt"
            with open(desc_path, 'w') as f:
                f.write(descriptions)
            print(f"✓ Node descriptions saved to: {desc_path}")
        else:
            print(visualization)
            print("\n" + "=" * 80 + "\n")
            print(descriptions)

    except FileNotFoundError as e:
        print(f"✗ File not found: {e}")
        exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
