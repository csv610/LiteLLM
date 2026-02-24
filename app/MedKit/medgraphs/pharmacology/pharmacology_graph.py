from core import PharmacologyTripletExtractor, PharmacologyGraphBuilder, GraphVisualizer

# =========================
# 5️⃣ Runner
# =========================
if __name__ == "__main__":
    text = """
    Paracetamol is an analgesic and antipyretic drug.
    It inhibits the cyclooxygenase enzyme, reducing prostaglandin synthesis.
    This leads to pain relief and fever reduction.
    Paracetamol is metabolized by the liver and eliminated through the kidneys.
    """

    extractor = PharmacologyTripletExtractor()  # Uses GEMINI_API_KEY from environment
    triples = extractor.extract(text)

    print("✅ Extracted Pharmacology Triples:")
    for t in triples:
        print(t.dict())

    builder = PharmacologyGraphBuilder()
    builder.add_triples(triples)

    print("🔹 Targets of Paracetamol:", builder.query_targets("Paracetamol"))
    print("🔹 Effects of Paracetamol:", builder.query_effects("Paracetamol"))

    builder.export_json("pharmacology_graph.json")

    visualizer = GraphVisualizer(builder.G)
    visualizer.show()