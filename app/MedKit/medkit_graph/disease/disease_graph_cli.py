from disease_models import DiseaseKnowledgeGraphBuilder, GraphVisualizer, Triple

# =========================
# 5️⃣ Main Runner
# =========================
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        disease_name = " ".join(sys.argv[1:])
    else:
        disease_name = input("Enter disease name: ").strip()

    if not disease_name:
        print("❌ No disease name provided.")
        sys.exit(1)

    print(f"🔍 Generating knowledge graph for: {disease_name}...")
    
    builder = DiseaseKnowledgeGraphBuilder()
    triples = builder.build_from_name(disease_name)

    if not triples:
        print(f"❌ Could not generate information for '{disease_name}'.")
        sys.exit(1)

    print(f"✅ Created {len(triples)} Disease Triples:")
    for t in triples:
        print(t.model_dump())

    # Use the first part of the disease name for query if it's long, or just the full name
    q_name = disease_name.split()[0] if " " in disease_name else disease_name

    print(
        f"\n🔹 Symptoms of {disease_name}:",
        builder.query_symptoms(disease_name) or builder.query_symptoms(q_name),
    )
    print(
        f"🔹 Treatments for {disease_name}:",
        builder.query_treatments(disease_name) or builder.query_treatments(q_name),
    )

    builder.export_dot(disease_name)

    visualizer = GraphVisualizer(builder)
    visualizer.show()
