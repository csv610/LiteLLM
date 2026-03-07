import argparse
import sys
from pathlib import Path

# Add the project root to sys.path to support absolute imports if needed,
# but we'll try to use relative or properly scoped imports.
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from lite.config import ModelConfig
from lite.logging_config import configure_logging

# Import generators from their respective locations
# We'll import them inside functions or here if paths are clean.
# Given the structure, we might need to adjust sys.path for each.


def setup_path(subfolder):
    p = str(Path(__file__).parent / subfolder)
    if p not in sys.path:
        sys.path.append(p)


def display_module_list():
    """Display a beautiful, categorized list of drug modules."""
    print("\n💊 MedKit Drug & Pharmacology Module Catalog\n")

    categories = {
        "Drug Information": {
            "info": "Comprehensive drug monographs (MOA, dosing, side effects).",
            "explain": "Explain medicine (generic name only, e.g. acetaminophen) simple terms.",
            "addiction": "Drug addiction, withdrawal symptoms, and recovery info.",
            "prescription": "Analyze prescription images for extraction and safety.",
        },
        "Interactions & Safety": {
            "interact": "Drug-drug interaction analysis between two medications.",
            "food": "Analysis of potential interactions between meds and foods.",
            "disease": "Checking for drug-disease contraindications and safety.",
        },
        "Alternatives & Research": {
            "similar": "Finding therapeutic alternatives or similar medications.",
            "compare": "Side-by-side comparison of two specific medicines.",
            "symptoms": "Suggesting drug categories for specific clinical symptoms.",
        },
    }

    for category, modules in categories.items():
        print(f"🔹 {category}:")
        for cmd, desc in modules.items():
            print(f"  - {cmd.ljust(15)}: {desc}")
        print()

    print('Usage: medkit-drug <subcommand> "Input Text"')


def main():
    parser = argparse.ArgumentParser(
        description="MedKit Drug CLI - Access all pharmacology AI tools."
    )

    # Global arguments
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use.")
    parser.add_argument(
        "-d", "--output-dir", default="outputs", help="Output directory."
    )
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

    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Drug tool subcommands"
    )

    # List Modules
    subparsers.add_parser(
        "list", help="List all available drug modules and descriptions"
    )

    # 1. Medicine Info
    info_p = subparsers.add_parser("info", help="Comprehensive medicine information")
    info_p.add_argument("medicine", help="Medicine name")

    # 2. Drug-Drug Interaction
    interact_p = subparsers.add_parser(
        "interact", help="Drug-drug interaction analysis"
    )
    interact_p.add_argument("medicine1", help="First medicine")
    interact_p.add_argument("medicine2", help="Second medicine")
    interact_p.add_argument("--age", type=int, help="Patient age")

    # 3. Drug-Food Interaction
    food_p = subparsers.add_parser("food", help="Drug-food interaction analysis")
    food_p.add_argument("medicine", help="Medicine name")
    food_p.add_argument("food", help="Food name")

    # 4. Drug-Disease Interaction
    disease_p = subparsers.add_parser(
        "disease", help="Drug-disease interaction analysis"
    )
    disease_p.add_argument("medicine", help="Medicine name")
    disease_p.add_argument("disease", help="Disease name")

    # 5. Similar Drugs
    similar_p = subparsers.add_parser(
        "similar", help="Find similar or alternative medicines"
    )
    similar_p.add_argument("medicine", help="Medicine name")

    # 6. Compare Drugs
    compare_p = subparsers.add_parser("compare", help="Compare two medicines")
    compare_p.add_argument("medicine1", help="First medicine")
    compare_p.add_argument("medicine2", help="Second medicine")

    # 7. Symptoms to Drugs
    symptoms_p = subparsers.add_parser(
        "symptoms", help="Suggest drugs for symptoms (for reference)"
    )
    symptoms_p.add_argument("symptoms", help="Symptom description")

    # 8. Drug Addiction
    addiction_p = subparsers.add_parser(
        "addiction", help="Drug addiction and recovery info"
    )
    addiction_p.add_argument("drug", help="Drug name")

    # 9. Explain (Simple)
    explain_p = subparsers.add_parser(
        "explain",
        help="Please enter your medication (generic name only, e.g. acetaminophen) and I will explain it in simple terms.",
    )
    explain_p.add_argument(
        "medicine",
        nargs="?",
        help="Medicine name (optional, if omitted, enters interactive mode)",
    )

    # 10. Prescription Analysis
    prescription_p = subparsers.add_parser(
        "prescription", help="Analyze prescription images"
    )
    prescription_p.add_argument("image_path", help="Path to the prescription image")

    args = parser.parse_args()

    # Logging config
    configure_logging(
        log_file="medkit_drug.log", verbosity=args.verbosity, enable_console=True
    )
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    model_config = ModelConfig(model=args.model, temperature=0.2)

    try:
        if args.command == "list":
            display_module_list()

        elif args.command == "info":
            setup_path("medicine/medinfo")
            from medicine_info import MedicineInfoGenerator

            gen = MedicineInfoGenerator(model_config)
            res = gen.generate_text(args.medicine, structured=args.structured)
            if res:
                gen.save(res, output_dir / f"{args.medicine.lower()}_info")

        elif args.command == "interact":
            setup_path("drug_drug")
            from drug_drug_interaction import DrugDrugInteractionGenerator
            from drug_drug_interaction_prompts import DrugDrugInput

            gen = DrugDrugInteractionGenerator(model_config)
            config = DrugDrugInput(
                medicine1=args.medicine1, medicine2=args.medicine2, age=args.age
            )
            res = gen.generate_text(config=config, structured=args.structured)
            if res:
                gen.save(res, output_dir)

        elif args.command == "food":
            setup_path("drug_food")
            from drug_food_interaction import DrugFoodInteractionGenerator

            gen = DrugFoodInteractionGenerator(model_config)
            res = gen.generate_text(
                medicine=args.medicine, food=args.food, structured=args.structured
            )
            if res:
                gen.save(res, output_dir)

        elif args.command == "disease":
            setup_path("drug_disease")
            from drug_disease_interaction import DrugDiseaseInteractionGenerator

            gen = DrugDiseaseInteractionGenerator(model_config)
            res = gen.generate_text(
                medicine=args.medicine, disease=args.disease, structured=args.structured
            )
            if res:
                gen.save(res, output_dir)

        elif args.command == "similar":
            setup_path("similar_drugs")
            from similar_drugs import SimilarDrugsGenerator

            gen = SimilarDrugsGenerator(model_config)
            res = gen.generate_text(medicine=args.medicine, structured=args.structured)
            if res:
                gen.save(res, output_dir)

        elif args.command == "compare":
            setup_path("drugs_comparision")
            from drugs_comparison import DrugsComparisonGenerator

            gen = DrugsComparisonGenerator(model_config)
            res = gen.generate_text(
                medicine1=args.medicine1,
                medicine2=args.medicine2,
                structured=args.structured,
            )
            if res:
                gen.save(res, output_dir)

        elif args.command == "symptoms":
            setup_path("symptoms_drugs")
            from symptom_drugs import SymptomDrugsGenerator

            gen = SymptomDrugsGenerator(model_config)
            res = gen.generate_text(symptoms=args.symptoms, structured=args.structured)
            if res:
                gen.save(res, output_dir)

        elif args.command == "addiction":
            setup_path("drug_addiction")
            from drug_addiction import DrugAddictionGenerator

            gen = DrugAddictionGenerator(model_config)
            res = gen.generate_text(drug=args.drug, structured=args.structured)
            if res:
                gen.save(res, output_dir)

        elif args.command == "prescription":
            setup_path("med_prescription")
            from prescription_analyzer import analyze_prescription

            res = analyze_prescription(args.image_path)
            if res:
                print(res.model_dump_json(indent=4))
                with open(output_dir / "prescription_analysis.json", "w") as f:
                    f.write(res.model_dump_json(indent=4))

        elif args.command == "explain":
            from drug.medicine_explainer import explain_medicine
            from drug.medicine_explainer import main as explainer_main

            if args.medicine:
                if args.medicine.lower() == "help":
                    print("\n--- MedKit Medicine Explainer Help ---")
                    print("Usage: medkit-drug explain [medicine_name]")
                    print("Example: medkit-drug explain ibuprofen")
                    print(
                        "If no medicine name is provided, it enters interactive mode."
                    )
                    return

                res = explain_medicine(args.medicine)
                print(res)
                with open(
                    output_dir / f"{args.medicine.lower()}_explanation.md", "w"
                ) as f:
                    f.write(res)
            else:
                explainer_main()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
