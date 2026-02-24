# MedKit Exhaustive CLI Reference

This manual provides detailed technical descriptions, primary usage scenarios, functional boundaries, and failure modes for the entire MedKit framework.

---

## 🤖 `medkit-agent`
**The Autonomous Medical Orchestrator**

*   **Primary Usage**: Solving high-level, multi-step clinical queries that require coordinating multiple data sources (e.g., "Identify this drug, check its interactions with the patient's existing meds, and find a relevant specialist").
*   **What it DOES**:
    *   Parses natural language intent.
    *   Executes a ReAct (Reasoning + Acting) loop.
    *   Calls other `medkit-*` tools as "tools" or "plugins."
    *   Synthesizes a final answer from multiple tool outputs.
*   **What it DOES NOT Do**:
    *   It is not a medical professional; it is a logic engine.
    *   It cannot perform physical actions or real-world diagnostics.
*   **Edge Cases**:
    *   **Infinite Loops**: Can get stuck if two tools provide contradictory info.
    *   **Hallucination**: If a tool fails, the agent might try to "guess" the missing data to fulfill the query.
*   **Example**:
    ```bash
    medkit-agent "Patient is a 65yo female with sudden onset of left-sided weakness. What are the priority diagnostic steps and potential specialist referrals?"
    ```

---

## 🏥 `medkit-medical`
**General Medical Knowledge & Clinical Tools**

### `advise`
*   **Primary Usage:** Providing evidence-based guidance for primary healthcare concerns and home management.
*   **Does:** Offers triage-style advice and self-care steps for minor ailments.
*   **Does NOT:** Provide a definitive diagnosis or emergency medical care.
*   **Edge Cases:** Struggles with vague symptoms like "I feel weird."
*   **Example:** `medkit-medical advise "Managing mild fever at home"`

### `anatomy`
*   **Primary Usage:** Deep-dive research into specific human anatomical structures.
*   **Does:** Provides classification, blood supply, innervation, and functional roles.
*   **Does NOT:** Interpret specific patient scans (X-rays/MRIs).
*   **Edge Cases:** May lack detail on rare anatomical variations (e.g., accessory muscles).
*   **Example:** `medkit-medical anatomy "Liver"`

### `case`
*   **Primary Usage:** Generating realistic, synthetic patient case reports for medical education and software testing.
*   **Does:** Creates a coherent narrative including history, physical exam, and labs for a specific condition.
*   **Does NOT:** Represent a real historical patient record.
*   **Edge Cases:** Sometimes generates "textbook-perfect" cases that lack the messiness of real-world comorbidities.
*   **Example:** `medkit-medical case "Type 2 Diabetes"`

### `decision`
*   **Primary Usage:** Clinical decision support for determining the next steps in a diagnostic workup.
*   **Does:** Provides logic trees or "if-then" scenarios based on presenting symptoms.
*   **Does NOT:** Replace the professional judgment of a physician.
*   **Edge Cases:** If critical vitals are missing, the suggested decision may be too conservative.
*   **Example:** `medkit-medical decision "Acute Cough"`

### `disease`
*   **Primary Usage:** Retrieving comprehensive clinical monographs for specific medical conditions.
*   **Does:** Details etiology, pathophysiology, clinical presentation, and standard treatment protocols.
*   **Does NOT:** Predict the prognosis of an individual patient.
*   **Edge Cases:** Rapidly evolving conditions (like new virus variants) may lag behind current research.
*   **Example:** `medkit-medical disease "Hypertension"`

### `ethics`
*   **Primary Usage:** Analyzing complex ethical dilemmas in healthcare (e.g., end-of-life care, AI in diagnostics).
*   **Does:** Applies established frameworks (Autonomy, Beneficence, Non-maleficence, Justice) to a scenario.
*   **Does NOT:** Provide a legally binding ruling or a single "correct" answer.
*   **Edge Cases:** Struggles with scenarios that have heavy cultural or religious specificities.
*   **Example:** `medkit-medical ethics "Patient confidentiality vs public safety"`

### `facts`
*   **Primary Usage:** Verifying or debunking specific medical statements found in the media or clinical literature.
*   **Does:** Cross-references statements against clinical guidelines and peer-reviewed consensus.
*   **Does NOT:** Act as a real-time "lie detector" for spoken conversation.
*   **Edge Cases:** Emerging science where no consensus yet exists will return an "inconclusive" or "variable evidence" result.
*   **Example:** `medkit-medical facts "Vaccines cause autism"`

### `faq`
*   **Primary Usage:** Automating the creation of patient education materials and frequently asked questions.
*   **Does:** Generates common questions and professional, plain-language answers for any medical topic.
*   **Does NOT:** Handle patient-specific questions ("Why is *my* leg hurting?").
*   **Edge Cases:** Can be overly verbose if the topic is too broad (e.g., "Cancer").
*   **Example:** `medkit-medical faq "Asthma"`

### `flashcard`
*   **Primary Usage:** Rapid extraction and explanation of medical terminology from visual labels or text lists.
*   **Does:** Performs OCR on images to find terms and provides 1-2 sentence clinical definitions for each.
*   **Does NOT:** Translate languages (it expects English medical terms).
*   **Edge Cases:** Blurred images or handwritten notes often result in failed extraction.
*   **Example:** `medkit-medical flashcard "label_image.jpg"`

### `herbal`
*   **Primary Usage:** Researching the safety, efficacy, and interactions of natural supplements and traditional medicines.
*   **Does:** Lists known active compounds, clinical evidence levels, and potential drug interactions.
*   **Does NOT:** Endorse "alternative" medicine over conventional evidence-based practice.
*   **Edge Cases:** Many herbs have very little high-quality clinical trial data, resulting in "limited evidence" warnings.
*   **Example:** `medkit-medical herbal "Turmeric"`

### `history`
*   **Primary Usage:** Standardizing the patient intake process by generating targeted history-taking questions.
*   **Does:** Provides a structured list of questions based on age, gender, and the purpose of the exam.
*   **Does NOT:** Record the patient's actual answers into an EMR automatically.
*   **Edge Cases:** May generate too many questions for a simple visit if the "purpose" is too broad.
*   **Example:** `medkit-medical history -e "Physical" -a 45 -g "Male"`

### `implant`
*   **Primary Usage:** Reference for technical and clinical information regarding surgical implants (pacemakers, joints).
*   **Does:** Describes materials, indications, common complications, and MRI compatibility notes.
*   **Does NOT:** Track individual serial numbers or recall statuses for specific batches.
*   **Edge Cases:** Proprietary/Brand-new devices might not be in the training set yet.
*   **Example:** `medkit-medical implant "Pacemaker"`

### `myth`
*   **Primary Usage:** Debunking widespread medical misconceptions (e.g., "Vaccines cause autism").
*   **Does:** Provides the origin of the myth and the scientific evidence that refutes it.
*   **Does NOT:** Debate "conspiracy theories" that lack any scientific basis.
*   **Edge Cases:** Cultural myths that are harmless (e.g., "Chicken soup cures colds") are treated with less scientific rigor.
*   **Example:** `medkit-medical myth "We use 10% of our brain"`

### `organ`
*   **Primary Usage:** Quick reference for organ-specific physiology and associated disease patterns.
*   **Does:** Summarizes the primary and secondary functions of an organ and its role in systemic disease.
*   **Does NOT:** Provide detailed surgical anatomy (use `anatomy` or `surgery` for that).
*   **Edge Cases:** Multiorgan systems (e.g., the HPA axis) are sometimes split awkwardly between individual organ commands.
*   **Example:** `medkit-medical organ "Pancreas"`

### `pose`
*   **Primary Usage:** Reference for correct patient positioning during specific surgical procedures.
*   **Does:** Describes positions (Lithotomy, Trendelenburg, etc.) and lists pressure-point risks and nerve safety notes.
*   **Does NOT:** Provide real-time intraoperative monitoring.
*   **Edge Cases:** Non-standard or "hybrid" positions used in robotic surgery might be missing.
*   **Example:** `medkit-medical pose "Prone"`

### `procedure`
*   **Primary Usage:** Step-by-step educational breakdown of non-surgical medical procedures (e.g., Lumbar Puncture).
*   **Does:** Lists indications, equipment needed, technique steps, and common complications.
*   **Does NOT:** Certify a user to perform the procedure.
*   **Edge Cases:** Pediatric vs. Adult variations might be merged unless specified in the query.
*   **Example:** `medkit-medical procedure "Knee Replacement"`

### `quiz`
*   **Primary Usage:** Generating assessment questions for medical students or clinical competency testing.
*   **Does:** Creates multiple-choice questions with rationales for the correct and incorrect answers.
*   **Does NOT:** Track scores or manage a student database.
*   **Edge Cases:** High difficulty settings can sometimes generate "trick" questions that rely on obscure trivia.
*   **Example:** `medkit-medical quiz "Cardiology"`

### `refer`
*   **Primary Usage:** Identifying the correct medical specialty or sub-specialty for a complex set of symptoms.
*   **Does:** Maps clinical findings to the appropriate board-certified specialty.
*   **Does NOT:** Book appointments or provide a list of local providers.
*   **Edge Cases:** Overlapping specialties (e.g., Nephrology vs. Urology for kidney stones) may return both.
*   **Example:** `medkit-medical refer "Chest pain and dyspnea"`

### `roles`
*   **Primary Usage:** Clarifying the scope of practice and responsibilities of different healthcare professionals.
*   **Does:** Defines what a specialist (e.g., Anesthesiologist vs. CRNA) can and cannot do.
*   **Does NOT:** Handle state-specific or country-specific licensing law variations.
*   **Edge Cases:** Rapidly changing "scope of practice" laws may not be reflected.
*   **Example:** `medkit-medical roles "Neurosurgeon"`

### `surgery`
*   **Primary Usage:** Detailed monographs for major surgical operations.
*   **Does:** Covers pre-op prep, technical approach, intra-op risks, and post-op recovery.
*   **Does NOT:** Provide a "how-to" guide for untrained individuals to operate.
*   **Edge Cases:** Experimental or "off-label" surgical techniques are excluded.
*   **Example:** `medkit-medical surgery "Appendectomy"`

### `tool`
*   **Primary Usage:** Reference for surgical instrumentation and medical equipment.
*   **Does:** Identifies the tool, its primary use, and sterilization requirements.
*   **Does NOT:** Interface with inventory management systems.
*   **Edge Cases:** Generic names (e.g., "Forceps") will return a list of many types rather than one.
*   **Example:** `medkit-medical tool "Scalpel"`

### `tray`
*   **Primary Usage:** Standardizing the "back table" setup for surgical technologists and nurses.
*   **Does:** Lists every instrument and consumable required for a specific standardized surgical tray.
*   **Does NOT:** Account for individual surgeon "preference cards."
*   **Edge Cases:** Local hospital naming conventions for trays may vary from the tool's output.
*   **Example:** `medkit-medical tray "Orthopedic"`

---

## 💊 `medkit-drug`
**Pharmacology & Medication Safety**

### `addiction`
*   **Primary Usage:** Clinical and social research into substance use disorders and recovery paths.
*   **Does:** Provides DSM-5 criteria, withdrawal timelines, and evidence-based treatment options (MAT).
*   **Does NOT:** Provide active crisis counseling or direct addiction therapy.
*   **Edge Cases:** New "designer drugs" (research chemicals) often have no data.
*   **Example:** `medkit-drug addiction "Oxycodone"`

### `compare`
*   **Primary Usage:** Side-by-side comparison of two drugs in the same or different classes.
*   **Does:** Compares efficacy, half-life, cost-profile, and side-effect frequency.
*   **Does NOT:** Recommend which drug is "better" for a specific patient.
*   **Edge Cases:** Comparing drugs with completely different indications (e.g., an antibiotic vs. a statin) provides low-value results.
*   **Example:** `medkit-drug compare "Tylenol" "Advil"`

### `disease`
*   **Primary Usage:** Identifying contraindications and necessary dosage adjustments for patients with specific comorbidities.
*   **Does:** Checks if a drug is safe for someone with, for example, Renal Failure or Myasthenia Gravis.
*   **Does NOT:** Provide a "Green Light" for prescribing; always requires physician oversight.
*   **Edge Cases:** Rare genetic conditions may not trigger a warning.
*   **Example:** `medkit-drug disease "Ibuprofen" "Kidney Disease"`

### `explain`
*   **Primary Usage:** Patient education and health literacy.
*   **Does:** Translates complex pharmacology into a 5th-grade reading level explanation.
*   **Does NOT:** Include technical details like cytochrome P450 metabolism.
*   **Edge Cases:** Over-simplification can sometimes miss critical "black box" warnings.
*   **Example:** `medkit-drug explain "Amoxicillin"`

### `food`
*   **Primary Usage:** Counseling patients on dietary restrictions while on medication.
*   **Does:** Identifies common interactions (e.g., Grapefruit juice and Statins, Leafy greens and Warfarin).
*   **Does NOT:** Provide a full "meal plan."
*   **Edge Cases:** Struggles with multi-ingredient processed foods.
*   **Example:** `medkit-drug food "Metformin" "Grapefruit"`

### `info`
*   **Primary Usage:** Rapid professional reference for drug monographs.
*   **Does:** Provides MOA, pharmacokinetics, standard adult dosing, and adverse reactions.
*   **Does NOT:** Provide pediatric weight-based calculations.
*   **Edge Cases:** Drug-drug combinations (e.g., Percocet) might be split into individual components.
*   **Example:** `medkit-drug info "Lisinopril"`

### `interact`
*   **Primary Usage:** Safety screening for polypharmacy patients.
*   **Does:** Identifies Major, Moderate, and Minor interactions between two or more drugs.
*   **Does NOT:** Account for the sequence of drug administration.
*   **Edge Cases:** "Interaction Fatigue" occurs when too many minor warnings are generated for common combinations.
*   **Example:** `medkit-drug interact "Warfarin" "Aspirin"`

### `similar`
*   **Primary Usage:** Finding therapeutic alternatives when a drug is out of stock or causes side effects.
*   **Does:** Lists drugs in the same class or with the same therapeutic goal.
*   **Does NOT:** Guarantee that the alternative will be as effective for that specific patient.
*   **Edge Cases:** May suggest an alternative that is much more expensive or requires different monitoring.
*   **Example:** `medkit-drug similar "Ozempic"`

### `symptoms`
*   **Primary Usage:** Reference tool for identifying common pharmacological treatments for a symptom set.
*   **Does:** Lists OTC and prescription options typically used for a symptom (e.g., "Neuropathic pain").
*   **Does NOT:** Recommend a specific drug for the user to take.
*   **Edge Cases:** Vague symptoms (e.g., "Tiredness") return too many unrelated drug categories.
*   **Example:** `medkit-drug symptoms "Neuropathic pain"`

---

## 📊 `medkit-graph`
**Medical Knowledge Graph Extraction**

### `anatomy`, `disease`, `medicine`, etc.
*   **Primary Usage:** Converting unstructured medical text into structured "Triples" (Subject -> Relation -> Object) for data science and visualization.
*   **Does:** Maps entities and their logical links (e.g., "Lisinopril --inhibits--> ACE").
*   **Does NOT:** Verify the medical truth of the input text.
*   **Edge Cases:**
    *   **Anaphora:** If the text says "This drug causes X," the tool may fail to identify what "This drug" refers to.
    *   **Complexity:** Extremely dense paragraphs can result in a "spiderweb" graph that is unreadable without filtering.
*   **Example:** `medkit-graph disease "Diabetes is a chronic condition caused by insulin resistance."`

---

## 🔍 `medkit-recognizer`
**Medical Entity Recognition (NER)**

### `drug`, `disease`, `symptom`, etc. (19 subcommands)
*   **Primary Usage:** High-accuracy extraction of medical entities from clinical notes for research or database population.
*   **Does:** Identifies the entity, its category, and often its standardized form (Normalization).
*   **Does NOT:** Understand clinical intent (e.g., "No signs of fever" might still extract "fever").
*   **Edge Cases:**
    *   **Abbreviations:** "MS" could be "Multiple Sclerosis" or "Mitral Stenosis" depending on context.
    *   **Spelling:** Typos in raw clinical notes significantly degrade extraction accuracy.
*   **Example:** `medkit-recognizer drug "Patient is taking 10mg of Lisinopril daily."`

---

## 📸 `medkit-media`
**Medical Image/Video Search & Analysis**

### `caption`
*   **Primary Usage:** Generating professional descriptions for medical images used in teaching or research.
*   **Does:** Identifies anatomy and pathology in a context-aware way.
*   **Does NOT:** Provide a diagnostic "Final Read" for a patient's scan.
*   **Edge Cases:** If the AI is not trained on a specific rare pathology, it will provide a generic description.
*   **Example:** `medkit-media caption "Rheumatoid hand x-ray"`

### `images`
*   **Primary Usage:** Sourcing visual aids for medical education.
*   **Does:** Downloads medical images from the web based on a query.
*   **Does NOT:** Filter for copyright or creative commons licenses automatically.
*   **Edge Cases:** Search "noise" can lead to non-medical images being downloaded if the query is ambiguous.
*   **Example:** `medkit-media images "Psoriasis plaques"`

### `summary`
*   **Primary Usage:** Rapidly digesting long-form medical video content or articles.
*   **Does:** Provides a structured summary of key learning points.
*   **Does NOT:** Replace the need to watch the full content for critical procedures.
*   **Edge Cases:** Summaries of highly technical lectures may lose nuanced data.
*   **Example:** `medkit-media summary "Laparoscopic cholecystectomy technique"`

### `videos`
*   **Primary Usage:** Finding educational medical content (procedures, lectures).
*   **Does:** Returns URLs and metadata for videos on the web.
*   **Does NOT:** Host the video files or remove ads from source sites.
*   **Edge Cases:** May return dead links or removed content.
*   **Example:** `medkit-media videos "CPR technique instructional"`

---

## 🧪 `medkit-diagnostics`
**Laboratory & Device Reference**

### `test`
*   **Primary Usage:** Understanding the clinical utility and normal ranges of lab tests.
*   **Does:** Explains *why* a test is ordered and what high/low values typically signify.
*   **Does NOT:** Interpret a specific patient's result.
*   **Edge Cases:** Normal ranges vary by lab/hospital; the tool provides a general "standard" range.
*   **Example:** `medkit-diagnostics test "HbA1c"`

### `device`
*   **Primary Usage:** Technical reference for diagnostic hardware.
*   **Does:** Covers physics of operation (e.g., how a CT works), indications, and safety.
*   **Does NOT:** Troubleshoot malfunctioning physical hardware.
*   **Edge Cases:** Newer "Point-of-Care" (POCUS) devices may have less documentation.
*   **Example:** `medkit-diagnostics device "MRI Scanner"`

---

## 📄 `medkit-article`
**PubMed & Research Search**

### `search`
*   **Primary Usage:** Evidence-based medicine research and literature review.
*   **Does:** Searches PubMed/BioMCP for the latest research on a disease.
*   **Does NOT:** Provide the full-text PDF (it provides the Abstract).
*   **Edge Cases:** Paywalled articles are not accessible beyond the abstract.
*   **Example:** `medkit-article search "Gout"`

### `cite`
*   **Primary Usage:** Generating bibliographies for medical papers or presentations.
*   **Does:** Formats research findings into standardized clinical citations.
*   **Does NOT:** Support every possible citation style (defaults to NLM/Vancouver).
*   **Example:** `medkit-article cite "Diabetes"`

---

## 🛡️ `medkit-privacy`
**Compliance & Data Governance**

### `audit`
*   **Primary Usage:** Maintaining a HIPAA-compliant record of all data access and modifications.
*   **Does:** Logs WHO accessed WHAT and WHEN into a secure, immutable-style JSON log.
*   **Does NOT:** Provide physical server security.
*   **Edge Cases:** If the session ID is lost, the audit trail becomes fragmented.
*   **Example:** `medkit-privacy audit --session "SESS123" --action "View Record" --role "Nurse"`

### `consent`
*   **Primary Usage:** Standardizing the informed consent process for digital health apps.
*   **Does:** Displays a HIPAA-standard notice and captures a digital "Yes/No" acknowledgement.
*   **Does NOT:** Serve as a replacement for a signed legal document in high-risk surgery.
*   **Example:** `medkit-privacy consent`

### `mask`
*   **Primary Usage:** De-identifying clinical text for research or sharing with LLMs.
*   **Does:** Uses regex and patterns to scrub Names, Phones, and Emails.
*   **Does NOT:** Guaranteed to find 100% of PII (especially handwritten or oddly formatted data).
*   **Edge Cases:** "Patient Rose" might not be masked if "Rose" is treated as a flower/common word.
*   **Example:** `medkit-privacy mask "Patient John Doe at 555-0199"`

### `report`
*   **Primary Usage:** Administrative oversight of data handling practices.
*   **Does:** Generates a high-level summary of active sessions and compliance status.
*   **Does NOT:** Automatically "fix" compliance violations.
*   **Example:** `medkit-privacy report`

---

## 🧠 `medkit-mental`
**Interactive Psychiatric Assessment**

*   **Primary Usage:** Preliminary screening for depression, anxiety, and other common mental health conditions.
*   **Does:** Conducts a structured conversation based on validated clinical scales.
*   **Does NOT:** Provide therapy, counseling, or emergency crisis intervention.
*   **Edge Cases:** **CRITICAL:** While it tries to detect self-harm risk, it is an AI and CAN miss cues. Never use for active crisis.
*   **Example:**
    ```bash
    medkit-mental
    ```

---

## ⚖️ `medkit-sane`
**Forensic Nursing Protocol**

*   **Primary Usage:** Standardizing the Sexual Assault Nurse Examiner (SANE) interview process.
*   **Does:** Guides the examiner through the legal and medical sequence required for a forensic exam.
*   **Does NOT:** Collect or store physical evidence (DNA kits).
*   **Edge Cases:** Highly traumatized patients may provide non-linear info that breaks the AI's "timeline" generation.
*   **Example:**
    ```bash
    medkit-sane start
    ```

---

## 📋 `medkit-codes`
**ICD-11 Diagnostic Coding**

*   **Primary Usage:** Mapping clinical descriptions to the official WHO ICD-11 diagnostic hierarchy.
*   **Does:** Searches the ICD-11 database and returns the most relevant diagnostic codes and their titles.
*   **Does NOT:** Handle billing (CPT) or insurance reimbursement logic.
*   **Edge Cases:** If the clinical description is too vague, it may return a "top-level" code (e.g., "Injury") instead of a specific one.
*   **Example:** `medkit-codes search "Asthma"`

---

## 📖 `medkit-dictionary`
**Medical Terminology Builder**

*   **Primary Usage:** Building and managing a custom structured medical glossary.
*   **Does:** Automates the generation of structured definitions and metadata for a large volume of medical terms.
*   **Does NOT:** Replace official medical dictionaries like Stedman's or Dorland's.
*   **Example:** `medkit-dictionary build`

---

## 📋 `medkit-exam`
**Standardized Physical Examination**

*   **Primary Usage:** Training or reference for performing standardized head-to-toe physical examinations.
*   **Does:** Lists 28+ standardized protocols (Heart, Lung, Neurological, etc.) and their required steps.
*   **Does NOT:** Perform the actual exam or provide real-time guidance during physical touch.
*   **Edge Cases:** Does not account for specialized "pediatric" or "geriatric" maneuvers unless specified.
*   **Example:**
    ```bash
    medkit-exam --list
    ```
