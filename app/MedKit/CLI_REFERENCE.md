# MedKit CLI Reference

This document provides a comprehensive guide to all CLI tools and subcommands available in the MedKit framework.

---

## 🤖 `medkit-agent`
**Autonomous Medical Reasoning Agent**

The orchestrator agent uses a ReAct (Reasoning and Acting) loop to solve complex clinical queries by dynamically selecting and chaining other MedKit tools.

*   **Usage:** `medkit-agent "<query>"`
*   **Key Arguments:**
    *   `-m, --model`: LLM model (default: `ollama/gemma3`).
    *   `-t, --temperature`: Creativity control (0.0 to 1.0).
*   **Example:**
    ```bash
    medkit-agent "Patient is a 65yo female with sudden onset of left-sided weakness. What are the priority diagnostic steps and potential specialist referrals?"
    ```

---

## 🏥 `medkit-medical`
**General Medical Knowledge & Clinical Tools**

Access a massive database of anatomical, pathological, and clinical reference data.

### Subcommands

#### `advise`
Primary health care guidance for common concerns.
*   **Example:** `medkit-medical advise "Managing mild fever at home"`

#### `anatomy`
Detailed anatomical information including classification, position, and function.
*   **Example:** `medkit-medical anatomy "Liver"`

#### `case`
Generates synthetic medical case reports for clinical training and simulation.
*   **Example:** `medkit-medical case "Type 2 Diabetes"`

#### `decision`
Clinical decision-making guides based on presenting symptoms.
*   **Example:** `medkit-medical decision "Acute Cough"`

#### `disease`
Comprehensive profiles of diseases including causes, symptoms, and treatments.
*   **Example:** `medkit-medical disease "Hypertension"`

#### `ethics`
Professional medical ethics analysis for complex scenarios or dilemmas.
*   **Example:** `medkit-medical ethics "Patient confidentiality vs public safety"`

#### `facts`
Fact-check medical statements against evidence-based clinical knowledge.
*   **Example:** `medkit-medical facts "Vaccines cause autism"`

#### `faq`
Generates common patient questions and professional answers for a given topic.
*   **Example:** `medkit-medical faq "Asthma"`

#### `flashcard`
Explains medical terms or labels. If an image path is provided, it extracts labels first.
*   **Example:** `medkit-medical flashcard "label_image.jpg"`

#### `herbal`
Evidence-based information on medicinal herbs and natural remedies.
*   **Example:** `medkit-medical herbal "Turmeric"`

#### `history`
Generates standardized patient intake and medical history questions.
*   **Example:** `medkit-medical history -e "Physical" -a 45 -g "Male"`

#### `implant`
Information on medical devices, implants, and surgical hardware.
*   **Example:** `medkit-medical implant "Pacemaker"`

#### `myth`
Debunks common medical myths and misconceptions with scientific evidence.
*   **Example:** `medkit-medical myth "We use 10% of our brain"`

#### `organ`
Organ-specific disease profiles and physiological summaries.
*   **Example:** `medkit-medical organ "Pancreas"`

#### `pose`
Guidance on surgical patient positioning for specific procedures.
*   **Example:** `medkit-medical pose "Prone"`

#### `procedure`
Step-by-step breakdown of medical and diagnostic procedures.
*   **Example:** `medkit-medical procedure "Knee Replacement"`

#### `quiz`
Generates medical test questions for students and professionals.
*   **Example:** `medkit-medical quiz "Cardiology"`

#### `refer`
Identifies the appropriate specialists for a given set of symptoms or conditions.
*   **Example:** `medkit-medical refer "Chest pain and dyspnea"`

#### `roles`
Detailed responsibilities and scope of practice for medical specialties.
*   **Example:** `medkit-medical roles "Neurosurgeon"`

#### `surgery`
Comprehensive information on surgical techniques, risks, and recovery.
*   **Example:** `medkit-medical surgery "Appendectomy"`

#### `tool`
Descriptions and usage of surgical instruments and medical tools.
*   **Example:** `medkit-medical tool "Scalpel"`

#### `tray`
Standardized surgical tray setup instructions for various operations.
*   **Example:** `medkit-medical tray "Orthopedic"`

---

## 💊 `medkit-drug`
**Pharmacology, Interactions & Safety**

Tools for pharmaceutical research and medication safety analysis.

### Subcommands

#### `addiction`
Detailed info on drug addiction, withdrawal symptoms, and recovery resources.
*   **Example:** `medkit-drug addiction "Oxycodone"`

#### `compare`
Side-by-side comparison of two medications (efficacy, side effects, etc.).
*   **Example:** `medkit-drug compare "Tylenol" "Advil"`

#### `disease`
Checks for contraindications and precautions between a drug and a disease.
*   **Example:** `medkit-drug disease "Ibuprofen" "Kidney Disease"`

#### `explain`
Provides a simple, patient-friendly explanation of a medication.
*   **Example:** `medkit-drug explain "Amoxicillin"`

#### `food`
Identifies potential interactions between medications and specific foods.
*   **Example:** `medkit-drug food "Metformin" "Grapefruit"`

#### `info`
Comprehensive drug monographs including mechanism, dosage, and side effects.
*   **Example:** `medkit-drug info "Lisinopril"`

#### `interact`
Detailed drug-drug interaction analysis between two or more medications.
*   **Example:** `medkit-drug interact "Warfarin" "Aspirin"`

#### `similar`
Finds therapeutic alternatives or similar medications within the same class.
*   **Example:** `medkit-drug similar "Ozempic"`

#### `symptoms`
Reference tool to find common medications used to treat specific symptoms.
*   **Example:** `medkit-drug symptoms "Migraine with aura"`

---

## 📊 `medkit-graph`
**Medical Knowledge Graph Extraction**

Extract structured knowledge triples (Entity-Relation-Entity) and visualize them as interactive graphs.

### Subcommands
*   `anatomy`: Extract anatomical relationships.
*   `disease`: Extract disease-symptom-treatment links.
*   `genetic`: Extract genetic & genomic relations.
*   `medicine`: Extract pharmaceutical knowledge.
*   `pathophysiology`: Extract physiological mechanisms.
*   `pharmacology`: Extract drug mechanisms of action.
*   `procedure`: Extract surgical/clinical steps.
*   `surgery`: Extract surgical anatomy/tools.
*   `symptoms`: Extract symptom-disease mappings.
*   `test`: Extract diagnostic test logic.

*   **Example:** `medkit-graph disease "Diabetes is a chronic condition..."`

---

## 🔍 `medkit-recognizer`
**Medical Entity Recognition (NER)**

Extract and normalize structured data from unstructured clinical text.

### Subcommands
*   `abbreviation`: Resolve medical abbreviations (e.g., "COPD").
*   `anatomy`: Identify anatomical structures.
*   `clinical_sign`: Identify clinical signs (e.g., "Babinski").
*   `coding`: Extract medical codes (ICD, CPT).
*   `condition`: Identify general medical conditions.
*   `device`: Identify medical devices and hardware.
*   `disease`: Specific disease identification.
*   `drug`: Pharmaceutical identification.
*   `genetic`: Genetic variants and markers.
*   `imaging`: Imaging findings (Radiology).
*   `lab_unit`: Standardize laboratory units.
*   `med_class`: Identify medication classes.
*   `pathogen`: Identify bacteria, viruses, fungi.
*   `procedure`: Identify medical procedures.
*   `specialty`: Identify medical specialties.
*   `supplement`: Identify dietary supplements.
*   `symptom`: Identify medical symptoms.
*   `test`: Identify laboratory/diagnostic tests.
*   `vaccine`: Identify vaccines and biologics.

*   **Example:** `medkit-recognizer drug "Patient is taking 10mg of Lisinopril daily."`

---

## 📸 `medkit-media`
**Medical Image/Video Search & Analysis**

### Subcommands

#### `caption`
Generates clinical captions for medical images or scans.
*   **Example:** `medkit-media caption "Rheumatoid hand x-ray"`

#### `images`
Searches and downloads medical images from DuckDuckGo.
*   **Example:** `medkit-media images "Psoriasis plaques"`

#### `summary`
Summarizes educational medical videos or long-form medical content.
*   **Example:** `medkit-media summary "Laparoscopic cholecystectomy"`

#### `videos`
Searches for medical educational videos.
*   **Example:** `medkit-media videos "CPR technique"`

---

## 🧪 `medkit-diagnostics`
**Medical Tests & Devices**

### Subcommands
#### `test`
Reference information for laboratory tests, including normal ranges and indications.
*   **Example:** `medkit-diagnostics test "HbA1c"`

#### `device`
Technical and clinical information about diagnostic medical devices.
*   **Example:** `medkit-diagnostics device "MRI Scanner"`

---

## 📄 `medkit-article`
**PubMed & Article Search**

### Subcommands
#### `search`
Search for professional medical articles and PubMed records by disease.
*   **Example:** `medkit-article search "Gout"`

#### `cite`
Retrieve formatted citations for medical articles.
*   **Example:** `medkit-article cite "Diabetes"`

---

## 🛡️ `medkit-privacy`
**HIPAA Compliance & Data Protection**

### Subcommands
#### `audit`
Logs compliance and data access events for audit trailing.
*   **Example:** `medkit-privacy audit --session "ID" --action "Login"`

#### `consent`
Displays and captures HIPAA-compliant informed consent.
*   **Example:** `medkit-privacy consent`

#### `mask`
Scrubs Personally Identifiable Information (PII) from clinical text.
*   **Example:** `medkit-privacy mask "Patient John Doe at 555-0199"`

#### `report`
Generates HIPAA compliance metrics and reports.
*   **Example:** `medkit-privacy report`

---

## 🧠 `medkit-mental`
**Mental Health Assessment**

Interactive assessment tool for psychological and mental health screening.
*   **Usage:** `medkit-mental` (Starts interactive session)

---

## ⚖️ `medkit-sane`
**SANE Interview Protocol**

Specialized forensic interview protocols for Sexual Assault Nurse Examiners.
*   **Usage:** `medkit-sane start`

---

## 📖 `medkit-dictionary`
**Medical Terminology Builder**

Builds and manages a custom structured medical dictionary.
*   **Usage:** `medkit-dictionary build`

---

## 📋 `medkit-exam`
**Physical Examination Protocols**

Reference for standardized physical examination protocols across multiple domains.
*   **Usage:** `medkit-exam --list`
