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

#### 🧪 Clinical Intelligence: AI Augmentation of Traditional Workflows

MedKit doesn't just provide definitions; it augments traditional medical practice through targeted AI reasoning:

*   **`advise` & `decision`**: Replaces static paper flowcharts with dynamic clinical decision support, suggesting prioritized differential diagnoses based on patient context.
*   **`interact` & `disease` (Pharmacology)**: Automates multi-drug interaction screening and drug-disease safety checks, identifying physiological contraindications often overlooked in rapid clinical encounters.
*   **`explain` (Patient Safety)**: Generates compassionate, plain-language patient education to improve adherence and bridge the health literacy gap.
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
