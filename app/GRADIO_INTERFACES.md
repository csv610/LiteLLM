# Gradio Interfaces for LiteLLM Applications

This document describes the Gradio-based web interfaces created for various applications in the LiteLLM project.

## Overview

Each application in the LiteLLM suite now has both a CLI (Command Line Interface) and a Gradio-based web interface. 

**Key Difference:**
- **CLI interfaces**: Save output to the `outputs` folder
- **Gradio interfaces**: Display results in the browser only (no file saving)

This distinction was implemented per your requirements.

## Created Interfaces

### 1. ArticleReviewer
- **File**: `app/ArticleReviewer/agentic/article_reviewer_gradio.py`
- **Port**: 7860
- **Description**: Multi-stage article review workflow using AI agents

### 2. DeepDeliberation
- **File**: `app/DeepDeliberation/agentic/deep_deliberation_gradio.py`
- **Port**: 7861
- **Description**: Knowledge discovery engine with iterative probing rounds

### 3. DeepIntuition
- **File**: `app/DeepIntuition/agentic/deep_intuition_gradio.py`
- **Port**: 7862
- **Description**: Intuitive problem-solving approach exploring problems from multiple angles

### 4. DigiTeacher Suite
#### FeynmanTutor
- **File**: `app/DigiTeacher/FeynmanTutor/feynman_tutor_gradio.py`
- **Port**: 7863
- **Description**: Learn by teaching using the Feynman technique

#### HadamardTutor
- **File**: `app/DigiTeacher/HadamardTutor/hadamard_tutor_gradio.py`
- **Port**: 7864
- **Description**: Discovery through Preparation, Incubation, Illumination, and Verification phases

#### SocratesTutor
- **File**: `app/DigiTeacher/SocratesTutor/socrates_tutor_gradio.py`
- **Port**: 7865
- **Description**: Discover truth through Socratic dialogue and questioning

### 5. GenerateBook
- **File**: `app/GenerateBook/agentic/bookchapters_gradio.py`
- **Port**: 7866
- **Description**: Educational curriculum chapter generation across education levels

### 6. MedKit Suite
#### MedKit Diagnose
- **File**: `app/MedKit/medkit_diagnose/diagnose_gradio.py`
- **Port**: 7867
- **Description**: Medical information retrieval and image classification (tests, devices, images)

#### MedKit Article
- **File**: `app/MedKit/medkit_article/article_gradio.py`
- **Port**: 7868
- **Description**: Medical article search, review, summarization, comparison, and keyword extraction

#### Primary Health Care Advisor
- **File**: `app/MedKit/medical/med_advise/agentic/primary_health_care_gradio.py`
- **Port**: 7869
- **Description**: Preliminary health information and advice for common health concerns

#### Medical Symptom Checker
- **File**: `app/MedKit/medical/med_symptom_checker/symptom_detection_gradio.py`
- **Port**: 7870
- **Description**: AI-powered structured medical consultation system using decision tree reasoning

## How to Launch

Each Gradio interface can be launched independently:

```bash
python /path/to/interface_file.py
```

For example:
```bash
python app/ArticleReviewer/agentic/article_reviewer_gradio.py
```

The application will be accessible at `http://localhost:7860` (or the respective port for each application).

## Output Handling

### CLI Applications
- Save all output to the `outputs` directory
- Follow existing CLI patterns for file naming and storage

### Gradio Applications
- Display results in the browser only
- No files are saved to disk
- Results are presented in formatted markdown/HTML in the web interface
- Follows your requirement: "For gradio, it must be in the browser"

## Features

All Gradio interfaces include:
- Clean, intuitive web interface
- Input validation and error handling
- Configurable model selection (Ollama, OpenAI, Claude options)
- Proper layout with input/output sections
- Help documentation about each application's purpose
- Logging configuration matching CLI patterns
- Responsive design that works on various screen sizes

## Dependencies

The Gradio interfaces require the `gradio` package, which can be installed with:

```bash
pip install gradio
```

All other dependencies are inherited from the existing LiteLLM project requirements.

## Notes

- The original CLI interfaces remain unchanged and fully functional (saving to outputs folder)
- Gradio interfaces connect to the same backend logic as the CLI versions but display results only in browser
- Each interface runs on a different port to avoid conflicts
- Interfaces can be run simultaneously without interference
- For production deployment, consider using a process manager or container orchestration