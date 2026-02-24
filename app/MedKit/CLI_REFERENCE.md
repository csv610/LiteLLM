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

## 💊 `medkit-drug` (Pharmacology & Safety)
**10 Specialized Subcommands for Medication Management**

*   **Global Arguments**:
    *   **`-s, --structured`**: Returns drug data in a machine-readable JSON format.

### `list`
*   **Primary Usage**: Discoverability tool to see all 10 pharmacology subcommands categorized by their clinical purpose.
*   **Does**: Prints a clean, descriptive table of every available drug module.
*   **Example**: `medkit-drug list`

#### Subcommand Catalog
| # | Subcommand | Primary Utility |
| :--- | :--- | :--- |
| 1 | **`addiction`** | Drug addiction, withdrawal symptoms, and recovery info. |
| 2 | **`compare`** | Side-by-side comparison of two specific medicines. |
| 3 | **`disease`** | Checking for drug-disease contraindications and safety. |
| 4 | **`explain`** | Plain-language medication explanations for patients. |
| 5 | **`food`** | Analysis of potential interactions between meds and foods. |
| 6 | **`info`** | Comprehensive drug monographs (MOA, dosing, side effects). |
| 7 | **`interact`** | Drug-drug interaction analysis between two medications. |
| 8 | **`similar`** | Finding therapeutic alternatives or similar medications. |
| 9 | **`symptoms`** | Suggesting drug categories for specific clinical symptoms. |

---

### 📘 Exhaustive Module Reference (Pharmacology)

The following sections provide a definitive guide to every `medkit-drug` module, detailing how AI augments traditional clinical practice.

#### `addiction`
*   **Problem**: Recovery requires clear info on withdrawal and support, which is often difficult to find in standardized monographs.
*   **Usage**: Substance abuse and recovery reference.
*   **Does**: Outlines symptoms, risks, and recovery pathways for specific drugs.
*   **Does NOT**: Provide clinical addiction treatment or professional counseling.
*   **AI Augmentation**: Outlines recovery pathways and withdrawal risks with scientific rigor, synthesizing data from multiple toxicology and recovery resources.
*   **Example**: `medkit-drug addiction "Fentanyl" -s`

#### `compare`
*   **Problem**: Choosing between two similar drugs for a specific patient profile requires manual cross-referencing of efficacy and safety data.
*   **Usage**: Side-by-side medication comparison.
*   **Does**: Highlights differences in MOA, side effects, and clinical utility.
*   **Does NOT**: Recommend one drug over another for a specific patient.
*   **AI Augmentation**: Performs multi-parametric comparison (MOA, safety, cost) to aid clinical choice, providing a comparative view that traditional monographs often lack.
*   **Example**: `medkit-drug compare "Atorvastatin" "Rosuvastatin" -s`

#### `disease`
*   **Problem**: Certain drugs are lethal if the patient has a secondary disease, and these contraindications can be easily missed.
*   **Usage**: Checking for drug-disease safety and contraindications.
*   **Does**: Flags risks like Beta-blockers in Asthma patients or NSAIDs in kidney disease.
*   **Does NOT**: Replace a full medical history review or pharmacy safety check.
*   **AI Augmentation**: Identifies potential contraindications between a drug and a specific disease state using advanced physiological reasoning.
*   **Example**: `medkit-drug disease "Ibuprofen" "Kidney Disease" -s`

#### `explain`
*   **Problem**: Clinical terminology confuses patients, leading to non-adherence and safety risks.
*   **Usage**: Generating simple, compassionate medication explanations for patients.
*   **Does**: Uses plain language to explain what a drug is, how it works, and how to take it.
*   **Does NOT**: Provide specific dosage instructions or therapeutic recommendations.
*   **AI Augmentation**: Generates compassionate, plain-language patient education materials to improve adherence and bridge the health literacy gap.
*   **Example**: `medkit-drug explain "Metformin"`

#### `food`
*   **Problem**: Many patients are unaware of dietary restrictions that can alter drug absorption or metabolism.
*   **Usage**: Checking for drug-food interactions.
*   **Does**: Identifies potential absorption issues or metabolic interference (e.g., grapefruit juice).
*   **Does NOT**: Provide comprehensive nutritional advice or meal plans.
*   **AI Augmentation**: Checks for clinically significant interactions between medications and specific foods or nutrients using metabolic pathway analysis.
*   **Example**: `medkit-drug food "Sertraline" "Grapefruit" -s`

#### `info`
*   **Problem**: Clinicians often need deeper monographs that include pharmacodynamics and adult dosing guidelines.
*   **Usage**: Professional medication reference and monograph retrieval.
*   **Does**: Covers MOA, pharmacodynamics, side effects, and standard adult dosing.
*   **Does NOT**: Provide real-time pricing, stock availability, or pediatric dosing by default.
*   **AI Augmentation**: Synthesizes professional monographs from diverse clinical sources, providing a unified view of MOA and pharmacodynamics.
*   **Example**: `medkit-drug info "Lisinopril" --structured`

#### `interact`
*   **Problem**: Multidrug regimens increase life-threatening interaction risks, which are complex to manage manually.
*   **Usage**: Screening for drug-drug interactions between multiple medications.
*   **Does**: Identifies Major, Moderate, and Minor severity interactions with physiological rationales.
*   **Does NOT**: Predict all possible idiosyncratic or rare adverse reactions.
*   **AI Augmentation**: Cross-checks multi-drug regimens for interaction severity and physiological mechanisms, acting as a redundant safety check for clinicians.
*   **Example**: `medkit-drug interact "Warfarin" "Aspirin" --structured`

#### `similar`
*   **Problem**: Allergies, side effects, or drug shortages require finding safe therapeutic alternatives.
*   **Usage**: Finding therapeutic substitutes within the same or similar drug classes.
*   **Does**: Identifies medications in the same class or with similar therapeutic utility.
*   **Does NOT**: Confirm bioequivalence for generic substitution (always consult a pharmacist).
*   **AI Augmentation**: Identifies therapeutic alternatives within the same chemical or functional class based on clinical indications.
*   **Example**: `medkit-drug similar "Lisinopril" -s`

#### `symptoms`
*   **Problem**: Rapidly identifying relevant drug classes for specific clinical symptoms is essential during initial diagnosis.
*   **Usage**: Symptom-to-medication category mapping for reference.
*   **Does**: Suggests relevant drug classes (not specific drugs) for clinical symptoms.
*   **Does NOT**: Recommend specific drugs for treatment or replace diagnostic protocols.
*   **AI Augmentation**: Maps clinical symptoms to physiological drug classes, aiding differential pharmacology and clinical reasoning.
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

*   **Global Argument**:
    *   **`-s, --structured`**: Outputs the extracted entities as a JSON object instead of a highlighted list.

### `list`
*   **Primary Usage**: Discoverability tool to see all 19 medical entity recognizers.
*   **Does**: Prints a clean, descriptive table of every available recognizer.
*   **Example**: `medkit-recognizer list`

#### Subcommand Catalog
| # | Subcommand | Primary Utility |
| :--- | :--- | :--- |
| 1 | **`abbreviation`** | Extracts and expands medical abbreviations and acronyms. |
| 2 | **`anatomy`** | Identifies anatomical structures and body parts. |
| 3 | **`clinical_sign`** | Detects objective clinical signs observed during examination. |
| 4 | **`coding`** | Extracts alphanumeric medical codes (ICD, CPT, etc.). |
| 5 | **`condition`** | Identifies broad medical conditions and pathologies. |
| 6 | **`device`** | Recognizes medical diagnostic and therapeutic devices. |
| 7 | **`disease`** | Extracts specific disease names and diagnoses. |
| 8 | **`drug`** | Identifies medications, generics, and brand names. |
| 9 | **`genetic`** | Recognizes genes, variants, and hereditary conditions. |
| 10 | **`imaging`** | Identifies radiological and diagnostic imaging modalities. |
| 11 | **`lab_unit`** | Extracts laboratory measurement units and values. |
| 12 | **`med_class`** | Categorizes medications into pharmacological classes. |
| 13 | **`pathogen`** | Identifies bacteria, viruses, and other microorganisms. |
| 14 | **`procedure`** | Recognizes surgical and clinical procedures. |
| 15 | **`specialty`** | Identifies medical specialties and sub-specialties. |
| 16 | **`supplement`** | Recognizes dietary supplements and nutraceuticals. |
| 17 | **`symptom`** | Detects subjective patient-reported symptoms. |
| 18 | **`test`** | Identifies laboratory and diagnostic tests. |
| 19 | **`vaccine`** | Recognizes immunizations and vaccine types. |

---

### 📘 Exhaustive Module Reference (NER & Extraction)

The following sections guide the use of MedKit’s 19 specialized entity recognizers, detailing how AI augments traditional medical NLP.

#### `abbreviation`
*   **Problem**: Unstructured medical notes are dense with ambiguous abbreviations (e.g., "PT" could mean Physical Therapy or Prothrombin Time).
*   **Usage**: Extraction and expansion of medical abbreviations within context.
*   **Does**: Identifies acronyms and provides the most likely clinical expansion based on surrounding text.
*   **Does NOT**: Resolve every possible non-medical abbreviation.
*   **AI Augmentation**: Uses context-aware reasoning to disambiguate medical acronyms, reducing the risk of misinterpretation in clinical documentation.
*   **Example**: `medkit-recognizer abbreviation "Patient started on PT for recovery." -s`

#### `anatomy`
*   **Problem**: Manually mapping body parts to systems in large datasets is labor-intensive.
*   **Usage**: Identification of anatomical entities in clinical or research text.
*   **Does**: Detects structures from microscopic (cells) to macroscopic (organs).
*   **Does NOT**: Provide functional physiological data (use `medkit-medical anatomy`).
*   **AI Augmentation**: Automates the tagging of anatomical structures across thousands of documents, enabling large-scale spatial research.
*   **Example**: `medkit-recognizer anatomy "Pain in the left distal radius." -s`

#### `clinical_sign`
*   **Problem**: Objective signs (e.g., "rebound tenderness") are often buried in narrative physical exam notes.
*   **Usage**: Extracting observed medical signs for structured reporting.
*   **Does**: Recognizes standardized clinical signs found in physical examinations.
*   **Does NOT**: Interpret the severity or significance of the sign.
*   **AI Augmentation**: Converts narrative physical exams into structured datasets of objective clinical markers.
*   **Example**: `medkit-recognizer clinical_sign "Positive Babinski sign noted." -s`

#### `coding`
*   **Problem**: Identifying alphanumeric codes like ICD-10 or CPT in text is error-prone for manual review.
*   **Usage**: Automated extraction of medical and billing codes.
*   **Does**: Detects patterns matching major medical coding systems.
*   **Does NOT**: Assign new codes or verify the accuracy of existing ones.
*   **AI Augmentation**: Rapidly identifies and categorizes existing codes within notes, streamlining billing and audit workflows.
*   **Example**: `medkit-recognizer coding "Diagnosis documented as ICD-10 I10." -s`

#### `condition`
*   **Problem**: General medical conditions are often described loosely, making data aggregation difficult.
*   **Usage**: Recognizing broad medical states, disorders, and conditions.
*   **Does**: Extracts a wide range of pathological states and disorders.
*   **Does NOT**: Differentiate between "active" and "historical" conditions without further agentic reasoning.
*   **AI Augmentation**: Clusters fragmented descriptions of health states into standardized "condition" entities for population health analysis.
*   **Example**: `medkit-recognizer condition "Chronic inflammatory state with fatigue." -s`

#### `device`
*   **Problem**: Medical devices are often mentioned by slang or vague descriptions in clinical notes.
*   **Usage**: Identifying diagnostic and therapeutic hardware.
*   **Does**: Recognizes everything from simple tools (stethoscopes) to complex implants (AICD).
*   **Does NOT**: Retrieve technical specifications (use `medkit-diagnose`).
*   **AI Augmentation**: Automates device tracking and vigilance by identifying equipment mentioned across clinical registries.
*   **Example**: `medkit-recognizer device "Patient has a Medtronic pacemaker." -s`

#### `disease`
*   **Problem**: Disease names have multiple synonyms and eponyms, complicating search and retrieval.
*   **Usage**: Extracting specific diagnoses and disease entities.
*   **Does**: Recognizes formal disease names, syndromes, and common variants.
*   **Does NOT**: Provide diagnostic evidence or management guidelines.
*   **AI Augmentation**: Normalizes varying nomenclature for the same disease state, ensuring consistent data extraction for researchers.
*   **Example**: `medkit-recognizer disease "Confirmed case of Graves' ophthalmopathy." -s`

#### `drug`
*   **Problem**: Medication lists in notes often mix generic names, brand names, and dosages.
*   **Usage**: Identification of pharmaceutical entities.
*   **Does**: Detects generic and brand-name medications.
*   **Does NOT**: Check for interactions (use `medkit-drug interact`).
*   **AI Augmentation**: Rapidly extracts medication mentions to build structured "Medication Reconciliation" datasets from raw text.
*   **Example**: `medkit-recognizer drug "Started on 5mg Amlodipine daily." -s`

#### `genetic`
*   **Problem**: Genetic nomenclature (e.g., BRCA1 c.5266dupC) is highly specialized and easily overlooked.
*   **Usage**: Recognizing genes, mutations, and hereditary patterns.
*   **Does**: Detects gene symbols, protein variants, and genetic disorders.
*   **Does NOT**: Interpret the clinical significance of a mutation.
*   **AI Augmentation**: Scales the extraction of genomic data from clinical reports, facilitating precision medicine research.
*   **Example**: `medkit-recognizer genetic "Positive for MTHFR mutation." -s`

#### `imaging`
*   **Problem**: Modality mentions (CT, MRI, PET) are often scattered throughout historical notes.
*   **Usage**: Identifying diagnostic imaging references.
*   **Does**: Recognizes imaging techniques and radiological modalities.
*   **Does NOT**: Analyze the actual image files.
*   **AI Augmentation**: Structures the "Imaging History" of a patient by identifying all radiological interventions mentioned in their record.
*   **Example**: `medkit-recognizer imaging "Scheduled for a contrast-enhanced CT scan." -s`

#### `lab_unit`
*   **Problem**: Laboratory values are meaningless without their specific units (e.g., mg/dL vs. mmol/L).
*   **Usage**: Extracting measurement units associated with lab results.
*   **Does**: Identifies standardized and non-standardized laboratory units.
*   **Does NOT**: Perform unit conversion or reference range checks.
*   **AI Augmentation**: Ensures that extracted numerical data is correctly paired with its clinical unit, preventing dangerous data entry errors.
*   **Example**: `medkit-recognizer lab_unit "Glucose measured at 110 mg/dL." -s`

#### `med_class`
*   **Problem**: Clinicians often remember a drug's class (e.g., "Statins") but need to find all specific instances in a record.
*   **Usage**: Categorizing medications into therapeutic or pharmacological classes.
*   **Does**: Recognizes broad drug categories and classes.
*   **Does NOT**: Provide specific drug monographs.
*   **AI Augmentation**: Automates the categorization of drugs, enabling "Class-level" safety audits across patient populations.
*   **Example**: `medkit-recognizer med_class "Patient is on several antihypertensives." -s`

#### `pathogen`
*   **Problem**: Microorganism names are complex and subject to frequent taxonomic changes.
*   **Usage**: Identifying bacteria, viruses, fungi, and parasites.
*   **Does**: Recognizes pathogen names across clinical and research text.
*   **Does NOT**: Recommend antimicrobial therapy.
*   **AI Augmentation**: Supports biosurveillance by identifying specific infectious agents mentioned in microbiology reports or public health data.
*   **Example**: `medkit-recognizer pathogen "Culture positive for S. aureus." -s`

#### `procedure`
*   **Problem**: Clinical procedures range from minor (blood draw) to major (CABG), making manual classification difficult.
*   **Usage**: Recognizing surgical and non-surgical clinical procedures.
*   **Does**: Extracts a wide array of medical interventions and procedures.
*   **Does NOT**: Explain the procedure (use `medkit-medical procedure`).
*   **AI Augmentation**: Builds a structured "Interventional Timeline" by identifying every procedure mentioned in a patient's longitudinal record.
*   **Example**: `medkit-recognizer procedure "Underwent urgent cholecystectomy." -s`

#### `specialty`
*   **Problem**: Determining which specialist saw a patient requires reading through signatures and letterheads.
*   **Usage**: Identifying medical specialties and sub-specialties.
*   **Does**: Detects mentions of clinical specialties (e.g., "Oncology", "Pediatrics").
*   **Does NOT**: Verify the credentials of the mentioned specialty.
*   **AI Augmentation**: Automatically routes documents or extracts "Consultation Histories" by identifying the specialties involved in a case.
*   **Example**: `medkit-recognizer specialty "Referred to Endocrinology for further workup." -s`

#### `supplement`
*   **Problem**: Supplements are often not documented in the "Medications" section, leading to interaction risks.
*   **Usage**: Identifying nutraceuticals and dietary supplements.
*   **Does**: Detects vitamins, minerals, and herbal supplements.
*   **Does NOT**: Check for drug-supplement interactions (use `medkit-drug`).
*   **AI Augmentation**: Captures the "hidden" medication list by identifying supplements mentioned in narrative "social history" or "dietary" notes.
*   **Example**: `medkit-recognizer supplement "Taking 2000IU Vitamin D3 daily." -s`

#### `symptom`
*   **Problem**: Subjective symptoms are often described using varied language (e.g., "short of breath" vs. "dyspnea").
*   **Usage**: Detecting subjective patient-reported symptoms.
*   **Does**: Recognizes symptoms and complaints reported by the patient.
*   **Does NOT**: Correlate symptoms to a diagnosis (use `medkit-medical decision`).
*   **AI Augmentation**: Extracts and standardizes subjective complaints, enabling better tracking of "Patient Reported Outcomes" (PROs).
*   **Example**: `medkit-recognizer symptom "Complaining of nocturnal diaphoresis." -s`

#### `test`
*   **Problem**: Clinical notes often mention "orders" for tests that need to be tracked for completion.
*   **Usage**: Identifying laboratory and diagnostic tests.
*   **Does**: Recognizes the names of medical tests and panels.
*   **Does NOT**: Provide test utility or normal ranges (use `medkit-diagnose`).
*   **AI Augmentation**: Automates the extraction of "Ordered Tests" from plan sections, ensuring better clinical follow-through.
*   **Example**: `medkit-recognizer test "Order CBC and Chem-7." -s`

#### `vaccine`
*   **Problem**: Immunization records are often fragmented across multiple systems.
*   **Usage**: Recognizing vaccines and immunization types.
*   **Does**: Identifies specific vaccine names and broad vaccine categories.
*   **Does NOT**: Verify the patient's actual immunization status.
*   **AI Augmentation**: Builds structured "Immunization Summaries" from raw pediatric or travel medicine notes.
*   **Example**: `medkit-recognizer vaccine "Received second dose of mRNA-1273." -s`

---

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

#### Subcommand Catalog
| # | Subcommand | Primary Utility |
| :--- | :--- | :--- |
| 1 | **`device`** | Get information about medical diagnostic and therapeutic devices. |
| 2 | **`test`** | Get information about medical laboratory and diagnostic tests. |

---

### 📘 Exhaustive Module Reference (Diagnostics)

The following sections provide a definitive guide to every `medkit-diagnose` module, detailing how AI augments traditional clinical practice.

#### `device`
*   **Problem**: Sourcing comprehensive data on medical devices (operating principles, safety specifications, and maintenance) requires searching fragmented manufacturer documentation.
*   **Usage**: Detailed research into medical hardware and diagnostic equipment.
*   **Does**: Provides technical specifications, clinical applications, operating principles, and safety considerations for medical devices.
*   **Does NOT**: Provide real-time repair instructions or individual device tracking.
*   **AI Augmentation**: Synthesizes complex hardware specifications and safety protocols into a unified reference, enabling rapid clinical and technical assessment of diagnostic equipment.
*   **Example**: `medkit-diagnose device "MRI Scanner" --structured`

#### `test`
*   **Problem**: Clinicians need rapid access to the clinical utility, normal ranges, and sample requirements for thousands of evolving medical laboratory tests.
*   **Usage**: Understanding the clinical utility and reference parameters of laboratory and diagnostic tests.
*   **Does**: Covers test purpose, indications, preparation, sample requirements, reference ranges, and interpretation guidelines.
*   **Does NOT**: Perform the actual laboratory analysis or provide real-time patient results.
*   **AI Augmentation**: Provides a dynamic, evidence-based reference for lab tests that includes nuanced interpretation guidelines and preparation requirements, acting as a "digital lab consultant."
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
