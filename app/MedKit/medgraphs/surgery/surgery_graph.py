from core import SurgeryTripletExtractor, SurgeryGraphBuilder, GraphVisualizer

# =========================
# 5️⃣ Runner
# =========================
if __name__ == "__main__":
    text = """
    Coronary Artery Bypass Surgery is performed to treat coronary artery disease.
    It involves grafting blood vessels to bypass blocked arteries in the heart.
    It is done by a cardiothoracic surgeon under general anesthesia.
    Risks include bleeding, infection, and heart attack.
    Patients undergo cardiac rehabilitation after surgery.
    """

    extractor = SurgeryTripletExtractor()  # Uses GEMINI_API_KEY from environment
    triples = extractor.extract(text)

    print("✅ Extracted Surgical Triples:")
    for t in triples:
        print(t.dict())

    builder = SurgeryGraphBuilder()
    builder.add_triples(triples)

    print("🔹 Surgeries that treat Coronary Artery Disease:", builder.query_treats("Coronary Artery Disease"))
    print("🔹 Risks of CABG:", builder.query_risks("Coronary Artery Bypass Surgery"))

    builder.export_json("surgery_graph.json")

    visualizer = GraphVisualizer(builder.G)
    visualizer.show()