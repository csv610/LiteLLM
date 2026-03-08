# MedKit Medicine Reference & Information

A collection of modules for retrieving and analyzing comprehensive pharmaceutical data, including standardized naming, classification, and detailed medication profiles.

## Overview

The `medicine` package serves as the foundational data layer for the MedKit drug suite. It integrates multiple authoritative sources—including DrugBank, RxNorm, and RxClass—to provide normalized, high-fidelity information about medications, their therapeutic roles, and their pharmacological properties.

## Included Sub-Modules

| Module | Description |
| :--- | :--- |
| **`drugbank`** | Detailed pharmaceutical profiles and biochemical data integration. |
| **`medinfo`** | AI-powered generation of comprehensive clinical drug profiles. |
| **`rxmed`** | Integration with NLM's RxNorm and RxClass for standardized naming and categorization. |

## Key Features

- **Data Normalization:** Ensures consistent drug identification across the entire MedKit ecosystem.
- **Multi-Source Integration:** Combines LLM-powered analysis with authoritative structured medical databases.
- **Therapeutic Triage:** Provides deep insights into drug classifications and indications.
- **Clinically Grounded:** Focuses on evidence-based pharmacological data for professional use.

## Project Structure

- `contract.md`: Legal and ethical framework for using the medicine reference tools.
- `drugbank/`: Specialized module for DrugBank data.
- `medinfo/`: General medication information generator.
- `rxmed/`: Standardized naming and classification integration.

## ⚠️ Important Medical Disclaimer

**THE DATA PROVIDED BY THESE MODULES IS FOR INFORMATIONAL AND EDUCATIONAL PURPOSES ONLY.**

- **Verification Required:** Always cross-reference AI-generated and database-derived information with current FDA labels and professional medical references (e.g., Lexicomp, Micromedex).
- **Professional Consultation:** This module is not a substitute for clinical judgment or professional medical consultation.
