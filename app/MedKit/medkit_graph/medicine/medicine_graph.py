import os
import argparse
from medicine_models import MedicineKnowledgeGraph

try:
    from lite.config import ModelConfig
except ImportError:
    ModelConfig = None

def main():
    parser = argparse.ArgumentParser(
        description="Build medicine graph from name using LLM."
    )
    parser.add_argument(
        "medicine_name",
        type=str,
        nargs='?',
        default="Paracetamol",
        help="Name of the medicine (e.g., Paracetamol, Ibuprofen)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="ollama/gemma3",
        help="Model name to use (default: ollama/gemma3)",
    )

    args = parser.parse_args()

    print(f"🚀 Building medicine graph for: {args.medicine_name} using {args.model}")

    # 1. Build graph from name
    config = ModelConfig(model=args.model) if ModelConfig else None
    builder = MedicineKnowledgeGraph(model_config=config)
    
    try:
        triples = builder.build_from_medicine(args.medicine_name)
        
        if not triples:
            print("❌ No triples generated.")
            return

        print(f"✅ Generated {len(triples)} biomedical triples.")

        # Print extracted triples
        for t in triples:
            print(f"  - {t.source} --({t.relation})--> {t.target}")

        print("🔹 Drugs that treat Fever:", builder.query_treats("Fever"))
        print("🔹 Side effects of Paracetamol:", builder.query_side_effects(args.medicine_name))

        # 2. Export
        builder.export_dot(args.medicine_name)
        
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        json_path = os.path.join(output_dir, "medicine_graph.json")
        builder.export_json(json_path)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
