from core import MedicineTripletExtractor, MedicineGraphBuilder, GraphVisualizer

# =========================
# 5️⃣ Main Runner
# =========================
if __name__ == "__main__":
    text = """
    Paracetamol is an analgesic and antipyretic used to treat fever and mild pain.
    It may cause liver toxicity and is contraindicated in patients with liver disease.
    """

    extractor = MedicineTripletExtractor()  # Uses GEMINI_API_KEY from environment
    triples = extractor.extract(text)

    print("✅ Extracted & validated triples:")
    for t in triples:
        print(t.dict())

    builder = MedicineGraphBuilder()
    builder.add_triples(triples)

    print("🔹 Drugs that treat Fever:", builder.query_treats("Fever"))
    print("🔹 Side effects of Paracetamol:", builder.query_side_effects("Paracetamol"))

    builder.export_json("medicine_graph.json")

    visualizer = GraphVisualizer(builder.G)
    visualizer.show()