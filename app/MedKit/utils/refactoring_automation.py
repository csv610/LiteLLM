"""refactoring_automation - Automate refactoring of exam files for code organization.

This module automates the analysis and refactoring of exam_*.py files into cleaner architecture
with separate core business logic (_core.py) and UI-specific files. Provides file analysis tools,
refactoring status reports, and code generation templates to support modular, maintainable code organization.

QUICK START:
    Analyze a single exam file:

    >>> from refactoring_automation import ExamAnalyzer
    >>> analyzer = ExamAnalyzer()
    >>> analyzer.print_analysis("exam_cardiac.py")

    List all exam files and their status:

    >>> analyzer.list_files()

    Generate refactoring report:

    >>> analyzer.generate_refactoring_report()

    Or use the CLI:

    $ python refactoring_automation.py --list
    $ python refactoring_automation.py --analyze exam_cardiac.py
    $ python refactoring_automation.py --report

COMMON USES:
    1. Code organization - identifying and extracting business logic from UI-coupled code
    2. Architecture planning - understanding dependencies and refactoring scope for each module
    3. Progress tracking - monitoring refactoring completion across multiple exam files
    4. Code generation - auto-generating core.py templates with extracted models and logic
    5. Quality assessment - analyzing code metrics (lines, size, complexity) to prioritize work

KEY FEATURES AND COVERAGE AREAS:
    - File discovery and analysis scanning project for exam_*.py files and existing refactored versions
    - Metrics analysis extracting line counts, file sizes, and identifying models, classes, functions
    - Dependency mapping extracting imports and understanding module interdependencies
    - Status tracking comparing original files to refactored versions with progress percentages
    - Report generation producing comprehensive refactoring status and completion checklists
    - Template generation creating _core.py skeleton files with extracted Pydantic models
    - Model extraction identifying BaseModel classes for core business logic separation
    - Function and class discovery cataloging all functions and classes for architectural decisions
    - Import analysis tracking all imports for identifying external and internal dependencies
    - Refactoring guidance providing structured recommendations for code organization
"""

import os
import re
from pathlib import Path
from typing import List, Tuple, Dict


class ExamAnalyzer:
    """Analyze exam files for refactoring"""

    def __init__(self, folder_path: str = "."):
        self.folder_path = Path(folder_path)
        self.exam_files = self._find_exam_files()

    def _find_exam_files(self) -> List[Path]:
        """Find all exam_*.py files"""
        return sorted(self.folder_path.glob("exam_*.py"))

    def list_files(self) -> None:
        """List all exam files with info"""
        print(f"\n{'File':<40} {'Lines':<8} {'Size':<10} {'Status':<15}")
        print("=" * 80)

        for filepath in self.exam_files:
            with open(filepath, 'r') as f:
                lines = len(f.readlines())

            size_kb = filepath.stat().st_size / 1024

            # Check if already refactored
            name = filepath.stem
            core_file = self.folder_path / f"{name}_core.py"
            status = "✓ Refactored" if core_file.exists() else "⏳ Pending"

            print(f"{filepath.name:<40} {lines:<8} {size_kb:>8.1f}KB {status:<15}")

    def analyze_file(self, filepath: str) -> Dict:
        """Analyze a single file"""
        path = Path(filepath)
        if not path.exists():
            print(f"❌ File not found: {filepath}")
            return {}

        with open(path, 'r') as f:
            content = f.read()

        analysis = {
            "filename": path.name,
            "lines": len(content.split('\n')),
            "size_kb": path.stat().st_size / 1024,
            "models": self._extract_models(content),
            "classes": self._extract_classes(content),
            "functions": self._extract_functions(content),
            "imports": self._extract_imports(content),
        }

        return analysis

    def _extract_models(self, content: str) -> List[str]:
        """Extract Pydantic model class names"""
        pattern = r'class (\w+)\(BaseModel\):'
        return re.findall(pattern, content)

    def _extract_classes(self, content: str) -> List[str]:
        """Extract all class names"""
        pattern = r'class (\w+)[\(\:]'
        return re.findall(pattern, content)

    def _extract_functions(self, content: str) -> List[str]:
        """Extract function names"""
        pattern = r'def (\w+)\('
        return re.findall(pattern, content)

    def _extract_imports(self, content: str) -> List[str]:
        """Extract imports"""
        pattern = r'^(?:from|import) .+$'
        return re.findall(pattern, content, re.MULTILINE)

    def print_analysis(self, filepath: str) -> None:
        """Print analysis of a file"""
        analysis = self.analyze_file(filepath)

        if not analysis:
            return

        print(f"\n📊 Analysis: {analysis['filename']}")
        print("=" * 80)
        print(f"Lines: {analysis['lines']}")
        print(f"Size: {analysis['size_kb']:.1f} KB")

        print(f"\n📦 Pydantic Models ({len(analysis['models'])}):")
        for model in analysis['models'][:10]:  # Show first 10
            print(f"  • {model}")
        if len(analysis['models']) > 10:
            print(f"  ... and {len(analysis['models']) - 10} more")

        print(f"\n🔧 Classes ({len(analysis['classes'])}):")
        for cls in analysis['classes'][:10]:
            print(f"  • {cls}")
        if len(analysis['classes']) > 10:
            print(f"  ... and {len(analysis['classes']) - 10} more")

        print(f"\n⚙️  Functions ({len(analysis['functions'])}):")
        for func in analysis['functions'][:10]:
            print(f"  • {func}")
        if len(analysis['functions']) > 10:
            print(f"  ... and {len(analysis['functions']) - 10} more")

        print(f"\n📚 Imports ({len(analysis['imports'])}):")
        for imp in analysis['imports'][:5]:
            print(f"  • {imp}")
        if len(analysis['imports']) > 5:
            print(f"  ... and {len(analysis['imports']) - 5} more")

    def generate_refactoring_report(self) -> None:
        """Generate refactoring report for all files"""
        print("\n📋 REFACTORING REPORT")
        print("=" * 80)

        total_lines = 0
        total_size = 0
        refactored = 0
        pending = 0

        for filepath in self.exam_files:
            with open(filepath, 'r') as f:
                lines = len(f.readlines())
            size_kb = filepath.stat().st_size / 1024

            total_lines += lines
            total_size += size_kb

            name = filepath.stem
            core_file = self.folder_path / f"{name}_core.py"

            if core_file.exists():
                refactored += 1
                status = "✓"
            else:
                pending += 1
                status = "⏳"

            module_name = name.replace("exam_", "").replace("_", " ").title()
            print(f"{status} {module_name:<35} {lines:>5} lines {size_kb:>8.1f}KB")

        print("=" * 80)
        print(f"Total: {len(self.exam_files)} modules | {total_lines} lines | {total_size:.1f}KB")
        print(f"Status: {refactored} refactored, {pending} pending")
        print(f"Progress: {refactored}/{len(self.exam_files)} ({refactored*100//len(self.exam_files)}%)")

    def generate_refactoring_checklist(self) -> None:
        """Generate a checklist for refactoring"""
        print("\n✅ REFACTORING CHECKLIST")
        print("=" * 80)

        for filepath in self.exam_files:
            name = filepath.stem.replace("exam_", "")
            core_file = self.folder_path / f"{filepath.stem}_core.py"

            if core_file.exists():
                status = "✓"
            else:
                status = "☐"

            print(f"{status} {name}")


class RefactoringGuide:
    """Generate refactoring guides"""

    @staticmethod
    def generate_core_template(filename: str, analysis: Dict) -> str:
        """Generate core.py template"""
        module_name = filename.replace("exam_", "").replace(".py", "").title()

        template = f'''"""
{module_name} - Core Business Logic (UI-Agnostic)

This module contains:
- Data models (Pydantic)
- Question definitions
- Business logic
- State management
- Export utilities
- Validation logic

Zero dependencies on UI frameworks. Can integrate with any UI.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime

# ============================================================================
# DATA MODELS
# ============================================================================

# TODO: Copy all Pydantic model definitions from original {filename}
# Example:
# class PatientHistory(BaseModel):
#     field1: str = Field(description="...")
#     field2: str = Field(description="...")

# TODO: Create main exam record model
# class ExamReport(BaseModel):
#     patient_name: str = "Unknown"
#     patient_id: str
#     timestamp: datetime
#     patient_answers: dict
#     exam_findings: dict
#     assessment: dict


# ============================================================================
# QUESTION DEFINITIONS
# ============================================================================

class QuestionSet:
    """All questions organized by category"""

    # TODO: Extract questions from original file
    PATIENT_QUESTIONS = [
        # ("question_id", "Question text?"),
    ]

    NURSE_EXAMINATION = [
        # ("field_id", "Examination field?"),
    ]


# ============================================================================
# BUSINESS LOGIC
# ============================================================================

class ExamProcessor:
    """Core exam processing logic"""

    @staticmethod
    def validate_answer(answer: str) -> str:
        """Validate and normalize answer"""
        return answer.strip() or "(no response)"

    @staticmethod
    def generate_assessment(patient_answers: dict, exam_findings: dict) -> dict:
        """Generate clinical assessment"""
        # TODO: Add assessment logic
        return {{
            "findings": [],
            "recommendations": [],
            "follow_up": "",
        }}


# ============================================================================
# STATE MANAGEMENT
# ============================================================================

class ExamState:
    """Manages exam state throughout workflow"""

    def __init__(self):
        self.patient_name: str = "Unknown"
        self.patient_answers: Dict[str, str] = {{}}
        self.exam_findings: Dict[str, str] = {{}}
        self.assessment: Optional[dict] = None

    def set_patient_name(self, name: str):
        self.patient_name = name or "Unknown"

    def add_patient_answer(self, question_id: str, answer: str):
        self.patient_answers[question_id] = ExamProcessor.validate_answer(answer)

    def add_exam_finding(self, field_id: str, value: str):
        self.exam_findings[field_id] = ExamProcessor.validate_answer(value)

    def generate_assessment(self) -> dict:
        self.assessment = ExamProcessor.generate_assessment(
            self.patient_answers,
            self.exam_findings
        )
        return self.assessment

    def finalize_exam(self) -> dict:
        if not self.assessment:
            self.generate_assessment()

        return {{
            "patient_name": self.patient_name,
            "patient_answers": self.patient_answers,
            "exam_findings": self.exam_findings,
            "assessment": self.assessment,
            "timestamp": datetime.now().isoformat(),
        }}


# ============================================================================
# EXPORT UTILITIES
# ============================================================================

class ExamExporter:
    """Export exam data in different formats"""

    @staticmethod
    def to_json(exam: dict) -> str:
        import json
        return json.dumps(exam, indent=2, default=str)

    @staticmethod
    def to_dict(exam: dict) -> dict:
        return exam

    @staticmethod
    def to_markdown(exam: dict) -> str:
        # TODO: Generate markdown report
        return ""

    @staticmethod
    def save_json(exam: dict, filepath: str) -> str:
        import json
        with open(filepath, "w") as f:
            json.dump(exam, f, indent=2, default=str)
        return filepath


# ============================================================================
# VALIDATION
# ============================================================================

class ExamValidator:
    """Validate exam completeness and quality"""

    @staticmethod
    def check_required_fields(state: ExamState) -> tuple:
        missing = []
        if not state.patient_name:
            missing.append("Patient name")
        if not state.patient_answers:
            missing.append("Patient answers")
        if not state.exam_findings:
            missing.append("Exam findings")
        return len(missing) == 0, missing

    @staticmethod
    def get_completion_percentage(state: ExamState) -> int:
        total = len(QuestionSet.PATIENT_QUESTIONS) + len(QuestionSet.NURSE_EXAMINATION)
        answered = len(state.patient_answers) + len(state.exam_findings)
        return int((answered / total) * 100) if total > 0 else 0
'''

        return template


def cli():
    """Main entry point"""
    import sys

    analyzer = ExamAnalyzer(Path(__file__).parent)

    if len(sys.argv) < 2:
        print(__doc__)
        analyzer.generate_refactoring_report()
        analyzer.generate_refactoring_checklist()
        return

    command = sys.argv[1]

    if command == "--list":
        analyzer.list_files()

    elif command == "--analyze" and len(sys.argv) > 2:
        analyzer.print_analysis(sys.argv[2])

    elif command == "--report":
        analyzer.generate_refactoring_report()

    elif command == "--checklist":
        analyzer.generate_refactoring_checklist()

    elif command == "--help":
        print(__doc__)

    else:
        print(f"❌ Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    cli()
