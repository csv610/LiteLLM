"""
liteagents.py - Unified for drug_disease
"""
import requests\nfrom lite.utils import save_model_response\nimport xml.etree.ElementTree as ET\nfrom typing import Optional, Any\nfrom app.MedKit.drug.drug_disease.shared.models import *\nimport sqlite_utils\nimport hashlib\nfrom typing import Optional\nimport logging\nfrom lite.lite_client import LiteClient\nfrom pathlib import Path\nfrom typing import List, Dict, Optional\nimport argparse\nfrom lite.config import ModelConfig\nimport json\nfrom lite.config import ModelConfig, ModelInput\nfrom lite.logging_config import configure_logging\n\n"""Drug-Disease Interaction Analysis module."""



logger = logging.getLogger(__name__)


def parse_prompt_style(style_str: str) -> PromptStyle:
    """Parse prompt style string to PromptStyle enum."""
    style_mapping = {
        "detailed": PromptStyle.DETAILED,
        "concise": PromptStyle.CONCISE,
        "balanced": PromptStyle.BALANCED,
    }

    if style_str.lower() not in style_mapping:
        raise ValueError(
            f"Invalid prompt style: {style_str}. "
            f"Choose from: {', '.join(style_mapping.keys())}"
        )
    return style_mapping[style_str.lower()]


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Drug-Disease Interaction Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "medicine_name",
        type=str,
        help="Name of the medicine to analyze",
    )

    parser.add_argument(
        "condition_name",
        type=str,
        help="Name of the medical condition",
    )

    parser.add_argument(
        "--severity",
        "-S",
        type=str,
        choices=["mild", "moderate", "severe"],
        default=None,
        help="Severity of the condition (mild, moderate, severe)",
    )

    parser.add_argument(
        "--age",
        "-a",
        type=int,
        default=None,
        help="Patient's age in years (0-150)",
    )

    parser.add_argument(
        "--medications",
        "-M",
        type=str,
        default=None,
        help="Other medications the patient is taking (comma-separated)",
    )

    parser.add_argument(
        "--style",
        "-s",
        type=str,
        choices=["detailed", "concise", "balanced"],
        default="detailed",
        help="Prompt style for analysis (default: detailed)",
    )

    parser.add_argument(
        "--output-dir",
        "-od",
        default="outputs",
        help="Directory for output files (default: outputs).",
    )

    parser.add_argument(
        "--verbosity",
        "-v",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2).",
    )

    parser.add_argument(
        "--structured",
        "-t",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response",
    )

    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="ollama/gemma3",
        help="LLM model to use for analysis (default: ollama/gemma3)",
    )

    parser.add_argument(
        "--hitl",
        action="store_true",
        default=False,
        help="Enable Human-in-the-loop approval for clinical recommendations",
    )

    return parser.parse_args()


def create_drug_disease_interaction_report(args) -> int:

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "drug_disease_interaction.log"),
        verbosity=args.verbosity,
        enable_console=True,
    )

    logger.info("=" * 80)
    logger.info("DRUG-DISEASE INTERACTION CLI - Starting")
    logger.info("=" * 80)

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        user_input = DrugDiseaseInput(
            medicine_name=args.medicine_name,
            condition_name=args.condition_name,
            condition_severity=args.severity,
            age=args.age,
            other_medications=args.medications,
            prompt_style=parse_prompt_style(args.style),
        )

        logger.info("Configuration created successfully")

        model_config = ModelConfig(model=args.model, temperature=0.2)
        analyzer = DrugDiseaseInteraction(model_config)
        result = analyzer.generate_text(user_input, structured=args.structured, hitl=args.hitl)

        if result is None:
            logger.error("✗ Failed to analyze drug-disease interaction.")
            return 1

        # Save result to output directory
        analyzer.save(result, output_dir)

        logger.debug("✓ Drug-disease interaction analysis completed successfully")
        return 0

    except ValueError as e:
        logger.error(f"✗ Invalid input: {e}")
        return 1
    except Exception as e:
        logger.error(f"✗ Drug-disease interaction analysis failed: {e}")
        logger.exception("Full exception details:")
        return 1


def main():
    args = get_user_arguments()
    create_drug_disease_interaction_report(args)


if __name__ == "__main__":
    main()


class InteractionCache:
    """SQLite-based cache for drug-disease interaction results."""
    
    def __init__(self, db_path: str = "interaction_cache.db"):
        self.db = sqlite_utils.Database(db_path)
        self.table = self.db.table("interactions", pk="id")
    
    def _generate_key(self, medicine: str, condition: str, age: Optional[int], severity: Optional[str]) -> str:
        """Generate a unique key based on inputs."""
        key_str = f"{medicine.lower()}|{condition.lower()}|{age}|{severity}"
        return hashlib.sha256(key_str.encode()).hexdigest()

    def get(self, medicine: str, condition: str, age: Optional[int], severity: Optional[str]) -> Optional[ModelOutput]:
        """Retrieve a cached result if it exists."""
        key = self._generate_key(medicine, condition, age, severity)
        try:
            row = self.table.get(key)
        except sqlite_utils.db.NotFoundError:
            return None
        
        if row:
            # Reconstruct ModelOutput from JSON
            data_dict = json.loads(row["data"])
            markdown = row["markdown"]
            
            # Reconstruct pydantic model
            interaction_data = DrugDiseaseInteractionModel(**data_dict) if data_dict else None
            return ModelOutput(data=interaction_data, markdown=markdown)
        return None

    def set(self, medicine: str, condition: str, age: Optional[int], severity: Optional[str], result: ModelOutput):
        """Store a result in the cache."""
        key = self._generate_key(medicine, condition, age, severity)
        data_json = json.dumps(result.data.dict()) if result.data else None
        
        self.table.insert({
            "id": key,
            "medicine": medicine.lower(),
            "condition": condition.lower(),
            "age": age,
            "severity": severity,
            "data": data_json,
            "markdown": result.markdown
        }, replace=True)

#!/usr/bin/env python3
"""
Drug-Disease Interaction Analysis module.

This module provides the core DrugDiseaseInteraction class for analyzing
how medical conditions affect drug efficacy, safety, and metabolism.
"""



try:
    from .drug_disease_interaction_models import (
        DrugDiseaseInteractionModel,
        ModelOutput,
    )
    from .drug_disease_interaction_prompts import DrugDiseaseInput, PromptBuilder
    from .pubmed_utils import PubMedTool
    from .cache_utils import InteractionCache
    from .hitl_utils import HITLManager
except ImportError:
    from drug_disease_interaction_models import DrugDiseaseInteractionModel, ModelOutput
    from drug_disease_interaction_prompts import DrugDiseaseInput, PromptBuilder
    from pubmed_utils import PubMedTool
    from cache_utils import InteractionCache
    from hitl_utils import HITLManager

logger = logging.getLogger(__name__)


class DrugDiseaseInteraction:
    """Analyzes drug-disease interactions based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.cache = InteractionCache()
        self.config = None  # Store the configuration for later use in save
        logger.debug("Initialized DrugDiseaseInteraction with Caching and HITL support")

    def generate_text(
        self, config: DrugDiseaseInput, structured: bool = False, hitl: bool = False
    ) -> ModelOutput:
        """Analyzes drug-disease interactions using a 3-tier system."""
        self.config = config
        
        # Check cache
        cached_result = self.cache.get(config.medicine_name, config.condition_name, config.age, config.condition_severity)
        if cached_result: return cached_result

        logger.info(f"Starting 3-tier analysis for: {config.medicine_name} vs {config.condition_name}")

        try:
            # --- Tier 1: Specialists (JSON Sequential) ---
            logger.info("Tier 1: Specialists running...")
            # 1. PubMed
            real_ev = PubMedTool.get_evidence(config.medicine_name, config.condition_name)
            pubmed_res = self._ask_llm(ModelInput(
                system_prompt=PromptBuilder.create_pubmed_system_prompt(),
                user_prompt=f"Evidence for {config.medicine_name} and {config.condition_name}:\n{real_ev}"
            )).markdown

            # 2. Researcher
            researcher_res = self._ask_llm(ModelInput(
                system_prompt=PromptBuilder.create_researcher_system_prompt(),
                user_prompt=PromptBuilder.create_researcher_user_prompt(config, pubmed_res)
            )).markdown

            # 3. Pharmacologist
            pharmacologist_res = self._ask_llm(ModelInput(
                system_prompt=PromptBuilder.create_pharmacologist_system_prompt(),
                user_prompt=PromptBuilder.create_pharmacologist_user_prompt(config, researcher_res)
            )).markdown

            # 4. Clinician
            clinician_res = self._ask_llm(ModelInput(
                system_prompt=PromptBuilder.create_clinician_system_prompt(),
                user_prompt=PromptBuilder.create_clinician_user_prompt(config, pharmacologist_res, researcher_res)
            )).markdown
            if hitl: clinician_res = HITLManager.request_approval("Clinical Safety", clinician_res.markdown)
            else: clinician_res = clinician_res.markdown

            spec_data_json = f"PUBMED:\n{pubmed_res}\n\nRESEARCH:\n{researcher_res}\n\nPHARMA:\n{pharmacologist_res}\n\nCLINICAL:\n{clinician_res}"

            # --- Tier 2: Compliance Auditor (JSON Audit) ---
            logger.info("Tier 2: Compliance Auditor running...")
            audit_res = self._ask_llm(ModelInput(
                system_prompt=PromptBuilder.create_compliance_system_prompt(),
                user_prompt=PromptBuilder.create_compliance_user_prompt(clinician_res, "Patient guidance included in clinical."),
                response_format=None # Audit result
            ))
            audit_json = audit_res.markdown

            # --- Tier 3: Final Output Synthesis (Markdown Closer) ---
            logger.info("Tier 3: Output Synthesis running...")
            out_sys, out_usr = PromptBuilder.create_output_synthesis_prompts(config, spec_data_json, audit_json)
            final_res = self._ask_llm(ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None
            ))

            return ModelOutput(
                data=None, # Tier 1 data is complex here, can be added if needed
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier Analysis failed: {e}")
            raise

    def _ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Helper to call LiteClient with error handling and normalization."""
        logger.debug("Calling LiteClient...")
        try:
            response = self.client.generate_text(model_input=model_input)
            
            # Normalize response to ModelOutput
            if isinstance(response, ModelOutput):
                return response
            elif hasattr(response, "markdown"):
                return response
            else:
                # Handle string or other unexpected types
                return ModelOutput(markdown=str(response))
                
        except Exception as e:
            logger.error(f"✗ Error during LLM analysis: {e}")
            logger.exception("Full exception details:")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the drug-disease interaction analysis to a file."""
        if self.config is None:
            raise ValueError(
                "No configuration information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        medicine_safe = self.config.medicine_name.lower().replace(" ", "_")
        condition_safe = self.config.condition_name.lower().replace(" ", "_")
        base_filename = f"{medicine_safe}_{condition_safe}_interaction"

        return save_model_response(result, output_dir / base_filename)


logger = logging.getLogger(__name__)

class PubMedTool:
    """Tool for searching and fetching abstracts from PubMed (NCBI Entrez API)."""
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    
    @staticmethod
    def search_pubmed(query: str, max_results: int = 5) -> List[str]:
        """Search PubMed for a query and return a list of PMIDs."""
        search_url = f"{PubMedTool.BASE_URL}esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json"
        }
        
        try:
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("esearchresult", {}).get("idlist", [])
        except Exception as e:
            logger.error(f"PubMed search failed: {e}")
            return []

    @staticmethod
    def fetch_details(pmids: List[str]) -> str:
        """Fetch titles and abstracts for a list of PMIDs."""
        if not pmids:
            return "No PubMed results found."
            
        fetch_url = f"{PubMedTool.BASE_URL}efetch.fcgi"
        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml"
        }
        
        try:
            response = requests.get(fetch_url, params=params)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            
            results = []
            for article in root.findall(".//PubmedArticle"):
                title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "No Title"
                abstract_elem = article.find(".//AbstractText")
                abstract = abstract_elem.text if abstract_elem is not None else "No Abstract available"
                
                # Some abstracts are split into multiple elements
                if abstract_elem is not None and not abstract:
                    abstract = " ".join([elem.text for elem in article.findall(".//AbstractText") if elem.text])
                
                results.append(f"Title: {title}\nAbstract: {abstract}\n---")
                
            return "\n".join(results)
        except Exception as e:
            logger.error(f"PubMed fetch failed: {e}")
            return "Failed to fetch PubMed details."

    @staticmethod
    def get_evidence(medicine: str, condition: str) -> str:
        """Helper to search and fetch in one go."""
        query = f"({medicine}[Title/Abstract]) AND ({condition}[Title/Abstract]) AND (interaction OR safety OR contraindication)"
        pmids = PubMedTool.search_pubmed(query)
        return PubMedTool.fetch_details(pmids)


logger = logging.getLogger(__name__)

class HITLManager:
    """Manages Human-in-the-loop interactions for clinical approval."""
    
    @staticmethod
    def request_approval(agent_name: str, content: str) -> str:
        """
        Request approval or edits for an agent's output.
        In a CLI context, this prompts the user.
        In a web context, this would wait for an API callback.
        """
        print(f"\n--- HITL APPROVAL REQUIRED: {agent_name} ---")
        print(f"Content:\n{content}")
        print("-" * 40)
        
        user_choice = input("Approve as is? (y/n/edit): ").lower().strip()
        
        if user_choice == 'y':
            return content
        elif user_choice == 'edit':
            print("Enter your edits (end with a single line containing 'END'):")
            lines = []
            while True:
                line = input()
                if line.strip() == 'END':
                    break
                lines.append(line)
            return "\n".join(lines)
        else:
            print("Rejecting content. Please provide required changes/feedback (will be appended to context):")
            feedback = input("> ")
            return f"REJECTED BY CLINICIAN. Feedback: {feedback}\nOriginal Content: {content}"

