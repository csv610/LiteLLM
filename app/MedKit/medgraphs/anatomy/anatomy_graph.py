
from .core import AnatomyTripletExtractor, AnatomyGraphBuilder, GraphVisualizer

# =========================
# 5️⃣ Runner
# =========================
if __name__ == "__main__":
    text = """
    The heart is a muscular organ located in the thoracic cavity.
    It is part of the circulatory system, supplied by the coronary arteries,
    drained by cardiac veins, and innervated by the vagus nerve.
    The rib cage protects the heart, while the diaphragm supports it.
    """

    extractor = AnatomyTripletExtractor()  # Uses GEMINI_API_KEY from environment
    triples = extractor.extract(text)

    print("✅ Extracted Anatomy Triples:")
    for t in triples:
        print(t.dict())

    builder = AnatomyGraphBuilder()
    builder.add_triples(triples)

    print("🔹 Systems containing Heart:", builder.query_part_of("Heart"))
    print("🔹 Organs adjacent to Heart:", builder.query_connections("Heart"))

    builder.export_json("anatomy_graph.json")

    visualizer = GraphVisualizer(builder.G)
    visualizer.show()
