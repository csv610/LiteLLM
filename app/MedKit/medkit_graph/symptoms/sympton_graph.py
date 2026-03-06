import sys
import os
from sympton_models import SymptomTripletExtractor, SymptomGraphBuilder, GraphVisualizer

def generate_symptom_graph(symptom_name: str, text: str = None):
    # Ensure outputs directory exists
    os.makedirs("outputs", exist_ok=True)

    if text is None:
        # Default text if none provided
        text = f"""
        {symptom_name} is a medical symptom that often indicates various conditions.
        It can be associated with specific diseases and might affect certain body parts.
        Diagnosis usually involves clinical tests, and treatment may include drugs or procedures.
        """

    print(f"🔍 Processing symptom: {symptom_name}")
    
    extractor = SymptomTripletExtractor()
    triples = extractor.extract(text)

    print(f"✅ Extracted {len(triples)} triples.")
    
    builder = SymptomGraphBuilder()
    builder.add_triples(triples)

    # Export to DOT
    dot_filename = os.path.join("outputs", f"{symptom_name}.dot")
    builder.export_dot(dot_filename)

    # Also export to JSON for convenience
    json_filename = os.path.join("outputs", f"{symptom_name}.json")
    builder.export_json(json_filename)

    print(f"🚀 Graph for '{symptom_name}' generated successfully.")
    return dot_filename

if __name__ == "__main__":
    if len(sys.argv) > 1:
        symptom = sys.argv[1]
    else:
        symptom = "Fever"
    
    # Example text for Fever if it's the default
    if symptom == "Fever":
        text = """
        Fever is a common symptom associated with infections such as malaria or flu.
        It causes elevation of body temperature and may affect the whole body.
        Blood tests are used for diagnosis, and paracetamol is often used for treatment.
        Prolonged fever may lead to dehydration.
        """
    else:
        text = None

    generate_symptom_graph(symptom, text)
