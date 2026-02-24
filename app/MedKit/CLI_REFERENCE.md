# MedKit Exhaustive CLI Reference

This manual is the definitive technical guide for MedKit. Every subcommand is detailed from an end-user perspective, focusing on clinical utility, safety boundaries, and technical parameters.

---

## 📂 Output & Data Storage

MedKit uses a standardized storage architecture to ensure data is organized and secure.

| Data Type | Default Location | Access Level | Description |
| :--- | :--- | :--- | :--- |
| **Generated Reports** | `./outputs/` | User | Clinical monographs, drug analyses, and test references. |
| **Compliance Logs** | `~/.medkit/sessions/` | Restricted (0700) | HIPAA audit trails, session history, and PII-masked data. |
| **Media Assets** | `./outputs/media/` | User | Downloaded medical images and video metadata. |
| **System Logs** | `<module>/logs/` | Developer | Technical debug logs for troubleshooting AI responses. |

**Global Flag: `-d, --output-dir`**
You can override the default output path for any non-restricted command.
*Example*: `medkit-medical anatomy "Liver" -d "./research_project_A"`

---

## 🤖 `medkit-agent` (The Orchestrator)
**"The Central Brain for Multi-Domain Queries"**

*   **Primary Usage**: Solving high-level, multi-step clinical queries that require coordinating multiple data sources (e.g., "Identify this drug, check its interactions with the patient's existing meds, and find a relevant specialist").
*   **Key Arguments**:
    *   `-m, --model`: Select the underlying LLM (e.g., `openai/gpt-4o`, `ollama/gemma3`).
    *   `-t, --temperature`: Controls randomness/creativity (0.0 to 1.0).
*   **What it DOES**: Parses natural language, dynamically selects tools, and synthesizes a final response.
*   **What it DOES NOT Do**: It does not possess medical intuition or a professional license.
*   **Failure Handling**: If a sub-tool fails, the agent reports the specific failure but continues reasoning with available data.
*   **Example**:
    ```bash
    medkit-agent "70yo on Warfarin with a new cough. Check interactions and suggest referral."
    ```

---

## 🏥 `medkit-medical` (Knowledge Engine)
**Standardized Reference for 24+ Medical Domains**

*   **Global Arguments**:
    *   **`-s, --structured`**: Forces the tool to return valid JSON (Pydantic model) instead of Markdown text. Essential for integration with other software.
    *   `-m, --model`: Override the default model.
    *   `-d, --output-dir`: Specify where to save the generated report.

### `list`
*   **Primary Usage**: Discoverability tool to see all 24+ medical subcommands categorized by their clinical purpose.
*   **Does**: Prints a clean, descriptive table of every available module.
*   **Example**: `medkit-medical list`

#### Subcommand Catalog
| # | Subcommand | Primary Utility |
| :--- | :--- | :--- |
| 1 | **`advise`** | Primary health care guidance and home management. |
| 2 | **`anatomy`** | Body structures, innervation, and blood supply. |
| 3 | **`case`** | Realistic synthetic patient case report generation. |
| 4 | **`decision`** | Diagnostic logic trees and clinical decision support. |
| 5 | **`disease`** | Etiology, symptoms, and treatment protocols. |
| 6 | **`ethics`** | Structured pillar-based analysis of bioethical dilemmas. |
| 7 | **`eval-procedure`** | Auditing and evaluating medical procedure documentation. |
| 8 | **`facts`** | Evidence-based verification of medical statements. |
| 9 | **`faq`** | Plain-language patient education materials. |
| 10 | **`flashcard`** | Terminology extraction and explanation from labels. |
| 11 | **`herbal`** | Evidence-based info on natural remedies and safety. |
| 12 | **`history`** | Standardized history-taking and intake questions. |
| 13 | **`implant`** | Detailed information on medical implants and prosthetics. |
| 14 | **`myth`** | Scientific debunking of common medical misconceptions. |
| 15 | **`organ`** | Organ-specific physiology and systemic disease roles. |
| 16 | **`pose`** | Standard patient positioning and associated risks. |
| 17 | **`procedure`** | Step-by-step educational breakdown of clinical procedures. |
| 18 | **`quiz`** | MCQ assessment generation with distractors and rationales. |
| 19 | **`refer`** | Identifying the correct specialty for clinical presentations. |
| 20 | **`roles`** | Scope of practice and responsibilities for medical specialties. |
| 21 | **`surgery`** | Exhaustive procedural monographs and recovery benchmarks. |
| 22 | **`tool`** | Reference for surgical instruments and sterilization needs. |
| 23 | **`topic`** | Synthesis of general medical subjects. |
| 24 | **`tray`** | Standardized setup lists for surgical instrument trays. |

---

### 📘 Exhaustive Module Reference

The following sections provide a definitive guide to every `medkit-medical` module, detailing how AI augments traditional clinical practice.

#### `advise`
*   **Problem**: Reliance on generic triage pamphlets or long wait times for nurse hotlines often leads to unnecessary ER visits or missed red flags.
*   **Usage**: Conservative triage guidance for primary health care concerns.
*   **Does**: Analyzes symptoms to differentiate between self-limiting conditions (home care) and emergent presentations.
*   **Does NOT**: Provide definitive diagnosis or replace emergency services.
*   **AI Augmentation**: MedKit analyzes specific symptoms and patient context to provide evidence-based triage. It identifies subtle patterns in clinical presentation that might be missed by generic flowcharts, ensuring patient safety while optimizing system resources.
*   **Example**: `medkit-medical advise "Persistent dry cough for 3 days, no fever" -s`

#### `anatomy`
*   **Problem**: Sourcing reliable anatomical data (innervation, blood supply) from static 2D atlases is slow and requires manual cross-referencing.
*   **Usage**: Detailed research into specific body structures and functional relationships.
*   **Does**: Provides names, body systems, innervation, blood supply, and functional mechanisms.
*   **Does NOT**: Analyze patient-specific medical images (DICOM/X-ray).
*   **AI Augmentation**: AI provides dynamic, semantic retrieval of anatomical relationships. It can instantly map the secondary implications of a lesion (e.g., "If this nerve is damaged, which muscle groups are affected?"), serving as a real-time "functional atlas."
*   **Example**: `medkit-medical anatomy "Brachial Plexus" --structured`

#### `case`
*   **Problem**: Educators manually writing patient cases is time-consuming and often results in repetitive or biased scenarios. Using real data is ethically complex.
*   **Usage**: Generating realistic patient scenarios for education and testing.
*   **Does**: Generates high-fidelity, diverse, and medically plausible synthetic patient cases with history, physical findings, and labs.
*   **Does NOT**: Represent any real individual (strictly synthetic).
*   **AI Augmentation**: AI generates high-fidelity, diverse, and medically plausible synthetic patient cases at scale. These cases include realistic history, physical findings, and labs, allowing for robust medical education and software testing without any HIPAA or privacy risks.
*   **Example**: `medkit-medical case "Uncontrolled Type 2 Diabetes with neuropathy" -s`

#### `decision`
*   **Problem**: Static paper flowcharts or memorized algorithms cannot easily account for complex patient-specific comorbidities.
*   **Usage**: Diagnostic logic trees and clinical decision support.
*   **Does**: Parses a constellation of symptoms into a prioritized differential diagnosis and suggests the next logical diagnostic step.
*   **Does NOT**: Make final clinical decisions or replace professional judgment.
*   **AI Augmentation**: MedKit creates dynamic diagnostic logic trees. It parses a constellation of symptoms into a prioritized differential diagnosis, suggesting the most logical next diagnostic step based on the principle of "Occam's Razor" (simplicity) and "Sutton's Law" (probability).
*   **Example**: `medkit-medical decision "Acute epigastric pain radiating to the back" -s`

#### `disease`
*   **Problem**: Searching exhaustive textbook chapters or subscription databases for standard-of-care treatments is slow.
*   **Usage**: Retrieving comprehensive, evidence-based disease monographs.
*   **Does**: Covers pathophysiology, etiology, symptoms, diagnostic criteria, and management.
*   **Does NOT**: Account for real-time drug shortages or local hospital protocols.
*   **AI Augmentation**: AI synthesizes the most recent peer-reviewed guidelines and clinical literature into concise, actionable monographs. It provides the "Clinical Essentials"—etiology, pathophysiology, and gold-standard management—in seconds rather than minutes.
*   **Example**: `medkit-medical disease "Systemic Lupus Erythematosus" -s`

#### `ethics`
*   **Problem**: Clinicians often rely on hospital policy or "gut feeling" for complex bioethical dilemmas like end-of-life care.
*   **Usage**: Structured analysis of complex bioethical scenarios.
*   **Does**: Applies frameworks like Autonomy, Beneficence, Non-maleficence, and Justice to a specific case.
*   **Does NOT**: Provide legal advice or make the final ethical decision for the committee.
*   **AI Augmentation**: AI applies structured bioethical frameworks (Autonomy, Beneficence, Non-maleficence, and Justice) to a specific case. It provides a balanced, multi-perspective analysis that helps clinicians navigate "gray areas" with consistent, logical rigor.
*   **Example**: `medkit-medical ethics "Family refuses life-saving treatment for a minor"`

#### `eval-procedure`
*   **Problem**: Manual review of operative notes for safety steps or terminology consistency is prone to human oversight.
*   **Usage**: Auditing and evaluating medical procedure documentation.
*   **Does**: Identifies missing safety steps, terminology inconsistencies, or omissions in follow-up instructions.
*   **Does NOT**: Edit the original legal record directly (provides an audit report).
*   **AI Augmentation**: AI audits medical documentation against clinical standards. It identifies missing safety steps (e.g., "Was the timeout documented?"), inconsistencies in anatomical terminology, or omissions in follow-up care instructions, ensuring high-quality, compliant records.
*   **Example**: `medkit-medical eval-procedure "path/to/operative_note.txt"`

#### `facts`
*   **Problem**: Manually verifying clinical claims on PubMed requires significant time to filter results.
*   **Usage**: Evidence-based verification of specific medical statements.
*   **Does**: Uses RAG to verify statements against authoritative datasets, providing a "truth score" and context.
*   **Does NOT**: Verify non-medical or speculative claims.
*   **AI Augmentation**: AI uses Retrieval-Augmented Generation (RAG) to verify medical statements against high-quality, authoritative datasets. It provides a "truth score" and clinical context, acting as a real-time guardrail against medical misinformation.
*   **Example**: `medkit-medical facts "High-dose Vitamin C cures viral pneumonia"`

#### `faq`
*   **Problem**: Generic patient education templates are often written at a reading level too high for the general public.
*   **Usage**: Generating plain-language patient education materials.
*   **Does**: Translates complex clinical concepts into empathetic, easy-to-understand explanations.
*   **Does NOT**: Give specific dosage or medical instructions to a patient.
*   **AI Augmentation**: AI generates personalized, empathetic patient education materials. It translates complex clinical concepts into plain language (e.g., "the pump in your chest" instead of "myocardial contractility") while ensuring the core medical facts remain accurate.
*   **Example**: `medkit-medical faq "How to manage high blood pressure at home"`

#### `flashcard`
*   **Problem**: Dense jargon on medical labels or pathology reports is inaccessible to patients and junior staff.
*   **Usage**: Terminology extraction and explanation from labels and reports.
*   **Does**: Uses OCR to find medical terms and provides instant, simplified clinical definitions.
*   **Does NOT**: Interpret the results as a diagnosis (e.g., "You have cancer").
*   **AI Augmentation**: AI uses computer vision (OCR) to extract medical terms directly from images of labels or reports and provides instant, simplified clinical explanations. This bridges the "health literacy gap" for both patients and junior staff.
*   **Example**: `medkit-medical flashcard "medication_bottle.jpg"`

#### `herbal`
*   **Problem**: Data on the safety or drug-drug interactions of herbal supplements is often scattered across non-clinical websites.
*   **Usage**: Evidence-based info on botanical remedies and safety.
*   **Does**: Analyzes therapeutic utility, toxicities, and herb-drug interactions.
*   **Does NOT**: Recommend herbal treatments over standard pharmaceutical care.
*   **AI Augmentation**: AI provides an evidence-based analysis of herbal supplements, focusing on therapeutic utility, toxicities, and—critically—herb-drug interactions (e.g., St. John's Wort's effect on cytochrome P450), ensuring holistic patient safety.
*   **Example**: `medkit-medical herbal "St. John's Wort" -s`

#### `history`
*   **Problem**: Unstructured intake or static forms often miss critical details like family history or environmental exposures.
*   **Usage**: Standardizing targeted, adaptive history-taking questions.
*   **Does**: Tailors intake questions to the patient's age, gender, and the purpose of the exam.
*   **Does NOT**: Conduct the interview (it provides the questions for the clinician).
*   **AI Augmentation**: AI generates adaptive, targeted history-taking questions. By knowing the patient's age, gender, and purpose of the visit, it prioritizes the most high-yield questions (e.g., "Review of Systems" specific to chest pain), ensuring no clinical "blind spots."
*   **Example**: `medkit-medical history -e "Pre-op" -a 60 -g "Female" -s`

#### `implant`
*   **Problem**: Finding data on an old implant's MRI compatibility or failure rates often requires searching physical manufacturer manuals.
*   **Usage**: Detailed reference for medical implants and prosthetics.
*   **Does**: Provides data on indications, complications, and safety parameters (like MRI safety).
*   **Does NOT**: Provide real-time tracking of individual serialized devices.
*   **AI Augmentation**: AI serves as a centralized reference for medical implants. It provides instant data on indications, complications, and critical safety parameters (e.g., "Is this heart valve MRI-safe at 3T?"), which is vital for radiologists and surgeons.
*   **Example**: `medkit-medical implant "St. Jude Medical Heart Valve" -s`

#### `myth`
*   **Problem**: Correcting patient misconceptions through repetitive verbal explanations is time-consuming during office visits.
*   **Usage**: Evidence-based debunking of common medical myths.
*   **Does**: Presents scientific consensus alongside the origins of the myth and provides a "script" for clinicians.
*   **Does NOT**: Engage in hostile debate; it remains professional and objective.
*   **AI Augmentation**: AI provides structured, evidence-based debunking of common medical myths. It presents the scientific consensus alongside the origins of the myth, providing clinicians with a "script" to handle difficult conversations effectively.
*   **Example**: `medkit-medical myth "Flu shots give you the flu"`

#### `organ`
*   **Problem**: Learning organ systems in isolation makes it difficult to understand systemic cascades (e.g., how liver failure leads to brain swelling).
*   **Usage**: Organ-specific physiology and systemic disease mapping.
*   **Does**: Explains the functional connections between organs and systemic disease.
*   **Does NOT**: Provide real-time diagnostic imaging of organs.
*   **AI Augmentation**: AI maps the functional connections between organs and systemic disease. It explains the "why" behind clinical signs (e.g., "How does kidney failure lead to bone disease?"), fostering a deeper, integrated understanding of medicine.
*   **Example**: `medkit-medical organ "Kidneys" -s`

#### `pose`
*   **Problem**: Relying on memory for surgical positioning can lead to rare but devastating nerve palsies or pressure ulcers.
*   **Usage**: Safety reference for surgical patient positioning.
*   **Does**: Identifies risks (nerve compression, joint strain) and padding requirements for specific positions.
*   **Does NOT**: Physically position the patient.
*   **AI Augmentation**: AI identifies the specific risks associated with every surgical position (e.g., Trendelenburg, Lithotomy). It lists "critical check-points" for padding and joint alignment, acting as a digital safety checklist for the surgical team.
*   **Example**: `medkit-medical pose "Trendelenburg"`

#### `procedure`
*   **Problem**: "See one, do one, teach one" relies on the teaching ability of senior colleagues and specific case availability.
*   **Usage**: Step-by-step educational breakdown of clinical procedures.
*   **Does**: Provides technical steps, equipment lists, pitfall warnings, and physiological rationale.
*   **Does NOT**: Grant clinical competency or license to perform the procedure.
*   **AI Augmentation**: AI provides an exhaustive, step-by-step breakdown of clinical procedures. It includes "Clinical Pearls," common pitfalls to avoid, and the physiological rationale for each step, ensuring a standardized and safe learning environment.
*   **Example**: `medkit-medical procedure "Lumbar Puncture" -s`

#### `quiz`
*   **Problem**: Educators manually writing high-quality MCQs with plausible distractors is notoriously difficult.
*   **Usage**: Generating clinical assessment questions and rationales.
*   **Does**: Creates realistic MCQs with detailed explanations for both correct and incorrect options.
*   **Does NOT**: Replace official board examinations or certification.
*   **AI Augmentation**: AI generates high-quality medical assessments. It creates realistic distractors based on common clinical errors and provides detailed rationales for why the correct answer is right and why others are wrong, enhancing active learning.
*   **Example**: `medkit-medical quiz "Cardiology" --difficulty "Advanced"`

#### `refer`
*   **Problem**: General practitioners often refer to broad specialties (e.g., "Surgery") without knowing the optimal sub-specialist for a specific case.
*   **Usage**: Identifying the correct medical sub-specialty for a clinical presentation.
*   **Does**: Recommends the specific sub-specialty best suited for a patient's symptoms or diagnosis.
*   **Does NOT**: Schedule the appointment or guarantee insurance coverage.
*   **AI Augmentation**: AI analyzes clinical presentations to recommend the most appropriate medical sub-specialty. This ensures the patient sees the right expert the first time, reducing wait times and improving diagnostic accuracy.
*   **Example**: `medkit-medical refer "Unexplained weight loss and chronic diarrhea"`

#### `roles`
*   **Problem**: Confusion in interdisciplinary teams about the scope of practice for various roles (e.g., PAs vs. NPs) can lead to safety risks.
*   **Usage**: Scope of practice and responsibilities for medical specialties.
*   **Does**: Outlines what each specialty can and cannot do based on standard clinical roles.
*   **Does NOT**: Override local state laws or hospital bylaws.
*   **AI Augmentation**: AI provides detailed mapping of roles and responsibilities within healthcare teams. It clarifies the scope of practice for various specialties, facilitating better communication and safer delegation in complex clinical environments.
*   **Example**: `medkit-medical roles "Anesthesiology Assistant" -s`

#### `surgery`
*   **Problem**: Operative notes are often sparse and don't explain the postoperative benchmarks or preoperative optimization required.
*   **Usage**: Exhaustive procedural monographs and recovery benchmarks.
*   **Does**: Covers preoperative prep, intraoperative highlights, and postoperative recovery timelines.
*   **Does NOT**: Provide real-time intraoperative guidance.
*   **AI Augmentation**: AI generates exhaustive procedural monographs. It covers preoperative optimization, intraoperative technical highlights, and specific postoperative recovery benchmarks (e.g., "When should the patient start mobilizing?"), providing a 360-degree view of the surgery.
*   **Example**: `medkit-medical surgery "Laparoscopic Cholecystectomy" -s`

#### `tool`
*   **Problem**: Junior staff "learning on the fly" in the OR is stressful and prone to error (e.g., picking the wrong forceps).
*   **Usage**: Detailed reference for surgical instruments and sterilization.
*   **Does**: Explains tool utility, handling techniques, and sterilization requirements.
*   **Does NOT**: Order instruments or manage inventory.
*   **AI Augmentation**: AI provides a detailed reference for surgical instruments. It explains what each tool is for, how it should be handled, and its sterilization requirements, serving as a "digital mentor" for surgical trainees and scrub techs.
*   **Example**: `medkit-medical tool "DeBakey Forceps" -s`

#### `topic`
*   **Problem**: Getting a comprehensive overview of a new field (e.g., "Immunotherapy") requires reading multiple fragmented sources.
*   **Usage**: Synthesis of general medical subjects into "Pillars of Knowledge."
*   **Does**: Provides a structured, high-level overview of complex medical topics.
*   **Does NOT**: Provide deep-dive research into specific niche pathologies.
*   **AI Augmentation**: AI provides a structured, high-level synthesis of complex medical subjects. It identifies the "Pillars of Knowledge" for that topic, allowing a clinician to get up to speed on a new or unfamiliar field in minutes.
*   **Example**: `medkit-medical topic "CRISPR in Medicine" -s`

#### `tray`
*   **Problem**: Senior scrub nurses relying on outdated "preference cards" leads to missing instruments and delays.
*   **Usage**: Standardized setup lists for surgical instrument trays.
*   **Does**: Lists every specific instrument required for a standardized procedural tray.
*   **Does NOT**: Track physical tray location in the sterile processing department.
*   **AI Augmentation**: AI generates standardized setup lists for surgical instrument trays. It ensures that the specific instruments required for a procedure (e.g., "Laparoscopic Cholecystectomy Tray") are correctly identified and ready, streamlining OR throughput and safety.
*   **Example**: `medkit-medical tray "Laparoscopic Appendix Tray" -s`

*(Note: All 24 medical subcommands accept the `--structured` argument to return machine-readable JSON reports.)*

---

## 💊 `medkit-drug` (Pharmacology & Safety)
**10 Specialized Subcommands for Medication Management**

*   **Global Arguments**:
    *   **`-s, --structured`**: Returns drug data in a machine-readable JSON format.

### `list`
*   **Primary Usage**: Discoverability tool to see all 10 pharmacology subcommands categorized by their clinical purpose.
*   **Does**: Prints a clean, descriptive table of every available drug module.
*   **Example**: `medkit-drug list`

### `info`
*   **Problem**: Clinicians need deeper monographs than simple definitions.
*   **Usage**: Professional medication reference.
*   **Does**: MOA, pharmacodynamics, and adult dosing guidelines.
*   **Example**: `medkit-drug info "Lisinopril" --structured`

### `interact`
*   **Problem**: Multidrug regimens increase life-threatening interaction risks.
*   **Usage**: Screening for drug-drug interactions.
*   **Does**: Identifies Major, Moderate, and Minor severity interactions.
*   **Example**: `medkit-drug interact "Warfarin" "Aspirin" --structured`

### `food`
*   **Problem**: Many patients are unaware of dietary restrictions with medications.
*   **Usage**: Checking for drug-food interactions.
*   **Does**: Identifies potential absorption issues or metabolic interference.
*   **Example**: `medkit-drug food "Sertraline" "Grapefruit" -s`

### `disease`
*   **Problem**: Certain drugs are lethal if the patient has a secondary disease.
*   **Usage**: Checking drug-disease safety.
*   **Does**: Flags risks like Beta-blockers in Asthma patients.
*   **Example**: `medkit-drug disease "Ibuprofen" "Kidney Disease" -s`

### `explain`
*   **Problem**: Clinical terminology confuses patients, leading to non-adherence.
*   **Usage**: Generating simple, compassionate medication explanations.
*   **Does**: Uses plain language to explain what a drug is and how to take it.
*   **Example**: `medkit-drug explain "Metformin"`

### `addiction`
*   **Problem**: Recovery requires clear info on withdrawal and support.
*   **Usage**: Substance abuse and recovery reference.
*   **Does**: Outlines symptoms, risks, and recovery pathways.
*   **Example**: `medkit-drug addiction "Fentanyl" -s`

### `similar`
*   **Problem**: Allergies or shortages require finding therapeutic alternatives.
*   **Usage**: Finding therapeutic substitutes.
*   **Does**: Identifies medications in the same class or with similar utility.
*   **Example**: `medkit-drug similar "Lisinopril" -s`

### `compare`
*   **Problem**: Choosing between two similar drugs for a specific patient profile.
*   **Usage**: Side-by-side medication comparison.
*   **Does**: Highlights differences in MOA, side effects, and cost.
*   **Example**: `medkit-drug compare "Atorvastatin" "Rosuvastatin" -s`

### `symptoms`
*   **Problem**: Rapidly identifying drug classes for specific clinical presentations.
*   **Usage**: Symptom-to-medication category mapping.
*   **Does**: Suggests relevant drug classes for clinical symptoms.
*   **Example**: `medkit-drug symptoms "Severe productive cough" -s`

---

## 📊 `medkit-graph` (Logic Visualization)
**Maps 10 Domains into Knowledge Triples**

*   **Key Argument**:
    *   **`--json`**: Disables the visual window and prints the raw Entity-Relation-Entity triples as a JSON list.
    *   `--no-viz`: Same as above, useful for headless server environments.

*   **Primary Usage**: Converting medical text into structured maps.
*   **Subcommands**: `disease`, `anatomy`, `medicine`, `pathophysiology`, `pharmacology`, `procedure`, `surgery`, `genetic`, `symptoms`, `test`.
*   **Example**: `medkit-graph pathophysiology "Fever resets the hypothalamus." --json`

---

## 🔍 `medkit-recognizer` (Medical NER)
**19 Identifiers for Unstructured Text Extraction**

*   **Key Argument**:
    *   **`-s, --structured`**: Outputs the extracted entities as a JSON object instead of a highlighted list.

*   **Primary Usage**: Extracting structured medical data from clinical notes.
*   **Subcommands**: `drug`, `disease`, `symptom`, `anatomy`, `coding`, `test`, `clinical_sign`, `pathogen`, `procedure`, `med_class`, `device`, `genetic`, `imaging`, `lab_unit`, `vaccine`, `specialty`, `supplement`, `abbreviation`, `condition`.
*   **Example**: `medkit-recognizer drug "Patient taking 10mg Lisinopril." -s`

---

## 📸 `medkit-media` (Visual Search & AI)
**Search, Download, and Analyze Medical Media**

*   **Global Arguments**:
    *   **`-s, --structured`**: Forces JSON output for captions and summaries.

### `images`
*   **Usage**: Searches and downloads medical images for reference.
*   **Example**: `medkit-media images "Psoriasis plaques" --size "Large"`

### `caption`
*   **Usage**: Generates professional descriptions for medical images.
*   **Example**: `medkit-media caption "Rheumatoid hand x-ray" -s`

---

## 🧪 `medkit-diagnose` (Tests & Devices)
**Laboratory and Diagnostic Hardware Reference**

*   **Global Arguments**:
    *   **`-s, --structured`**: Forces JSON output.

### `test`
*   **Usage**: Understanding the clinical utility and normal ranges of lab tests.
*   **Example**: `medkit-diagnose test "HbA1c" -s`

---

## 📄 `medkit-article` (PubMed Search)
**Peer-Reviewed Research Retrieval**

*   **Key Argument**:
    *   **`--json`**: Returns the list of articles, PMIDs, and DOIs as a JSON array.

*   **Usage**: Literature review and citation generation.
*   **Example**: `medkit-article search "Gout" --json`

---

## 🛡️ `medkit-privacy` (HIPAA Compliance)
**Automated Data Protection Workflows**

*   **Usage**: Managing HIPAA consent, audit logs, and PII masking.
*   **Output**: The `report` subcommand always outputs structured JSON by default.
*   **Example**: `medkit-privacy report`
