# LiteLLM

A unified command-line interface for accessing multiple language model providers through a single client. Supports text generation, image analysis, and specialized medical information tools.

## Why Use LiteLLM

### **Unified Access to Multiple AI Providers**
- Single interface for OpenAI, Anthropic, Google Gemini, Ollama, and other providers
- Switch between models without changing code or learning different APIs
- Consistent response format across all providers

### **Medical Information Tools (MedKit)**
- 19 specialized medical recognizers for disease, symptom, and drug identification
- Drug interaction checking and medical reference information
- Clinical decision support tools for healthcare professionals

### **Specialized Content Tools**
- Article analysis and improvement
- FAQ generation from existing content
- Educational content creation and tutoring systems
- Medical terminology extraction and validation

### **Cost and Performance Optimization**
- Local model support with Ollama (no API costs)
- Provider selection based on cost, speed, or capability requirements
- Structured output with Pydantic models for type-safe responses

## Quick Start

### **Basic Usage**
```bash
# Text generation
python app/cli/liteclient_cli.py -q "Explain machine learning concepts"

# Image analysis
python app/cli/liteclient_cli.py -i image.jpg -q "Describe this image"

# Model selection
python app/cli/liteclient_cli.py -q "Write Python code" -m "gpt-4"
```

### **Medical Tools**
```bash
# Disease identification
python app/MedKit/recognizers/disease/disease_identifier_cli.py "diabetes mellitus"

# Drug interaction check
python app/MedKit/drug/drug_drug/drug_drug_interaction_cli.py --drug1 "aspirin" --drug2 "warfarin"

# Medical symptom recognition
python app/MedKit/recognizers/medical_symptom/medical_symptom_cli.py "chest pain"
```

### **Content Tools**
```bash
# Article review
python app/cli/article_reviewer.py "your article text here"

# FAQ generation
python app/cli/faq_generator.py "your content text here"

# Educational tutoring
python app/cli/feymann_tutor.py "explain quantum computing"
```

## Installation

### **Standard Installation**
```bash
git clone <repository-url>
cd LiteLLM
pip install -r requirements.txt
pip install -e .
```

### **API Configuration**
```bash
# Optional: Configure API keys for cloud providers
export OPENAI_API_KEY="your-openai-key"
export GEMINI_API_KEY="your-gemini-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
```

### **Local Model Setup**
```bash
# Install Ollama for local model access
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama2
ollama pull gemma3
```

## Core Components

### **LiteClient Interface**
- Unified client for text and vision tasks
- Provider-agnostic API calls
- Structured output with validation
- Error handling and retry logic

### **MedKit Medical Tools**
- **Medical Recognizers** (19 modules): Disease, symptom, drug, and medical terminology identification
- **Drug Information**: Interactions, contraindications, and safety information
- **Clinical Tools**: Physical examination guides and decision support
- **Medical Reference**: Disease information, anatomy, and procedures

### **Content Processing Tools**
- Article analysis and improvement suggestions
- FAQ generation from source material
- Educational content creation
- Medical terminology extraction

### **Specialized Utilities**
- Data extraction and analysis tools
- Web interface through Streamlit
- Comprehensive testing framework
- Automation through Makefile commands

## Usage Examples

### **For General AI Tasks**
```bash
# Research and analysis
python app/cli/liteclient_cli.py -q "Summarize recent developments in renewable energy"

# Content creation
python app/cli/liteclient_cli.py -q "Write a technical blog post about cloud computing"

# Problem solving
python app/cli/liteclient_cli.py -q "Debug this Python code: [code]"
```

### **For Healthcare Applications**
```bash
# Clinical reference
python app/MedKit/medical/disease_info/disease_info_cli.py --disease "hypertension"

# Drug safety checks
python app/MedKit/drug/drug_disease/drug_disease_interaction_cli.py --drug "metformin" --disease "renal impairment"

# Medical education
python app/MedKit/recognizers/clinical_sign/clinical_sign_cli.py "babinski sign"
```

### **For Development and Integration**
```bash
# Code review and improvement
python app/cli/liteclient_cli.py -q "Review this Python code for security issues"

# Documentation generation
python app/cli/faq_generator.py "generate FAQ from technical documentation"

# Data analysis
python app/cli/liteclient_cli.py -q "Analyze this dataset and provide insights"
```

## Provider Support

### **Cloud Providers**
- OpenAI (GPT models)
- Anthropic (Claude models)
- Google (Gemini models)
- Other OpenAI-compatible providers

### **Local Models**
- Ollama integration
- Custom model endpoints
- Local deployment options

### **Model Selection**
```bash
# Specify provider and model
python app/cli/liteclient_cli.py -q "question" -m "openai/gpt-4"
python app/cli/liteclient_cli.py -q "question" -m "anthropic/claude-3"
python app/cli/liteclient_cli.py -q "question" -m "ollama/llama2"
```

## Output Formats

### **Structured Responses**
```json
{
  "response": "Generated text content",
  "provider": "openai",
  "model": "gpt-4",
  "tokens_used": 150,
  "response_time": 2.3
}
```

### **Medical Recognition Results**
```json
{
  "identification": {
    "term": "diabetes mellitus",
    "is_recognized": true,
    "confidence": "high",
    "category": "disease"
  },
  "data_available": true
}
```

## Development and Testing

### **Run Tests**
```bash
make test
```

### **Web Interface**
```bash
make run-web
```

### **Development Setup**
```bash
make dev
```

## Architecture

### **Core Components**
- `lite/lite_client.py` - Unified client interface
- `lite/config.py` - Configuration and model management
- `app/cli/` - Command-line tools and interfaces
- `app/MedKit/` - Medical information tools
- `app/web/` - Web interface components

### **Data Models**
- Pydantic models for structured output
- Type-safe response validation
- Consistent data formats across providers

## Limitations and Considerations

### **Medical Tools**
- Medical information is for reference and educational purposes
- Not intended for clinical diagnosis or treatment decisions
- Always verify critical medical information with authoritative sources
- Consult qualified healthcare professionals for medical decisions

### **AI Model Limitations**
- Responses may contain inaccuracies or hallucinations
- Model capabilities vary between providers
- API rate limits and costs apply to cloud providers
- Local models require sufficient computational resources

### **Usage Guidelines**
- Verify important information through primary sources
- Use appropriate models for specific tasks
- Consider cost and performance requirements
- Follow provider terms of service and usage policies

## Support and Documentation

### **Additional Documentation**
- `app/MedKit/README.md` - Medical tools documentation
- Module-specific README files in respective directories
- Contract files for legal and ethical usage terms

### **Technical Support**
- Check requirements.txt for dependency information
- Verify Python version compatibility (3.8+)
- Test with basic commands before complex usage
- Review API key configuration for cloud providers

### **Contributing**
- Follow development guidelines in CONTRIBUTING.md
- Run tests before submitting changes
- Maintain documentation consistency
- Respect medical AI safety and ethical guidelines

**Using standard venv:**
```bash
make venv
source litenv/bin/activate
```

3. Install dependencies:

**Using uv:**
```bash
uv pip install -r requirements.txt
uv pip install -e .
```

**Using make/pip:**
```bash
make install
```

4. Set up your API keys in a `.env` file or as environment variables:
```bash
export OPENAI_API_KEY="your-openai-key"
export GEMINI_API_KEY="your-gemini-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
```

For Ollama models, ensure Ollama is running locally.

## Project Structure

```
LiteLLM/
├── lite/                        # Core library package
│   ├── config.py                # Model configuration & input validation
│   ├── lite_client.py           # Unified client for text/vision operations
│   ├── image_utils.py           # Image processing and encoding
│   └── logging_config.py        # Centralized logging
├── app/                         # Applications layer
│   ├── cli/                     # Specialized command-line interfaces
│   │   ├── liteclient_cli.py    # Main unified CLI
│   │   ├── article_reviewer.py  # AI-powered article review
│   │   ├── faq_generator.py     # FAQ generation tool
│   │   ├── feymann_tutor.py     # Feynman technique tutor
│   │   └── ... (many other specialized tools)
│   ├── MedKit/                  # Comprehensive Medical Toolkit
│   │   ├── recognizers/         # 19 medical recognizer modules
│   │   │   ├── disease/         # Disease identification
│   │   │   ├── medical_symptom/ # Medical symptom identification
│   │   │   ├── clinical_sign/   # Clinical sign identification
│   │   │   ├── lab_unit/        # Laboratory unit identification
│   │   │   ├── medical_test/     # Medical test identification
│   │   │   ├── medical_specialty/ # Medical specialty identification
│   │   │   ├── medication_class/ # Medication class identification
│   │   │   ├── medical_device/   # Medical device identification
│   │   │   ├── medical_procedure/ # Medical procedure identification
│   │   │   ├── medical_vaccine/  # Medical vaccine identification
│   │   │   ├── medical_condition/ # Medical condition identification
│   │   │   ├── medical_coding/   # Medical coding identification
│   │   │   ├── medical_abbreviation/ # Medical abbreviation identification
│   │   │   ├── imaging_finding/  # Imaging finding identification
│   │   │   ├── genetic_variant/  # Genetic variant identification
│   │   │   ├── medical_pathogen/ # Medical pathogen identification
│   │   │   ├── medical_supplement/ # Medical supplement identification
│   │   │   └── medical_anatomy/  # Medical anatomy identification
│   │   ├── drug/                # Drug information and interactions
│   │   ├── medical/             # Disease info, anatomy, procedures
│   │   ├── phyexams/            # 26+ Physical examination modules
│   │   ├── mental_health/       # Mental health assessment & reporting
│   │   └── diagnostics/         # Medical devices and tests
│   └── web/                     # Web applications
│       └── streamlit_liteclient.py # Interactive web UI
├── utilities/                   # Search and experimental utilities
├── tests/                       # Comprehensive test suite
├── Makefile                     # Automation for setup, testing, and execution
└── requirements.txt             # Project dependencies
```

## Usage

### Unified CLI

The main CLI tool handles both text queries and vision analysis:

```bash
# Text query
python app/cli/liteclient_cli.py -q "Explain the benefits of modular software design"

# Vision analysis
python app/cli/liteclient_cli.py -i path/to/image.jpg -q "What is shown in this image?"

# Custom model and temperature
python app/cli/liteclient_cli.py -q "Write a poem about AI" -m "gpt-4" -t 0.8
```

#### Arguments:
- `-q, --question`: Input prompt (required for text mode, optional for vision).
- `-i, --image`: Path or URL to an image file (enables vision mode).
- `-m, --model`: Model identifier (e.g., `ollama/gemma3`, `gpt-4o`, `gemini/gemini-2.0-flash`).
- `-t, --temperature`: Sampling temperature (0.0 to 2.0).
- `-o, --output`: Optional file path to save the response.

### MedKit

MedKit provides specialized medical information tools with 19 recognizer modules for quick medical terminology identification:

#### Medical Recognizers

The recognizers module contains 19 specialized tools for identifying medical terminology:

```bash
# Disease identification
python app/MedKit/recognizers/disease/disease_identifier_cli.py "diabetes mellitus"

# Medical symptom identification  
python app/MedKit/recognizers/medical_symptom/medical_symptom_cli.py "chest pain"

# Clinical sign identification
python app/MedKit/recognizers/clinical_sign/clinical_sign_cli.py "Babinski sign"

# Laboratory unit identification
python app/MedKit/recognizers/lab_unit/lab_unit_cli.py "mg/dL"

# Medical test identification
python app/MedKit/recognizers/medical_test/medical_test_cli.py "CBC"

# Genetic variant identification
python app/MedKit/recognizers/genetic_variant/genetic_variant_cli.py "BRCA1 mutation"

# Imaging finding identification
python app/MedKit/recognizers/imaging_finding/imaging_finding_cli.py "pulmonary nodule"

# Medical pathogen identification
python app/MedKit/recognizers/medical_pathogen/medical_pathogen_cli.py "Staphylococcus aureus"

# And 11 more specialized recognizers...
```

All recognizers support:
- `--model`: Model selection (default: ollama/gemma3)
- `--temperature`: Temperature control (default: 0.2)

#### Traditional MedKit Modules

```bash
# Get disease information
python app/MedKit/medical/disease_info/disease_info_cli.py --disease "Diabetes"

# Check drug information
python app/MedKit/drug/medicine/medicine_cli.py -i "Aspirin"

# Run a physical exam module
python app/MedKit/phyexams/exam_depression_screening.py
```

See [app/MedKit/README.md](app/MedKit/README.md) for more details.

### Streamlit Web UI

Launch the interactive web interface:

```bash
make run-web
```

## Architecture

### LiteClient (`lite/lite_client.py`)
The core `LiteClient` provides a unified interface for all model interactions. It abstracts the complexities of different providers and handles message formatting for both text and multimodal (vision) inputs.

### Structured Output
The library leverages Pydantic for structured data extraction. By passing a Pydantic model to `generate_text`, you can ensure the LLM response is validated and parsed into a Python object.

## Testing

Run the full test suite using the Makefile:
```bash
make test
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.