import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from medkit.core.medkit_client import MedKitClient, MedKitConfig

from medkit.utils.logging_config import setup_logger

import hashlib
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig

from medical_faq_models import (
    FAQItem, MisconceptionItem, WhenToSeekCare, SeeAlsoTopics,
    PatientFAQ, ProviderFAQ, ComprehensiveFAQ
)

# Configure logging
logger = setup_logger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class Config(MedKitConfig):
    """Configuration for the FAQ generator."""
    verbose: bool = False

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "medical_faq.lmdb"
            )
        # Call parent validation
        super().__post_init__()
# ============================================================================
# FAQ GENERATOR CLASS
# ============================================================================

class FAQGenerator:
    """Generate comprehensive FAQs for medical topics.

    Provides both patient-friendly and provider-focused FAQ content
    with clinical reasoning and evidence-based practices.
    """

    def __init__(self, config: Optional[Config] = None):
        """Initialize FAQ generator with MedKit client."""
        self.config = config or Config()

        # Load model name from ModuleConfig
        model_name = "gemini-1.5-flash"  # Default model for this module

        self.client = MedKitClient(model_name=model_name)
        self.topic_name: Optional[str] = None
        self.output_path: Optional[Path] = None

    def generate_patient_faq(self, topic_name: str) -> PatientFAQ:
        """Generate patient-friendly FAQs for a medical topic.

        Args:
            topic_name: Name of the medical topic

        Returns:
            PatientFAQ: Patient-friendly FAQ content
        """
        logger.info(f"Generating patient-friendly FAQs for: {topic_name}")

        prompt = f"""Generate comprehensive patient-friendly FAQs for: {topic_name}

Create content that:
1. Uses plain, simple language (avoid medical jargon)
2. Addresses common patient concerns and questions
3. Provides practical, actionable information
4. Builds patient confidence and understanding
5. Emphasizes prevention and healthy living

Include sections:
- Introduction: Brief, reassuring overview of the topic
- FAQs: 8-10 common patient questions with clear, comprehensive answers
- When to Seek Care: Signs and symptoms requiring medical attention with urgency levels
- Common Misconceptions: 4-5 myths with clarifications
- See Also: 3-4 related health topics, tests, or devices patients should understand (include category: 'topic', 'test', or 'device')

Format as JSON matching the PatientFAQ schema."""

        result = self.client.generate_text(prompt, schema=PatientFAQ)
        logger.info(f"✓ Patient FAQ generated: {len(result.faqs)} questions")
        return result

    def generate_provider_faq(self, topic_name: str) -> ProviderFAQ:
        """Generate provider-focused FAQs for a medical topic.

        Args:
            topic_name: Name of the medical topic

        Returns:
            ProviderFAQ: Provider-focused FAQ content
        """
        logger.info(f"Generating provider-focused FAQs for: {topic_name}")

        prompt = f"""Generate comprehensive provider-focused FAQs for: {topic_name}

Create content that:
1. Uses medical terminology and clinical concepts
2. Addresses clinical decision-making questions
3. References evidence-based practices
4. Includes quality metrics and outcome measures
5. Provides referral guidance

Include sections:
- Clinical Overview: Summary of pathophysiology, epidemiology, and clinical significance
- Clinical FAQs: 8-10 questions with clinical relevance addressing clinical assessment, diagnosis, and management
- Evidence-Based Practices: 4-5 current best practices and clinical guidelines
- Quality Metrics: Key performance indicators and outcome measures
- Referral Criteria: When to refer to specialists or higher levels of care

Format as JSON matching the ProviderFAQ schema."""

        result = self.client.generate_text(prompt, schema=ProviderFAQ)
        logger.info(f"✓ Provider FAQ generated: {len(result.clinical_faqs)} questions")
        return result

    def generate(self, topic_name: str, output_path: Optional[Path] = None, include_provider: bool = False) -> ComprehensiveFAQ:
        """Generate FAQ package for a medical topic (patient-focused by default).

        Args:
            topic_name: Name of the medical topic
            output_path: Path to save JSON output. Defaults to outputs/{topic_name}_faq.json
            include_provider: If True, also generate provider-focused FAQs. Default is False (patient-only)

        Returns:
            ComprehensiveFAQ: FAQ content with patient FAQs (and optional provider section)

        Raises:
            ValueError: If topic_name is empty or invalid
        """
        if not topic_name or not topic_name.strip():
            raise ValueError("Topic name cannot be empty")

        self.topic_name = topic_name

        # Determine output path
        if output_path is None:
            output_path = Path("outputs") / f"{topic_name.lower().replace(' ', '_')}_faq.json"

        self.output_path = output_path

        logger.info(f"Starting FAQ generation for: {topic_name}")

        # Always generate patient FAQs (default behavior)
        patient_faq = self.generate_patient_faq(topic_name)

        # Optionally generate provider FAQs if requested
        provider_faq = None
        if include_provider:
            provider_faq = self.generate_provider_faq(topic_name)

        # Create comprehensive FAQ package
        metadata = {
            "generated_for": topic_name,
            "patient_audience": "General public, patients seeking health information",
            "faq_focus": "Patient-friendly (primary)" + (" + Provider-focused (secondary)" if include_provider else ""),
        }

        if include_provider:
            metadata["provider_audience"] = "Healthcare professionals, medical students, clinical staff"
            metadata["language_level"] = "Patient section uses plain language; Provider section uses medical terminology"
        else:
            metadata["language_level"] = "Plain language, patient-friendly explanations"

        comprehensive_faq = ComprehensiveFAQ(
            topic_name=topic_name,
            metadata=metadata,
            patient_faq=patient_faq,
            provider_faq=provider_faq
        )

        # Save to file
        self.save(comprehensive_faq, output_path)

        return comprehensive_faq

    def save(self, faq: ComprehensiveFAQ, output_path: Path) -> Path:
        """Save FAQ to JSON file.

        Args:
            faq: ComprehensiveFAQ object to save
            output_path: Path to save the file

        Returns:
            Path: Path to saved file
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(faq.model_dump(), f, indent=2)

        logger.info(f"✓ FAQ saved to {output_path}")
        print(f"✓ FAQ generated and saved to {output_path}")
        return output_path

    def print_summary(self, faq: ComprehensiveFAQ) -> None:
        """Print generation summary.

        Args:
            faq: ComprehensiveFAQ object with generated content
        """
        if not self.config.verbose:
            return
        print("\n" + "="*70)
        print(f"FAQ GENERATION SUMMARY: {faq.topic_name}")
        print("="*70)
        print(f"\nFocus: {faq.metadata.get('faq_focus', 'Patient-friendly')}")
        print(f"Language: {faq.metadata.get('language_level', 'Plain language')}")

        print(f"\n📋 PATIENT FAQ (Primary):")
        print(f"  - Introduction included: ✓")
        print(f"  - FAQs: {len(faq.patient_faq.faqs)} questions")
        print(f"  - When to Seek Care: {len(faq.patient_faq.when_to_seek_care)} criteria")
        print(f"  - Common Misconceptions: {len(faq.patient_faq.misconceptions)} addressed")
        print(f"  - See Also: {len(faq.patient_faq.see_also)} topics")

        if faq.provider_faq:
            print(f"\n🏥 PROVIDER FAQ (Optional - Included):")
            print(f"  - Clinical Overview: ✓")
            print(f"  - Clinical FAQs: {len(faq.provider_faq.clinical_faqs)} questions")
            print(f"  - Evidence-Based Practices: {len(faq.provider_faq.evidence_based_practices)} practices")
            print(f"  - Quality Metrics: {len(faq.provider_faq.quality_metrics)} metrics")
            print(f"  - Referral Criteria: {len(faq.provider_faq.referral_criteria)} criteria")
        else:
            print(f"\n🏥 PROVIDER FAQ: Not included (patient-friendly content only)")

        print("\n✓ Success!")


# ============================================================================
# CLI AND MAIN FUNCTIONS
# ============================================================================

def user_arguments():
    """Command-line interface for FAQ generation.

    Provides argument parsing and execution of the FAQ generator with
    support for custom topics and output paths.

    Examples:
        Generate patient-friendly FAQs:
            python medical_faq.py -i "Diabetes"

        Generate both patient and provider FAQs:
            python medical_faq.py -i "Hypertension" --provider

        Save to custom output path:
            python medical_faq.py -i "Asthma" -o results/asthma_faq.json
    """
    parser = argparse.ArgumentParser(
        description="Generate comprehensive FAQs for medical topics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  Generate patient-friendly FAQs:
    python medical_faq.py -i "Kidney Disease"

  Include provider-focused FAQs:
    python medical_faq.py -i "Diabetes" --provider

  Save to custom location:
    python medical_faq.py -i "Asthma" -o my_output/asthma_faq.json
        """
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        type=str,
        help="Medical topic name for FAQ generation (required)"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output path for generated FAQ JSON file (default: outputs/{topic}_faq.json)"
    )

    parser.add_argument(
        "--provider",
        action="store_true",
        help="Include provider-focused FAQs in addition to patient FAQs"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging output"
    )

    return parser.parse_args()


def main():
    """Main entry point for FAQ generation.

    Parses command-line arguments and executes the FAQ generation pipeline.
    Handles errors gracefully with informative error messages.

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    try:
        # Parse command-line arguments
        args = user_arguments()

        # Create configuration
        config = Config(verbose=args.verbose)

        # Initialize generator
        generator = FAQGenerator(config=config)

        # Convert output path to Path object if provided
        output_path = Path(args.output) if args.output else None

        # Generate FAQ
        logger.info(f"Generating FAQ for topic: {args.input}")
        faq = generator.generate(
            topic_name=args.input,
            output_path=output_path,
            include_provider=args.provider
        )

        # Print summary if not quiet mode
        if args.verbose:
            generator.print_summary(faq)

        return 0

    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        print(f"❌ Error: {e}", file=__import__('sys').stderr)
        return 1

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"❌ Error: Output directory could not be created: {e}", file=__import__('sys').stderr)
        return 1

    except KeyboardInterrupt:
        logger.info("FAQ generation interrupted by user")
        print("\n⚠️  FAQ generation cancelled by user", file=__import__('sys').stderr)
        return 1

    except Exception as e:
        logger.error(f"Unexpected error during FAQ generation: {e}")
        print(f"❌ Error: {e}", file=__import__('sys').stderr)
        return 1


if __name__ == "__main__":
    main()


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
