# MedKit Exhaustive CLI Reference

This manual provides detailed technical descriptions, primary usage scenarios, and specific examples for the entire MedKit suite.

---

## 🤖 `medkit-agent`
**Autonomous Medical Orchestrator**

*   **Primary Usage**: This tool is designed to solve complex, multi-step clinical queries that require information from multiple specialized domains. It interprets high-level intent and coordinates other MedKit tools to form a comprehensive answer.
*   **What it DOES**: It parses natural language instructions, executes a reasoning loop, identifies which sub-tools are needed, and synthesizes their outputs into a final response.
*   **What it DOES NOT Do**: It does not possess medical intuition or a professional license. It is strictly a logic engine that relies on the accuracy of the tools it calls.
*   **Edge Cases**: The agent can occasionally enter a tool-calling loop if sub-tools provide conflicting data, and it may lose context if the query involves too many logical branches.
*   **Example**:
    ```bash
    medkit-agent "Patient is a 65yo male with sudden onset of left-sided weakness. Check for drug side effects and find relevant specialists."
    ```

---

## 🏥 `medkit-medical`
**General Medical Knowledge & Clinical Tools**

This tool provides access to a massive database of static medical reference data across 20+ specialized domains.

### Subcommands

*   **`advise`**: Provides evidence-based guidance for primary healthcare concerns and minor home management.
    *   *Example*: `medkit-medical advise "Managing mild fever at home"`
*   **`anatomy`**: Retrieves detailed anatomical information including classification, blood supply, and functional roles of body parts.
    *   *Example*: `medkit-medical anatomy "Liver"`
*   **`case`**: Generates synthetic medical case reports for clinical training, simulation, or software testing.
    *   *Example*: `medkit-medical case "Type 2 Diabetes"`
*   **`decision`**: Provides diagnostic logic trees and clinical decision support based on a patient's presenting symptoms.
    *   *Example*: `medkit-medical decision "Acute Cough"`
*   **`disease`**: Accesses comprehensive monographs for medical conditions, covering etiology, presentation, and standard treatments.
    *   *Example*: `medkit-medical disease "Hypertension"`
*   **`ethics`**: Analyzes complex medical ethics scenarios using established principles like autonomy, beneficence, and justice.
    *   *Example*: `medkit-medical ethics "Patient confidentiality vs public safety"`
*   **`facts`**: Verifies or refutes medical statements by cross-referencing them against established clinical guidelines.
    *   *Example*: `medkit-medical facts "Vaccines cause autism"`
*   **`faq`**: Automatically generates patient education materials consisting of common questions and plain-language answers.
    *   *Example*: `medkit-medical faq "Asthma"`
*   **`flashcard`**: Extracts medical terms from images via OCR or processes text lists to provide concise clinical definitions.
    *   *Example*: `medkit-medical flashcard "label_image.jpg"`
*   **`herbal`**: Researches the safety and clinical evidence levels for medicinal herbs and natural supplements.
    *   *Example*: `medkit-medical herbal "Turmeric"`
*   **`history`**: Generates standardized and targeted history-taking questions based on a patient's age, gender, and the purpose of the visit.
    *   *Example*: `medkit-medical history -e "Physical" -a 45 -g "Male"`
*   **`implant`**: Provides technical reference data for surgical hardware, including materials, indications, and MRI safety notes.
    *   *Example*: `medkit-medical implant "Pacemaker"`
*   **`myth`**: Debunks widespread medical misconceptions with documented scientific evidence and explains the origin of the myth.
    *   *Example*: `medkit-medical myth "We use 10% of our brain"`
*   **`organ`**: Offers quick summaries of organ-specific physiology and the organ's role in systemic disease patterns.
    *   *Example*: `medkit-medical organ "Pancreas"`
*   **`pose`**: Details the correct patient positioning for surgical procedures and lists associated pressure-point and nerve risks.
    *   *Example*: `medkit-medical pose "Prone"`
*   **`procedure`**: Breaks down medical and diagnostic procedures into step-by-step educational instructions.
    *   *Example*: `medkit-medical procedure "Knee Replacement"`
*   **`quiz`**: Generates multiple-choice questions with rationales for use in medical education and competency assessments.
    *   *Example*: `medkit-medical quiz "Cardiology"`
*   **`refer`**: Identifies the most appropriate medical specialty or sub-specialty based on a complex set of clinical findings.
    *   *Example*: `medkit-medical refer "Chest pain and dyspnea"`
*   **`roles`**: Defines the scope of practice and specific clinical responsibilities for different healthcare professional specialties.
    *   *Example*: `medkit-medical roles "Neurosurgeon"`
*   **`surgery`**: Provides detailed surgical monographs covering preoperative preparation, technique, and postoperative recovery.
    *   *Example*: `medkit-medical surgery "Appendectomy"`
*   **`tool`**: Identifies and describes surgical instruments and medical equipment, including their primary use and sterilization needs.
    *   *Example*: `medkit-medical tool "Scalpel"`
*   **`tray`**: Lists the standard instrument and consumable requirements for setting up specific surgical back tables.
    *   *Example*: `medkit-medical tray "Orthopedic"`

---

## 💊 `medkit-drug`
**Pharmacology, Interactions & Medication Safety**

This tool provides a unified interface for researching medications and screening for safety issues.

### Subcommands

*   **`addiction`**: Provides clinical information on substance use disorders, including withdrawal timelines and evidence-based recovery paths.
    *   *Example*: `medkit-drug addiction "Oxycodone"`
*   **`compare`**: Performs a side-by-side comparison of two medications, highlighting differences in efficacy, side effects, and cost profiles.
    *   *Example*: `medkit-drug compare "Tylenol" "Advil"`
*   **`disease`**: Checks for contraindications and necessary dosage adjustments for drugs when a patient has specific comorbid conditions.
    *   *Example*: `medkit-drug disease "Ibuprofen" "Kidney Disease"`
*   **`explain`**: Translates complex pharmacological mechanisms into simple, patient-friendly language for better health literacy.
    *   *Example*: `medkit-drug explain "Amoxicillin"`
*   **`food`**: Identifies known interactions between specific medications and dietary components like grapefruit or leafy greens.
    *   *Example*: `medkit-drug food "Metformin" "Grapefruit"`
*   **`info`**: Provides comprehensive professional drug monographs, including pharmacokinetics, dosing, and adverse reactions.
    *   *Example*: `medkit-drug info "Lisinopril"`
*   **`interact`**: Conducts a detailed safety screening for interactions between two or more drugs, categorized by severity.
    *   *Example*: `medkit-drug interact "Warfarin" "Aspirin"`
*   **`similar`**: Finds therapeutic alternatives or similar drugs within the same pharmacological class for substitution research.
    *   *Example*: `medkit-drug similar "Ozempic"`
*   **`symptoms`**: Identifies common pharmacological treatments typically used to manage a specific set of clinical symptoms.
    *   *Example*: `medkit-drug symptoms "Neuropathic pain"`

---

## 📊 `medkit-graph`
**Medical Knowledge Graph Extraction**

This tool converts unstructured medical text into structured knowledge triples (Subject-Relation-Object) and generates interactive visual graphs.

### Subcommands
*   **`anatomy`**: Maps anatomical relationships and structural links from descriptive text.
*   **`disease`**: Extracts links between diseases, their symptoms, and standard treatments.
*   **`genetic`**: Identifies relationships between genes, variants, and associated clinical conditions.
*   **`medicine`**: Maps pharmaceutical knowledge and drug targets from research text.
*   **`pathophysiology`**: Extracts physiological mechanisms and causal pathways of diseases.
*   **`pharmacology`**: Maps drug mechanisms of action and enzymatic pathways.
*   **`procedure`**: Extracts the logical sequence of steps in a medical or surgical procedure.
*   **`surgery`**: Maps surgical anatomy, tool requirements, and procedural landmarks.
*   **`symptoms`**: Extracts symptom-to-disease and symptom-to-anatomy mappings.
*   **`test`**: Extracts the logic behind diagnostic tests, including what they measure and why.

*   *Example*: `medkit-graph disease "Diabetes is a chronic condition caused by insulin resistance."`

---

## 🔍 `medkit-recognizer`
**Medical Entity Recognition (NER)**

This tool extracts and standardizes medical entities from unstructured clinical text using 19 specialized identifiers.

### Subcommands
*   **`abbreviation`**: Resolves medical abbreviations into their full clinical forms.
*   **`anatomy`**: Identifies and extracts anatomical structures and body locations.
*   **`clinical_sign`**: Identifies specific clinical examination findings and signs.
*   **`coding`**: Extracts and maps medical descriptions to standard codes like ICD or CPT.
*   **`condition`**: Identifies general medical conditions and states of health.
*   **`device`**: Identifies medical hardware, diagnostic devices, and clinical tools.
*   **`disease`**: Performs high-accuracy identification of specific medical diseases.
*   **`drug`**: Extracts pharmaceutical names and medication mentions.
*   **`genetic`**: Identifies genetic variants, markers, and genomic mentions.
*   **`imaging`**: Extracts findings and technical terms from radiology reports.
*   **`lab_unit`**: Identifies and standardizes laboratory measurement units.
*   **`med_class`**: Identifies broader pharmacological and medication classes.
*   **`pathogen`**: Identifies bacteria, viruses, and other infectious agents.
*   **`procedure`**: Extracts mentions of medical, surgical, or diagnostic procedures.
*   **`specialty`**: Identifies medical specialties and sub-specialty mentions.
*   **`supplement`**: Identifies dietary supplements and nutraceuticals.
*   **`symptom`**: Extracts subjective medical symptoms reported by patients.
*   **`test`**: Identifies mentions of laboratory and diagnostic tests.
*   **`vaccine`**: Extracts mentions of vaccines and biological products.

*   *Example*: `medkit-recognizer drug "Patient is taking 10mg of Lisinopril daily."`

---

## 📸 `medkit-media`
**Medical Image/Video Search & Analysis**

This tool enables the searching, downloading, and AI-powered analysis of medical visual content.

### Subcommands

*   **`caption`**: Generates professional, context-aware descriptions for medical images or clinical scans.
    *   *Example*: `medkit-media caption "Rheumatoid hand x-ray"`
*   **`images`**: Searches DuckDuckGo for medical images and downloads them to a local directory for reference.
    *   *Example*: `medkit-media images "Psoriasis plaques" -n 5`
*   **`summary`**: Summarizes the key learning points and clinical significance of long-form medical videos or articles.
    *   *Example*: `medkit-media summary "Laparoscopic cholecystectomy technique"`
*   **`videos`**: Searches for educational medical videos and returns metadata and source URLs.
    *   *Example*: `medkit-media videos "CPR technique instructional"`

---

## 🧪 `medkit-diagnostics`
**Medical Tests & Diagnostic Devices**

This tool provides technical and clinical reference data for the diagnostics domain.

### Subcommands

*   **`test`**: Provides reference information for lab tests, including why they are ordered and what their normal ranges represent.
    *   *Example*: `medkit-diagnostics test "HbA1c"`
*   **`device`**: Offers technical information on diagnostic hardware, including physics of operation and clinical safety.
    *   *Example*: `medkit-diagnostics device "MRI Scanner"`

---

## 📄 `medkit-article`
**PubMed & Medical Research Search**

This tool is used for evidence-based research by searching peer-reviewed medical literature.

### Subcommands

*   **`search`**: Searches PubMed and BioMCP for the latest research articles related to a specific medical condition.
    *   *Example*: `medkit-article search "Gout"`
*   **`cite`**: Retrieves and formats article citations in standardized clinical formats for bibliographies.
    *   *Example*: `medkit-article cite "Diabetes"`

---

## 🛡️ `medkit-privacy`
**HIPAA Compliance & Data Protection**

This tool automates privacy workflows and ensures sensitive data is handled according to healthcare standards.

### Subcommands

*   **`audit`**: Logs all data access and modification events into a secure, HIPAA-compliant audit trail.
    *   *Example*: `medkit-privacy audit --session "SESS123" --action "View Record" --role "Nurse"`
*   **`consent`**: Displays standardized HIPAA privacy notices and captures digital informed consent from users.
    *   *Example*: `medkit-privacy consent`
*   **`mask`**: Uses patterns and regex to identify and scrub Personally Identifiable Information (PII) from clinical text.
    *   *Example*: `medkit-privacy mask "Patient John Doe at 555-0199"`
*   **`report`**: Generates administrative reports on active sessions and overall system compliance metrics.
    *   *Example*: `medkit-privacy report`

---

## 🧠 `medkit-mental`
**Interactive Mental Health Assessment**

This tool conducts an interactive psychiatric screening session using validated clinical scales. It is intended for preliminary assessment and longitudinal tracking of mental health symptoms.
*   **Usage**: Run `medkit-mental` to start a structured, conversational screening session.
*   **What it DOES**: It asks diagnostic questions, evaluates responses based on scales like PHQ-9, and provides a summary.
*   **What it DOES NOT Do**: It does not provide therapy, crisis counseling, or definitive psychiatric diagnosis.
*   **Example**:
    ```bash
    medkit-mental
    ```

---

## ⚖️ `medkit-sane`
**Forensic Nursing & SANE Interview Protocol**

This specialized tool guides Sexual Assault Nurse Examiners through the complex sequence of a forensic interview. It ensures that all legal and clinical steps are followed according to strict protocols.
*   **Usage**: Run `medkit-sane start` to begin a guided interview protocol.
*   **What it DOES**: It provides the correct interview sequence, ensures legally necessary questions are asked, and helps build a coherent timeline.
*   **What it DOES NOT Do**: It does not collect physical DNA evidence or serve as a legal representative.
*   **Example**:
    ```bash
    medkit-sane start
    ```

---

## 📋 `medkit-codes`
**ICD-11 Diagnostic Coding**

This tool maps clinical descriptions to the official WHO ICD-11 diagnostic hierarchy. It is used for medical record-keeping and diagnostic standardization.
*   **Usage**: `medkit-codes search "<description>"`
*   **What it DOES**: It searches the ICD-11 database and returns the most relevant diagnostic codes and their titles.
*   **What it DOES NOT Do**: It does not handle medical billing, insurance claim submission, or CPT/HCPCS coding.
*   *Example*: `medkit-codes search "Asthma"`

---

## 📖 `medkit-dictionary`
**Medical Terminology Builder**

This tool is designed to build and manage a custom, structured medical dictionary for use in other clinical software applications.
*   **Usage**: `medkit-dictionary build`
*   **What it DOES**: It automates the generation of structured definitions and metadata for a large volume of medical terms.
*   **Example**: `medkit-dictionary build`

---

## 📋 `medkit-exam`
**Standardized Physical Examination Protocols**

This tool serves as a reference and training guide for performing standardized head-to-toe physical examinations. It contains 28+ specific protocols for different body systems.
*   **Usage**: `medkit-exam --list`
*   **What it DOES**: It provides step-by-step checklists and maneuvers required for a professional physical exam (e.g., Cardiac, Neurological).
*   **What it DOES NOT Do**: It does not perform the exam or provide real-time haptic feedback to the examiner.
*   **Example**:
    ```bash
    medkit-exam --list
    ```
