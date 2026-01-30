# Medical Quiz Generator 🏥

A powerful CLI tool for generating comprehensive, board-style medical quizzes using AI models. This tool leverages advanced prompting techniques and structured data models to produce high-quality medical quiz questions that test clinical reasoning and practical application.

## ✨ Features

- 🧠 **Board-Style Questions**: Generates questions adhering to USMLE, MCCQE, and PLAB/UKMLA standards
- 🎯 **Clinical Vignettes**: Every question starts with realistic patient presentations
- 🔄 **Unique & Diverse**: Ensures questions are unique and cover diverse clinical scenarios
- ⚙️ **Highly Customizable**: Adjustable difficulty, question count, and options
- 📊 **Structured Output**: JSON format with Pydantic models or plain Markdown
- 🚀 **Progress Indicators**: Visual feedback for large quiz generation
- 🔒 **Input Validation**: Robust validation prevents invalid inputs
- 📝 **Smart Sanitization**: Safe filename generation for all operating systems

## 🚀 Quick Start

### Installation

Ensure you have Python 3.8+ installed and are in the MedKit project directory:

```bash
cd path/to/MedKit/medical/med_quiz
```

### Basic Usage

Generate a simple quiz:
```bash
python medical_quiz_cli.py -i "diabetes"
```

### Advanced Usage

Generate a comprehensive quiz with custom settings:
```bash
python medical_quiz_cli.py -i "cardiology" -df Hard -nq 10 -no 5 -s -d "quizzes/cardiology"
```

## 📋 Command Line Arguments

| Argument | Short | Long | Description | Default |
|----------|-------|------|-------------|---------|
| **Topic** | `-i` | `--topic` | **Required.** Medical topic for quiz generation | N/A |
| **Output Dir** | `-d` | `--output-dir` | Directory for output files | `outputs` |
| **Model** | `-m` | `--model` | AI model to use | `ollama/gemma3` |
| **Verbosity** | `-v` | `--verbosity` | Logging level (0-4) | `2` (WARNING) |
| **Structured** | `-s` | `--structured` | Use structured JSON output | `False` |
| **Difficulty** | `-df` | `--difficulty` | Quiz difficulty level | `Intermediate` |
| **Questions** | `-nq` | `--num-questions` | Number of questions to generate | `5` |
| **Options** | `-no` | `--num-options` | Number of options per question | `4` |

## 🎯 Usage Examples

### Basic Quiz Generation
```bash
# Simple diabetes quiz
python medical_quiz_cli.py -i diabetes

# Heart disease quiz with custom difficulty
python medical_quiz_cli.py -i "heart disease" -df Easy

# Large quiz with progress indicator
python medical_quiz_cli.py -i neurology -nq 15 -s
```

### Advanced Customization
```bash
# Comprehensive cardiology quiz
python medical_quiz_cli.py \
  -i "cardiology" \
  -df Hard \
  -nq 20 \
  -no 5 \
  -s \
  -d "medical_quizzes" \
  -m "ollama/llama3" \
  -v 3
```

### Batch Processing (Scripting)
```bash
#!/bin/bash
topics=("diabetes" "hypertension" "asthma" "copd")

for topic in "${topics[@]}"; do
  echo "Generating quiz for: $topic"
  python medical_quiz_cli.py -i "$topic" -df Intermediate -nq 5 -s -d "batch_quizzes"
done
```

## 📁 Project Structure

```
med_quiz/
├── medical_quiz_cli.py           # CLI interface and argument parsing
├── medical_quiz.py               # Core quiz generation logic
├── medical_quiz_models.py         # Pydantic data models
├── medical_quiz_prompts.py        # System and user prompts
├── README.md                     # This documentation
└── logs/                         # Application logs
```

## 📊 Output Formats

### Structured JSON Output
```json
{
  "topic": "Diabetes Mellitus",
  "difficulty": "Intermediate",
  "questions": [
    {
      "id": 1,
      "question": "A 45-year-old patient presents with polyuria, polydipsia, and weight loss...",
      "options": {
        "A": "Type 1 Diabetes Mellitus",
        "B": "Type 2 Diabetes Mellitus",
        "C": "Diabetes Insipidus",
        "D": "Hyperthyroidism"
      },
      "answer": "B",
      "explanation": "The clinical presentation is most consistent with Type 2 Diabetes..."
    }
  ]
}
```

### Plain Text Output
```markdown
# Medical Quiz: Diabetes Mellitus
Difficulty: Intermediate

## Question 1
A 45-year-old patient presents with polyuria, polydipsia, and weight loss...

**Options:**
A) Type 1 Diabetes Mellitus
B) Type 2 Diabetes Mellitus
C) Diabetes Insipidus
D) Hyperthyroidism

**Answer:** B

**Explanation:** The clinical presentation is most consistent with Type 2 Diabetes...
```

## 🏥 Question Quality Standards

### Clinical Vignette Requirements
- Every question starts with a realistic patient presentation
- Includes relevant history, physical findings, and laboratory data
- Tests clinical reasoning rather than rote memorization

### Uniqueness & Diversity
- **Patient Demographics**: Varied age, gender, ethnicity, and background
- **Clinical Settings**: Emergency, primary care, specialty, and community care
- **Disease Stages**: Acute, chronic, preventive, and follow-up scenarios
- **Cognitive Skills**: Diagnosis, management, prognosis, and prevention

### Board Exam Standards
- **USMLE (USA)**: United States Medical Licensing Examination
- **MCCQE (Canada)**: Medical Council of Canada Qualifying Examination
- **PLAB/UKMLA (UK)**: Professional and Linguistic Assessments Board

## 🔧 Configuration

### Supported Models
- `ollama/gemma3` (default)
- `ollama/llama3`
- `ollama/mistral`
- `anthropic/claude-3-5-sonnet`
- Any model supported by LiteClient

### Logging Levels
- `0`: CRITICAL only
- `1`: ERROR and above
- `2`: WARNING and above (default)
- `3`: INFO and above
- `4`: DEBUG and above

## 🛡️ Safety & Validation

### Input Validation
- Topic cannot be empty
- Questions must be ≥ 1 and ≤ 100
- Options must be ≥ 2 and ≤ 26 (A-Z)
- Difficulty level must be specified

### Security Features
- Filename sanitization prevents path traversal
- Input validation prevents injection attacks
- Cross-platform compatible file generation

## 📝 Examples

### Example 1: Diabetes Quiz
```bash
python medical_quiz_cli.py -i diabetes -df Intermediate -nq 5 -s
```
**Output**: `diabetes_quiz.json` with 5 diverse questions covering diagnosis, management, complications, and prevention.

### Example 2: Emergency Medicine Quiz
```bash
python medical_quiz_cli.py -i "emergency medicine" -df Hard -nq 10 -no 4 -v 3
```
**Output**: `emergency_medicine_quiz.json` with 10 challenging emergency scenarios.

### Example 3: Pediatric Quiz
```bash
python medical_quiz_cli.py -i pediatrics -df Easy -nq 8 -no 3 -d "teaching_materials"
```
**Output**: `teaching_materials/pediatrics_quiz.json` with 8 beginner-friendly pediatric questions.

## 🔄 Error Handling

The tool provides comprehensive error handling with clear error messages:

```bash
# Invalid inputs
$ python medical_quiz_cli.py -i "" -nq 0
ValueError: Topic cannot be empty
ValueError: Number of questions must be >= 1

# Progress tracking
Generating 15 quiz questions: |██████████████████████████████████████████████████| 100.0% (15/15) ETA: 0.0s
```

## 🤝 Contributing

This tool is part of the MedKit suite. To contribute:

1. Follow the established code patterns
2. Add comprehensive tests for new features
3. Update documentation for any API changes
4. Ensure all prompts maintain medical accuracy

## 📄 License

This project is part of the MedKit medical toolkit suite.

## 🆘 Support

For issues or questions:
1. Check the logs in the `logs/` directory
2. Run with verbosity `-v 4` for detailed debugging
3. Ensure your model is properly configured in LiteClient

---

**Generated by Medical Quiz Generator v1.0**  
*Empowering medical education through AI-powered quiz generation* 🏥📚
