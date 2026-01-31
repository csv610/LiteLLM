# Medical Topic Information Generator

A command-line tool that generates structured medical topic documentation using large language models to create detailed educational and reference materials for healthcare topics.

## Overview

The Medical Topic Information Generator analyzes medical topics and produces documentation covering 17 distinct aspects including epidemiology, pathophysiology, clinical presentation, diagnosis, treatment, prognosis, prevention, psychosocial impact, and more. The tool uses a large language model to generate detailed, well-structured medical topic overviews suitable for educational purposes, clinical reference, or medical knowledge base development.

## Important Medical Disclaimers

**This tool is for informational and educational purposes only.** It is not a substitute for professional medical advice, clinical guidelines, or evidence-based medical literature. Users should:

- Understand that this tool generates AI-generated content that may contain errors, inaccuracies, or outdated information
- Verify all medical information with authoritative sources, clinical guidelines, and peer-reviewed literature
- Not use this tool for clinical decision-making, patient diagnosis, treatment planning, or medical advice
- Recognize that LLM-generated content may include hallucinations, misrepresentations, or incomplete medical knowledge
- Always consult current medical textbooks, clinical practice guidelines, and medical experts
- Validate information against established evidence-based sources (UpToDate, medical textbooks, clinical trials)
- Be aware that medical knowledge evolves rapidly and AI-generated content may not reflect the latest research
- Not distribute generated content as professional medical literature without expert review
- Understand that this tool does not replace comprehensive medical education or clinical training
- Use generated content only as a starting point for further research and validation

The information generated reflects the capabilities and limitations of the underlying language model and should not be considered definitive, clinically validated, or suitable for patient care without thorough expert review.

## Installation

### Requirements

- Python 3.8+
- LiteClient and related dependencies from the parent project
- Rich library for formatted console output

### Setup

```bash
cd med_topic
pip install -r requirements.txt
```

## Usage

### Basic Command

Generate medical topic information:

```bash
python medical_topic_cli.py -i "diabetes mellitus"
```

### Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--topic` | `-i` | **Required.** The name of the medical topic to generate information for | — |
| `--output` | `-o` | Path to save the output JSON file | None (auto-generated) |
| `--output-dir` | `-d` | Directory for output files | `outputs` |
| `--model` | `-m` | Language model to use | `ollama/gemma3` |
| `--verbosity` | `-v` | Logging level (0-4): 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG | 2 |

### Examples

Generate topic information with default settings:
```bash
python medical_topic_cli.py -i inflammation
```

Specify custom output file:
```bash
python medical_topic_cli.py -i "immune response" -o immune_response.json
```

Use custom output directory with verbose logging:
```bash
python medical_topic_cli.py -i metabolism -d outputs/topics -v 3
```

Use a different language model:
```bash
python medical_topic_cli.py -i "cardiovascular disease" -m "gpt-4" -v 4
```

Generate multiple topics:
```bash
python medical_topic_cli.py -i "hypertension" -o hypertension.json
python medical_topic_cli.py -i "type 2 diabetes" -o diabetes_t2.json
python medical_topic_cli.py -i "asthma" -o asthma.json
```

## Features

- **Detailed Coverage**: Generates 17 distinct aspects of medical topic information
- **Structured Output**: Returns `MedicalTopic` objects with standardized Pydantic schema
- **System Prompting**: Uses specialized prompts for medical information expertise
- **JSON Export**: Saves results in machine-readable format for downstream processing
- **Formatted Console Display**: Results organized in panels using Rich
- **Flexible Input**: Accepts any medical topic name or phrase
- **Configurable Models**: Supports multiple LLM backends
- **Logging**: Comprehensive logging with adjustable verbosity levels
- **Auto-naming**: Automatically generates output filenames based on topic name

## Code Architecture

### Core Components

**`MedicalTopicGenerator`** - Main class for topic information generation
- Initializes with language model configuration
- Validates input topic
- Generates comprehensive medical documentation
- Handles result display and file output
- Integrates with LiteClient for LLM communication

**Prompt Functions**
- `create_system_prompt()`: Defines the LLM's role as a medical information expert with specific quality guidelines
- `create_user_prompt(topic)`: Creates structured generation queries for the specified medical topic

**Output Functions**
- `save()`: Persists results to JSON files with proper serialization

**CLI Entry Point**
- `app_cli()`: Handles argument parsing, logging configuration, and orchestrates the generation workflow
- `get_user_arguments()`: Command-line argument parser with comprehensive help text

## Output Format

The tool generates a `MedicalTopic` object with 17 comprehensive sections (see `medical_topic_models.py` for complete schema):

### Structure Overview

```json
{
  "overview": {
    "topic_name": "Diabetes Mellitus",
    "alternative_names": "Diabetes, DM, Sugar diabetes",
    "topic_category": "Metabolic disorder",
    "medical_specialties": "Endocrinology, Internal Medicine, Family Medicine",
    "prevalence": "Affects approximately 10.5% of adults worldwide"
  },
  "definition": {
    "plain_language_explanation": "Diabetes is a condition where the body cannot properly process sugar...",
    "medical_definition": "A chronic metabolic disorder characterized by hyperglycemia...",
    "key_characteristics": "Hyperglycemia, insulin deficiency, insulin resistance",
    "disease_classification": "Endocrine/metabolic disorder"
  },
  "epidemiology": {
    "incidence_rate": "Approximately 1.5 million new cases annually in the US",
    "prevalence_rate": "10.5% of global population",
    "age_of_onset": "Type 1: childhood/adolescence; Type 2: typically after age 45",
    "gender_differences": "Slightly higher in males",
    "geographic_variation": "Higher in developed nations",
    "risk_groups": "Obese individuals, family history, sedentary lifestyle"
  },
  "etiology": {
    "primary_causes": "Genetic predisposition, autoimmune destruction, insulin resistance",
    "genetic_factors": "Multiple genetic variants, family history increases risk",
    "environmental_factors": "Diet, sedentary lifestyle, urbanization",
    "lifestyle_factors": "Obesity, physical inactivity, unhealthy diet",
    "infectious_agents": "Viral infections may trigger Type 1 in susceptible individuals",
    "contributing_factors": "Age, ethnicity, previous gestational diabetes"
  },
  "pathophysiology": {
    "mechanism_of_disease": "Insulin deficiency or resistance leads to impaired glucose uptake...",
    "affected_systems": "Endocrine, cardiovascular, renal, nervous, integumentary",
    "cellular_changes": "Beta cell destruction (Type 1), insulin receptor dysfunction (Type 2)",
    "progression_stages": "Prediabetes, early diabetes, established diabetes, complications",
    "inflammatory_response": "Chronic low-grade inflammation in Type 2",
    "immune_involvement": "Autoimmune destruction of beta cells in Type 1"
  },
  "clinical_presentation": {
    "primary_symptoms": "Polyuria, polydipsia, polyphagia, weight loss",
    "secondary_symptoms": "Fatigue, blurred vision, slow wound healing",
    "symptom_onset": "Acute in Type 1, gradual in Type 2",
    "severity_spectrum": "Mild to severe with acute complications",
    "acute_vs_chronic": "Chronic disease with acute exacerbations",
    "symptom_triggers": "Dietary indiscretion, illness, stress, medications",
    "asymptomatic_presentation": "Type 2 often asymptomatic in early stages"
  },
  "diagnosis": {
    "diagnostic_tests": "Fasting plasma glucose, HbA1c, oral glucose tolerance test",
    "imaging_studies": "Not typically required for diagnosis",
    "laboratory_findings": "Hyperglycemia, elevated HbA1c, glucosuria",
    "diagnostic_criteria": "FPG ≥126 mg/dL or HbA1c ≥6.5% or OGTT ≥200 mg/dL",
    "differential_diagnosis": "Other causes of hyperglycemia, diabetes insipidus, MODY",
    "diagnostic_challenges": "Early Type 2 may be asymptomatic",
    "time_to_diagnosis": "Type 1: days to weeks; Type 2: often years"
  },
  "complications": {
    "acute_complications": "Diabetic ketoacidosis, hyperosmolar hyperglycemic state, hypoglycemia",
    "chronic_complications": "Retinopathy, nephropathy, neuropathy, cardiovascular disease",
    "complication_rates": "High if poorly controlled",
    "organ_system_effects": "Eyes, kidneys, nerves, heart, blood vessels",
    "mortality_rate": "Doubles risk of premature death",
    "disability_outcomes": "Blindness, kidney failure, amputations, stroke"
  },
  "treatment": {
    "first_line_treatment": "Type 1: Insulin therapy; Type 2: Metformin + lifestyle",
    "medications": "Insulin, metformin, sulfonylureas, GLP-1 agonists, SGLT2 inhibitors",
    "surgical_interventions": "Bariatric surgery in selected Type 2 patients",
    "physical_therapy": "Exercise programs for metabolic control",
    "lifestyle_modifications": "Diet, exercise, weight loss, smoking cessation",
    "dietary_management": "Carbohydrate counting, low glycemic index foods",
    "complementary_approaches": "Continuous glucose monitoring, diabetes education programs",
    "treatment_duration": "Lifelong management required"
  },
  "prognosis": {
    "overall_prognosis": "Good with proper management; poor if uncontrolled",
    "remission_possibility": "Type 2 may achieve remission with significant weight loss",
    "cure_potential": "Currently incurable; Type 2 may achieve remission",
    "recovery_rates": "Not applicable; requires lifelong management",
    "factors_affecting_prognosis": "Glycemic control, compliance, complication prevention",
    "long_term_outlook": "Normal life expectancy possible with good control",
    "quality_of_life_impact": "Moderate to significant depending on control and complications"
  },
  "prevention": {
    "primary_prevention": "Healthy diet, regular exercise, maintain healthy weight",
    "secondary_prevention": "Screening in high-risk individuals, prediabetes intervention",
    "screening_recommendations": "Adults 45+ every 3 years; earlier if risk factors present",
    "protective_factors": "Normal weight, physical activity, healthy diet",
    "lifestyle_prevention": "Mediterranean diet, 150 min/week exercise, weight management",
    "vaccinations": "Not applicable for prevention"
  },
  "research_and_evidence": {
    "evidence_quality": "High-quality evidence from numerous large trials",
    "current_research_areas": "Artificial pancreas, stem cell therapy, prevention strategies",
    "emerging_treatments": "Smart insulin, beta cell regeneration, immunotherapy for Type 1",
    "clinical_trials": "Numerous ongoing trials for medications and devices",
    "guideline_sources": "ADA, EASD, WHO, IDF clinical practice guidelines"
  },
  "psychosocial_impact": {
    "mental_health_effects": "Depression, anxiety, diabetes distress common",
    "emotional_burden": "Daily management stress, fear of complications",
    "social_impact": "Social stigma, dietary restrictions in social settings",
    "occupational_impact": "May affect job choices, insurance costs",
    "coping_strategies": "Support groups, counseling, diabetes education, self-care",
    "support_resources": "ADA, JDRF, diabetes educators, online communities"
  },
  "education": {
    "key_takeaways": "Chronic but manageable, requires daily attention, prevention possible",
    "common_misconceptions": "Eating sugar causes diabetes, insulin is a last resort",
    "frequently_asked_questions": "Comprehensive FAQ section",
    "when_to_see_doctor": "Symptoms of hyperglycemia, hypoglycemia, or complications"
  },
  "special_populations": {
    "pediatric_considerations": "Type 1 more common, unique psychosocial challenges",
    "geriatric_considerations": "Hypoglycemia risk, simplified regimens often needed",
    "pregnancy_considerations": "Gestational diabetes, tight control needed in pregnancy",
    "gender_specific_aspects": "Gestational diabetes in women, erectile dysfunction in men",
    "ethnic_variations": "Higher prevalence in certain ethnic groups"
  },
  "cost_and_impact": {
    "healthcare_costs": "Estimated $327 billion annually in US",
    "productivity_loss": "Significant absenteeism and disability costs",
    "burden_on_healthcare_system": "Major driver of healthcare expenditures",
    "insurance_considerations": "Medications and supplies may be expensive"
  },
  "see_also": {
    "related_topics": "Metabolic syndrome, obesity, cardiovascular disease",
    "connection_types": "Risk factor, complication, related condition",
    "reason": "These conditions are interconnected through metabolic pathways"
  },
  "metadata": {
    "last_updated": "2024",
    "information_sources": "ADA guidelines, medical textbooks, clinical trials",
    "confidence_level": "High",
    "complexity_level": "Intermediate"
  }
}
```

## Sections Generated

### 1. **Overview** (TopicOverview)
Basic identification and classification
- Topic name and alternative names
- Category and medical specialties
- Prevalence information

### 2. **Definition** (Definition)
Core understanding of the topic
- Plain language explanation
- Medical definition
- Key characteristics
- Disease classification

### 3. **Epidemiology** (Epidemiology)
Statistical and demographic information
- Incidence and prevalence rates
- Age of onset and gender differences
- Geographic variation and risk groups

### 4. **Etiology** (Etiology)
Causes and risk factors
- Primary causes and genetic factors
- Environmental and lifestyle factors
- Infectious agents and contributing factors

### 5. **Pathophysiology** (Pathophysiology)
Disease mechanisms and progression
- Mechanism of disease
- Affected systems and cellular changes
- Progression stages and immune involvement

### 6. **Clinical Presentation** (ClinicalPresentation)
Symptoms and manifestations
- Primary and secondary symptoms
- Symptom onset and severity spectrum
- Acute vs chronic presentation
- Symptom triggers

### 7. **Diagnosis** (Diagnosis)
Diagnostic approach
- Diagnostic tests and imaging studies
- Laboratory findings and criteria
- Differential diagnosis and challenges
- Time to diagnosis

### 8. **Complications** (Complications)
Potential adverse outcomes
- Acute and chronic complications
- Complication rates and organ effects
- Mortality rate and disability outcomes

### 9. **Treatment** (Treatment)
Management strategies
- First-line treatment and medications
- Surgical interventions and physical therapy
- Lifestyle modifications and dietary management
- Complementary approaches
- Treatment duration

### 10. **Prognosis** (Prognosis)
Expected outcomes
- Overall prognosis and remission possibility
- Cure potential and recovery rates
- Factors affecting prognosis
- Long-term outlook and quality of life impact

### 11. **Prevention** (Prevention)
Risk reduction strategies
- Primary and secondary prevention
- Screening recommendations
- Protective factors and lifestyle prevention
- Vaccinations if applicable

### 12. **Research and Evidence** (ResearchAndEvidence)
Current state of knowledge
- Evidence quality and research areas
- Emerging treatments and clinical trials
- Guideline sources

### 13. **Psychosocial Impact** (PsychosocialImpact)
Mental health and quality of life
- Mental health effects and emotional burden
- Social and occupational impact
- Coping strategies and support resources

### 14. **Education** (TopicEducation)
Patient communication
- Key takeaways and common misconceptions
- Frequently asked questions
- When to seek medical attention

### 15. **Special Populations** (SpecialPopulations)
Group-specific considerations
- Pediatric and geriatric considerations
- Pregnancy considerations
- Gender-specific aspects and ethnic variations

### 16. **Cost and Impact** (CostAndImpact)
Economic implications
- Healthcare costs and productivity loss
- Burden on healthcare system
- Insurance considerations

### 17. **See Also** (SeeAlso)
Cross-references
- Related topics and connection types
- Explanation of relationships

### 18. **Metadata** (TopicMetadata)
Information quality indicators
- Last updated and information sources
- Confidence level and complexity level

## Use Cases

### Medical Education
- Generate topic overviews for medical students
- Create study guides and reference materials
- Build comprehensive topic libraries for curricula
- Support self-directed learning

### Clinical Reference
- Quick reference for healthcare professionals
- Topic summaries for continuing medical education
- Foundation for evidence-based practice reviews
- Starting point for guideline development

### Health Communication
- Patient education material development
- Health literacy resources
- Medical writing and content creation
- Healthcare website content generation

### Knowledge Base Development
- Medical knowledge graph construction
- Clinical decision support system content
- Healthcare chatbot training data
- Medical information retrieval systems

### Research and Analysis
- Literature review starting points
- Topic mapping and taxonomy development
- Medical concept analysis
- Comparative disease analysis

## Limitations

1. **AI-Generated Content**: Information is generated by LLMs and may contain inaccuracies, biases, or outdated information
2. **Not Evidence-Based**: Does not cite specific research studies or clinical trials
3. **Lacks Clinical Validation**: Not reviewed or validated by medical experts
4. **Currency Issues**: May not reflect the most recent medical advances or guideline updates
5. **Completeness**: May miss important nuances or recent developments in the field
6. **Consistency**: Different runs may produce different information for the same topic
7. **Context Limitations**: May oversimplify complex medical topics
8. **No Source Attribution**: Does not provide specific references or citations
9. **Generalization**: May not capture all variations and subtypes of conditions
10. **Regional Variations**: May not account for geographic differences in practice or prevalence
11. **Quality Variability**: Output quality depends on the underlying LLM's medical knowledge
12. **No Clinical Applicability**: Not suitable for direct clinical use without expert review

## Best Practices

- Use generated content as a **starting point** for further research and validation
- Always **cross-reference** with authoritative medical sources (textbooks, guidelines, UpToDate)
- Have medical experts **review and validate** all generated information before distribution
- **Date-stamp** generated content and regularly update with current medical knowledge
- **Cite original sources** when using generated content in publications or educational materials
- Combine with **evidence-based databases** for comprehensive medical information
- Use for **educational purposes** and topic exploration, not clinical decision-making
- **Compare multiple sources** to identify and correct potential inaccuracies
- **Customize prompts** for specific medical domains or educational levels
- Keep **version history** to track changes in generated content over time
- Consider **human-in-the-loop** workflows where experts curate and refine LLM output
- Use for **ideation and structure** rather than definitive medical content

## Technical Details

### Temperature Setting
The model uses `temperature=0.7` to balance creativity and consistency in generating comprehensive topic information.

### Model Configuration
- Default model: `ollama/gemma3`
- Supports any LiteLLM-compatible model
- Configurable via command-line argument

### Logging
- Comprehensive logging with 5 verbosity levels (0-4)
- Logs saved to `medical_topic.log`
- Console output with rich formatting
- Debug mode includes full prompts and API interactions

### Input Validation
- Validates that topic is non-empty
- Handles errors gracefully with proper exit codes
- Provides clear error messages

### Output Management
- Auto-generates filenames based on topic name
- Creates output directories automatically
- Ensures proper JSON serialization with indentation
- Handles special characters in filenames

### Error Handling
- Validates inputs before processing
- Catches and logs exceptions
- Returns proper exit codes for automation
- Provides detailed error messages

## Related Files

- `medical_topic_models.py` - Comprehensive Pydantic models for structured medical topic information (17 distinct sections)
- `medical_topic_cli.py` - Command-line interface and generation logic

## Future Enhancements

Potential improvements for future versions:
- Integration with medical knowledge bases (PubMed, ClinicalTrials.gov)
- Citation generation with specific research references
- Multi-language support for international medical education
- Topic comparison and relationship mapping
- Visual diagram generation (pathophysiology flowcharts, treatment algorithms)
- Batch processing for multiple topics
- Customizable output templates
- Integration with medical terminology standards (SNOMED CT, ICD)
- Evidence level indicators for each section
- Automatic fact-checking against medical databases
- Version control and change tracking for topic updates
- Export to various formats (PDF, HTML, Markdown)
- Interactive web interface
- Collaboration features for expert review
- Integration with medical education platforms

## License

See parent project LICENSE file.
