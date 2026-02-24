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

### 📘 Detailed Module Analysis: AI Augmentation of Clinical Workflows

The following sections provide an exhaustive breakdown of how each `medkit-medical` subcommand leverages AI to transcend traditional medical reference methods.

#### 1. `advise` (Primary Health Care Advice)
*   **Traditional Method**: Reliance on generic triage pamphlets, nurse hotlines with high wait times, or "Dr. Google," which often leads to unnecessary ER visits or missed red flags.
*   **AI Augmentation**: MedKit analyzes specific symptoms and patient context to provide evidence-based, conservative triage guidance. It differentiates between self-limiting conditions (home care) and emergent presentations requiring immediate intervention, reducing healthcare system load while ensuring patient safety.

#### 2. `anatomy` (Structural & Functional Reference)
*   **Traditional Method**: Static 2D atlases or heavy physical textbooks (e.g., Gray’s Anatomy) that require manual cross-referencing for innervation and vascular supply.
*   **AI Augmentation**: AI provides dynamic, semantic retrieval of anatomical relationships. It can instantly map the secondary implications of a lesion (e.g., "If this nerve is damaged, which specific muscle groups and sensory zones are affected?"), serving as a real-time "functional atlas" for clinicians and students.

#### 3. `case` (Synthetic Clinical Scenarios)
*   **Traditional Method**: Educators manually write patient cases, which is time-consuming and often results in repetitive or biased scenarios. Using real patient data for training is ethically complex and requires heavy de-identification.
*   **AI Augmentation**: AI generates high-fidelity, diverse, and medically plausible synthetic patient cases at scale. These cases include realistic history, physical findings, and labs, allowing for robust medical education and software testing without any HIPAA or privacy risks.

#### 4. `decision` (Clinical Decision Support)
*   **Traditional Method**: Static paper flowcharts or memorized diagnostic algorithms (e.g., the Ottawa Ankle Rules) that cannot easily account for complex comorbidities.
*   **AI Augmentation**: MedKit creates dynamic diagnostic logic trees. It parses a constellation of symptoms into a prioritized differential diagnosis, suggesting the most logical next diagnostic step based on the principle of "Occam's Razor" (simplicity) and "Sutton's Law" (probability).

#### 5. `disease` (Comprehensive Monographs)
*   **Traditional Method**: Searching subscription-based databases like UpToDate or reading exhaustive textbook chapters that may be months or years out of date.
*   **AI Augmentation**: AI synthesizes the most recent peer-reviewed guidelines and clinical literature into concise, actionable monographs. It provides the "Clinical Essentials"—etiology, pathophysiology, and gold-standard management—in seconds rather than minutes.

#### 6. `ethics` (Bioethical Framework Analysis)
*   **Traditional Method**: Ethics committees meet infrequently, and clinicians often rely on "gut feeling" or hospital policy when faced with dilemmas like end-of-life care or organ allocation.
*   **AI Augmentation**: AI applies structured bioethical frameworks (Autonomy, Beneficence, Non-maleficence, and Justice) to a specific case. It provides a balanced, multi-perspective analysis that helps clinicians navigate "gray areas" with consistent, logical rigor.

#### 7. `eval-procedure` (Documentation Auditing)
*   **Traditional Method**: Manual review of operative notes or discharge summaries by senior attendings or billing coders, which is prone to human oversight.
*   **AI Augmentation**: AI audits medical documentation against clinical standards. It identifies missing safety steps (e.g., "Was the timeout documented?"), inconsistencies in anatomical terminology, or omissions in follow-up care instructions, ensuring high-quality, compliant records.

#### 8. `facts` (Evidence Verification)
*   **Traditional Method**: Manual literature searches on PubMed or Google Scholar to verify a specific clinical claim, which requires significant time to filter through thousands of results.
*   **AI Augmentation**: AI uses Retrieval-Augmented Generation (RAG) to verify medical statements against high-quality, authoritative datasets. It provides a "truth score" and clinical context, acting as a real-time guardrail against medical misinformation.

#### 9. `faq` (Patient Education)
*   **Traditional Method**: Handing patients generic, one-size-fits-all printed templates that are often written at a reading level too high for the general public.
*   **AI Augmentation**: AI generates personalized, empathetic patient education materials. It translates complex clinical concepts into plain language (e.g., "the pump in your chest" instead of "myocardial contractility") while ensuring the core medical facts remain accurate.

#### 10. `flashcard` (Visual Terminology Extraction)
*   **Traditional Method**: Manually typing or looking up unfamiliar terms found on medication labels, pathology reports, or device packaging.
*   **AI Augmentation**: AI uses computer vision (OCR) to extract medical terms directly from images of labels or reports and provides instant, simplified clinical explanations. This bridges the "health literacy gap" for both patients and junior staff.

#### 11. `herbal` (Botanical Safety Reference)
*   **Traditional Method**: Herbal remedies are often omitted from patient records, and data on their safety or drug interactions is scattered across non-clinical websites.
*   **AI Augmentation**: AI provides an evidence-based analysis of herbal supplements, focusing on therapeutic utility, toxicities, and—critically—herb-drug interactions (e.g., St. John's Wort's effect on cytochrome P450), ensuring holistic patient safety.

#### 12. `history` (Standardized Intake)
*   **Traditional Method**: Unstructured history-taking or static intake forms that often miss critical details like family history or environmental exposures.
*   **AI Augmentation**: AI generates adaptive, targeted history-taking questions. By knowing the patient's age, gender, and purpose of the visit, it prioritizes the most high-yield questions (e.g., "Review of Systems" specific to chest pain), ensuring no clinical "blind spots."

#### 13. `implant` (Prosthetic & Device Reference)
*   **Traditional Method**: Searching for physical manufacturer manuals or calling reps to find out if an old implant is MRI-compatible or what its expected failure rate is.
*   **AI Augmentation**: AI serves as a centralized reference for medical implants. It provides instant data on indications, complications, and critical safety parameters (e.g., "Is this heart valve MRI-safe at 3T?"), which is vital for radiologists and surgeons.

#### 14. `myth` (Misinformation Debunking)
*   **Traditional Method**: Correcting patient misconceptions (e.g., "vaccines cause autism") through repetitive, time-consuming verbal explanations during short office visits.
*   **AI Augmentation**: AI provides structured, evidence-based debunking of common medical myths. It presents the scientific consensus alongside the origins of the myth, providing clinicians with a "script" to handle difficult conversations effectively.

#### 15. `organ` (Systemic Pathophysiology)
*   **Traditional Method**: Learning organ systems in isolation, which makes it difficult to understand how a failure in one (e.g., the liver) causes a systemic cascade (e.g., hepatic encephalopathy or coagulopathy).
*   **AI Augmentation**: AI maps the functional connections between organs and systemic disease. It explains the "why" behind clinical signs (e.g., "How does kidney failure lead to bone disease?"), fostering a deeper, integrated understanding of medicine.

#### 16. `pose` (Surgical Positioning Safety)
*   **Traditional Method**: Relying on the memory of the OR staff or old posters on the wall, which can lead to rare but devastating nerve palsies (e.g., ulnar nerve compression) or pressure ulcers.
*   **AI Augmentation**: AI identifies the specific risks associated with every surgical position (e.g., Trendelenburg, Lithotomy). It lists "critical check-points" for padding and joint alignment, acting as a digital safety checklist for the surgical team.

#### 17. `procedure` (Step-by-Step Education)
*   **Traditional Method**: "See one, do one, teach one," which relies on the availability of a specific case and the teaching ability of a senior colleague.
*   **AI Augmentation**: AI provides an exhaustive, step-by-step breakdown of clinical procedures. It includes "Clinical Pearls," common pitfalls to avoid, and the physiological rationale for each step, ensuring a standardized and safe learning environment.

#### 18. `quiz` (Clinical Assessment Generation)
*   **Traditional Method**: Educators manually writing Multiple Choice Questions (MCQs), which is notoriously difficult to do well (e.g., creating plausible distractors).
*   **AI Augmentation**: AI generates high-quality medical assessments. It creates realistic distractors based on common clinical errors and provides detailed rationales for why the correct answer is right and why others are wrong, enhancing active learning.

#### 19. `refer` (Specialty Optimization)
*   **Traditional Method**: General practitioners referring to a broad specialty (e.g., "Surgery") without knowing if the patient needs a more specific sub-specialist (e.g., "Colorectal" vs. "Hepatobiliary").
*   **AI Augmentation**: AI analyzes clinical presentations to recommend the most appropriate medical sub-specialty. This ensures the patient sees the right expert the first time, reducing wait times and improving diagnostic accuracy.

#### 20. `roles` (Scope of Practice Reference)
*   **Traditional Method**: Confusion in interdisciplinary teams about who is responsible for what (e.g., "Can a Physician Assistant perform this specific procedure in this state?").
*   **AI Augmentation**: AI provides detailed mapping of roles and responsibilities within healthcare teams. It clarifies the scope of practice for various specialties, facilitating better communication and safer delegation in complex clinical environments.

#### 21. `surgery` (Operative Monographs)
*   **Traditional Method**: Reading sparse operative notes or watching videos that may not explain the "why" behind a specific technique or the evidence for postoperative benchmarks.
*   **AI Augmentation**: AI generates exhaustive procedural monographs. It covers preoperative optimization, intraoperative technical highlights, and specific postoperative recovery benchmarks (e.g., "When should the patient start mobilizing?"), providing a 360-degree view of the surgery.

#### 22. `tool` (Surgical Instrument Reference)
*   **Traditional Method**: Junior staff or students "learning on the fly" in the OR, which is stressful and prone to error (e.g., using the wrong forceps for delicate tissue).
*   **AI Augmentation**: AI provides a detailed reference for surgical instruments. It explains what each tool is for, how it should be handled, and its sterilization requirements, serving as a "digital mentor" for surgical trainees and scrub techs.

#### 23. `topic` (High-Level Subject Synthesis)
*   **Traditional Method**: Reading multiple Wikipedia entries or broad textbook chapters to get an overview of a complex field (e.g., "Immunotherapy in Oncology").
*   **AI Augmentation**: AI provides a structured, high-level synthesis of complex medical subjects. It identifies the "Pillars of Knowledge" for that topic, allowing a clinician to get up to speed on a new or unfamiliar field in minutes.

#### 24. `tray` (Surgical Setup Standardization)
*   **Traditional Method**: Senior scrub nurses relying on "preference cards" which are often outdated, leading to missing instruments and delays during surgery.
*   **AI Augmentation**: AI generates standardized setup lists for surgical instrument trays. It ensures that the specific instruments required for a procedure (e.g., "Laparoscopic Cholecystectomy Tray") are correctly identified and ready, streamlining OR throughput and safety.

---

### `anatomy`
*   **Problem**: Sourcing reliable anatomical data (innervation, blood supply) is slow.
*   **Usage**: Detailed research into specific body structures.
*   **Does**: Provides names, body systems, and functional mechanisms.
*   **Does NOT**: Analyze patient-specific medical images.
*   **Example**: `medkit-medical anatomy "Liver" --structured`

### `disease`
*   **Problem**: Clinicians need rapid access to etiology and standard-of-care treatments.
*   **Usage**: Retrieving comprehensive disease monographs.
*   **Does**: Covers pathophysiology, symptoms, and management.
*   **Example**: `medkit-medical disease "Hypertension" -s`

### `ethics`
*   **Problem**: Healthcare professionals face "gray area" decisions with no clear right answer.
*   **Usage**: Analyzing complex bioethical scenarios.
*   **Does**: Applies frameworks like Autonomy and Justice.
*   **Example**: `medkit-medical ethics "Confidentiality vs public safety"`

### `flashcard`
*   **Problem**: Dense jargon on medical labels is inaccessible to many.
*   **Usage**: Extraction and explanation of medical labels from images.
*   **Does**: Uses OCR to find terms and provides professional definitions.
*   **Example**: `medkit-medical flashcard "label_image.jpg" --structured`

### `history`
*   **Problem**: Unstructured intake results in missing clinical data.
*   **Usage**: Standardizing targeted history-taking questions.
*   **Does**: Tailors questions to age, gender, and purpose.
*   **Example**: `medkit-medical history -e "Physical" -a 45 -g "Male" -s`

*(Note: All 24+ medical subcommands like `advise`, `decision`, `facts`, `faq`, `herbal`, `implant`, `myth`, `organ`, `pose`, `procedure`, `quiz`, `refer`, `roles`, `surgery`, `tool`, `tray` accept the `--structured` argument.)*

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
