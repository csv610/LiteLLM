# Examples

This directory contains complete, runnable Python scripts demonstrating how to use LiteKit for various tasks.

## Getting Started

Make sure you have installed the package first:

```bash
pip install -e ..
```

## Available Examples

### 1. Basic Text & Vision (`01_basic_usage.py`)
Learn the basics of creating a `LiteClient` and generating completions for both text prompts and images.
- Uses: `LiteClient`, `ModelInput`
- Demonstrates: Simple text generation, image analysis.

### 2. Structured Data Extraction (`02_structured_data.py`)
Shows how to force the LLM to return structured JSON data that adheres to a Pydantic schema.
- Uses: `Pydantic`, `response_format`
- Demonstrates: Extracting ingredients from a recipe text.

### 3. Multiple-Choice Solver (`03_mcq_solver.py`)
A specialized example for solving multiple-choice questions (MCQs) with reasoning.
- Uses: `LiteMCQClient`, `MCQInput`
- Demonstrates: Providing options and getting a structured answer with reasoning.

### 4. LLM-as-a-Judge (`04_llm_judge.py`)
Evaluate the quality of an LLM's response against a ground truth answer using another LLM as a judge.
- Uses: `ResponseJudge`, `UserInput`
- Demonstrates: Scoring accuracy, completeness, and relevance.

## Running an Example

 simply run the script with python:

```bash
python 01_basic_usage.py
```
