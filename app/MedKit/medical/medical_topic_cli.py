import json
import sys
import logging
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

from medkit.core.medkit_client import MedKitClient, MedKitConfig
from medkit.medical.medical_faq import FAQGenerator
from medkit.utils.logging_config import setup_logger

import hashlib
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig
from medical_topic_models import MedicalTopic

# Configure logging
logger = setup_logger(__name__)

# ============================================================================ 
# CONFIGURATION
# ============================================================================ 

@dataclass
class Config(MedKitConfig):
    """Configuration for the medical topic generator."""

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "medical_topic.lmdb"
            )
        # Call parent validation
        super().__post_init__()

# ============================================================================ 
# MEDICAL TOPIC GENERATOR CLASS
# ============================================================================ 

class MedicalTopicGenerator:
    """Generate comprehensive information for medical topics."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the generator."""
        self.config = config or Config()
        # Load model name from ModuleConfig

        model_name = "gemini-1.5-flash"  # Default model for this module

        

        self.client = MedKitClient(model_name=model_name)
        self.topic_name: Optional[str] = None
        self.output_path: Optional[Path] = None

        # Apply verbosity level to logger
        verbosity_levels = {0: "CRITICAL", 1: "ERROR", 2: "WARNING", 3: "INFO", 4: "DEBUG"}
        logger.setLevel(verbosity_levels.get(self.config.verbosity, "WARNING"))
        logging.getLogger("medkit").setLevel(verbosity_levels.get(self.config.verbosity, "WARNING"))

    def generate(self, topic_name: str, output_path: Optional[Path] = None) -> MedicalTopic:
        """
        Generate and save comprehensive medical topic information.

        Args:
            topic_name: Name of the medical topic.
            output_path: Optional path to save the JSON output.

        Returns:
            The generated MedicalTopic object.
        
        Raises:
            ValueError: If topic_name is empty.
        """
        if not topic_name or not topic_name.strip():
            raise ValueError("Topic name cannot be empty")

        self.topic_name = topic_name

        if output_path is None:
            output_path = self.config.output_dir / f"{topic_name.lower().replace(' ', '_')}_topic.json"
        
        self.output_path = output_path

        logger.info(f"Starting medical topic information generation for: {topic_name}")

        topic_info = self._generate_info()
        
        self._embed_faq(topic_info)

        self.save(topic_info, self.output_path)
        self.print_summary(topic_info)
        
        return topic_info

    def _generate_info(self) -> MedicalTopic:
        """Generates the topic information."""
        prompt = f"""Generate comprehensive medical information for the topic: {self.topic_name}

Include:
1. Definition and overview
2. Epidemiology (prevalence, incidence, demographics)
3. Pathophysiology and mechanisms
4. Risk factors and etiology
5. Clinical presentation and symptoms
6. Diagnostic criteria and tests
7. Differential diagnosis
8. Treatment options
9. Prognosis and complications
10. Prevention strategies
11. Cross-references to related topics (see_also) - include similar conditions, related treatments, complications that can become independent conditions, conditions that may co-occur, and preventive topics

For see_also cross-references, identify:
- Related medical topics that help readers understand the full context
- Types of connections (similar condition, related treatment, complication, risk factor, prevention, differential diagnosis, co-occurrence, etc.)
- Brief explanation of why each topic is relevant

Provide accurate, evidence-based medical information."""

        result = self.client.generate_text(
            prompt,
            schema=MedicalTopic
        )
        return result

    def _embed_faq(self, topic_info: MedicalTopic) -> None:
        """Generates and embeds a patient-friendly FAQ."""
        logger.info(f"Generating FAQs for: {self.topic_name}")
        try:
            faq_generator = FAQGenerator()
            faq = faq_generator.generate_patient_faq(self.topic_name)
            topic_info.faq = faq
            logger.info(f"✓ FAQ generated and embedded: {len(faq.faqs)} questions")
        except Exception as e:
            logger.warning(f"Warning: FAQ generation failed: {e}")
            topic_info.faq = None

    def save(self, topic_info: MedicalTopic, output_path: Path) -> Path:
        """
        Save the generated topic information to a JSON file.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(topic_info.model_dump(), f, indent=2)
        
        logger.info(f"✓ Topic information with FAQ saved to {output_path}")
        return output_path

    def print_summary(self, topic_info: MedicalTopic) -> None:
        """
        Print a summary of the generated topic information.
        """
        if not self.config.verbose:
            return

        print("\n" + "="*70)
        print(f"MEDICAL TOPIC SUMMARY: {topic_info.overview.topic_name}")
        print("="*70)
        print(f"  - Category: {topic_info.overview.topic_category}")
        print(f"  - Specialties: {topic_info.overview.medical_specialties}")

        if topic_info.faq:
            print("\n📋 FAQ Summary:")
            print(f"  - Questions: {len(topic_info.faq.faqs)}")
            print(f"  - When to Seek Care: {len(topic_info.faq.when_to_seek_care)} criteria")
            print(f"  - Misconceptions: {len(topic_info.faq.misconceptions)} addressed")

        print(f"\n✓ Generation complete. Saved to {self.output_path}")

def get_topic_info(topic_name: str, output_path: Optional[Path] = None, verbose: bool = False) -> MedicalTopic:
    """
    High-level function to generate and optionally save topic information.
    """
    config = Config(verbose=verbose)
    generator = MedicalTopicGenerator(config=config)
    return generator.generate(topic_name, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate comprehensive information for a medical topic.")
    parser.add_argument("-i", "--topic", type=str, required=True, help="The name of the medical topic to generate information for.")
    parser.add_argument("-o", "--output", type=str, help="Optional: The path to save the output JSON file.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show verbose console output.")

    args = parser.parse_args()
    print("Starting ...")
    get_topic_info( args.topic, args.output, args.verbose)
    print(f"Success: output stored in outputs/{args.output}")



    def close(self):
        """Close LMDB storage and release resources."""
        if self.storage:
            try:
                self.storage.close()
                logger.info("LMDB storage closed successfully.")
            except Exception as e:
                logger.error(f"Error closing LMDB storage: {e}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
