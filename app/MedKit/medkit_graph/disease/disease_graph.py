from disease_models import DiseaseTripletExtractor, DiseaseGraphBuilder, GraphVisualizer

# =========================
# 5️⃣ Main Runner
# =========================
if __name__ == "__main__":
    text = """
    Malaria is a life-threatening disease caused by Plasmodium parasites that are transmitted through the bites of infected female Anopheles mosquitoes.
    Symptoms of malaria include fever, chills, headache, nausea, and vomiting.
    It primarily affects the liver and red blood cells.
    Standing water is a major risk factor as it serves as a breeding ground for mosquitoes.
    Severe malaria can lead to complications such as cerebral malaria, anemia, and organ failure.
    Treatment typically involves antimalarial medications like Artemisinin-based combination therapy (ACT).
    Prevention strategies include using mosquito nets and indoor residual spraying.
    """

    extractor = DiseaseTripletExtractor()  
    triples = extractor.extract(text)

    print("✅ Extracted Disease Triples:")
    for t in triples:
        print(t.model_dump())

    builder = DiseaseGraphBuilder()
    builder.add_triples(triples)

    print("\n🔹 Symptoms of Malaria:", builder.query_symptoms("Malaria"))
    print("🔹 Treatments for Malaria:", builder.query_treatments("Malaria"))

    builder.export_dot("malaria")

    visualizer = GraphVisualizer(builder)
    visualizer.show()
