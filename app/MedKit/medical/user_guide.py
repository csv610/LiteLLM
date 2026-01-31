"""
MedKit Medical Module User Guide

This interactive guide provides comprehensive documentation for all modules
in the MedKit medical package. It includes usage examples, quick start guides,
and detailed information about each module's capabilities.

USAGE:
    python user_guide.py                    # Display interactive menu
    python user_guide.py --module <name>    # Show specific module guide
    python user_guide.py --list             # List all available modules
    python user_guide.py --search <keyword> # Search for modules by keyword
"""

import argparse



from medkit.utils.logging_config import setup_logger

# Configure logging
logger = setup_logger(__name__)

# ============================================================================
# CHAPTER ORGANIZATION
# ============================================================================

CHAPTERS = {
    "chapter_1": {
        "title": "Getting Started with MedKit",
        "description": "Introduction to MedKit modules and basic usage",
        "modules": ["medical_dictionary", "medical_faq"],
        "overview": "Start with these foundational modules to understand how to use MedKit. Learn about medical terminology and how to generate FAQs."
    },
    "chapter_2": {
        "title": "Medical Information & Documentation",
        "description": "Generate comprehensive medical information",
        "modules": ["medical_topic", "medical_anatomy", "disease_info"],
        "overview": "Learn how to generate detailed medical documentation for diseases, anatomical structures, and general topics."
    },
    "chapter_3": {
        "title": "Clinical Procedures & Surgery",
        "description": "Surgical and clinical procedure documentation",
        "modules": ["surgery_info", "surgical_tool_info", "medical_procedure_info"],
        "overview": "Generate comprehensive documentation for surgical procedures, surgical instruments, and clinical procedures."
    },
    "chapter_4": {
        "title": "Diagnostic & Testing",
        "description": "Medical tests and diagnostic information",
        "modules": ["medical_test_info", "medical_test_devices", "medical_term_extractor"],
        "overview": "Learn about medical tests, diagnostic devices, and techniques for extracting medical information from text."
    },
    "chapter_5": {
        "title": "Specialized Medical Resources",
        "description": "Alternative medicine and medical specialties",
        "modules": ["herbal_info", "medical_speciality"],
        "overview": "Explore herbal remedies and create a comprehensive medical specialties database."
    }
}

# ============================================================================
# MODULE DOCUMENTATION
# ============================================================================

MODULES = {
    "medical_faq": {
        "name": "Medical FAQ Generator",
        "description": "Generate comprehensive patient and provider FAQs for medical topics",
        "main_function": "FAQGenerator.generate()",
        "quick_start": """
from medical_faq import FAQGenerator

# Initialize generator
generator = FAQGenerator()

# Generate patient-friendly FAQs only
faq = generator.generate("Kidney disease")
print(f"Generated {len(faq.patient_faq.faqs)} questions")

# Generate with provider FAQs
faq = generator.generate("Diabetes", include_provider=True)
        """,
        "key_features": [
            "Patient-friendly FAQ section with plain language",
            "Optional provider-focused FAQ with clinical terminology",
            "When to seek care guidance with urgency levels",
            "Common misconceptions and clarifications",
            "Cross-references to related topics and medical devices",
            "Structured JSON output with Pydantic validation"
        ],
        "output_format": "ComprehensiveFAQ (Pydantic model)",
        "output_location": "outputs/{topic_name}_faq.json",
        "logs": "logs/medical_faq.log"
    },

    "medical_anatomy": {
        "name": "Anatomical Structure Documentation",
        "description": "Generate detailed anatomical information for any body structure",
        "main_function": "get_anatomy_info()",
        "quick_start": """
from medical_anatomy import get_anatomy_info

# Generate comprehensive anatomy information
result = get_anatomy_info("Heart")
print(result.overview.structure_name)
print(result.overview.body_system)

# Custom output path
result = get_anatomy_info("Femur", output_path="anatomy/femur.json")
        """,
        "key_features": [
            "Official and common names with classifications",
            "Embryological origin and anatomical location",
            "Gross and microscopic structure details",
            "Vascular supply and innervation",
            "Anatomical variations and anomalies",
            "Clinical significance and imaging characteristics",
            "Surgical landmarks and approaches",
            "12 comprehensive sections of documentation"
        ],
        "output_format": "MedicalAnatomy (Pydantic model)",
        "output_location": "outputs/{structure_name}_anatomy.json",
        "logs": "logs/medical_anatomy.log"
    },

    "medical_topic": {
        "name": "Medical Topic Documentation",
        "description": "Generate comprehensive medical information with embedded FAQs",
        "main_function": "get_topic_info()",
        "quick_start": """
from medical_topic import get_topic_info

# Generate comprehensive topic information
result = get_topic_info("Diabetes")
print(result.overview.topic_name)

# Access different sections
symptoms = result.clinical_presentation.primary_symptoms
treatments = result.treatment.medications

# With custom path
result = get_topic_info("Hypertension", output_path="topics/hypertension.json")
        """,
        "key_features": [
            "Epidemiology and risk factors",
            "Pathophysiology and disease mechanisms",
            "Clinical presentation and symptoms",
            "Diagnostic methods and criteria",
            "Treatment options and management",
            "Prognosis and complications",
            "Prevention strategies",
            "Embedded patient-friendly FAQ",
            "Psychosocial impact and special populations"
        ],
        "output_format": "MedicalTopic (Pydantic model)",
        "output_location": "outputs/{topic_name}_topic.json",
        "logs": "logs/medical_topic.log"
    },

    "medical_term_extractor": {
        "name": "Medical Term Extraction",
        "description": "Extract and categorize medical concepts from unstructured text",
        "main_function": "extract_medical_terms()",
        "quick_start": """
from medical_term_extractor import extract_medical_terms, extract_from_file

# Extract from text
text = "Patient has diabetes and hypertension. Prescribed metformin and lisinopril."
result = extract_medical_terms(text)
print(f"Diseases: {len(result.diseases)}")
print(f"Medicines: {len(result.medicines)}")

# Extract from file
result = extract_from_file("medical_note.txt")
        """,
        "key_features": [
            "Disease and condition extraction",
            "Medication identification",
            "Symptom and sign recognition",
            "Treatment and procedure extraction",
            "Medical specialty identification",
            "Anatomical term extraction",
            "Side effects and adverse reactions",
            "Causation relationship mapping",
            "Context preservation for each term"
        ],
        "output_format": "MedicalTerms (Pydantic model)",
        "output_location": "outputs/temp_medical_terms.json",
        "logs": "logs/medical_term_extractor.log"
    },

    "surgery_info": {
        "name": "Surgical Procedure Documentation",
        "description": "Generate comprehensive surgical procedure information",
        "main_function": "get_surgery_info()",
        "quick_start": """
from surgery_info import get_surgery_info

# Generate surgery information
result = get_surgery_info("Knee Replacement")
print(result.metadata.surgery_name)

# Custom output path
result = get_surgery_info("Coronary Artery Bypass",
                         output_path="surgery/cardiac.json")

# Using CLI
# python surgery_info.py "Knee Replacement"
# python surgery_info.py "Knee Replacement" -o custom.json
        """,
        "key_features": [
            "Surgical indications and contraindications",
            "Pre-operative, operative, and post-operative phases",
            "Step-by-step surgical procedures",
            "Operative risks and complications",
            "Recovery timeline and rehabilitation",
            "Alternative treatment options",
            "Technical details and surgeon qualifications",
            "Current research and innovations",
            "Cost and insurance information",
            "Special population considerations"
        ],
        "output_format": "SurgeryInfo (Pydantic model)",
        "output_location": "outputs/{surgery_name}_info.json",
        "logs": "logs/surgery_info.log"
    },

    "surgical_tool_info": {
        "name": "Surgical Instrument Documentation",
        "description": "Generate comprehensive surgical tool and instrument information",
        "main_function": "get_surgical_tool_info()",
        "quick_start": """
from surgical_tool_info import get_surgical_tool_info

# Generate tool information
result = get_surgical_tool_info("Surgical Scalpel")
print(result.tool_basics.tool_name)

# Custom output
result = get_surgical_tool_info("Surgical Forceps",
                               output_path="instruments/forceps.json")

# Using CLI
# python surgical_tool_info.py "Surgical Scalpel"
# python surgical_tool_info.py "Hemostatic Clamp" -o instruments/
        """,
        "key_features": [
            "Physical specifications and dimensions",
            "Operational characteristics and force specifications",
            "Safety features and mechanisms",
            "Pre-operative preparation and inspection",
            "Intraoperative use and handling",
            "Maintenance and care requirements",
            "Sterilization and disinfection protocols",
            "Alternatives and comparisons",
            "Historical context and evolution",
            "Training and certification requirements"
        ],
        "output_format": "SurgicalToolInfo (Pydantic model)",
        "output_location": "outputs/{tool_name}_info.json",
        "logs": "logs/surgical_tool_info.log"
    },

    "medical_speciality": {
        "name": "Medical Specialty Database",
        "description": "Generate and query medical specialty database",
        "main_function": "generate_specialist_database()",
        "quick_start": """
from medical_speciality import generate_specialist_database, MedicalSpecialistDatabase

# Generate database
db = generate_specialist_database("specialists.json")

# Query by category
cardiologists = db.get_by_category("Cardiovascular")

# Search by condition
heart_specialists = db.search_by_condition("heart disease")

# Get surgical specialties
surgeons = db.get_surgical_specialists()

# Get all categories
categories = db.get_all_categories()

# Using CLI
# python medical_speciality.py
# python medical_speciality.py -o custom_specialists.json
        """,
        "key_features": [
            "Comprehensive medical specialties database",
            "Organized by medical categories",
            "Specialty descriptions and roles",
            "Conditions treated by each specialty",
            "Common referral reasons",
            "Subspecialty information",
            "Surgical vs non-surgical classification",
            "Patient population focus",
            "Query methods for searching",
            "JSON output with Pydantic validation"
        ],
        "output_format": "MedicalSpecialistDatabase (Pydantic model)",
        "output_location": "outputs/medical_specialists.json",
        "logs": "logs/medical_speciality.log"
    },

    "herbal_info": {
        "name": "Herbal Remedy Documentation",
        "description": "Generate comprehensive herbal remedy and medicinal plant information",
        "main_function": "get_herbal_info()",
        "quick_start": """
from herbal_info import get_herbal_info

# Generate herbal information
result = get_herbal_info("Ginger")
print(result.metadata.common_name)
print(result.metadata.botanical_name)

# Custom output
result = get_herbal_info("Turmeric", output_path="herbs/turmeric.json")

# Using CLI
# python herbal_info.py -i "Chamomile"
# python herbal_info.py -i "Chamomile" -o herbs/chamomile.json
        """,
        "key_features": [
            "Botanical identification and classification",
            "Traditional medicine system information",
            "Active constituents and phytochemistry",
            "Mechanism of action",
            "Forms and preparation methods",
            "Dosage guidelines by age",
            "Safety profile and side effects",
            "Drug, herb, and food interactions",
            "Special population considerations",
            "Clinical evidence and efficacy",
            "Cost and availability information"
        ],
        "output_format": "HerbalInfo (Pydantic model)",
        "output_location": "outputs/{herb_name}_info.json",
        "logs": "logs/herbal_info.log"
    },

    "medical_dictionary": {
        "name": "Medical Dictionary",
        "description": "Generate medical term definitions and explanations",
        "main_function": "MedicalDictionary.query()",
        "quick_start": """
from medical_dictionary import MedicalDictionary

# Initialize dictionary
dictionary = MedicalDictionary()

# Look up a term
entry = dictionary.query("Hypertension")
print(entry['definition'])
print(entry['explanation'])
print(entry['category'])

# Different models
custom_dict = MedicalDictionary(model="gemini-2.5-flash")
entry = custom_dict.query("Arrhythmia")
        """,
        "key_features": [
            "Medical term definitions",
            "Alternative names and synonyms",
            "Detailed explanations",
            "Contraindications and precautions",
            "Medical category classification",
            "Structured dictionary format",
            "LLM-powered generation",
            "Expert medical lexicography"
        ],
        "output_format": "MedicalTerm (Pydantic model)",
        "output_location": "In-memory (optional file save)",
        "logs": "logs/medical_dictionary.log"
    },

    "medical_procedure_info": {
        "name": "Medical Procedure Documentation",
        "description": "Generate comprehensive medical and surgical procedure information",
        "main_function": "get_procedure_info()",
        "quick_start": """
from medical_procedure_info import get_procedure_info

# Generate procedure information
result = get_procedure_info("Knee Replacement")
print(result.metadata.procedure_name)

# Custom output and specialty
result = get_procedure_info("Colonoscopy",
                           output_path="procedures/colonoscopy.json",
                           specialty="Gastroenterology")

# Using CLI
# python medical_procedure_info.py -i "Knee Replacement"
# python medical_procedure_info.py -i "Colonoscopy" -o custom.json
        """,
        "key_features": [
            "Procedure indications and contraindications",
            "Preparation requirements",
            "Step-by-step procedure details",
            "Expected discomfort and risks",
            "Recovery information",
            "Outcomes and effectiveness",
            "Follow-up care requirements",
            "Alternative treatment options",
            "Technical details and qualifications",
            "Cost and insurance information"
        ],
        "output_format": "ProcedureInfo (Pydantic model)",
        "output_location": "outputs/{procedure_name}_info.json",
        "logs": "logs/medical_procedure_info.log"
    },

    "medical_test_devices": {
        "name": "Medical Device Documentation",
        "description": "Generate comprehensive medical device and equipment information",
        "main_function": "get_device_info()",
        "quick_start": """
from medical_test_devices import get_device_info

# Generate device information
result = get_device_info("Ultrasound Machine")
print(result.basic_info.device_name)

# Custom output
result = get_device_info("CT Scanner",
                        output_path="devices/ct_scanner.json")

# Using CLI
# python medical_test_devices.py -i "Electrocardiogram Machine"
# python medical_test_devices.py -i "Laparoscopic Surgical Tower" -o devices/
        """,
        "key_features": [
            "Device classification and FDA status",
            "Purpose and clinical applications",
            "Physical and technical specifications",
            "Safety features and risks",
            "Operational procedures",
            "Maintenance and calibration",
            "Cleaning and sterilization",
            "Performance characteristics",
            "Regulatory compliance",
            "Manufacturer and support information"
        ],
        "output_format": "MedicalDeviceInfo (Pydantic model)",
        "output_location": "outputs/{device_name}_device_info.json",
        "logs": "logs/medical_test_devices.log"
    },

    "medical_test_info": {
        "name": "Medical Test Documentation",
        "description": "Generate comprehensive medical test and diagnostic information",
        "main_function": "get_medical_test_info()",
        "quick_start": """
from medical_test_info import get_medical_test_info

# Generate test information
result = get_medical_test_info("Blood glucose test")
print(result.test_name)
print(result.results_information.normal_range)

# Custom output
result = get_medical_test_info("Complete blood count",
                              output_path="tests/cbc.json")

# Using CLI
# python medical_test_info.py -i "Blood glucose test"
# python medical_test_info.py -i "Lipid panel" -o tests/
        """,
        "key_features": [
            "Test purpose and indications",
            "Preparation requirements",
            "Sample collection methods",
            "Test procedure and methodology",
            "Normal reference ranges",
            "Result interpretation",
            "Age-specific variations",
            "Interfering factors",
            "Sensitivity and specificity",
            "Cost and insurance information"
        ],
        "output_format": "TestInfo (Pydantic model)",
        "output_location": "outputs/{test_name}_info.json",
        "logs": "logs/medical_test_info.log"
    },

    "disease_info": {
        "name": "Disease Information Generator",
        "description": "Generate comprehensive disease and condition documentation",
        "main_function": "get_disease_info()",
        "quick_start": """
from disease_info import get_disease_info

# Generate disease information
result = get_disease_info("Hypertension")
print(result.identity.disease_name)
print(result.epidemiology.prevalence_incidence)

# Custom output
result = get_disease_info("Diabetes", output_path="diseases/diabetes.json")

# Incremental generation (avoids token limits)
result = get_disease_info("Cancer", incremental_generate=True)

# Using CLI
# python disease_info.py
# python disease_info.py -o custom.json
        """,
        "key_features": [
            "Disease identification and classification",
            "Epidemiology and statistics",
            "Risk factors and etiology",
            "Prevention strategies",
            "Clinical presentation",
            "Diagnosis and diagnostic criteria",
            "Disease management and treatment",
            "Current research and breakthroughs",
            "Special population considerations",
            "Quality of life and support resources",
            "Incremental generation support"
        ],
        "output_format": "DiseaseInfo (Pydantic model)",
        "output_location": "outputs/{disease_name}_info.json",
        "logs": "logs/disease_info.log"
    }
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def print_header(text: str, char: str = "=") -> None:
    """Print a formatted header."""
    width = 80
    print(f"\n{char * width}")
    print(f"{text.center(width)}")
    print(f"{char * width}\n")

def print_module_list() -> None:
    """Print list of all available modules."""
    print_header("AVAILABLE MODULES IN MEDKIT MEDICAL PACKAGE")

    for idx, (key, info) in enumerate(MODULES.items(), 1):
        print(f"{idx}. {info['name']:.<50} ({key})")

    print(f"\nTotal modules: {len(MODULES)}\n")
    logger.info(f"Displayed list of {len(MODULES)} modules")

def print_module_guide(module_name: str) -> None:
    """Print detailed guide for a specific module."""
    if module_name not in MODULES:
        print(f"Error: Module '{module_name}' not found.")
        print(f"Available modules: {', '.join(MODULES.keys())}")
        logger.warning(f"Module '{module_name}' not found")
        return

    module = MODULES[module_name]

    print_header(f"{module['name'].upper()}")

    print(f"Module Name: {module_name}")
    print(f"Description: {module['description']}\n")

    print("Quick Start:")
    print("-" * 80)
    print(module['quick_start'])
    print("-" * 80)

    print("\nKey Features:")
    for feature in module['key_features']:
        print(f"  • {feature}")

    print(f"\nMain Function: {module['main_function']}")
    print(f"Output Format: {module['output_format']}")
    print(f"Default Output Location: {module['output_location']}")
    print(f"Logging: {module['logs']}\n")

    logger.info(f"Displayed guide for module: {module_name}")

def search_modules(keyword: str) -> None:
    """Search modules by keyword."""
    keyword_lower = keyword.lower()
    results = []

    for key, info in MODULES.items():
        if (keyword_lower in info['name'].lower() or
            keyword_lower in info['description'].lower() or
            any(keyword_lower in feature.lower() for feature in info['key_features'])):
            results.append((key, info))

    if not results:
        print(f"No modules found matching '{keyword}'")
        logger.info(f"Search for '{keyword}' returned no results")
        return

    print_header(f"SEARCH RESULTS FOR '{keyword.upper()}'")

    for key, info in results:
        print(f"Module: {info['name']} ({key})")
        print(f"Description: {info['description']}\n")

    print(f"Found {len(results)} module(s) matching '{keyword}'\n")
    logger.info(f"Search for '{keyword}' returned {len(results)} results")

def print_chapters() -> None:
    """Print list of all chapters."""
    print_header("MEDKIT MEDICAL MODULE CHAPTERS")

    for key, chapter in CHAPTERS.items():
        chapter_num = key.replace("chapter_", "")
        print(f"\nChapter {chapter_num}: {chapter['title']}")
        print(f"Description: {chapter['description']}")
        print(f"Modules: {', '.join(chapter['modules'])}")
        print("-" * 80)

    print(f"\nTotal chapters: {len(CHAPTERS)}\n")
    logger.info(f"Displayed list of {len(CHAPTERS)} chapters")

def print_chapter_guide(chapter_key: str) -> None:
    """Print detailed guide for a specific chapter."""
    if chapter_key not in CHAPTERS:
        print(f"Error: Chapter '{chapter_key}' not found.")
        print(f"Available chapters: {', '.join(CHAPTERS.keys())}")
        logger.warning(f"Chapter '{chapter_key}' not found")
        return

    chapter = CHAPTERS[chapter_key]
    chapter_num = chapter_key.replace("chapter_", "")

    print_header(f"CHAPTER {chapter_num}: {chapter['title'].upper()}")

    print(f"Description: {chapter['description']}\n")
    print(f"Overview:\n{chapter['overview']}\n")

    print("Modules in this chapter:")
    print("-" * 80)

    for i, module_name in enumerate(chapter['modules'], 1):
        if module_name in MODULES:
            module_info = MODULES[module_name]
            print(f"\n{i}. {module_info['name']} ({module_name})")
            print(f"   {module_info['description']}")

    print("\n" + "-" * 80)
    print("\nWould you like to view the detailed guide for any of these modules?")
    print("Enter the module name or number (or 'n' to skip): ")
    logger.info(f"Displayed chapter {chapter_num} guide")

def select_chapter_and_module() -> None:
    """Allow user to select a chapter and then a module."""
    print_chapters()

    chapter_choice = input("Enter chapter number (1-5) or name (chapter_1, etc.): ").strip()

    # Convert number to chapter key
    if chapter_choice.isdigit() and 1 <= int(chapter_choice) <= len(CHAPTERS):
        chapter_key = f"chapter_{chapter_choice}"
    else:
        chapter_key = chapter_choice

    if chapter_key not in CHAPTERS:
        print(f"Invalid chapter selection: {chapter_choice}")
        logger.warning(f"Invalid chapter selection: {chapter_choice}")
        return

    chapter = CHAPTERS[chapter_key]
    print_chapter_guide(chapter_key)

    # Ask user to select a module from the chapter
    print("\nModules in this chapter:")
    for i, module_name in enumerate(chapter['modules'], 1):
        print(f"  {i}. {module_name}")

    module_choice = input("\nSelect module number or name (or 'n' to skip): ").strip()

    if module_choice.lower() == 'n':
        return

    if module_choice.isdigit() and 1 <= int(module_choice) <= len(chapter['modules']):
        module_name = chapter['modules'][int(module_choice) - 1]
    else:
        module_name = module_choice

    if module_name in MODULES:
        print_module_guide(module_name)
        input("\nPress Enter to continue...")
    else:
        print(f"Invalid module selection: {module_choice}")
        logger.warning(f"Invalid module selection: {module_choice}")

def print_interactive_menu() -> None:
    """Display interactive menu."""
    while True:
        print_header("MEDKIT MEDICAL MODULE USER GUIDE")

        print("Select an option:")
        print("  1. Browse chapters")
        print("  2. List all modules")
        print("  3. View module guide")
        print("  4. Search modules")
        print("  5. Quick reference")
        print("  6. Exit\n")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            select_chapter_and_module()

        elif choice == "2":
            print_module_list()

        elif choice == "3":
            print("\nAvailable modules:")
            for i, key in enumerate(MODULES.keys(), 1):
                print(f"  {i:2d}. {key}")

            try:
                module_idx = int(input("\nEnter module number or name: ").strip())
                if isinstance(module_idx, int) and 1 <= module_idx <= len(MODULES):
                    module_name = list(MODULES.keys())[module_idx - 1]
                else:
                    module_name = input("Enter module name: ").strip()
            except (ValueError, IndexError):
                module_name = input("Enter module name: ").strip()

            print_module_guide(module_name)
            input("\nPress Enter to continue...")

        elif choice == "4":
            keyword = input("\nEnter search keyword: ").strip()
            if keyword:
                search_modules(keyword)
            input("\nPress Enter to continue...")

        elif choice == "5":
            print_quick_reference()
            input("\nPress Enter to continue...")

        elif choice == "6":
            print("\nThank you for using MedKit Medical Module Guide!")
            logger.info("User exited interactive menu")
            break

        else:
            print("Invalid choice. Please try again.")

def print_quick_reference() -> None:
    """Print quick reference guide."""
    print_header("QUICK REFERENCE GUIDE")

    print("Common Usage Patterns:\n")

    print("1. GENERATE MEDICAL INFORMATION:")
    print("   from medical_topic import get_topic_info")
    print("   result = get_topic_info('Diabetes')")
    print("   result.save_to_file()\n")

    print("2. EXTRACT MEDICAL TERMS FROM TEXT:")
    print("   from medical_term_extractor import extract_medical_terms")
    print("   result = extract_medical_terms('Patient has diabetes...')")
    print("   print(result.diseases)\n")

    print("3. LOOK UP MEDICAL TERMS:")
    print("   from medical_dictionary import MedicalDictionary")
    print("   dict = MedicalDictionary()")
    print("   entry = dict.query('Hypertension')\n")

    print("4. GENERATE SURGICAL INFO:")
    print("   from surgery_info import get_surgery_info")
    print("   result = get_surgery_info('Knee Replacement')\n")

    print("5. QUERY SPECIALISTS:")
    print("   from medical_speciality import generate_specialist_database")
    print("   db = generate_specialist_database()")
    print("   specialists = db.search_by_condition('diabetes')\n")

    print("Key Notes:")
    print("  • All modules use Pydantic for data validation")
    print("  • JSON output is saved to outputs/ folder by default")
    print("  • Logs are stored in logs/ folder")
    print("  • Use logging to track module execution")
    print("  • Most modules support custom output paths\n")

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="MedKit Medical Module User Guide",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--chapters", action="store_true",
                       help="List all chapters")
    parser.add_argument("--chapter", type=str,
                       help="Show guide for specific chapter (1-5 or chapter_N)")
    parser.add_argument("--list", action="store_true",
                       help="List all available modules")
    parser.add_argument("--module", type=str,
                       help="Show guide for specific module")
    parser.add_argument("--search", type=str,
                       help="Search modules by keyword")
    parser.add_argument("--reference", action="store_true",
                       help="Show quick reference guide")

    args = parser.parse_args()

    if args.chapters:
        print_chapters()

    elif args.chapter:
        # Convert number to chapter key if needed
        if args.chapter.isdigit() and 1 <= int(args.chapter) <= len(CHAPTERS):
            chapter_key = f"chapter_{args.chapter}"
        else:
            chapter_key = args.chapter

        print_chapter_guide(chapter_key)

    elif args.list:
        print_module_list()

    elif args.module:
        print_module_guide(args.module)

    elif args.search:
        search_modules(args.search)

    elif args.reference:
        print_quick_reference()

    else:
        # Interactive menu if no arguments provided
        try:
            print_interactive_menu()
        except KeyboardInterrupt:
            print("\n\nExiting user guide...")
            logger.info("User interrupted guide with Ctrl+C")

if __name__ == "__main__":
    logger.info("MedKit Medical Module User Guide started")
    main()
    logger.info("MedKit Medical Module User Guide ended")
