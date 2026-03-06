# Medical Dictionary Toolkit

A professional suite of tools for building, classifying, reviewing, and exploring a comprehensive medical dictionary. This toolkit leverages Large Language Models (LLMs) for content generation and classification, while integrating with official medical APIs for standardized coding.

## Core Features

- **Automated Dictionary Building**: Generate precise, professional medical definitions for terms using LLMs (defaulting to Ollama/Gemma3).
- **Medical Term Classification**: Categorize terms into structured medical categories and subcategories (e.g., Anatomy, Diseases, Procedures).
- **Standardized Code Extraction**: Retrieve codes from major medical terminologies:
  - **RxNorm** (Medications)
  - **ICD-10-CM / ICD-11** (Diseases)
  - **LOINC** (Lab Tests & Measurements)
  - **SNOMED CT / MeSH** (Clinical Terminology - requires UMLS API key)
- **Quality Assurance Review**: Automated 4-point validation system ensuring definitions are:
  1. Medically recognized.
  2. Free of abbreviations in the term.
  3. Objective and professional in tone.
  4. Precise (avoiding circular definitions).
- **Interactive Exploration**: Search the dictionary with fuzzy matching support for misspelled terms and prefix-based discovery.

## Project Structure

```text
├── medical_dictionary_cli.py     # Main entry point for building definitions
├── medical_term_classify.py      # Classification engine
├── review_medical_dictionary.py  # Quality control and validation tool
├── extract_medical_codes.py      # API integration for medical codes
├── explore_medical_dictionary.py # Interactive CLI search tool
├── assets/                       # Seed data and term lists (anatomy, drugs, etc.)
└── outputs/                      # Generated dictionaries and classification reports
```

## Installation

### Prerequisites
- Python 3.8+
- [Ollama](https://ollama.ai/) (for local LLM support)
- (Optional) UMLS API Key for SNOMED CT and MeSH lookups.

### Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install tqdm requests rapidfuzz
   ```
3. (Optional) Set your UMLS API key:
   ```bash
   export UMLS_API_KEY="your-api-key-here"
   ```

## Usage

### 1. Building a Dictionary
Generate definitions for a single term or a file containing terms:
```bash
python medical_dictionary_cli.py "Myocardial Infarction"
python medical_dictionary_cli.py assets/diseases.txt
```

### 2. Classifying Terms
Organize terms into medical hierarchies:
```bash
python medical_term_classify.py assets/extracted_terms.txt
```

### 3. Extracting Medical Codes
Fetch standardized codes from RxNorm, ICD, and LOINC:
```bash
python extract_medical_codes.py "Aspirin"
```

### 4. Reviewing Dictionary Quality
Run the automated quality check on a generated dictionary:
```bash
python review_medical_dictionary.py outputs/dictionary_ollama_gemma3.json
```

### 5. Exploring the Dictionary
Search the dictionary interactively:
```bash
python explore_medical_dictionary.py outputs/dictionary_ollama_gemma3.json
```

## Data Assets
The toolkit includes pre-defined lists of terms in the `assets/` directory, covering:
- Anatomy & Microorganisms
- Diseases & Surgeries
- Drugs & Procedures
- Tests & Clinical Measurements

## Technical Standards
- **Objectivity**: Definitions are filtered for subjective or conversational language.
- **Precision**: Automated checks ensure definitions are concise (10-100 words).
- **Traceability**: All outputs are saved in structured JSON format for easy integration into other systems.
