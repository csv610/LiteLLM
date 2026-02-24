from .core import GeneticsTripletExtractor, GeneticsGraphBuilder, GraphVisualizer

# =========================
# 5️⃣ Runner
# =========================
if __name__ == "__main__":
    text = """
    The BRCA1 gene encodes the BRCA1 protein, which plays a key role in DNA repair.
    Mutations in BRCA1 are associated with breast and ovarian cancers.
    The BRCA1 protein participates in the DNA repair pathway.
    Certain BRCA1 variants are pathogenic in hereditary breast cancer.
    "

    extractor = GeneticsTripletExtractor()  # Uses GEMINI_API_KEY from environment
    triples = extractor.extract(text)

    print("✅ Extracted Triples:")
    for t in triples:
        print(t.dict())

    builder = GeneticsGraphBuilder()
    builder.add_triples(triples)
    builder.export_json("genetics_graph.json")

    print("\n🔹 Disease-linked Genes (Breast Cancer):", builder.find_disease_genes("Breast Cancer"))
    print("🔹 Pathways involving BRCA1:", builder.find_gene_pathways("BRCA1"))

    visualizer = GraphVisualizer(builder.G)
    visualizer.show()