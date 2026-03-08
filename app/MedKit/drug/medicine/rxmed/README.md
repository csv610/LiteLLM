# RxMed Standardized Drug Data Integration

A specialized integration module for accessing and utilizing RxNorm and RxClass data within the MedKit ecosystem.

## Overview

The **RxMed Integration Module** provides standardized access to the National Library of Medicine's RxNorm and RxClass datasets. It ensures medication names, classes, and therapeutic categories are normalized across all MedKit modules, facilitating clinical accuracy and interoperability.

## Key Features

- **Standardized Naming (RxNorm):** Normalizes drug names and codes for consistent cross-module identification.
- **Therapeutic Classification (RxClass):** Maps medications to their respective therapeutic and pharmacological classes.
- **Data Clients:** Robust API clients for interacting with RxNorm and RxClass web services.
- **Reference Examples:** Includes practical scripts (`rxclass_examples.py`) for common classification workflows.
- **CLI Utilities:** Feature-rich command-line tools for manual RxNorm/RxClass queries.

## Project Structure

- `rxnorm_client.py`: Core client for the RxNorm API.
- `rxclass_client.py`: Core client for the RxClass API.
- `rxmed_info_cli.py`: Integrated CLI for RxMed queries.
- `rxnorm_client_cli.py`: Specialized CLI for direct RxNorm interaction.
- `rxclass_examples.py`: Usage examples for therapeutic classification.

## Installation

Ensure dependencies are installed:

```bash
pip install requests
```

## Usage

### Command Line Interface

Query RxNorm for a medicine's standardized information:

```bash
python rxmed_info_cli.py "Aspirin"
```

## ⚠️ Data Accuracy and Licensing

- **External Source Reliance:** This module depends on live API data from the NLM. Availability and accuracy are subject to the source provider's updates.
- **Licensing:** Usage must comply with the National Library of Medicine's (NLM) terms of service for RxNorm and related datasets.
- **Clinical Verification:** Standardized names and classes are for reference and should be cross-verified for critical clinical applications.
