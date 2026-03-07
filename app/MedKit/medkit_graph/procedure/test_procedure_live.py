import argparse
from procedure_models import ModelConfig, ProcedureGraphBuilder

def run_live_test(procedure_name: str, model_name: str = "ollama/gemma3"):
    """Runs a live test for building a procedure graph."""
    print(f"🚀 Running live test for procedure: {procedure_name} (Model: {model_name})")
    
    config = ModelConfig(model=model_name)
    builder = ProcedureGraphBuilder(model_config=config)
    
    # Attempt to build triples
    triples = builder.build(procedure_name)
    
    if not triples:
        print(f"❌ Failed to extract any triples for {procedure_name}.")
        return

    print(f"✅ Successfully extracted {len(triples)} triples.")
    
    # Perform basic validation
    # Since we might be hitting a simulator or an LLM, let's check some properties
    valid_relations = set([
        "treats_disease", "used_for_diagnosis", "performed_on", "requires_instrument",
        "performed_by_specialist", "has_risk", "has_benefit", "has_complication",
        "has_contraindication", "requires_anesthesia", "requires_preparation", "follow_up_by", "related_to_procedure", "other"
    ])
    
    valid_nodes = set([
        "Procedure", "Disease", "Organ", "BodySystem", "Instrument", "Specialist", 
        "Risk", "Benefit", "Complication", "AnesthesiaType", "Preparation", "FollowUp", "Condition", "Contraindication", "Other"
    ])

    for i, t in enumerate(triples):
        print(f"  [{i+1}] {t.source} ({t.source_type}) --({t.relation})--> {t.target} ({t.target_type})")
        assert t.relation in valid_relations, f"Invalid relation: {t.relation}"
        assert t.source_type in valid_nodes, f"Invalid source type: {t.source_type}"
        assert t.target_type in valid_nodes, f"Invalid target type: {t.target_type}"

    print(f"\n✨ Live test for '{procedure_name}' passed basic validation.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Live test for Procedure Knowledge Graph")
    parser.add_argument("--procedure", type=str, default="Knee Replacement", help="Procedure to test")
    parser.add_argument("--model", type=str, default="ollama/gemma3", help="LLM model to use")
    
    args = parser.parse_args()
    run_live_test(args.procedure, args.model)
