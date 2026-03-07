import argparse
import os

from procedure_models import ModelConfig, ProcedureGraphBuilder


def main():
    parser = argparse.ArgumentParser(
        description="Build a medical procedure knowledge graph using LLM."
    )
    parser.add_argument(
        "--procedure",
        type=str,
        required=True,
        help="Name of the medical procedure (e.g., 'Appendectomy').",
    )
    parser.add_argument(
        "--model", type=str, default="ollama/gemma3", help="LLM model name to use."
    )

    args = parser.parse_args()

    procedure_name = args.procedure
    model_name = args.model

    print(f"🚀 Generating graph for: {procedure_name} using model: {model_name}")

    model_config = ModelConfig(model=model_name)
    builder = ProcedureGraphBuilder(model_config=model_config)
    triples = builder.build(procedure_name)

    if not triples:
        print(f"❌ No triples extracted for '{procedure_name}'.")
        return

    print(f"✅ Extracted {len(triples)} Procedure Triples:")
    for t in triples:
        print(f"  - {t.source} --({t.relation})--> {t.target}")

    # Sanitize procedure name for filename
    filename = procedure_name.replace(" ", "_").lower()

    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    dot_path = os.path.join(output_dir, f"{filename}.dot")
    builder.export_dot(dot_path)

    json_path = os.path.join(output_dir, f"{filename}.json")
    builder.export_json(json_path)

    print(f"\n📂 Outputs saved in {output_dir}/")
    print(f"   - DOT file: {dot_path}")
    print(f"   - JSON file: {json_path}")


if __name__ == "__main__":
    main()
