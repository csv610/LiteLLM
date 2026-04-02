import argparse
import json
import os
import sys


def main():
    parser = argparse.ArgumentParser(
        description="MedKit Knowledge Graph CLI - Extract and visualize medical triples."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Common domains
    domains = [
        "disease",
        "anatomy",
        "medicine",
        "procedure",
        "surgery",
        "genetic",
        "symptoms",
    ]

    for domain in domains:
        p = subparsers.add_parser(domain, help=f"Extract and visualize {domain} graph")
        p.add_argument("text", help="Medical text to process or file path")
        p.add_argument("--json", action="store_true", help="Output results as JSON")
        p.add_argument("--no-viz", action="store_true", help="Disable visualization")

    # Special case: Medical Test Graph
    test_p = subparsers.add_parser("test", help="Generate medical test knowledge graph")
    test_p.add_argument("text", help="Medical text or file path")
    test_p.add_argument("--json", action="store_true", help="Output results as JSON")
    test_p.add_argument("--no-viz", action="store_true", help="Disable visualization")

    args = parser.parse_args()

    # Handle input text
    input_text = args.text
    if os.path.isfile(args.text):
        with open(args.text, "r") as f:
            input_text = f.read()

    try:
        if args.command in domains:
            if args.command == "disease":
                from medkit_graph.disease.disease_models import (
                    DiseaseKnowledgeGraphBuilder as Builder,
                )
                from medkit_graph.disease.disease_models import (
                    GraphVisualizer as Visualizer,
                )

                builder = Builder()
                triples = builder.build_from_name(input_text)
            elif args.command == "anatomy":
                from medkit_graph.anatomy.anatomy_models import (
                    AnatomyKnowledgeGraph as Builder,
                )
                from medkit_graph.anatomy.anatomy_models import (
                    GraphVisualizer as Visualizer,
                )

                builder = Builder()
                triples = builder.build_from_name(input_text)
            elif args.command == "medicine":
                from medkit_graph.medicine.medicine_models import MedicineKnowledgeGraph

                builder = MedicineKnowledgeGraph()
                triples = builder.build_from_medicine(input_text)
                Visualizer = None
            elif args.command == "procedure":
                from medkit_graph.procedure.procedure_models import (
                    ModelConfig,
                )
                from medkit_graph.procedure.procedure_models import (
                    ProcedureGraphBuilder as Builder,
                )

                builder = Builder(ModelConfig(model="ollama/gemma3", temperature=0.0))
                triples = builder.build(input_text)
            elif args.command == "surgery":
                from medkit_graph.surgery.surgery_models import (
                    SurgeryGraphBuilder as Builder,
                )
                from medkit_graph.surgery.surgery_models import (
                    SurgeryTripletExtractor as Extractor,
                )

                extractor = Extractor()
                triples = extractor.extract(input_text)
                builder = Builder()
                builder.add_triples(triples)
                Visualizer = None
            elif args.command == "genetic":
                from medkit_graph.genetic.core import (
                    GeneticsGraphBuilder as Builder,
                )
                from medkit_graph.genetic.core import (
                    GeneticsTripletExtractor as Extractor,
                )

                extractor = Extractor()
                triples = extractor.extract(input_text)
                builder = Builder()
                builder.add_triples(triples)
            elif args.command == "symptoms":
                from medkit_graph.symptoms.sympton_models import (
                    SymptomGraphBuilder as Builder,
                )
                from medkit_graph.symptoms.sympton_models import (
                    SymptomTripletExtractor as Extractor,
                )

                extractor = Extractor()
                triples = extractor.extract(input_text)
                builder = Builder()
                builder.add_triples(triples)

            if args.json:
                print(json.dumps([t.model_dump() for t in triples], indent=2))
            else:
                print(f"✅ Extracted {len(triples)} {args.command} triples.")
                for t in triples:
                    print(f" - {t.source} --({t.relation})--> {t.target}")

            if not args.no_viz:
                if Visualizer is None:
                    print("Visualization is not implemented for surgery.")
                else:
                    visualizer = (
                        Visualizer(builder)
                        if args.command == "disease"
                        else Visualizer(builder.G)
                    )
                    print("📊 Opening visualization window...")
                    visualizer.show()

        elif args.command == "test":
            from medkit_diagnose.medical_tests_graph import (
                MedicalTestGraphBuilder,
                MedicalTestTripletExtractor,
            )

            extractor = MedicalTestTripletExtractor()
            triples = extractor.extract(input_text)

            if args.json:
                print(json.dumps([t.dict() for t in triples], indent=2))
            else:
                print(f"✅ Extracted {len(triples)} test triples.")

            if not args.no_viz:
                builder = MedicalTestGraphBuilder()
                builder.add_triples(triples)
                print("Visualization is not implemented for test graphs.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
