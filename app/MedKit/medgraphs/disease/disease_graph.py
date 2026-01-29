from core import DiseaseTripletExtractor, DiseaseGraphBuilder, GraphVisualizer

# =========================
# 5️⃣ Main Runner
# =========================
if __name__ == "__main__":
    text = """
    Diabetes Mellitus is a chronic metabolic disease caused by insulin deficiency or resistance.
    It is characterized by increased thirst, frequent urination, and weight loss.
    Obesity is a major risk factor.
    Diagnosis is done by a blood sugar test.
    Untreated diabetes may lead to kidney failure.
    """

    extractor = DiseaseTripletExtractor()  # Uses GEMINI_API_KEY from environment
    triples = extractor.extract(text)

    print("✅ Extracted Disease Triples:")
    for t in triples:
        print(t.dict())

    builder = DiseaseGraphBuilder()
    builder.add_triples(triples)

    print("🔹 Symptoms of Diabetes:", builder.query_symptoms("Diabetes Mellitus"))
    print("🔹 Treatments for Diabetes:", builder.query_treatments("Diabetes Mellitus"))

    builder.export_json("disease_graph.json")

    visualizer = GraphVisualizer(builder.G)
    visualizer.show()