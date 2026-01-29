from core import SymptomTripletExtractor, SymptomGraphBuilder, GraphVisualizer

# =========================
# 5️⃣ Runner
# =========================
if __name__ == "__main__":
    text = """
    Fever is a common symptom associated with infections such as malaria or flu.
    It causes elevation of body temperature and may affect the whole body.
    Blood tests are used for diagnosis, and paracetamol is often used for treatment.
    Prolonged fever may lead to dehydration.
    """

    extractor = SymptomTripletExtractor()  # Uses GEMINI_API_KEY from environment
    triples = extractor.extract(text)

    print("✅ Extracted Symptom Triples:")
    for t in triples:
        print(t.dict())

    builder = SymptomGraphBuilder()
    builder.add_triples(triples)

    print("🔹 Diseases related to Fever:", builder.query_diseases("Fever"))
    print("🔹 Treatments for Fever:", builder.query_treatments("Fever"))

    builder.export_json("symptom_graph.json")

    visualizer = GraphVisualizer(builder.G)
    visualizer.show()