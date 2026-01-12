import sys
import json
import argparse
from pathlib import Path
from typing import Optional
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pydantic import BaseModel, Field
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from logging_util import setup_logging

log_file = Path(__file__).parent / "logs" / "medical_myths_checker.log"
logger = setup_logging(str(log_file))


class MythAnalysis(BaseModel):
    statement: str = Field(..., description="The medical myth or claim being analyzed.")
    status: str = Field(..., description="Whether the statement is 'TRUE', 'FALSE', or 'UNCERTAIN'. Must be one of these values.")
    explanation: str = Field(..., description="Detailed, medically accurate explanation of why the statement is true, false, or uncertain, backed by evidence-based medicine.")
    peer_reviewed_sources: str = Field(..., description="REQUIRED: Specific peer-reviewed journals, papers, or medical organizations that support or refute the claim. Include journal names and publication years. If no peer-reviewed evidence exists, state 'No peer-reviewed evidence found' and explain what research gaps exist.")
    risk_level: str = Field(default="LOW", description="Health risk level if the myth is believed: 'LOW', 'MODERATE', or 'HIGH'.")


class MythAnalysisResponse(BaseModel):
    myths: list[MythAnalysis]


class MythChecker:
    """Encapsulates medical myth analysis functionality."""

    def __init__(self, model: str, temperature: float = 0.3, output_file: str = None):
        """Initialize the MythChecker with a model and temperature."""
        try:
            model_config = ModelConfig(model=model, temperature=temperature)
            self.client = LiteClient(model_config=model_config)
            self.logger = logger
            self.output_file = output_file
            self.myths_data = []
            self.logger.info(f"MythChecker initialized with model: {model}, temperature: {temperature}")
        except Exception as e:
            self.logger.error(f"Failed to initialize MythChecker: {e}")
            raise

    def analyze(self, statements: list[str]) -> Optional[dict]:
        """Analyze medical myths using the LLM, making one API call per statement."""
        if not statements:
            self.logger.error("No statements provided for analysis")
            raise ValueError("No statements to analyze")

        # Initialize output file if specified
        if self.output_file:
            self._initialize_output_file()

        failed_myths = []

        try:
            # Use tqdm for progress bar
            for i, statement in enumerate(tqdm(statements, desc="Analyzing myths", unit="myth"), 1):
                try:
                    prompt = self._create_prompt([statement])
                    model_input = ModelInput(user_prompt=prompt, response_format=MythAnalysisResponse)
                    response_content = self.client.generate_text(model_input=model_input)

                    if not isinstance(response_content, str):
                        self.logger.error(f"Expected string response for statement {i}")
                        failed_myths.append({"statement": statement, "error": "Invalid response type from model"})
                        continue

                    parsed = self._parse_response(response_content, statement_num=i)
                    if parsed and "myths" in parsed:
                        for myth in parsed["myths"]:
                            self.myths_data.append(myth)
                            # Save immediately to file if output file is specified
                            if self.output_file:
                                self._append_to_file(myth)
                        self.logger.info(f"Successfully analyzed statement {i}/{len(statements)}")
                    else:
                        failed_myths.append({"statement": statement, "error": "No myths in parsed response"})
                except Exception as e:
                    error_msg = str(e)
                    self.logger.error(f"Failed to analyze statement {i}: {error_msg}")
                    failed_myths.append({"statement": statement, "error": error_msg})
                    # Continue with next myth instead of stopping
                    continue

            self.logger.info(f"Successfully analyzed {len(self.myths_data)}/{len(statements)} myth(s)")
            if failed_myths:
                self.logger.warning(f"Failed to analyze {len(failed_myths)} myth(s)")
                for failed in failed_myths:
                    self.logger.warning(f"  - {failed['statement'][:50]}...: {failed['error']}")

            return {"myths": self.myths_data, "failed": failed_myths}
        finally:
            # Always finalize the output file even if errors occurred
            if self.output_file and self.myths_data:
                try:
                    _finalize_output_file(self.output_file)
                except Exception as e:
                    self.logger.error(f"Failed to finalize output file: {e}")

    def _create_prompt(self, statements: list[str]) -> str:
        """Generate the prompt for myth analysis."""
        statements_text = "\n".join([f"{i+1}. {s}" for i, s in enumerate(statements)])
        is_single = len(statements) == 1
        statement_label = "statement" if is_single else "statements"

        prompt = f"""You are a medical fact-checker with expertise in evidence-based medicine. Your task is to analyze the following medical claim/myth and provide an assessment grounded EXCLUSIVELY in peer-reviewed scientific evidence.

CRITICAL REQUIREMENTS:
1. ALL claims must be verified against peer-reviewed medical literature, clinical trials, and established medical guidelines
2. Only cite evidence from peer-reviewed journals, systematic reviews, meta-analyses, or official medical organizations (WHO, NIH, CDC, etc.)
3. If a claim cannot be supported by peer-reviewed evidence, mark it as FALSE or UNCERTAIN and explain what peer-reviewed research contradicts or is lacking
4. Include specific journal names, publication years, and authors when possible
5. Do NOT use general knowledge or anecdotal evidence - only evidence-based medicine

For this {statement_label}:
1. Clearly state the claim
2. Provide a status (TRUE, FALSE, or UNCERTAIN) - mark UNCERTAIN only if peer-reviewed evidence is genuinely conflicting or insufficient
3. Give a detailed medical explanation based ONLY on peer-reviewed research
4. Cite SPECIFIC peer-reviewed sources: journal names, publication years, authors, or official medical organizations
5. If peer-reviewed evidence contradicts the claim, explain clearly what the evidence shows
6. Rate the health risk level (LOW, MODERATE, or HIGH) based on potential harms if believed
7. If no peer-reviewed evidence exists for the claim, explicitly state this and mark as UNCERTAIN or FALSE

Medical Myth/Claim to Analyze:
{statements_text}

Respond ONLY with valid JSON in this exact format:
{{
    "myths": [
        {{
            "statement": "exact claim from the input",
            "status": "TRUE or FALSE or UNCERTAIN",
            "explanation": "detailed medical explanation grounded in peer-reviewed evidence",
            "peer_reviewed_sources": "Specific citations: Journal names, publication years, and research findings. Or: 'No peer-reviewed evidence found' with explanation of research gaps",
            "risk_level": "LOW or MODERATE or HIGH"
        }}
    ]
}}

VERIFICATION STANDARD:
- TRUE: Supported by multiple peer-reviewed studies and/or major medical organizations
- FALSE: Contradicted by peer-reviewed evidence or guidelines from established medical authorities
- UNCERTAIN: Conflicting peer-reviewed evidence or insufficient research (be specific about what is unclear)

Be rigorous, objective, and prioritize evidence-based medicine over any other consideration."""
        self.logger.debug(f"Generated prompt for {len(statements)} statement(s)")
        return prompt

    def _parse_response(self, response_content: str, statement_num: int = 0) -> Optional[dict]:
        """Parse JSON response content."""
        try:
            data = json.loads(response_content)
            self.logger.debug("Successfully parsed JSON response")
            return data
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response for statement {statement_num}: {e}")
            # Log first 500 chars of problematic response for debugging
            preview = response_content[:500] if len(response_content) > 500 else response_content
            self.logger.error(f"Problematic response preview: {preview}")
            raise RuntimeError(f"Failed to parse response from model: {e}")

    def _handle_api_error(self, error: Exception) -> None:
        """Handle API errors with helpful messages."""
        error_str = str(error).lower()

        if "401" in str(error) or "authentication" in error_str:
            raise RuntimeError("API authentication failed. Check credentials.")
        elif "429" in str(error):
            raise RuntimeError("API rate limit exceeded. Try again later.")
        elif "404" in str(error):
            raise RuntimeError("Model not found.")
        else:
            raise RuntimeError(f"Analysis failed: {error}")

    def _initialize_output_file(self) -> None:
        """Initialize the output file with an empty myths array."""
        try:
            output_path = Path(self.output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w') as f:
                f.write('{\n  "myths": [\n')

            self.logger.info(f"Initialized output file: {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to initialize output file: {e}")
            raise

    def _append_to_file(self, myth: dict) -> None:
        """Append a single myth analysis to the output file."""
        try:
            output_path = Path(self.output_file)

            with open(output_path, 'a') as f:
                # Add comma and newline before new entries (except the first)
                if len(self.myths_data) > 1:
                    f.seek(f.tell() - 1)  # Remove the closing newline temporarily
                    f.write(',\n')

                # Write the myth with indentation
                myth_json = json.dumps(myth, indent=4, ensure_ascii=False)
                indented_myth = '\n'.join('    ' + line for line in myth_json.split('\n'))
                f.write(indented_myth)
                f.write('\n')

            self.logger.debug(f"Appended myth to output file: {myth.get('statement', 'Unknown')}")
        except Exception as e:
            self.logger.error(f"Failed to append to output file: {e}")
            raise


def _finalize_output_file(file_path: str) -> None:
    """Finalize the output file by closing the JSON structure."""
    try:
        with open(file_path, 'a') as f:
            f.write('  ]\n}\n')
        logger.info(f"Finalized output file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to finalize output file: {e}")
        raise


def read_input_file(file_path: str) -> list[str]:
    """Read medical myths from a file, one per line."""
    try:
        with open(file_path, 'r') as f:
            statements = [line.strip() for line in f if line.strip()]
        logger.info(f"Read {len(statements)} statements from file: {file_path}")
        return statements
    except FileNotFoundError:
        raise IOError(f"File not found: {file_path}")
    except Exception as e:
        raise IOError(f"Failed to read file: {e}")


def read_myths_from_json(file_path: str) -> list[str]:
    """Read all medical myths from a JSON file.

    Args:
        file_path: Path to the medical_myths.json file

    Returns:
        List of all myth statements from all topics
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("JSON file must contain an array of topic objects")

        myths = []

        for topic_obj in data:
            if not isinstance(topic_obj, dict) or 'topic' not in topic_obj or 'myths' not in topic_obj:
                logger.warning(f"Skipping invalid topic object: {topic_obj}")
                continue

            topic_name = topic_obj['topic']

            if isinstance(topic_obj['myths'], list):
                myths.extend(topic_obj['myths'])
                logger.debug(f"Added {len(topic_obj['myths'])} myths from topic: {topic_name}")

        logger.info(f"Read {len(myths)} myths from JSON file: {file_path}")
        return myths
    except FileNotFoundError:
        raise IOError(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        raise IOError(f"Invalid JSON in file {file_path}: {e}")
    except Exception as e:
        raise IOError(f"Failed to read JSON file: {e}")


def save_results(data: dict, output_file: str = None) -> Path:
    """Save myth analysis results to a JSON file."""
    try:
        if output_file is None:
            output_dir = Path(__file__).parent / "outputs"
            output_dir.mkdir(exist_ok=True)
            output_file = output_dir / "medical_facts.json"
        else:
            output_file = Path(output_file)
            output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"Results saved to {output_file}")
        print(f"Medical myths analysis saved to {output_file}")
        return output_file
    except Exception as e:
        logger.error(f"Failed to save results: {e}")
        raise IOError(f"Failed to save results: {e}")


def validate_temperature(temp_str: str) -> float:
    """Validate and convert temperature string to float."""
    try:
        temp = float(temp_str)
        if not (0.0 <= temp <= 1.0):
            raise argparse.ArgumentTypeError("Temperature must be between 0.0 and 1.0")
        return temp
    except ValueError:
        raise argparse.ArgumentTypeError(f"Temperature must be a float, got '{temp_str}'")


def validate_model(model: str) -> str:
    """Validate model format."""
    if not model or len(model.strip()) == 0:
        raise argparse.ArgumentTypeError("Model cannot be empty")
    return model.strip()


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and return configured argument parser."""
    parser = argparse.ArgumentParser(
        description="Analyze medical myths and provide fact-checked, medically accurate explanations"
    )
    parser.add_argument(
        "input",
        nargs='?',
        help="A medical myth/claim as a sentence, or a path to a file containing one claim per line"
    )
    parser.add_argument(
        "-m", "--model",
        type=validate_model,
        default="ollama/gemma3",
        help="The model to use for analysis (default: ollama/gemma3)"
    )
    parser.add_argument(
        "-t", "--temperature",
        type=validate_temperature,
        default=0.3,
        help="Temperature for model response (default: 0.3, lower for more factual responses)"
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output file path (default: outputs/medical_facts.json)"
    )
    parser.add_argument(
        "--json",
        default=None,
        help="Path to JSON file containing medical myths (default: medical_myths.json in current directory)"
    )
    return parser


def main() -> int:
    """Main entry point for the CLI."""
    parser = create_argument_parser()
    args = parser.parse_args()

    try:
        # Determine source of myths
        statements = []

        # Priority 1: --json flag (loads all myths from JSON)
        if args.json:
            json_path = Path(args.json)
            if not json_path.exists():
                print(f"Error: JSON file not found: {args.json}", file=sys.stderr)
                return 1
            statements = read_myths_from_json(str(json_path))
            print(f"Loaded {len(statements)} myths from {args.json}")

        # Priority 2: Check if default medical_myths.json exists and no input provided
        elif not args.input:
            default_json = Path("medical_myths.json")
            if default_json.exists():
                statements = read_myths_from_json(str(default_json))
                print(f"Loaded {len(statements)} myths from medical_myths.json")
            else:
                print("Error: No input provided and medical_myths.json not found", file=sys.stderr)
                print("Usage: Provide a myth statement, file path, or use --json flag", file=sys.stderr)
                return 1

        # Priority 3: Traditional input (text file or single statement)
        else:
            input_path = Path(args.input)
            if input_path.exists() and input_path.is_file():
                # Check if it's a JSON file
                if input_path.suffix == '.json':
                    statements = read_myths_from_json(str(input_path))
                    print(f"Loaded {len(statements)} myths from {args.input}")
                else:
                    statements = read_input_file(args.input)
            else:
                statements = [args.input]

        if not statements:
            print("Error: No statements to analyze", file=sys.stderr)
            return 1

        # Determine output file path
        output_file = args.output
        if output_file is None:
            output_dir = Path(__file__).parent / "outputs"
            output_dir.mkdir(exist_ok=True)
            output_file = str(output_dir / "medical_facts.json")

        checker = MythChecker(args.model, args.temperature, output_file=output_file)
        results = checker.analyze(statements)

        if results is None:
            print("Error: Failed to analyze myths", file=sys.stderr)
            return 1

        # Report results
        num_successful = len(results.get("myths", []))
        num_failed = len(results.get("failed", []))

        print(f"\nAnalysis complete:")
        print(f"  Successfully analyzed: {num_successful}/{len(statements)} myths")
        if num_failed > 0:
            print(f"  Failed to analyze: {num_failed} myths")
            print(f"\nFailed myths:")
            for failed in results.get("failed", []):
                myth_preview = failed['statement'][:60]
                print(f"  - {myth_preview}...")
                print(f"    Error: {failed['error']}")

        print(f"\nResults saved to {output_file}")
        return 0

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        logger.error(f"Validation error: {e}")
        return 1
    except IOError as e:
        print(f"Error: {e}", file=sys.stderr)
        logger.error(f"File error: {e}")
        return 1
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        logger.error(f"Runtime error: {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
