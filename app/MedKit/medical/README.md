# Medical Module

Medical information system with 30+ specialized modules for clinical support, surgical reference, anatomical research, and medical education.

## Overview

The Medical Module provides a unified interface to a comprehensive suite of AI-driven medical information tools. From anatomical structures to complex surgical tray setups and clinical decision support, the system is designed to provide high-quality, structured medical information for educational and reference purposes.

## Module Structure

```
medical/
├── anatomy/                   # Anatomical structures and functions
├── disease_info/              # Disease etiology, symptoms, and treatment
├── organ_diseases/            # Organ-specific physiology and diseases
├── med_topic/                 # Synthesis of general medical subjects
├── herbal_info/               # Evidence-based natural remedies
├── med_advise/                # Primary health care and home management
├── med_decision_guide/        # Clinical decision support logic
├── med_facts_checker/         # Evidence-based fact verification
├── med_myths_checker/         # Scientific debunking of medical myths
├── med_refer/                 # Specialty referral recommendations
├── med_history/               # Standardized history-taking protocols
├── med_implant/               # Medical implants and surgical devices
├── med_faqs/                  # Plain-language patient education
├── surgical_info/             # Procedural monographs and benchmarks
├── surgical_pose_info/        # Patient positioning and nerve risks
├── surgical_tool_info/        # Surgical instruments and sterilization
├── surgical_tray/             # Standardized instrument tray setups
├── med_ethics/                # Pillar-based bioethical analysis
├── synthetic_case_report/     # Realistic synthetic patient cases
├── med_quiz/                  # MCQ assessment generation
├── med_flashcard/             # Terminology extraction and explanation
├── med_speciality/            # Medical specialties and areas of practice
├── med_speciality_roles/      # Scope of practice and responsibilities
├── med_procedure_info/        # Educational breakdown of procedures
├── med_physical_exams_questions/ # Exam-specific clinical questions
├── med_prescription/          # Prescription analysis and extraction
├── med_media/                 # Medical image and video search
└── med_utils/                 # Shared utilities and helpers
```

## Unified CLI Usage

The system features a unified CLI to access all modules from a single entry point.

```bash
# List all available modules
python medical_cli.py list

# Get help for a specific command
python medical_cli.py <command> --help
```

### Global Options

| Option | Description | Default |
|--------|-------------|---------|
| `-m, --model` | LLM model to use | `ollama/gemma3` |
| `-d, --output-dir` | Directory to save results | `outputs` |
| `-v, --verbosity` | Log level (0-4) | `2` |
| `-s, --structured` | Use structured JSON output | `False` |

---

## Key Module Categories

### 1. General Reference
Foundational medical knowledge about the human body and diseases.

*   **Anatomy**: `python medical_cli.py anatomy heart`
*   **Disease**: `python medical_cli.py disease diabetes`
*   **Organ-specific**: `python medical_cli.py organ liver`
*   **Medical Topics**: `python medical_cli.py topic "immunology"`
*   **Implant Info**: `python medical_cli.py implant "pacemaker"`
*   **Herbal Info**: `python medical_cli.py herbal "ashwagandha"`

### 2. Clinical Support
Tools for clinical reasoning and evidence-based practice.

*   **PHC Advise**: `python medical_cli.py advise "persistent dry cough"`
*   **Decision Guide**: `python medical_cli.py decision "acute chest pain"`
*   **Fact Checker**: `python medical_cli.py facts "Vitamin C prevents the common cold"`
*   **Myth Checker**: `python medical_cli.py myth "We only use 10% of our brain"`
*   **Referral**: `python medical_cli.py refer "blurry vision and sudden headaches"`
*   **Medical History**: `python medical_cli.py history -e neurological_exam -a 45 -g female`

### 3. Surgical Suite
Comprehensive references for the operating room.

*   **Surgical Info**: `python medical_cli.py surgery appendectomy`
*   **Positioning**: `python medical_cli.py pose supine`
*   **Surgical Tools**: `python medical_cli.py tool scalpel`
*   **Tray Setup**: `python medical_cli.py tray "total knee replacement"`

### 4. Education & Ethics
Advanced modules for medical learning and ethical analysis.

*   **Medical Ethics**: `python medical_cli.py ethics "triage in resource-limited settings"`
*   **Case Reports**: `python medical_cli.py case "type 2 diabetes"`
*   **Quiz Gen**: `python medical_cli.py quiz cardiology --num-questions 10`
*   **Flashcards**: `python medical_cli.py flashcard "amoxicillin_label.png"`
*   **Procedures**: `python medical_cli.py procedure "venipuncture"`

---

## Python API Usage

Most modules can be used directly in Python scripts for programmatic access.

### Disease Information

```python
from medical.disease_info.disease_info import DiseaseInfoGenerator
from lite.config import ModelConfig

config = ModelConfig(model="ollama/gemma3")
generator = DiseaseInfoGenerator(config)
result = generator.generate_text("hypertension", structured=True)

print(f"Etiology: {result.etiology}")
```

### Medical Ethics Analysis

```python
from medical.med_ethics.med_ethics import MedEthicalQA
from lite.config import ModelConfig

config = ModelConfig(model="ollama/gemma3")
qa = MedEthicalQA(config)
result = qa.generate_text("Should a physician disclose a terminal diagnosis against family wishes?")

print(result.analysis)
```

## Limitations

1. **Information Quality**: Output quality depends on the underlying LLM's training data.
2. **Knowledge Cutoff**: Information may not reflect the absolute latest clinical trials or research.
3. **Not Personalized**: System cannot provide individualized medical advice or diagnosis.
4. **Educational Purpose**: Intended for learning, research, and reference only.
5. **No Professional Review**: Outputs are AI-generated and have not been reviewed by medical professionals.

## Important Disclaimers

**THIS SYSTEM IS FOR EDUCATIONAL AND INFORMATIONAL PURPOSES ONLY.** 

It is NOT a substitute for professional medical advice, diagnosis, or treatment. 
- Always seek the advice of a physician or other qualified health provider with any questions regarding a medical condition.
- Never disregard professional medical advice or delay in seeking it because of something you have read here.
- In case of a medical emergency, call your local emergency services immediately.

---

**Last Updated**: February 24, 2026
**Related**: [ARCHITECTURE.md](../ARCHITECTURE.md) | [CLI_REFERENCE.md](../CLI_REFERENCE.md)
