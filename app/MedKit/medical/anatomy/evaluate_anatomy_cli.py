#!/usr/bin/env python3
"""
CLI interface for Anatomy Report Evaluator.

Provides command-line access to evaluate anatomy reports with strict quality standards.
"""

import logging
import sys
import json
from pathlib import Path
from typing import Optional

# Add the project root to sys.path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

try:
    from .evaluate_anatomy_report import AnatomyReportEvaluator, AnatomyEvaluationResult
except (ImportError, ValueError):
    from evaluate_anatomy_report import AnatomyReportEvaluator, AnatomyEvaluationResult

from lite.logging_config import configure_logging

logger = logging.getLogger(__name__)


class EvaluationCLI:
    """Command-line interface for anatomy report evaluation."""

    def __init__(self, model: str = "ollama/gemma3", verbose: bool = False):
        self.evaluator = AnatomyReportEvaluator(model=model)
        self.verbose = verbose
        logger.debug("Initialized EvaluationCLI")

    def evaluate_single(self, file_path: Path, output_json: Optional[Path] = None) -> AnatomyEvaluationResult:
        """Evaluate a single anatomy report file."""
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        logger.info(f"Evaluating: {file_path}")
        result = self.evaluator.evaluate_file(file_path)

        # Display results
        if self.verbose:
            self._display_results(result)

        # Save JSON output if specified
        if output_json:
            self._save_json_results(result, output_json)

        return result

    def evaluate_directory(self, directory: Path, output_dir: Optional[Path] = None) -> dict:
        """Evaluate all anatomy report files in a directory."""
        if not directory.is_dir():
            logger.error(f"Directory not found: {directory}")
            raise NotADirectoryError(f"Directory not found: {directory}")

        logger.info(f"Scanning directory: {directory}")

        # Find all markdown and text files
        files = list(directory.glob("*.md")) + list(directory.glob("*.txt"))
        if not files:
            logger.warning(f"No .md or .txt files found in {directory}")
            return {}

        results = {}
        logger.info(f"Found {len(files)} files to evaluate")

        for file_path in sorted(files):
            logger.info(f"Processing: {file_path.name}")
            try:
                result = self.evaluator.evaluate_file(file_path)
                results[file_path.name] = result.to_dict()
            except Exception as e:
                logger.error(f"Error evaluating {file_path.name}: {e}")
                results[file_path.name] = {"error": str(e)}

        # Summary report
        if self.verbose:
            self._display_batch_summary(results)

        # Save results if output directory specified
        if output_dir:
            self._save_batch_results(results, output_dir)

        return results

    def _display_results(self, result: AnatomyEvaluationResult) -> None:
        """Display evaluation results in formatted output."""
        border = "=" * 90
        print(f"\n{border}")
        print(f"ANATOMY REPORT EVALUATION: {result.structure_name.upper()}")
        print(border)

        # Anatomical Accuracy
        print(f"\n📋 ANATOMICAL ACCURACY")
        print(f"   {result.anatomical_accuracy[0].value}")
        if result.anatomical_accuracy[1]:
            for issue in result.anatomical_accuracy[1]:
                prefix = "   ❌" if "CRITICAL" in issue else "   ⚠️"
                print(f"{prefix} {issue}")

        # Terminology Precision
        print(f"\n📚 TERMINOLOGY PRECISION")
        print(f"   {result.terminology_precision[0].value}")
        if result.terminology_precision[1]:
            for issue in result.terminology_precision[1]:
                print(f"   ⚠️ {issue}")

        # Embryology
        print(f"\n🧬 EMBRYOLOGY")
        print(f"   {result.embryology[0].value}")
        if result.embryology[1]:
            for issue in result.embryology[1]:
                print(f"   ⚠️ {issue}")

        # Clinical Reliability
        print(f"\n⚕️ CLINICAL RELIABILITY")
        print(f"   {result.clinical_reliability[0].value}")
        if result.clinical_reliability[1]:
            for issue in result.clinical_reliability[1]:
                prefix = "   ❌" if "UNSAFE" in issue or "CRITICAL" in issue else "   ⚠️"
                print(f"{prefix} {issue}")

        # Structural Organization
        print(f"\n🏗️ STRUCTURAL ORGANIZATION")
        print(f"   {result.structural_organization[0].value}")
        if result.structural_organization[1]:
            for issue in result.structural_organization[1]:
                print(f"   ⚠️ {issue}")

        # Summary
        print(f"\n{border}")
        print(f"Overall Quality Score: {result.overall_quality_score}/100")
        print(f"Status: {self._status_emoji(result.pass_fail_status)} {result.pass_fail_status}")
        print(border)

        # Critical Issues
        if result.critical_issues:
            print(f"\n🔴 CRITICAL ISSUES (MUST FIX):")
            for issue in result.critical_issues:
                print(f"   ❌ {issue}")

        # Recommendations
        if result.recommendations:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in result.recommendations:
                print(f"   → {rec}")

        print()

    def _display_batch_summary(self, results: dict) -> None:
        """Display summary of batch evaluation results."""
        if not results:
            print("No results to display")
            return

        print("\n" + "=" * 90)
        print("BATCH EVALUATION SUMMARY")
        print("=" * 90)

        # Count results
        passed = sum(1 for r in results.values() if isinstance(r, dict) and r.get("pass_fail_status") == "PASS")
        failed = sum(1 for r in results.values() if isinstance(r, dict) and r.get("pass_fail_status") == "FAIL")
        conditional = sum(1 for r in results.values() if isinstance(r, dict) and r.get("pass_fail_status") == "CONDITIONAL_PASS")
        errors = sum(1 for r in results.values() if isinstance(r, dict) and "error" in r)

        print(f"\nTotal Files: {len(results)}")
        print(f"  ✓ PASSED: {passed}")
        print(f"  ⚠️  CONDITIONAL: {conditional}")
        print(f"  ❌ FAILED: {failed}")
        print(f"  🔴 ERRORS: {errors}")

        # Score distribution
        scores = [r["overall_quality_score"] for r in results.values() if isinstance(r, dict) and "overall_quality_score" in r]
        if scores:
            avg_score = sum(scores) / len(scores)
            max_score = max(scores)
            min_score = min(scores)
            print(f"\nScore Statistics:")
            print(f"  Average: {avg_score:.1f}/100")
            print(f"  Highest: {max_score:.1f}/100")
            print(f"  Lowest: {min_score:.1f}/100")

        # Details by file
        print(f"\nDetailed Results:")
        print("-" * 90)
        for filename, result in sorted(results.items()):
            if isinstance(result, dict) and "overall_quality_score" in result:
                status = self._status_emoji(result["pass_fail_status"])
                print(f"{status} {filename:40s} {result['overall_quality_score']:6.1f}/100 {result['pass_fail_status']}")
            else:
                print(f"🔴 {filename:40s} ERROR")

    def _save_json_results(self, result: AnatomyEvaluationResult, output_path: Path) -> None:
        """Save evaluation results to JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)

        logger.info(f"Results saved to: {output_path}")
        print(f"✓ JSON results saved to: {output_path}")

    def _save_batch_results(self, results: dict, output_dir: Path) -> None:
        """Save batch evaluation results to directory."""
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save individual results
        for filename, result in results.items():
            if isinstance(result, dict) and "overall_quality_score" in result:
                output_file = output_dir / f"{Path(filename).stem}_evaluation.json"
                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=2)

        # Save summary report
        summary = {
            "total_files": len(results),
            "results": results
        }
        summary_file = output_dir / "evaluation_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

        logger.info(f"Batch results saved to: {output_dir}")
        print(f"✓ Batch results saved to: {output_dir}")

    @staticmethod
    def _status_emoji(status: str) -> str:
        """Return emoji for status."""
        status_map = {
            "PASS": "✅",
            "CONDITIONAL_PASS": "⚠️",
            "FAIL": "❌"
        }
        return status_map.get(status, "❓")


def main():
    """Main CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Strict Anatomy Report Evaluator - Zero Tolerance for Inaccuracies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Evaluate single file
  python evaluate_anatomy_cli.py path/to/report.md

  # Evaluate with JSON output
  python evaluate_anatomy_cli.py path/to/report.md -o output.json

  # Evaluate entire directory
  python evaluate_anatomy_cli.py path/to/reports/ -b -o output_dir/

  # Verbose output
  python evaluate_anatomy_cli.py path/to/report.md -v
        """
    )

    parser.add_argument(
        "path",
        type=Path,
        help="File or directory to evaluate"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output file/directory for results (JSON format)"
    )
    parser.add_argument(
        "-m", "--model",
        type=str,
        default="ollama/gemma3",
        help="Model to use for evaluation"
    )
    parser.add_argument(
        "-b", "--batch",
        action="store_true",
        help="Evaluate all files in directory (if path is directory)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Configure logging
    configure_logging(
        log_file="evaluate_anatomy.log", 
        verbosity=4 if args.verbose else 3, 
        enable_console=args.verbose
    )

    try:
        cli = EvaluationCLI(model=args.model, verbose=args.verbose)

        if args.path.is_dir() and args.batch:
            cli.evaluate_directory(args.path, args.output)
        elif args.path.is_file():
            cli.evaluate_single(args.path, args.output)
        else:
            print(f"Error: {args.path} is not a valid file or directory")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=args.verbose)
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
