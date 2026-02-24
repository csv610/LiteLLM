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

| Category | Modules |
| :--- | :--- |
| **General Reference** | `anatomy`, `disease`, `organ`, `topic`, `herbal` |
| **Clinical Support** | `advise`, `decision`, `facts`, `myth`, `refer`, `history`, `faq`, `implant` |
| **Surgical Suite** | `surgery`, `pose`, `tool`, `tray` |
| **Education & Ethics** | `ethics`, `case`, `quiz`, `flashcard`, `roles`, `procedure`, `eval-procedure` |

> **📘 Exhaustive Reference**: For every subcommand, clinical safety boundary, and failure mode, see the [**Detailed CLI Reference**](./CLI_REFERENCE.md).

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
