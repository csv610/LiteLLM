from core import PathophysiologyTripletExtractor, PathophysiologyGraphBuilder, GraphVisualizer

# =========================
# 5️⃣ Runner
# =========================
if __name__ == "__main__":
    text = """
    Infection triggers inflammation, which causes cytokine release.
    Cytokine release leads to fever and tissue damage.
    Fever is often alleviated by paracetamol.
    """

    extractor = PathophysiologyTripletExtractor()  # Uses GEMINI_API_KEY from environment
    triples = extractor.extract(text)

    print("✅ Extracted Triples:")
    for t in triples:
        print(t.dict())

    builder = PathophysiologyGraphBuilder()
    builder.add_triples(triples)
    builder.export_json("pathophysiology_graph.json")

    visualizer = GraphVisualizer(builder.G)
    visualizer.show()