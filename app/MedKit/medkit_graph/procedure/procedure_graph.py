from core import ProcedureTripletExtractor, ProcedureGraphBuilder, GraphVisualizer

if __name__ == "__main__":
    text = """
    Appendectomy is a surgical procedure to remove the appendix.
    It is used to treat appendicitis.
    Risks include infection and bleeding.
    """

    extractor = ProcedureTripletExtractor()
    triples = extractor.extract(text)

    print("✅ Extracted Procedure Triples:")
    for t in triples:
        print(t.dict())

    builder = ProcedureGraphBuilder()
    builder.add_triples(triples)

    print("🔹 Procedures treating Appendicitis:", builder.query_treats("Appendicitis"))

    builder.export_json("procedure_graph.json")

    visualizer = GraphVisualizer(builder.G)
    visualizer.show()