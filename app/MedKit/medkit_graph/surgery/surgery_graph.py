from surgery_models import SurgeryTripletExtractor, SurgeryGraphBuilder
import os

# =========================
# 5️⃣ Runner
# =========================
def generate_surgery_graph(surgery_name: str, text: str):
    print(f"🚀 Generating Knowledge Graph for: {surgery_name}")
    
    extractor = SurgeryTripletExtractor()
    triples = extractor.extract(text)

    if not triples:
        print("❌ No triples extracted.")
        return

    print(f"✅ Extracted {len(triples)} Surgical Triples")

    builder = SurgeryGraphBuilder()
    builder.add_triples(triples)

    # Export to .dot as requested
    builder.export_dot(surgery_name)
    
    # Also export to JSON for utility
    builder.export_json(f"outputs/{surgery_name.replace(' ', '_').lower()}_graph.json")

if __name__ == "__main__":
    surgery = "Coronary Artery Bypass Surgery"
    description = """
    Coronary Artery Bypass Surgery (CABG) is performed to treat coronary artery disease.
    It involves grafting blood vessels to bypass blocked arteries in the heart.
    It is done by a cardiothoracic surgeon under general anesthesia.
    Risks include bleeding, infection, and heart attack.
    Patients undergo cardiac rehabilitation after surgery.
    """
    
    generate_surgery_graph(surgery, description)
