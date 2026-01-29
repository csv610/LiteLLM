"""rxclass_examples - Comprehensive demonstrations of RxClass API use cases.

This module showcases practical applications of the National Library of Medicine's RxClass
API through six real-world use cases. Each example demonstrates how to retrieve drug
classifications, navigate class hierarchies, identify therapeutic relationships,
contraindications, disease treatment options, and prepare for drug interaction checking.
Examples use both RxClass and RxNorm APIs together for comprehensive drug information.

QUICK START:
    Run all use case demonstrations:

    $ python rxclass_examples.py

    The script will display detailed output for each of the 6 use cases showing
    practical patterns for working with drug classification data.

COMMON USES:
    1. Drug classification lookup - understanding therapeutic categories for medications
    2. Contraindication identification - finding disease/drug conflicts
    3. Treatment discovery - finding drugs for specific conditions
    4. Class hierarchy exploration - understanding drug classification systems
    5. Drug profile generation - comprehensive medication information
    6. Interaction preparation - gathering data for interaction checking

KEY FEATURES AND COVERAGE AREAS:
    - Use Case 1: Drug Classification System - ATC and MEDRT classifications
    - Use Case 2: Contraindication Checking - disease/drug conflicts and therapeutic uses
    - Use Case 3: Drug Hierarchy Navigation - ATC class trees and subclasses
    - Use Case 4: Disease Treatment Options - finding drugs for conditions
    - Use Case 5: Complete Drug Profile - comprehensive classification data
    - Use Case 6: Drug Interaction Preparation - gathering interaction-relevant data
    - RxNorm Integration: converting drug names to RxCUI identifiers
    - Data Source Handling: working with ATC, MEDRT, and other classification systems
    - Relationship Types: navigating may_treat, ci_with, and other relationships
"""

import requests
import json
from typing import Dict, List, Any, Optional

# =============================================================================
# RxClass API Wrapper
# =============================================================================

class RxClassClient:
    """Client for RxClass API - Drug classification and relationships"""

    BASE_URL = "https://rxnav.nlm.nih.gov/REST/rxclass"

    def __init__(self):
        self.session = requests.Session()

    def get_classes_by_rxcui(self, rxcui: str, rela_source: str = "MEDRT") -> Dict[str, Any]:
        """Get classes containing a specific drug (by RxCUI)"""
        response = self.session.get(
            f"{self.BASE_URL}/class/byRxcui.json",
            params={"rxcui": rxcui, "relaSource": rela_source}
        )
        return response.json() if response.status_code == 200 else {}

    def get_classes_by_drug_name(self, drug_name: str, rela_source: str = "MEDRT") -> Dict[str, Any]:
        """Get classes for a drug by name"""
        response = self.session.get(
            f"{self.BASE_URL}/class/byDrugName.json",
            params={"drugName": drug_name, "relaSource": rela_source}
        )
        return response.json() if response.status_code == 200 else {}

    def find_class_by_name(self, class_name: str) -> Dict[str, Any]:
        """Find drug classes by name"""
        response = self.session.get(
            f"{self.BASE_URL}/class/byName.json",
            params={"className": class_name}
        )
        return response.json() if response.status_code == 200 else {}

    def get_class_tree(self, class_id: str, rela_source: str = "ATC") -> Dict[str, Any]:
        """Get class hierarchy/subclasses"""
        response = self.session.get(
            f"{self.BASE_URL}/classTree.json",
            params={"classId": class_id, "relaSource": rela_source}
        )
        return response.json() if response.status_code == 200 else {}

    def get_class_members(self, class_id: str, rela_source: str = "ATC") -> Dict[str, Any]:
        """Get drugs in a specific class"""
        response = self.session.get(
            f"{self.BASE_URL}/classMembers.json",
            params={"classId": class_id, "relaSource": rela_source}
        )
        return response.json() if response.status_code == 200 else {}

    def get_class_types(self) -> List[str]:
        """Get available class types"""
        response = self.session.get(f"{self.BASE_URL}/classTypes.json")
        data = response.json()
        if "classTypeList" in data:
            return data["classTypeList"].get("classTypeName", [])
        return []

    def get_rela_sources(self) -> List[str]:
        """Get available relationship sources"""
        response = self.session.get(f"{self.BASE_URL}/relaSources.json")
        data = response.json()
        if "relaSourceList" in data:
            return data["relaSourceList"].get("relaSourceName", [])
        return []

    def get_relas(self, source: str) -> List[str]:
        """Get relationship types from a source"""
        response = self.session.get(
            f"{self.BASE_URL}/relas.json",
            params={"source": source}
        )
        data = response.json()
        if "relaList" in data:
            return data["relaList"].get("rela", [])
        return []

# =============================================================================
# RxNorm Client (for getting RxCUI from drug names)
# =============================================================================

class RxNormClient:
    """Client for RxNorm API"""

    BASE_URL = "https://rxnav.nlm.nih.gov/REST"

    def __init__(self):
        self.session = requests.Session()

    def get_identifier(self, name: str) -> Optional[str]:
        """Get RxCUI for a drug name"""
        url = f"{self.BASE_URL}/rxcui.json"
        response = self.session.get(url, params={"name": name})
        data = response.json()
        ids = data.get("idGroup", {}).get("rxnormId")
        return ids[0] if ids else None

# =============================================================================
# USE CASE 1: Drug Classification System
# =============================================================================

def use_case_1_drug_classification():
    """
    USE CASE 1: Get comprehensive drug classification
    Find all therapeutic classes and properties for a drug
    """
    print("\n" + "="*80)
    print("USE CASE 1: DRUG CLASSIFICATION SYSTEM")
    print("="*80)
    print("Objective: Get all therapeutic classes for a specific drug")
    print("-"*80)

    rxnorm = RxNormClient()
    rxclass = RxClassClient()

    drug_name = "Aspirin"
    print(f"\n🔍 Looking up drug: {drug_name}")

    # Step 1: Get RxCUI
    rxcui = rxnorm.get_identifier(drug_name)
    if not rxcui:
        print(f"❌ Drug not found: {drug_name}")
        return

    print(f"✅ Found RxCUI: {rxcui}")

    # Step 2: Get ATC classifications
    print(f"\n📊 ATC Classifications (Anatomical Therapeutic Chemical):")
    atc_data = rxclass.get_classes_by_rxcui(rxcui, rela_source="ATC")

    if "rxclassDrugInfoList" in atc_data:
        drugs_info = atc_data["rxclassDrugInfoList"].get("rxclassDrugInfo", [])
        for idx, drug_info in enumerate(drugs_info[:5], 1):
            class_item = drug_info.get("rxclassMinConceptItem", {})
            class_id = class_item.get("classId", "N/A")
            class_name = class_item.get("className", "N/A")
            class_type = class_item.get("classType", "N/A")
            print(f"   {idx}. {class_name}")
            print(f"      ID: {class_id} | Type: {class_type}")

    # Step 3: Get MEDRT classifications (therapeutic indications)
    print(f"\n💊 MEDRT Classifications (Medical Reference Terminology):")
    medrt_data = rxclass.get_classes_by_rxcui(rxcui, rela_source="MEDRT")

    if "rxclassDrugInfoList" in medrt_data:
        drugs_info = medrt_data["rxclassDrugInfoList"].get("rxclassDrugInfo", [])

        # Group by relationship type
        by_rela = {}
        for drug_info in drugs_info[:10]:
            rela = drug_info.get("rela", "Unknown")
            class_item = drug_info.get("rxclassMinConceptItem", {})
            if rela not in by_rela:
                by_rela[rela] = []
            by_rela[rela].append({
                "name": class_item.get("className"),
                "type": class_item.get("classType")
            })

        for rela, items in by_rela.items():
            print(f"\n   Relationship: {rela}")
            for item in items[:3]:
                print(f"      • {item['name']} ({item['type']})")

# =============================================================================
# USE CASE 2: Contraindication Check
# =============================================================================

def use_case_2_contraindication_check():
    """
    USE CASE 2: Check for contraindications
    Find diseases/conditions where a drug is contraindicated
    """
    print("\n" + "="*80)
    print("USE CASE 2: CONTRAINDICATION CHECK")
    print("="*80)
    print("Objective: Find diseases/conditions contraindicated with a drug")
    print("-"*80)

    rxclass = RxClassClient()

    drug_name = "Metformin"
    print(f"\n💉 Checking contraindications for: {drug_name}")

    # Get MEDRT classifications which include contraindications
    medrt_data = rxclass.get_classes_by_drug_name(drug_name, rela_source="MEDRT")

    if "rxclassDrugInfoList" in medrt_data:
        drugs_info = medrt_data["rxclassDrugInfoList"].get("rxclassDrugInfo", [])

        # Filter by relationship type
        contraindications = []
        treatments = []
        preventions = []

        for drug_info in drugs_info:
            rela = drug_info.get("rela", "")
            class_item = drug_info.get("rxclassMinConceptItem", {})

            class_info = {
                "name": class_item.get("className"),
                "type": class_item.get("classType"),
                "id": class_item.get("classId")
            }

            if rela == "ci_with":
                contraindications.append(class_info)
            elif rela == "may_treat":
                treatments.append(class_info)
            elif rela == "may_prevent":
                preventions.append(class_info)

        if contraindications:
            print(f"\n⚠️  CONTRAINDICATIONS (ci_with):")
            for idx, item in enumerate(contraindications[:5], 1):
                print(f"   {idx}. {item['name']}")
                print(f"      Type: {item['type']}")

        if treatments:
            print(f"\n✅ THERAPEUTIC USES (may_treat):")
            for idx, item in enumerate(treatments[:5], 1):
                print(f"   {idx}. {item['name']}")

        if preventions:
            print(f"\n🛡️  PREVENTIVE USES (may_prevent):")
            for idx, item in enumerate(preventions[:5], 1):
                print(f"   {idx}. {item['name']}")
    else:
        print("❌ No data found")

# =============================================================================
# USE CASE 3: Drug Class Hierarchy Navigation
# =============================================================================

def use_case_3_drug_hierarchy():
    """
    USE CASE 3: Navigate drug class hierarchies
    Show complete classification tree for a drug class
    """
    print("\n" + "="*80)
    print("USE CASE 3: DRUG CLASS HIERARCHY NAVIGATION")
    print("="*80)
    print("Objective: Show drug class hierarchy tree")
    print("-"*80)

    rxclass = RxClassClient()

    # Start with analgesics
    class_id = "N02"
    print(f"\n🌳 Analgesics Drug Class Hierarchy (ATC Code: {class_id})")

    def print_tree(tree_data, indent=0):
        """Recursively print class tree"""
        if isinstance(tree_data, list):
            for item in tree_data:
                print_tree(item, indent)
        elif isinstance(tree_data, dict):
            concept = tree_data.get("rxclassMinConceptItem", {})
            if concept:
                class_id = concept.get("classId", "")
                class_name = concept.get("className", "")
                class_type = concept.get("classType", "")
                prefix = "   " * indent + "├─ "
                print(f"{prefix}{class_id}: {class_name} ({class_type})")

            # Recursively print children
            children = tree_data.get("rxclassTree", [])
            if children:
                print_tree(children, indent + 1)

    tree_data = rxclass.get_class_tree(class_id, rela_source="ATC")
    if "rxclassTree" in tree_data:
        print_tree(tree_data["rxclassTree"])
    else:
        print("❌ No hierarchy data found")

    # Show available class types
    print(f"\n📋 Available Classification Systems:")
    class_types = rxclass.get_class_types()
    for i, ctype in enumerate(class_types, 1):
        print(f"   {i}. {ctype}")

# =============================================================================
# USE CASE 4: Disease Treatment Options
# =============================================================================

def use_case_4_disease_treatments():
    """
    USE CASE 4: Find drugs that treat specific diseases
    Look up what drugs are indicated for a disease
    """
    print("\n" + "="*80)
    print("USE CASE 4: DISEASE TREATMENT OPTIONS")
    print("="*80)
    print("Objective: Find drugs indicated for specific diseases")
    print("-"*80)

    rxclass = RxClassClient()

    # Find disease classes
    print("\n🔍 Searching for 'Diabetes' disease classes...")
    diabetes_classes = rxclass.find_class_by_name("Diabetes")

    if "rxclassMinConceptList" in diabetes_classes:
        concepts = diabetes_classes["rxclassMinConceptList"].get("rxclassMinConcept", [])

        print(f"Found {len(concepts)} related classes:")
        for idx, concept in enumerate(concepts[:5], 1):
            class_id = concept.get("classId")
            class_name = concept.get("className")
            class_type = concept.get("classType")
            print(f"\n   {idx}. {class_name} (Type: {class_type})")
            print(f"      ID: {class_id}")

        # For the first result, show available sources and relationships
        if concepts:
            first_class = concepts[0]
            class_id = first_class.get("classId")

            print(f"\n📊 Available Data Sources:")
            sources = rxclass.get_rela_sources()
            for source in sources[:5]:
                print(f"   • {source}")

            print(f"\n🔗 Available Relationships:")
            relationships = rxclass.get_relas("MEDRT")
            relationship_desc = {
                "may_treat": "May treat this disease",
                "may_prevent": "May prevent this disease",
                "ci_with": "Contraindicated with",
                "has_moa": "Has mechanism of action",
                "has_pe": "Has pharmacologic effect"
            }
            for rela in relationships[:10]:
                desc = relationship_desc.get(rela, "Relationship type")
                if rela:  # Skip empty strings
                    print(f"   • {rela:25s} - {desc}")

# =============================================================================
# USE CASE 5: Complete Drug Profile
# =============================================================================

def use_case_5_complete_drug_profile():
    """
    USE CASE 5: Generate complete drug profile
    Comprehensive view of a drug with all classifications and relationships
    """
    print("\n" + "="*80)
    print("USE CASE 5: COMPLETE DRUG PROFILE")
    print("="*80)
    print("Objective: Generate comprehensive drug profile")
    print("-"*80)

    rxnorm = RxNormClient()
    rxclass = RxClassClient()

    drug_names = ["Ibuprofen", "Lisinopril", "Omeprazole"]

    for drug_name in drug_names:
        print(f"\n{'='*80}")
        print(f"Drug: {drug_name}")
        print(f"{'='*80}")

        # Get RxCUI
        rxcui = rxnorm.get_identifier(drug_name)
        if not rxcui:
            print(f"❌ Not found")
            continue

        print(f"✅ RxCUI: {rxcui}")

        # Get all classifications
        print(f"\n📋 CLASSIFICATIONS:")

        # ATC
        print(f"\n  ATC (Anatomical Therapeutic Chemical):")
        atc_data = rxclass.get_classes_by_rxcui(rxcui, rela_source="ATC")
        if "rxclassDrugInfoList" in atc_data:
            drugs_info = atc_data["rxclassDrugInfoList"].get("rxclassDrugInfo", [])
            for drug_info in drugs_info[:3]:
                class_item = drug_info.get("rxclassMinConceptItem", {})
                print(f"     • {class_item.get('className')} ({class_item.get('classId')})")

        # MEDRT
        print(f"\n  MEDRT (Medical Reference Terminology):")
        medrt_data = rxclass.get_classes_by_rxcui(rxcui, rela_source="MEDRT")
        if "rxclassDrugInfoList" in medrt_data:
            drugs_info = medrt_data["rxclassDrugInfoList"].get("rxclassDrugInfo", [])

            # Count by relationship
            rela_count = {}
            for drug_info in drugs_info:
                rela = drug_info.get("rela", "other")
                rela_count[rela] = rela_count.get(rela, 0) + 1

            for rela, count in rela_count.items():
                if rela:
                    print(f"     • {rela}: {count} relationships")

# =============================================================================
# USE CASE 6: Drug Interaction Preparation
# =============================================================================

def use_case_6_interaction_preparation():
    """
    USE CASE 6: Prepare for drug interaction checking
    Get classification data needed for interaction checking
    """
    print("\n" + "="*80)
    print("USE CASE 6: DRUG INTERACTION PREPARATION")
    print("="*80)
    print("Objective: Get data needed for interaction checking")
    print("-"*80)

    rxnorm = RxNormClient()
    rxclass = RxClassClient()

    # Get common interaction-related data sources
    print(f"\n📊 Available Data Sources for Interactions:")
    sources = rxclass.get_rela_sources()
    for source in sources:
        print(f"   • {source}")

    # Get interaction-related relationships
    print(f"\n🔗 Interaction-Related Relationships (from MEDRT):")
    relationships = rxclass.get_relas("MEDRT")
    interaction_relas = ["ci_with", "induces", "has_moa", "site_of_metabolism"]
    for rela in interaction_relas:
        if rela in relationships:
            print(f"   ✅ {rela}")

    # Example: Check for enzyme induction
    print(f"\n💊 Example: Looking for drug interactions...")
    drugs = ["Aspirin", "Metformin"]

    print(f"\nDrugs to check: {', '.join(drugs)}")
    drug_profiles = {}

    for drug in drugs:
        rxcui = rxnorm.get_identifier(drug)
        if rxcui:
            medrt = rxclass.get_classes_by_rxcui(rxcui, rela_source="MEDRT")
            if "rxclassDrugInfoList" in medrt:
                drugs_info = medrt["rxclassDrugInfoList"].get("rxclassDrugInfo", [])

                # Extract interaction-relevant info
                interactions = []
                for drug_info in drugs_info:
                    rela = drug_info.get("rela")
                    if rela in ["ci_with", "induces"]:
                        class_item = drug_info.get("rxclassMinConceptItem", {})
                        interactions.append({
                            "relationship": rela,
                            "class": class_item.get("className")
                        })

                if interactions:
                    drug_profiles[drug] = interactions

    print(f"\n⚠️  Potential Interactions Found:")
    for drug, interactions in drug_profiles.items():
        print(f"\n   {drug}:")
        for interaction in interactions[:3]:
            print(f"      • {interaction['relationship']}: {interaction['class']}")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def cli():
    """Run all use cases"""
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  RXCLASS API - COMPREHENSIVE USE CASE DEMONSTRATIONS".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)

    try:
        use_case_1_drug_classification()
        use_case_2_contraindication_check()
        use_case_3_drug_hierarchy()
        use_case_4_disease_treatments()
        use_case_5_complete_drug_profile()
        use_case_6_interaction_preparation()

        print("\n" + "█"*80)
        print("█" + " "*78 + "█")
        print("█" + "  ALL USE CASES COMPLETED SUCCESSFULLY!".center(78) + "█")
        print("█" + " "*78 + "█")
        print("█"*80 + "\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    cli()
