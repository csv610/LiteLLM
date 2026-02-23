# MedKit: The Agentic Medical Intelligence Platform

[![CI/CD](https://github.com/csv610/LiteLLM/actions/workflows/ci.yml/badge.svg)](https://github.com/csv610/LiteLLM/actions)
[![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.archive.org/details/github-MIT-license-blue.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Production--Ready-success)](https://github.com/csv610/LiteLLM)

MedKit is a high-integrity, agent-driven medical intelligence platform. It transforms fragmented clinical data into actionable insights through a professional suite of specialized tools and an autonomous reasoning orchestrator.

---

## 🏗 Key Architectural Pillars

### 1. Autonomous Reasoning (The Orchestrator)
The **MedKit Orchestrator Agent** uses a **ReAct (Reason + Act)** reasoning loop to solve complex clinical queries. It autonomously coordinates multiple specialized tools, synthesizes observations, and provides professional medical assessments.

### 2. Specialized Clinical Tools
A robust suite of deterministic tools covering:
*   **Terminology Recognition:** 19 specialized identifiers for drugs, pathogens, and signs.
*   **Safety & Interactions:** Deep analysis of drug-drug, drug-food, and drug-disease risks.
*   **Clinical Reference:** Direct access to anatomy, ICD-11 codes, and surgical protocols.
*   **Mental Health:** HIPAA-aligned, trauma-informed assessment and screening.

### 3. Engineering Excellence (CI/CD)
*   **Automated Quality:** Every commit is validated via **GitHub Actions**.
*   **Multi-Version Support:** Continuous testing across Python 3.8 through 3.12.
*   **Linting & Standards:** Rigorous code quality enforcement using **Ruff**.
*   **Testing:** 160+ comprehensive unit and integration tests with 90%+ coverage in core utilities.

---

## 🎯 Clinical Stakeholder Utility

MedKit provides specialized value across the healthcare ecosystem:

### 👤 Patients (Health Empowerment)
*   **Medicine Explainer:** Translate complex pharmacological data into compassionate, plain-language summaries (`medkit-drug`).
*   **Self-Screening:** Private, trauma-informed access to mental health assessments and preliminary medical info.
*   **Safety Verification:** Cross-check potential drug and food interactions from a patient-centered perspective.

### 🩺 Doctors (Decision Support)
*   **Agentic Reasoning:** Use `medkit-agent` as a reasoning partner for complex cases involving co-morbidities and multiple medications.
*   **Rapid Identification:** Instant recognition of rare clinical signs, pathogens, and imaging findings during diagnostic workflows.
*   **Trauma-Informed Frameworks:** Utilize standardized SANE interview protocols for forensic and compassionate care.

### 🧪 Researchers (Data & Discovery)
*   **Entity Extraction:** Scale medical entity recognition across massive clinical datasets using standardized recognizers.
*   **Codified Metadata:** Automate ICD-11 coding and terminology mapping for research papers and clinical trials.
*   **Synthetic Modeling:** Generate standardized case reports for teaching and algorithm training.

### 💊 Pharmacists (Pharmacovigilance)
*   **Safety Intersections:** Deep analysis of drug-drug, drug-disease, and drug-food contraindications.
*   **Mechanism Insights:** Rapid retrieval of medicine indications and side-effect profiles.
*   **Terminology Mapping:** Resolve medical abbreviations and standardized drug classes instantly.

---

## 🚀 Professional Quick Start

### 1. Installation
Install MedKit as a professional system package:

```bash
git clone https://github.com/csv610/LiteLLM.git
cd app/MedKit
pip install -e .
```

### 2. Autonomous Agency
Solve complex queries using the MedKit Agent:
```bash
medkit-agent "Patient on Metformin has a new rash. Analyze risks."
```

### 3. Direct Tool Usage
Access specialized modules directly from any directory:
```bash
medkit-medical anatomy "heart"
medkit-recognizer drug "Aspirin"
medkit-drug "Ibuprofen"
```

---

## 🛠 Command Reference Table

| Command | Capability | Source Module |
| :--- | :--- | :--- |
| **`medkit-agent`** | **Autonomous Clinical Reasoning** | `medkit_agent` |
| `medkit-medical` | Unified Medical Info (Anatomy/Disease/Surgery) | `medical` |
| `medkit-sane` | Trauma-Informed SANE Interview | `sane_interview` |
| `medkit-recognizer` | Multi-Entity Medical Recognition | `recognizers` |
| `medkit-dictionary` | Medical Dictionary Generation | `med_dictionary` |
| `medkit-mental` | Mental Health Assessment Chat | `mental_health` |
| `medkit-drug` | Medicine & Interaction Explainer | `drug` |
| `medkit-codes` | ICD-11 WHO Code Retrieval | `med_codes` |

---

## 📂 System Architecture

```text
MedKit/
├── .github/workflows/    # CI/CD Pipelines (Lint, Test, Build)
├── medkit_agent/         # Autonomous ReAct Orchestrator
├── drug/                 # Standardized Pharmacology Suite
├── medical/              # Specialized Clinical Reference
├── recognizers/          # Medical Entity Identification Engine
├── mental_health/        # Trauma-Informed Assessment
├── sane_interview/       # Forensic Interview Framework
├── scripts/              # Internal Development Utilities
├── tests/                # 160+ Unit & Integration Tests
└── pyproject.toml        # Professional Packaging Definition
```

---

## 🧪 Development & Standards

We maintain a zero-tolerance policy for "bullshit" code. All contributions must pass:

1.  **Static Analysis:** `ruff check .`
2.  **Formatting:** `ruff format .`
3.  **Automated Testing:** `pytest tests/`

To run the developer suite locally:
```bash
pip install pytest pytest-cov ruff build
pytest tests/ --cov=.
```

---

## 📜 Medical Disclaimer
MedKit is an AI-assisted clinical support tool. It is **not** a substitute for professional medical judgment. All clinical decisions must be verified by a licensed healthcare professional.

---
**Version**: 1.2 (Agentic Orchestration Edition)
**Last Updated**: February 23, 2026
**Architecture**: Senior Engineer / Architect Verified
