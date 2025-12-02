import pytest
import json
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.cli.drugbank_medicine import (
    DrugType,
    DrugGroup,
    RouteOfAdministration,
    ChemicalProperties,
    Taxonomy,
    ExternalIdentifier,
    Patent,
    ATCCode,
    Interaction,
    FoodInteraction,
    Target,
    Enzyme,
    Carrier,
    Transporter,
    Pharmacodynamics,
    Pharmacokinetics,
    Dosage,
    ClinicalTrial,
    Manufacturer,
    PricingInfo,
    Contraindication,
    AdverseReaction,
    BasicInfo,
    Classification,
    Pharmacology,
    Indications,
    Administration,
    Interactions,
    Safety,
    Regulation,
    References,
    MedicineInfo,
    sanitize_filename,
)


class TestEnums:
    """Test enum classes"""

    def test_drug_type_values(self):
        assert DrugType.SMALL_MOLECULE.value == "small_molecule"
        assert DrugType.BIOTECH.value == "biotech"
        assert DrugType.VACCINE.value == "vaccine"
        assert DrugType.BIOLOGIC.value == "biologic"
        assert DrugType.HERB.value == "herb"

    def test_drug_group_values(self):
        assert DrugGroup.APPROVED.value == "approved"
        assert DrugGroup.EXPERIMENTAL.value == "experimental"
        assert DrugGroup.INVESTIGATIONAL.value == "investigational"
        assert DrugGroup.WITHDRAWN.value == "withdrawn"
        assert DrugGroup.ILLICIT.value == "illicit"
        assert DrugGroup.NUTRACEUTICAL.value == "nutraceutical"

    def test_route_of_administration_values(self):
        assert RouteOfAdministration.ORAL.value == "oral"
        assert RouteOfAdministration.INTRAVENOUS.value == "intravenous"
        assert RouteOfAdministration.TOPICAL.value == "topical"
        assert RouteOfAdministration.INHALATION.value == "inhalation"


class TestChemicalProperties:
    """Test ChemicalProperties model"""

    def test_minimal_chemical_properties(self):
        props = ChemicalProperties()
        assert props.molecular_formula is None
        assert props.molecular_weight is None

    def test_chemical_properties_with_data(self):
        props = ChemicalProperties(
            molecular_formula="C6H12O6",
            molecular_weight=180.156,
            smiles="C1=CC=CC=C1",
            cas_number="50-00-0",
        )
        assert props.molecular_formula == "C6H12O6"
        assert props.molecular_weight == 180.156
        assert props.smiles == "C1=CC=CC=C1"
        assert props.cas_number == "50-00-0"


class TestTaxonomy:
    """Test Taxonomy model"""

    def test_minimal_taxonomy(self):
        tax = Taxonomy()
        assert tax.kingdom is None
        assert tax.superclass is None

    def test_taxonomy_with_data(self):
        tax = Taxonomy(
            kingdom="Organic compounds",
            superclass="Benzene and substituted derivatives",
            drug_class="Phenols",
            subclass="Anilines",
            alternative_parents=["Aromatic compounds", "Alcohols"],
        )
        assert tax.kingdom == "Organic compounds"
        assert len(tax.alternative_parents) == 2


class TestDosage:
    """Test Dosage model"""

    def test_dosage_creation(self):
        dosage = Dosage(
            form="tablet",
            route=RouteOfAdministration.ORAL,
            strength="500mg",
            dosage_instructions="Take one tablet twice daily",
        )
        assert dosage.form == "tablet"
        assert dosage.route == RouteOfAdministration.ORAL
        assert dosage.strength == "500mg"
        assert dosage.dosage_instructions == "Take one tablet twice daily"

    def test_dosage_required_fields(self):
        with pytest.raises(Exception):  # ValidationError from Pydantic
            Dosage(form="tablet", route=RouteOfAdministration.ORAL)


class TestBasicInfo:
    """Test BasicInfo model"""

    def test_basic_info_minimal(self):
        info = BasicInfo(name="Aspirin")
        assert info.name == "Aspirin"
        assert info.synonyms == []
        assert info.drugbank_id is None

    def test_basic_info_with_data(self):
        info = BasicInfo(
            name="Aspirin",
            drugbank_id="DB00945",
            synonyms=["Acetylsalicylic acid", "ASA"],
            description="A salicylate drug",
        )
        assert info.name == "Aspirin"
        assert info.drugbank_id == "DB00945"
        assert len(info.synonyms) == 2


class TestClassification:
    """Test Classification model"""

    def test_classification_creation(self):
        classif = Classification(
            drug_type=DrugType.SMALL_MOLECULE,
            groups=[DrugGroup.APPROVED, DrugGroup.INVESTIGATIONAL],
            categories=["Analgesics", "Anti-inflammatory"],
        )
        assert classif.drug_type == DrugType.SMALL_MOLECULE
        assert len(classif.groups) == 2
        assert "Analgesics" in classif.categories


class TestMedicineInfo:
    """Test MedicineInfo model"""

    def test_medicine_info_minimal(self):
        basic = BasicInfo(name="Aspirin")
        medicine = MedicineInfo(basic_info=basic)
        assert medicine.basic_info.name == "Aspirin"
        assert medicine.classification is None
        assert medicine.pharmacology is None

    def test_medicine_info_complete(self):
        basic = BasicInfo(
            name="Aspirin",
            drugbank_id="DB00945",
            synonyms=["ASA"],
        )
        classif = Classification(
            drug_type=DrugType.SMALL_MOLECULE,
            groups=[DrugGroup.APPROVED],
        )
        dosages = [
            Dosage(
                form="tablet",
                route=RouteOfAdministration.ORAL,
                strength="500mg",
            )
        ]
        admin = Administration(dosages=dosages)

        medicine = MedicineInfo(
            basic_info=basic,
            classification=classif,
            administration=admin,
        )

        assert medicine.basic_info.name == "Aspirin"
        assert medicine.classification.drug_type == DrugType.SMALL_MOLECULE
        assert len(medicine.administration.dosages) == 1


class TestSanitizeFilename:
    """Test sanitize_filename function"""

    def test_sanitize_removes_special_characters(self):
        assert sanitize_filename("Aspirin<>") == "Aspirin"
        assert sanitize_filename("Drug|Name") == "DrugName"
        assert sanitize_filename('Drug"Name') == "DrugName"

    def test_sanitize_replaces_spaces(self):
        assert sanitize_filename("Drug Name") == "Drug_Name"
        assert sanitize_filename("Drug  Name") == "Drug_Name"

    def test_sanitize_removes_leading_trailing_dots(self):
        assert sanitize_filename(".Drug.") == "Drug"
        assert sanitize_filename("...Drug...") == "Drug"

    def test_sanitize_empty_string(self):
        assert sanitize_filename("") == "medicine"
        assert sanitize_filename("...") == "medicine"

    def test_sanitize_preserves_alphanumeric(self):
        assert sanitize_filename("Aspirin123") == "Aspirin123"
        assert sanitize_filename("Drug-Name") == "Drug-Name"


class TestInteraction:
    """Test Interaction model"""

    def test_interaction_creation(self):
        inter = Interaction(
            drug_name="Warfarin",
            description="Increased risk of bleeding",
            severity="major",
        )
        assert inter.drug_name == "Warfarin"
        assert inter.description == "Increased risk of bleeding"
        assert inter.severity == "major"


class TestTarget:
    """Test Target model"""

    def test_target_creation(self):
        target = Target(
            target_id="ENSG00000100030",
            name="Prostaglandin G/H synthase 1",
            organism="Homo sapiens",
            action="inhibitor",
            gene_name="PTGS1",
        )
        assert target.target_id == "ENSG00000100030"
        assert target.name == "Prostaglandin G/H synthase 1"
        assert target.action == "inhibitor"


class TestPharmacokinetics:
    """Test Pharmacokinetics model"""

    def test_pharmacokinetics_creation(self):
        pk = Pharmacokinetics(
            absorption="Rapidly absorbed",
            distribution="Widely distributed",
            half_life="2-3 hours",
            metabolism="Hepatic",
            bioavailability="50-60%",
        )
        assert pk.absorption == "Rapidly absorbed"
        assert pk.half_life == "2-3 hours"
        assert pk.bioavailability == "50-60%"


class TestPatent:
    """Test Patent model"""

    def test_patent_creation(self):
        patent = Patent(
            patent_number="US123456",
            country="US",
            approved=datetime(2000, 1, 1),
            expires=datetime(2020, 1, 1),
            pediatric_extension=False,
        )
        assert patent.patent_number == "US123456"
        assert patent.country == "US"
        assert patent.approved.year == 2000


class TestATCCode:
    """Test ATCCode model"""

    def test_atc_code_creation(self):
        atc = ATCCode(code="N02BA01", level="Salicylic acid and derivatives")
        assert atc.code == "N02BA01"
        assert atc.level == "Salicylic acid and derivatives"


class TestAdverseReaction:
    """Test AdverseReaction model"""

    def test_adverse_reaction_creation(self):
        reaction = AdverseReaction(
            reaction="Gastrointestinal bleeding",
            frequency="rare",
            severity="severe",
        )
        assert reaction.reaction == "Gastrointestinal bleeding"
        assert reaction.frequency == "rare"
        assert reaction.severity == "severe"


class TestSafety:
    """Test Safety model"""

    def test_safety_creation(self):
        contraind = Contraindication(
            condition="Peptic ulcer disease",
            severity="absolute",
        )
        adverse = AdverseReaction(reaction="Rash")

        safety = Safety(
            contraindications=[contraind],
            adverse_reactions=[adverse],
            warnings="Use with caution in renal impairment",
            pregnancy_category="D",
        )

        assert len(safety.contraindications) == 1
        assert len(safety.adverse_reactions) == 1
        assert safety.pregnancy_category == "D"


class TestRegulation:
    """Test Regulation model"""

    def test_regulation_creation(self):
        patent = Patent(patent_number="US123456", country="US")
        manufacturer = Manufacturer(name="Bayer", country="Germany")
        pricing = PricingInfo(country="US", price="$5.99")

        reg = Regulation(
            approval_date=datetime(1950, 3, 6),
            patents=[patent],
            manufacturers=[manufacturer],
            pricing=[pricing],
        )

        assert reg.approval_date.year == 1950
        assert len(reg.patents) == 1
        assert len(reg.manufacturers) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
