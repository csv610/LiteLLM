# Medical Term Extractor

A command-line tool that extracts and categorizes medical concepts from unstructured text using structured language model processing with named entity recognition for healthcare domains.

## Overview

The Medical Term Extractor analyzes medical text and identifies key medical entities including diseases, medicines, symptoms, treatments, procedures, specialties, anatomical terms, side effects, and causation relationships. The tool uses a large language model to parse clinical narratives, medical literature, or patient documentation and structures the extracted information into standardized categories.

## Important Medical Disclaimers

**This tool is for informational and educational purposes only.** It is not a substitute for professional medical documentation review, clinical coding expertise, or healthcare informatics systems. Users should:

- Understand that this tool performs automated text analysis and may miss or misclassify medical terms
- Verify extracted information with qualified medical coders or clinical documentation specialists
- Be aware that LLM-generated extractions may contain errors, hallucinations, or incomplete information
- Not use this tool for clinical decision-making, patient diagnosis, or treatment planning
- Recognize that context and medical meaning may be lost in automated extraction processes
- Always follow HIPAA and other privacy regulations when processing patient-related text
- Consult with healthcare informatics professionals for production medical NLP systems
- Validate results against established medical terminologies (SNOMED CT, ICD, RxNorm, etc.)

The information extracted reflects the capabilities and limitations of the underlying language model and should not be considered definitive or suitable for clinical use without human expert review.

## Installation

### Requirements

- Python 3.8+
- LiteClient and related dependencies from the parent project
- Rich library for formatted console output

### Setup

```bash
cd med_terms_extractor
pip install -r requirements.txt
```

## Usage

### Basic Command

Extract medical terms from text:

```bash
python medical_term_extractor_cli.py "The patient presents with hypertension and was prescribed lisinopril."
```

Extract from a file:

```bash
python medical_term_extractor_cli.py patient_notes.txt
```

### Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `input` | — | **Required.** Input text string or path to text file | — |
| `--output` | `-o` | Path to save output JSON file | None (display only) |
| `--model` | `-m` | Language model to use | `gemini-1.5-pro` |

### Examples

Save extraction results to JSON:
```bash
python medical_term_extractor_cli.py clinical_notes.txt -o extraction_results.json
```

Use a different model:
```bash
python medical_term_extractor_cli.py "Patient has diabetes mellitus type 2" -m "gpt-4"
```

Process a medical report:
```bash
python medical_term_extractor_cli.py discharge_summary.txt -o discharge_terms.json -m "gemini-1.5-pro"
```

## Features

- **Multi-Category Extraction**: Identifies 9 distinct types of medical concepts
- **Contextual Preservation**: Maintains the original text context where each term was found
- **Relationship Detection**: Identifies causation relationships between medical concepts
- **Structured Output**: Returns `MedicalTerms` objects with standardized schema
- **JSON Export**: Save results for downstream processing or medical NLP pipelines
- **Flexible Input**: Accepts both direct text strings and file paths
- **System Prompting**: Uses specialized prompts for medical documentation expertise

## Code Architecture

### Core Components

**`MedicalTermExtractor`** - Main class for term extraction
- Initializes with language model configuration
- Validates input text
- Extracts and categorizes medical terms
- Handles result display and file output

**Prompt Functions**
- `create_system_prompt()`: Defines the LLM's role as a medical documentation specialist
- `create_user_prompt(text)`: Creates structured extraction queries with category-specific instructions

**Output Functions**
- File output handled via standard JSON serialization

**CLI Entry Point**
- `main()`: Handles argument parsing and orchestrates the extraction workflow

## Output Format

The tool generates a `MedicalTerms` object with 9 distinct categories (see `medical_term_extractor_models.py` for complete schema):

```json
{
  "diseases": [
    {
      "name": "hypertension",
      "context": "The patient presents with hypertension"
    }
  ],
  "medicines": [
    {
      "name": "lisinopril",
      "context": "was prescribed lisinopril for blood pressure control"
    }
  ],
  "symptoms": [
    {
      "name": "chest pain",
      "context": "Patient reports chest pain on exertion"
    }
  ],
  "treatments": [
    {
      "name": "physical therapy",
      "context": "referred to physical therapy for rehabilitation"
    }
  ],
  "procedures": [
    {
      "name": "echocardiogram",
      "context": "echocardiogram performed to assess cardiac function"
    }
  ],
  "specialties": [
    {
      "name": "cardiology",
      "context": "consultation with cardiology department"
    }
  ],
  "anatomical_terms": [
    {
      "name": "left ventricle",
      "context": "left ventricle shows reduced ejection fraction"
    }
  ],
  "side_effects": [
    {
      "name": "dizziness",
      "related_medicine": "lisinopril",
      "context": "Patient reports dizziness after starting lisinopril"
    }
  ],
  "causation_relationships": [
    {
      "cause": "smoking",
      "effect": "chronic obstructive pulmonary disease",
      "relationship_type": "causes",
      "context": "Long-term smoking causes COPD"
    }
  ]
}
```

## Extracted Categories

### 1. **Diseases**
Medical conditions, diagnoses, disorders, and pathologies
- Examples: diabetes, hypertension, pneumonia, cancer

### 2. **Medicines**
Drugs, pharmaceuticals, medications, and therapeutic agents
- Examples: aspirin, insulin, antibiotics, chemotherapy agents

### 3. **Symptoms**
Clinical signs, patient-reported symptoms, and observable manifestations
- Examples: fever, pain, cough, fatigue

### 4. **Treatments**
Therapeutic interventions, therapies, and treatment modalities
- Examples: radiation therapy, counseling, rehabilitation

### 5. **Procedures**
Medical procedures, diagnostic tests, and clinical interventions
- Examples: MRI, blood test, surgery, biopsy

### 6. **Specialties**
Medical specialties, subspecialties, and clinical disciplines
- Examples: cardiology, neurology, oncology, pediatrics

### 7. **Anatomical Terms**
Body structures, organs, tissues, and anatomical locations
- Examples: heart, kidney, cerebellum, femoral artery

### 8. **Side Effects**
Adverse reactions, medication side effects, and treatment complications
- Examples: nausea, allergic reaction, hair loss
- Includes optional linkage to the related medicine

### 9. **Causation Relationships**
Causal connections between medical concepts
- Format: `[cause] → [relationship_type] → [effect]`
- Examples: "obesity causes diabetes", "infection leads to sepsis"

## Use Cases

### Clinical Documentation
- Extract key concepts from clinical notes and discharge summaries
- Support clinical documentation improvement (CDI) programs
- Assist with medical coding and billing review

### Medical Literature Analysis
- Parse research articles and extract medical entities
- Build knowledge graphs from medical publications
- Support systematic literature reviews

### Patient Data Processing
- Analyze patient feedback and surveys for symptoms
- Extract medication lists from unstructured records
- Identify adverse events from clinical notes

### Medical Education
- Create study materials from textbook content
- Generate flashcards from medical literature
- Support clinical case analysis

### Healthcare NLP Pipelines
- Preprocessing step for downstream clinical NLP tasks
- Entity recognition for medical knowledge extraction
- Input for clinical decision support systems

## Limitations

1. **Model Dependency**: Extraction quality depends on the underlying language model's medical knowledge
2. **Context Sensitivity**: Complex medical context may be oversimplified or misinterpreted
3. **No Medical Validation**: Extracted terms are not verified by medical professionals
4. **Terminology Variations**: May miss synonyms, abbreviations, or non-standard terminology
5. **Ambiguity Handling**: Homonyms and polysemy in medical language may cause misclassification
6. **Relationship Complexity**: Causation relationships may oversimplify complex medical mechanisms
7. **Privacy Considerations**: Not designed for HIPAA-compliant processing without additional safeguards
8. **No Negation Detection**: May extract terms even when negated in the source text
9. **Language Limitations**: Optimized for English medical text; other languages may not be supported
10. **No Code Mapping**: Does not map terms to standard medical terminologies (ICD-10, SNOMED CT, etc.)

## Best Practices

- Use this tool for exploratory analysis and educational purposes
- Always validate extractions with medical experts or coding specialists
- Consider implementing negation detection for production use cases
- Map extracted terms to standard medical ontologies for interoperability
- Test on domain-specific medical text to assess accuracy for your use case
- Combine with established medical NLP libraries (scispaCy, MedSpaCy, etc.) for robust systems
- Implement PHI detection and removal before processing patient data
- Keep records of model versions and extraction dates for audit trails
- Review and curate extraction results before using in downstream applications
- Consider fine-tuning or prompt engineering for specialized medical domains

## Technical Details

### Temperature Setting
The model uses `temperature=0.1` for more deterministic and consistent extractions.

### Input Handling
- Accepts plain text strings directly via command line
- Automatically detects and reads from file paths
- Validates that input text is non-empty

### Error Handling
- Validates input text before processing
- Returns clear error messages on failure
- Exits with proper status codes for automation

## Related Files

- `medical_term_extractor_models.py` - Pydantic models for structured medical entity extraction
- `medical_term_extractor_cli.py` - Command-line interface and extraction logic

## Future Enhancements

Potential improvements for future versions:
- Integration with medical terminology APIs (RxNorm, SNOMED CT)
- Negation and uncertainty detection
- Multi-language support
- Abbreviation expansion
- Temporal relationship extraction
- Dosage and frequency extraction for medications
- Batch processing for multiple documents
- Configurable extraction categories
- Entity linking to knowledge bases

## License

See parent project LICENSE file.
