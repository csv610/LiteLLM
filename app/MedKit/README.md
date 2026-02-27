# MedKit: Clinical-Grade AI Orchestration

**Stop using raw LLMs for medicine.** MedKit wraps AI reasoning into deterministic, type-safe, and HIPAA-aware clinical workflows. Designed for researchers, healthcare developers, and medical educators.

---

## 💡 Why MedKit?

Most AI tools provide "chat." MedKit provides **Standardized Clinical Output**. 

*   **🧩 Logical Chaining**: Don't just ask about a drug; use the `medkit-agent` to check that drug against a patient's comorbidities and current research simultaneously.
*   **🛡️ Safety Boundaries**: Every tool is built with explicit "Clinical Boundaries"—it knows what it can't do and tells you when to call a specialist.
*   **📊 Structured Data**: Turn messy doctor's notes into clean JSON datasets with 19 specialized entity recognizers.
*   **🔒 HIPAA-Ready**: Built-in privacy tools for audit logging, PII masking, and patient consent capture.

---

## 🚀 Quick Start in 60 Seconds

1.  **Analyze a Complex Scenario**:
    ```bash
    medkit-agent "70yo on Warfarin with a new cough. Check interactions and specialist referral."
    ```
2.  **Safety-Screen a Medication List**:
    ```bash
    medkit-drug interact "Lisinopril" "Ibuprofen" "Spironolactone"
    ```
3.  **Extract Research Data**:
    ```bash
    medkit-recognizer disease "Patient presents with signs of acute bronchitis and mild fever."
    ```

---

## 🛠️ The MedKit Suite

| Command | The Solution |
| :--- | :--- |
| **`medkit-agent`** | **The Brain**: Orchestrates multiple tools to solve multi-step clinical queries. |
| **`medkit-drug`** | **Safety**: 10 specialized modules for interactions, pharmacology, and patient education. |
| **`medkit-medical`**| **Knowledge**: 24 specialized modules for anatomy, ethics, surgery, and triage. |
| **`medkit-graph`** | **Insight**: Visualizes the logical causal links in dense medical text. |
| **`medkit-privacy`**| **Compliance**: Automates HIPAA consent, audit logs, and PII scrubbing. |
| **`medkit-exam`** | **Protocol**: Standardized head-to-toe physical examination checklists. |
| **`medkit-article`**| **Evidence**: Searches PubMed and BioMCP for peer-reviewed research. |
| **`medkit-diagnose`**| **Diagnostics**: Comprehensive information on medical laboratory tests and diagnostic devices. |
| **`medkit-legal`**   | **Rights**: Educational materials for healthcare law, ethics, and patient rights. |

---

### 🏥 `medkit-medical` Subcommands (24 Modules)

| # | Subcommand | Primary Utility |
| :--- | :--- | :--- |
| 1 | **`advise`** | Primary health care guidance and home management. |
| 2 | **`anatomy`** | Body structures, innervation, and blood supply. |
| 3 | **`case`** | Realistic synthetic patient case report generation. |
| 4 | **`decision`** | Diagnostic logic trees and clinical decision support. |
| 5 | **`disease`** | Etiology, symptoms, and treatment protocols. |
| 6 | **`ethics`** | Structured pillar-based analysis of bioethical dilemmas. |
| 7 | **`eval-procedure`** | Auditing and evaluating medical procedure documentation. |
| 8 | **`facts`** | Evidence-based verification of medical statements. |
| 9 | **`faq`** | Plain-language patient education materials. |
| 10 | **`flashcard`** | Terminology extraction and explanation from labels. |
| 11 | **`herbal`** | Evidence-based info on natural remedies and safety. |
| 12 | **`history`** | Standardized history-taking and intake questions. |
| 13 | **`implant`** | Detailed information on medical implants and prosthetics. |
| 14 | **`myth`** | Scientific debunking of common medical misconceptions. |
| 15 | **`organ`** | Organ-specific physiology and systemic disease roles. |
| 16 | **`pose`** | Standard patient positioning and associated risks. |
| 17 | **`procedure`** | Step-by-step educational breakdown of clinical procedures. |
| 18 | **`quiz`** | MCQ assessment generation with distractors and rationales. |
| 19 | **`refer`** | Identifying the correct specialty for clinical presentations. |
| 20 | **`roles`** | Scope of practice and responsibilities for medical specialties. |
| 21 | **`surgery`** | Exhaustive procedural monographs and recovery benchmarks. |
| 22 | **`tool`** | Reference for surgical instruments and sterilization needs. |
| 23 | **`topic`** | Synthesis of general medical subjects. |
| 24 | **`tray`** | Standardized setup lists for surgical instrument trays. |

---

### 💊 `medkit-drug` Subcommands (10 Modules)

| # | Subcommand | Primary Utility |
| :--- | :--- | :--- |
| 1 | **`addiction`** | Drug addiction, withdrawal symptoms, and recovery info. |
| 2 | **`compare`** | Side-by-side comparison of two specific medicines. |
| 3 | **`disease`** | Checking for drug-disease contraindications and safety. |
| 4 | **`explain`** | Plain-language medication explanations for patients. |
| 5 | **`food`** | Analysis of potential interactions between meds and foods. |
| 6 | **`info`** | Comprehensive drug monographs (MOA, dosing, side effects). |
| 7 | **`interact`** | Drug-drug interaction analysis between two medications. |
| 8 | **`similar`** | Finding therapeutic alternatives or similar medications. |
| 9 | **`symptoms`** | Suggesting drug categories for specific clinical symptoms. |

---

### 🔍 `medkit-recognizer` Subcommands (19 Identifiers)

| # | Subcommand | Primary Utility |
| :--- | :--- | :--- |
| 1 | **`abbreviation`** | Extracts and expands medical abbreviations and acronyms. |
| 2 | **`anatomy`** | Identifies anatomical structures and body parts. |
| 3 | **`clinical_sign`** | Detects objective clinical signs observed during examination. |
| 4 | **`coding`** | Extracts alphanumeric medical codes (ICD, CPT, etc.). |
| 5 | **`condition`** | Identifies broad medical conditions and pathologies. |
| 6 | **`device`** | Recognizes medical diagnostic and therapeutic devices. |
| 7 | **`disease`** | Extracts specific disease names and diagnoses. |
| 8 | **`drug`** | Identifies medications, generics, and brand names. |
| 9 | **`genetic`** | Recognizes genes, variants, and hereditary conditions. |
| 10 | **`imaging`** | Identifies radiological and diagnostic imaging modalities. |
| 11 | **`lab_unit`** | Extracts laboratory measurement units and values. |
| 12 | **`med_class`** | Categorizes medications into pharmacological classes. |
| 13 | **`pathogen`** | Identifies bacteria, viruses, and other microorganisms. |
| 14 | **`procedure`** | Recognizes surgical and clinical procedures. |
| 15 | **`specialty`** | Identifies medical specialties and sub-specialties. |
| 16 | **`supplement`** | Recognizes dietary supplements and nutraceuticals. |
| 17 | **`symptom`** | Detects subjective patient-reported symptoms. |
| 18 | **`test`** | Identifies laboratory and diagnostic tests. |
| 19 | **`vaccine`** | Recognizes immunizations and vaccine types. |

---

### 🧪 `medkit-diagnose` Subcommands (2 Modules)

| # | Subcommand | Primary Utility |
| :--- | :--- | :--- |
| 1 | **`device`** | Get information about medical diagnostic and therapeutic devices. |
| 2 | **`test`** | Get information about medical laboratory and diagnostic tests. |

---

### ⚖️ `medkit-legal` Subcommands (2 Modules)

| # | Subcommand | Primary Utility |
| :--- | :--- | :--- |
| 1 | **`ls`** | List available patient legal right topics and scenarios. |
| 2 | **`generate`** | Create comprehensive documentation for a specific legal right topic. |

---

#### 🧪 Clinical Intelligence: AI Augmentation of Traditional Workflows

MedKit doesn't just provide definitions; it augments traditional medical practice through targeted AI reasoning:

*   **`advise` & `decision`**: Replaces static paper flowcharts with dynamic clinical decision support, suggesting prioritized differential diagnoses based on patient context.
*   **`interact` & `disease` (Pharmacology)**: Automates multi-drug interaction screening and drug-disease safety checks, identifying physiological contraindications often overlooked in rapid clinical encounters.
*   **`explain` (Patient Safety)**: Generates compassionate, plain-language patient education to improve adherence and bridge the health literacy gap.
*   **`abbreviation` & `lab_unit` (NLP Precision)**: Uses context-aware reasoning to disambiguate medical acronyms and ensure laboratory values are correctly paired with clinical units, reducing data entry errors.
*   **`genetic` (Precision Medicine)**: Scales the extraction of complex genomic nomenclature from narrative reports, facilitating large-scale precision medicine research.
*   **`test` & `device` (Diagnostics)**: Synthesizes fragmented hardware specifications and evolving laboratory reference parameters into a unified, evidence-based clinical resource.
*   **`ls` & `generate` (Legal Rights)**: Bridges the health literacy gap by providing patient-centric explanations of complex healthcare laws, informed consent requirements, and medical-legal recourse mechanisms.
*   **`anatomy` & `organ`**: Moves beyond 2D atlases to semantic functional mapping, explaining the systemic "why" behind clinical findings.
*   **`case` & `quiz`**: Automates the generation of high-fidelity synthetic patient data and MCQs for rapid, bias-free medical education.
*   **`eval-procedure` & `surgery`**: Acts as a digital auditor for operative documentation, flagging inconsistencies and identifying nerve/pressure risks in patient positioning (`pose`).
*   **`facts` & `myth`**: Leverages RAG to verify medical statements against high-quality evidence, systematically debunking clinical misinformation.
*   **`flashcard`**: Uses computer vision to bridge the health literacy gap by extracting and explaining terms directly from physical medical labels.
*   **`history` & `refer`**: Standardizes clinical intake with adaptive, targeted questions and optimizes specialist referrals to ensure patient-expert matching.

> **📘 Exhaustive Reference**: For a deep-dive into all 24 medical modules and how they augment traditional practice, see the [**Detailed CLI Reference**](./CLI_REFERENCE.md).

---

## 📦 Installation

1.  **Clone & Enter**:
    ```bash
    git clone https://github.com/csv610/LiteLLM.git
    cd LiteLLM/app/MedKit
    ```
2.  **Install Locally**:
    ```bash
    pip install -e .
    ```
3.  **Set Up AI**:
    MedKit defaults to local models via Ollama (`gemma3`). Supports OpenAI/Anthropic via environment variables.

---

## 📂 Output & Storage

*   **General Reports**: All generated medical, drug, and research reports are saved to the `./outputs/` directory by default.
*   **Privacy Data**: HIPAA-compliant sessions and audit logs are stored securely at `~/.medkit/sessions/`.
*   **Customization**: Use the `-d` or `--output-dir` flag with any command to override the default storage path.

---

## ⚖️ License & Disclaimer

Distributed under the MIT License. **MedKit is a research tool.** It is NOT a medical device and should NOT be used for direct patient diagnosis without professional oversight.
