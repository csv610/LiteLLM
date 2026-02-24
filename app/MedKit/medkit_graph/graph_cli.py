import argparse
import sys
import os
import json
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

def setup_path(domain):
    p = str(Path(__file__).parent.parent / "medgraphs" / domain)
    if p not in sys.path:
        sys.path.append(p)

def main():
    parser = argparse.ArgumentParser(description="MedKit Knowledge Graph CLI - Extract and visualize medical triples.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Common domains
    domains = ["disease", "anatomy", "medicine", "pathophysiology", "pharmacology", "procedure", "surgery", "genetic", "symptoms"]
    
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
        with open(args.text, 'r') as f:
            input_text = f.read()

    try:
        if args.command in domains:
            setup_path(args.command)
            
            # Dynamic imports based on domain
            if args.command == "disease":
                from medgraphs.disease.core import DiseaseTripletExtractor as Extractor, DiseaseGraphBuilder as Builder, GraphVisualizer as Visualizer
            elif args.command == "anatomy":
                from medgraphs.anatomy.core import AnatomyTripletExtractor as Extractor, AnatomyGraphBuilder as Builder, GraphVisualizer as Visualizer
            elif args.command == "medicine":
                from medgraphs.medicine.core import MedicineTripletExtractor as Extractor, MedicineGraphBuilder as Builder, GraphVisualizer as Visualizer
            elif args.command == "pathophysiology":
                from medgraphs.pathophysiology.core import PathophysiologyTripletExtractor as Extractor, PathophysiologyGraphBuilder as Builder, GraphVisualizer as Visualizer
            elif args.command == "pharmacology":
                from medgraphs.pharmacology.core import PharmacologyTripletExtractor as Extractor, PharmacologyGraphBuilder as Builder, GraphVisualizer as Visualizer
            elif args.command == "procedure":
                from medgraphs.procedure.core import ProcedureTripletExtractor as Extractor, ProcedureGraphBuilder as Builder, GraphVisualizer as Visualizer
            elif args.command == "surgery":
                from medgraphs.surgery.core import SurgeryTripletExtractor as Extractor, SurgeryGraphBuilder as Builder, GraphVisualizer as Visualizer
            elif args.command == "genetic":
                from medgraphs.genetic.core import GeneticTripletExtractor as Extractor, GeneticGraphBuilder as Builder, GraphVisualizer as Visualizer
            elif args.command == "symptoms":
                from medgraphs.symptoms.core import SymptomTripletExtractor as Extractor, SymptomGraphBuilder as Builder, GraphVisualizer as Visualizer

            extractor = Extractor()
            triples = extractor.extract(input_text)
            
            if args.json:
                print(json.dumps([t.dict() for t in triples], indent=2))
            else:
                print(f"✅ Extracted {len(triples)} {args.command} triples.")
                for t in triples:
                    print(f" - {t.source} --({t.relation})--> {t.target}")

            if not args.no_viz:
                builder = Builder()
                builder.add_triples(triples)
                visualizer = Visualizer(builder.G)
                print("📊 Opening visualization window...")
                visualizer.show()

        elif args.command == "test":
            from diagnostics.medical_tests_graph import MedicalTestTripletExtractor, MedicalTestGraphBuilder, GraphVisualizer
            
            extractor = MedicalTestTripletExtractor()
            triples = extractor.extract(input_text)
            
            if args.json:
                print(json.dumps([t.dict() for t in triples], indent=2))
            else:
                print(f"✅ Extracted {len(triples)} test triples.")
            
            if not args.no_viz:
                builder = MedicalTestGraphBuilder()
                builder.add_triples(triples)
                visualizer = Visualizer(builder.G)
                print("📊 Opening visualization window...")
                visualizer.show()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
