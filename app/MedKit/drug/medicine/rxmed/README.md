# MedKit RxMed Tools

A comprehensive suite of Python tools for interacting with the National Library of Medicine's **RxNorm** and **RxClass** APIs. These tools provide capabilities for drug classification, therapeutic class hierarchy navigation, clinical relationship lookups (contraindications, interactions), and standardized drug identification.

## 📂 Components

This repository is structured into core libraries and CLI tools:

### Core Libraries
*   **`rxclass_client.py`**: The main library for interacting with the **RxClass API**. Use this for integrating drug classification features into your own applications.
*   **`rxnorm_client.py`**: The main library for the **RxNorm API**, handling drug name standardization and property retrieval.

### CLI Tools
*   **`rx_med_info_cli.py`**: A command-line interface wrapper for `rxclass_client.py`, enabling quick lookups and demos.
*   **`rxnorm_client_cli.py`**: A command-line interface for `rxnorm_client.py` to look up drug RxCUIs from the terminal.

### Examples
*   **`rxclass_examples.py`**: A demonstration script showcasing six real-world use cases, including finding disease treatments and checking for contraindications.

## 🚀 Features

*   **Drug Standardization**: Convert clinical drug names (e.g., "Tylenol") to standardized RxCUIs.
*   **Classification Lookup**: Find therapeutic categories (ATC, MEDRT, etc.) for any medication.
*   **Clinical Relationships**: Identify drug-disease contraindications, therapeutic uses, and mechanism of action.
*   **Hierarchy Navigation**: Explore the full tree of drug classifications (e.g., from "Analgesics" down to specific subclasses).
*   **Fuzzy Search**: Handle misspelled drug names with approximate matching.

## 🛠️ Installation

### Prerequisites

*   Python 3.7+
*   `requests` library
*   `rich` library (for formatted CLI output)

### Install Dependencies

```bash
pip install requests rich
```

## 📖 Usage

### 1. RxNorm Client

**CLI Usage (`rxnorm_client_cli.py`):**

```bash
# Look up a drug
python rxnorm_client_cli.py aspirin

# Look up with JSON output
python rxnorm_client_cli.py "metformin 500mg" --json-output
```

**Python Library Usage (`rxnorm_client.py`):**

```python
from rxnorm_client import RxNormClient

with RxNormClient() as client:
    # Get RxCUI
    rxcui = client.get_identifier("Lipitor")
    print(f"RxCUI: {rxcui}")
    
    # Get properties
    props = client.get_properties(rxcui)
    print(props)
```

### 2. RxClass Client

**CLI Usage (`rx_med_info_cli.py`):**

Runs a set of standard examples to demonstrate functionality:

```bash
python rx_med_info_cli.py
```

**Python Library Usage (`rxclass_client.py`):**

```python
from rxclass_client import RxClassClient

client = RxClassClient()

# Find classes for a drug
classes = client.get_class_by_drug_name("ibuprofen")

# Check for contraindications (using MEDRT source)
# Note: Requires traversing class members and relationships
members = client.get_class_members(class_id="N02", rela_source="ATC")
```

### 3. Examples & Use Cases (`rxclass_examples.py`)

Run this script to see comprehensive demonstrations of what the APIs can do. It covers 6 specific use cases:

1.  Drug Classification System
2.  Contraindication Checking
3.  Drug Hierarchy Navigation
4.  Disease Treatment Options
5.  Complete Drug Profile
6.  Drug Interaction Preparation

**Run Examples:**

```bash
python rxclass_examples.py
```

## 📚 API References

*   **RxNorm API**: [https://rxnav.nlm.nih.gov/APIs/RxNormAPIs.html](https://rxnav.nlm.nih.gov/APIs/RxNormAPIs.html)
*   **RxClass API**: [https://rxnav.nlm.nih.gov/APIs/RxClassAPIs.html](https://rxnav.nlm.nih.gov/APIs/RxClassAPIs.html)
