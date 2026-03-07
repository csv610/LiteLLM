import argparse

from anatomy_models import AnatomyKnowledgeGraph, GraphVisualizer

try:
    from lite.config import ModelConfig
except ImportError:
    ModelConfig = None


def main():
    parser = argparse.ArgumentParser(
        description="Build anatomy graph from name using LLM."
    )
    parser.add_argument(
        "anatomy_name",
        type=str,
        help="Name of the anatomy (e.g., Liver, Kidney, Brain)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="ollama/gemma3:27b-cloud",
        help="Model name to use (default: ollama/gemma3:27b-cloud)",
    )
    parser.add_argument(
        "--visualize", action="store_true", help="Show the graph visualization"
    )

    args = parser.parse_args()

    print(f"🚀 Building anatomy graph for: {args.anatomy_name} using {args.model}")

    # 1. Build graph from name
    config = ModelConfig(model=args.model) if ModelConfig else None
    builder = AnatomyKnowledgeGraph(model_config=config)
    triples = builder.build_from_name(args.anatomy_name)

    if not triples:
        print("❌ No triples generated.")
        return

    print(f"✅ Generated {len(triples)} anatomical triples.")

    # 2. Export
    builder.export_dot(args.anatomy_name)
    json_path = f"outputs/{args.anatomy_name.lower().replace(' ', '_')}.json"
    builder.export_json(json_path)

    # 3. Optional Visualization
    if args.visualize:
        visualizer = GraphVisualizer(builder.G)
        visualizer.show()


if __name__ == "__main__":
    main()
