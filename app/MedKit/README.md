# MedKit: LLM-Powered Medical Tooling & Orchestration Framework

[![CI/CD Status](https://github.com/csv610/LiteLLM/actions/workflows/ci.yml/badge.svg)](https://github.com/csv610/LiteLLM/actions)
[![Test Coverage](https://img.shields.io/badge/Coverage-90%25+-green)](#-engineering-audit)
[![Version](https://img.shields.io/badge/Version-1.2--Experimental-orange)](#)

## ⚖️ Brutal Objectivity: What MedKit Is and Is Not

MedKit is **not** a medical device, a doctor, or a source of truth. It is a **technical framework** that wraps Large Language Model (LLM) calls into structured clinical tools. Its value lies in **standardizing the interaction** between AI and medical data, not in the medical accuracy of the LLM itself.

### The Reality Check:
1.  **LLM Dependency:** MedKit's intelligence is strictly bounded by the underlying model (default: `ollama/gemma3`). If the model hallucinates, the tool returns a hallucination.
2.  **Experimental Agency:** The `medkit-agent` uses a ReAct (Reasoning + Acting) loop. While powerful for multi-step lookups, it is subject to logic loops and requires human supervision.
3.  **CLI-First:** This is a developer/researcher tool. It lacks a GUI and assumes terminal proficiency.
4.  **Privacy:** While the code includes privacy utilities, data security depends entirely on your local/provider LLM configuration (e.g., Ollama vs. OpenAI).

---

## 🛠 Functional Scope & Implementation

### 1. The Orchestration Layer (`medkit-agent`)
A basic implementation of the ReAct pattern. It parses user queries into function calls for the underlying MedKit tools.
*   **Best For:** Automating repetitive lookups across multiple modules.
*   **Risk:** Can "hallucinate" tool sequences if the query is underspecified.

### 2. Standardized Tool Suite
19+ Python modules that enforce **Structured Output** (JSON/Pydantic) from LLM responses.
*   **Capabilities:** Entity recognition (Pathogens, Drugs, Signs), ICD-11 search, and interaction analysis.
*   **Reliability:** High structural reliability (it will return valid JSON); variable content reliability (dependent on LLM).

### 3. Engineering Audit
*   **Architecture:** Modular package structure with formal entry points (`pyproject.toml`).
*   **CI/CD:** Mandatory linting (`ruff`) and testing across 5 Python versions (3.8-3.12).
*   **Testing:** 160+ tests focused on **logic, paths, and structural integrity**. Note: Tests do *not* validate medical accuracy (which is non-deterministic).

---

## 👤 Stakeholder Context

### 🩺 For Clinicians & Pharmacists
*   **Utility:** Use as a "Reasoning Assistant" for quick reference cross-checks and interaction lookups.
*   **Warning:** Never use as a primary decision-making tool. Verify all outputs against established clinical databases (Lexicomp, UpToDate).

### 🧪 For Researchers
*   **Utility:** Automate the extraction of structured entities from clinical notes and map them to standardized codes (ICD-11).
*   **Warning:** Review LLM-extracted entities for "false positives" in rare disease categories.

### 👤 For Patients
*   **Utility:** Translate jargon-heavy medical documents into readable summaries.
*   **Warning:** This tool is for **educational purposes only**. It cannot diagnose or treat any condition.

---

## 🚀 Quick Start (Technical)

```bash
# 1. Install as an editable package
pip install -e .

# 2. Run the Agent (Requires Ollama/Gemma3 running)
medkit-agent "Analyze Metformin side effects."

# 3. Direct Module Access
medkit-medical anatomy "heart"
medkit-recognizer drug "Aspirin"
```

---

## 📜 Mandatory Medical Disclaimer
**MedKit IS NOT A LICENSED MEDICAL TOOL.** It is provided "as is" for research and educational purposes. The creators assume no liability for any medical decisions made based on this software. **ALL OUTPUTS MUST BE VERIFIED BY A LICENSED PROFESSIONAL.**

---
**Technical Specification**: v1.2.0-Alpha
**Engineering Status**: Verified Package Structure & CI/CD Pipeline
