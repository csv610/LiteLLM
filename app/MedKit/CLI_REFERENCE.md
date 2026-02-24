# MedKit CLI Reference

This document provides a comprehensive guide to all CLI tools and subcommands available in the MedKit framework, including their primary usage, limitations, and failure modes.

---

## 🤖 `medkit-agent`
**Autonomous Medical Reasoning Agent**

The orchestrator agent uses a ReAct (Reasoning and Acting) loop to solve complex clinical queries by dynamically selecting and chaining other MedKit tools.

*   **Primary Usage:** Solving multi-step clinical queries that require multiple data points (e.g., "Check interactions and find specialist").
*   **Key Arguments:**
    *   `-m, --model`: LLM model (default: `ollama/gemma3`).
    *   `-t, --temperature`: Creativity control (0.0 to 1.0).
*   **Does NOT:** Guarantee the accuracy of medical facts; it only orchestrates the tools it has access to. It does not possess a "medical license" or intuition.
*   **Edge Cases:**
    *   **Tool Loop:** If the LLM gets stuck, it might call the same tool repeatedly.
    *   **Context Exhaustion:** Very complex queries can exceed the LLM's memory, leading it to forget the original goal.
*   **Example:**
    ```bash
    medkit-agent "Patient is a 65yo female with sudden onset of left-sided weakness. What are the priority diagnostic steps and potential specialist referrals?"
    ```

---

## 🏥 `medkit-medical`
**General Medical Knowledge & Clinical Tools**

Access a massive database of anatomical, pathological, and clinical reference data.

*   **Primary Usage:** Rapid reference for anatomical facts, disease profiles, or healthcare advice.
*   **Does NOT:** Provide real-time patient diagnosis or monitor patient vitals.
*   **Edge Cases:**
    *   **Rare Conditions:** For extremely rare orphan diseases, it may return generic information instead of specific details.
    *   **Ethics Bias:** Ethical analysis is based on established frameworks (AMA, etc.); it may struggle with emerging cultural variations.

### Subcommands
*   `advise`: Primary health care guidance for common concerns.
*   `anatomy`: Detailed anatomical information (classification, position, function).
*   `case`: Generates synthetic medical case reports for training.
*   `decision`: Clinical decision-making guides based on symptoms.
*   `disease`: Comprehensive profiles of diseases.
*   `ethics`: Professional medical ethics analysis for complex scenarios.
*   `facts`: Fact-check medical statements.
*   `faq`: Generates patient FAQs and professional answers.
*   `flashcard`: Explains medical terms or labels (supports image OCR).
*   `herbal`: Information on medicinal herbs and natural remedies.
*   `history`: Generates standardized patient intake questions.
*   `implant`: Information on medical devices and implants.
*   `myth`: Debunk common medical myths with scientific evidence.
*   `organ`: Organ-specific disease profiles and summaries.
*   `pose`: Guidance on surgical patient positioning.
*   `procedure`: Step-by-step breakdown of medical procedures.
*   `quiz`: Generates medical test questions for students.
*   `refer`: Identifies appropriate specialists for symptoms.
*   `roles`: Responsibilities and scope of medical specialties.
*   `surgery`: Information on surgical techniques and recovery.
*   `tool`: Descriptions of surgical instruments.
*   `tray`: Standardized surgical tray setup instructions.

---

## 💊 `medkit-drug`
**Pharmacology, Interactions & Safety**

*   **Primary Usage:** Verifying medication safety and explaining pharmacology to patients or students.
*   **Does NOT:** Provide precise pediatric or geriatric weight-based dosing; not a substitute for a pharmacist.
*   **Edge Cases:**
    *   **Brand vs. Generic:** Very new brand names may fail to link to their generic counterparts.
    *   **Multidrug Complexity:** Checking 10+ drugs simultaneously can lead to "interaction fatigue."

### Subcommands
*   `addiction`: Info on addiction, withdrawal, and recovery.
*   `compare`: Side-by-side comparison of two medications.
*   `disease`: Checks drug-disease contraindications.
*   `explain`: Simple, patient-friendly medication explanation.
*   `food`: Identifies drug-food interactions.
*   `info`: Comprehensive drug monographs.
*   `interact`: Detailed drug-drug interaction analysis.
*   `similar`: Finds therapeutic alternatives within the same class.
*   `symptoms`: Find common medications used to treat specific symptoms.

---

## 📊 `medkit-graph`
**Medical Knowledge Graph Extraction**

*   **Primary Usage:** Visualizing complex medical text to identify hidden relationships between symptoms and causes.
*   **Does NOT:** Verify if the input text is medically true; it only maps what you provide.
*   **Edge Cases:**
    *   **Ambiguity:** "It causes pain" may result in a broken link if "It" is not clearly defined in context.

### Subcommands
*   `anatomy`, `disease`, `genetic`, `medicine`, `pathophysiology`, `pharmacology`, `procedure`, `surgery`, `symptoms`, `test`.

---

## 🔍 `medkit-recognizer`
**Medical Entity Recognition (NER)**

*   **Primary Usage:** Transforming unstructured doctor's notes into clean, structured datasets for research.
*   **Does NOT:** Understand clinical intent (e.g., cannot distinguish "Patient denies cough" from "Patient has cough").
*   **Edge Cases:**
    *   **Overlapping Terms:** "Lung Cancer" might be incorrectly split into separate Anatomy and Disease concepts.

### Subcommands
*   `abbreviation`, `anatomy`, `clinical_sign`, `coding`, `condition`, `device`, `disease`, `drug`, `genetic`, `imaging`, `lab_unit`, `med_class`, `pathogen`, `procedure`, `specialty`, `supplement`, `symptom`, `test`, `vaccine`.

---

## 📸 `medkit-media`
**Medical Image/Video Search & Analysis**

*   **Primary Usage:** Sourcing visual aids for medical presentations or generating captions for educational scans.
*   **Does NOT:** Verify image copyright or ensure 100% medical accuracy of web-sourced results.
*   **Edge Cases:**
    *   **Search Noise:** A search for "Stapes" might return a picture of a stapler if the index is noisy.

### Subcommands
*   `caption`: Generates clinical captions for images.
*   `images`: Searches and downloads medical images.
*   `summary`: Summarizes educational medical videos.
*   `videos`: Searches for medical educational videos.

---

## 🧪 `medkit-diagnostics`
**Medical Tests & Devices**

*   **Primary Usage:** Understanding the logic behind lab tests and the mechanics of diagnostic hardware.
*   **Does NOT:** Interpret a specific patient's lab results (e.g., "My result is X, what does it mean?").
*   **Edge Cases:**
    *   **Non-Standard Abbreviations:** Fails on proprietary or rare regional lab shorthand.

### Subcommands
*   `test`: Reference info for lab tests (normal ranges, indications).
*   `device`: Technical info about diagnostic medical devices.

---

## 📄 `medkit-article`
**PubMed & Article Search**

*   **Primary Usage:** Literature review and finding peer-reviewed evidence for specific medical conditions.
*   **Does NOT:** Provide full-text PDFs; only provides metadata and abstracts.
*   **Edge Cases:**
    *   **Rate Limits:** Excessive searching can lead to temporary blocks from PubMed servers.

### Subcommands
*   `search`: Search for articles and PubMed records by disease.
*   `cite`: Retrieve formatted citations.

---

## 🛡️ `medkit-privacy`
**HIPAA Compliance & Data Protection**

*   **Primary Usage:** Automating HIPAA compliance workflows like consent capture and PII scrubbing.
*   **Does NOT:** Provide legal indemnity or technical encryption.
*   **Edge Cases:**
    *   **Masking Failures:** If a name is also a common word (e.g., "Patient Rose"), it may remain unmasked.

### Subcommands
*   `audit`: Logs compliance and data access events.
*   `consent`: Displays HIPAA-compliant informed consent.
*   `mask`: Scrubs PII from clinical text.
*   `report`: Generates HIPAA compliance metrics.

---

## 🧠 `medkit-mental`
**Mental Health Assessment**

*   **Primary Usage:** Conducting preliminary psychiatric screenings and longitudinal tracking.
*   **Does NOT:** Provide therapy, counseling, or emergency crisis intervention.
*   **Edge Cases:**
    *   **Crisis Detection:** AI can miss subtle linguistic cues of immediate self-harm risk.

---

## ⚖️ `medkit-sane`
**SANE Interview Protocol**

*   **Primary Usage:** Standardizing forensic interview protocols to ensure legal and clinical consistency.
*   **Does NOT:** Collect physical DNA evidence or serve as a legal witness.
*   **Edge Cases:**
    *   **Trauma Response:** Struggles to build coherent timelines from non-linear accounts.

---

## 📖 `medkit-dictionary`
**Medical Terminology Builder**

*   **Primary Usage:** Building and managing a custom structured medical glossary.
*   **Does NOT:** Replace official medical dictionaries like Stedman's or Dorland's.

---

## 📋 `medkit-codes`
**ICD-11 Coding**

*   **Primary Usage:** Mapping clinical descriptions to international standard ICD-11 codes.
*   **Does NOT:** Handle medical billing, insurance claims, or CPT/HCPCS codes.
*   **Edge Cases:**
    *   **Granularity:** May return a "parent" code if input is not specific enough.

---

## 📋 `medkit-exam`
**Physical Examination Protocols**

*   **Primary Usage:** Training or reference for performing standardized physical examinations.
*   **Does NOT:** Perform the actual exam or provide real-time guidance during physical touch.
