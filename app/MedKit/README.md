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
| **`medkit-drug`** | **Safety**: Interaction checking, contraindications, and patient-friendly explanations. |
| **`medkit-medical`**| **Knowledge**: 20+ specialized modules for anatomy, ethics, surgery, and triage. |
| **`medkit-graph`** | **Insight**: Visualizes the logical causal links in dense medical text. |
| **`medkit-privacy`**| **Compliance**: Automates HIPAA consent, audit logs, and PII scrubbing. |
| **`medkit-exam`** | **Protocol**: Standardized head-to-toe physical examination checklists. |
| **`medkit-article`**| **Evidence**: Searches PubMed and BioMCP for peer-reviewed research. |

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

## ⚖️ License & Disclaimer

Distributed under the MIT License. **MedKit is a research tool.** It is NOT a medical device and should NOT be used for direct patient diagnosis without professional oversight.
