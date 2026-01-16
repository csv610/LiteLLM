"""Medical Facts Checker - Comprehensive fact vs. fiction analysis with confidence scoring.

Analyzes medical statements and claims to determine factual accuracy with supporting evidence,
identifies red flags, provides confidence levels, and explains misconceptions for fact-checking workflows.

QUICK START:
    from medical_facts_checker import MedicalFactsChecker
    checker = MedicalFactsChecker()
    result = checker.generate("Vitamin C prevents common cold")
    print(f"Classification: {result.detailed_analysis.statement_analysis.classification}")
    print(f"Explanation: {result.detailed_analysis.explanation}")

COMMON USES:
    - Verify medical claims and health information accuracy
    - Create fact-checking databases with supporting evidence
    - Debunk medical myths with explanations of misconceptions
    - Evaluate medical statements for credibility assessment
    - Generate audit trails for medical fact verification tasks

KEY CONCEPTS:
    - DetailedAnalysis structure with StatementAnalysis, FactualSupport, FictionIndicators
    - Confidence levels (HIGH, MODERATE, LOW) for assessment reliability
    - ContextInformation captures domain, key terms, assumptions, scope clarity
    - Metadata includes analysis date, knowledge cutoff, limitations, method used
"""

import json
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from pydantic import BaseModel, Field
from typing import Optional, List

from medkit.core.medkit_client import MedKitClient, MedKitConfig

import hashlib
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig

# ============================================================================ 
# CONFIGURATION
# ============================================================================ 

@dataclass
class Config(MedKitConfig):
    """Configuration for the medical facts checker."""
    log_file: Path = field(default_factory=lambda: Path("logs/medical_facts_checker.log"))
    verbose: bool = False

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "medical_facts_checker.lmdb"
            )
        # Call parent validation
        super().__post_init__()
# ============================================================================ 
# PYDANTIC MODELS FOR FACT CHECKING STRUCTURE
# ============================================================================ 

class StatementAnalysis(BaseModel):
    """Detailed analysis of a single statement."""
    statement: str = Field(description="The original statement being analyzed")
    classification: str = Field(description="Fact or Fiction")
    confidence_level: str = Field(description="Confidence level (high, medium, low)")
    confidence_percentage: int = Field(description="Confidence as percentage (0-100)")


class FactualSupport(BaseModel):
    """Support for factual statements."""
    supporting_sources: str = Field(description="Known sources that support this fact, comma-separated")
    evidence_type: str = Field(description="Type of evidence (scientific, historical, observational, etc)")
    verification_method: str = Field(description="How this fact can be verified")
    related_facts: str = Field(description="Related facts that corroborate this statement, comma-separated")


class FictionIndicators(BaseModel):
    """Indicators suggesting a statement is fiction."""
    red_flags: str = Field(description="Red flags or indicators of fiction, comma-separated")
    factual_errors: str = Field(description="Specific factual errors or contradictions found")
    lack_of_evidence: str = Field(description="Absence of supporting evidence or contradictions with known facts")
    fictional_elements: str = Field(description="Elements that appear to be fictional or speculative, comma-separated")


class ContextInformation(BaseModel):
    """Context and background information."""
    subject_area: str = Field(description="Subject area or domain of the statement (science, history, general knowledge, etc)")
    key_terms: str = Field(description="Key terms or concepts in the statement, comma-separated")
    assumptions: str = Field(description="Assumptions made in the statement, comma-separated")
    scope_clarity: str = Field(description="Whether the scope of the statement is clear (too vague, precise, etc)")


class DetailedAnalysis(BaseModel):
    """Comprehensive fact/fiction analysis of a statement."""
    statement_analysis: StatementAnalysis
    factual_support: Optional[FactualSupport] = Field(description="Support information if statement is a fact")
    fiction_indicators: Optional[FictionIndicators] = Field(description="Fiction indicators if statement is fiction")
    context: ContextInformation
    explanation: str = Field(description="Plain language explanation of why statement is fact or fiction")
    potential_confusion: str = Field(description="Common misconceptions or reasons why people might believe differently")


class AnalyzerMetadata(BaseModel):
    """Metadata about the analysis."""
    analysis_date: str = Field(description="Date of analysis")
    knowledge_cutoff: str = Field(description="Knowledge cutoff date of the analyzer")
    analysis_method: str = Field(description="Method used for analysis")
    limitations: str = Field(description="Limitations of this analysis")


class FactFictionAnalysis(BaseModel):
    """
    Comprehensive fact/fiction analysis for statements.
    """
    detailed_analysis: DetailedAnalysis
    metadata: AnalyzerMetadata

# ============================================================================ 
# MEDICAL FACTS CHECKER CLASS
# ============================================================================ 

class MedicalFactsChecker:
    """Analyzes medical statements for factual accuracy."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the facts checker."""
        self.config = config or Config()
        # Load model name from ModuleConfig

        model_name = "gemini-1.5-pro"  # Default model for this module

        

        self.client = MedKitClient(model_name=model_name)
        self.statement: Optional[str] = None
        self.output_path: Optional[Path] = None

    def generate(self, statement: str, output_path: Optional[Path] = None) -> FactFictionAnalysis:
        """
        Analyze a statement and determine if it is a fact or fiction.

        Args:
            statement: The statement to analyze.
            output_path: Optional path to save the JSON output.

        Returns:
            The generated FactFictionAnalysis object.
        
        Raises:
            ValueError: If statement is empty.
        """
        if not statement or not statement.strip():
            raise ValueError("Statement cannot be empty")

        self.statement = statement

        if output_path is None:
            safe_name = "".join(c if c.isalnum() else "_" for c in statement[:50].lower())
            output_path = self.config.output_dir / f"{safe_name}_analysis.json"
        
        self.output_path = output_path

        result = self.client.generate_text(
            prompt=f"Analyze the following statement and determine if it is a fact or fiction: {statement}",
            schema=FactFictionAnalysis,
        )

        # Save output to file
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                json.dump(result.model_dump(), f, indent=2)

        self.print_summary(result)

        return result

    def print_summary(self, analysis: FactFictionAnalysis) -> None:
        """
        Print a summary of the analysis.
        """
        if not self.config.verbose:
           return

        print("\n" + "="*70)
        print(f"FACT CHECK SUMMARY: {analysis.detailed_analysis.statement_analysis.statement}")
        print("="*70)
        print(f"  - Classification: {analysis.detailed_analysis.statement_analysis.classification}")
        print(f"  - Confidence: {analysis.detailed_analysis.statement_analysis.confidence_level} ({analysis.detailed_analysis.statement_analysis.confidence_percentage}%)")
        print(f"  - Explanation: {analysis.detailed_analysis.explanation}")
        print(f"\n✓ Analysis complete. Saved to {self.output_path}")

def analyze_statement(statement: str, output_path: Optional[Path] = None, verbosity: int = 2) -> FactFictionAnalysis:
    """
    High-level function to generate and optionally save fact check analysis.
    """
    config = Config(verbosity=verbosity)
    checker = MedicalFactsChecker(config=config)
    return checker.generate(statement, output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze statements and determine if they are fact or fiction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default - saves to outputs/{statement}_analysis.json
  python medical_facts_checker.py "The Earth is round"

  # Custom output path
  python medical_facts_checker.py "Gravity causes objects to fall" -o gravity_analysis.json
        """
    )
    parser.add_argument("-i", "--statement", required=True, help="Statement to analyze")
    parser.add_argument("-o", "--output", type=Path, help="Path to save JSON output.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity level (default: 2=WARNING)")

    args = parser.parse_args()

    try:
        checker = MedicalFactsChecker()
        print("Starting ...")
        checker.generate(statement=args.statement, output_path=args.output)
        if args.verbose:
            print(f"Success: output stored in output/{args.output}")

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
   main()
