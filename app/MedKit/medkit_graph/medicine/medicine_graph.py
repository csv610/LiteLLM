import os
from medicine_models import MedicineTripletExtractor, MedicineGraphBuilder, GraphVisualizer

# =========================
# 5️⃣ Main Runner
# =========================
if __name__ == "__main__":
    medicine_name = "Paracetamol"
    text = f"""
    {medicine_name} is an analgesic and antipyretic used to treat fever and mild pain.
    It may cause liver toxicity and is contraindicated in patients with liver disease.
    """

    extractor = MedicineTripletExtractor()  # Uses GEMINI_API_KEY from environment
    triples = extractor.extract(text)

    print("✅ Extracted & validated triples:")
    for t in triples:
        print(t.model_dump())

    builder = MedicineGraphBuilder()
    builder.add_triples(triples)

    print("🔹 Drugs that treat Fever:", builder.query_treats("Fever"))
    print("🔹 Side effects of Paracetamol:", builder.query_side_effects("Paracetamol"))

    # Ensure outputs directory exists
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    dot_filename = os.path.join(output_dir, f"{medicine_name}.dot")
    builder.export_dot(dot_filename)

    builder.export_json(os.path.join(output_dir, "medicine_graph.json"))

    # visualizer = GraphVisualizer(builder.G)
    # visualizer.show()