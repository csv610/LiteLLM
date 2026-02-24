# MedKit Exhaustive CLI Reference

This manual is the definitive technical guide for MedKit. Every subcommand is detailed from an end-user perspective, focusing on clinical utility, safety boundaries, and error handling.

---

## 🏥 `medkit-medical` (Clinical Knowledge Engine)
**Standardized Reference for 24+ Medical Domains**

### 1. `anatomy`
*   **Problem**: Sourcing reliable anatomical data (innervation, blood supply) is time-consuming.
*   **Usage**: Detailed research into specific body structures.
*   **Does**: Provides names, body systems, embryological origin, and functional mechanisms.
*   **Does NOT**: Analyze patient-specific medical images.
*   **Edge Case**: Rare anatomical variations may be listed as "Variable."
*   **Example**: `medkit-medical anatomy "Liver"`

### 2. `disease`
*   **Problem**: Clinicians need rapid access to etiology and standard-of-care treatments.
*   **Usage**: Retrieving comprehensive disease monographs.
*   **Does**: Covers pathophysiology, symptoms, diagnostic criteria, and management.
*   **Does NOT**: Provide individual patient prognosis.
*   **Edge Case**: Newer clinical trials might not yet be integrated.
*   **Example**: `medkit-medical disease "Hypertension"`

### 3. `herbal`
*   **Problem**: Patients often use supplements that interact with conventional meds.
*   **Usage**: Researching evidence levels and safety for natural remedies.
*   **Does**: Lists active compounds, clinical evidence, and drug interactions.
*   **Does NOT**: Endorse supplements over evidence-based medicine.
*   **Example**: `medkit-medical herbal "Turmeric"`

### 4. `advise`
*   **Problem**: Minor health concerns often require triage-style home management.
*   **Usage**: Primary health care guidance for patients or providers.
*   **Does**: Offers self-care steps and "When to see a doctor" warnings.
*   **Does NOT**: Provide definitive diagnosis or replace emergency care.
*   **Example**: `medkit-medical advise "Managing mild fever at home"`

### 5. `decision`
*   **Problem**: High-pressure clinical environments require structured logic for workups.
*   **Usage**: Clinical decision-making guides based on symptoms.
*   **Does**: Provides logic trees and immediate "next steps."
*   **Does NOT**: Substitute for board-certified clinical judgment.
*   **Example**: `medkit-medical decision "Acute Cough"`

### 6. `facts`
*   **Problem**: Medical misinformation spreads rapidly in the public domain.
*   **Usage**: Verifying or debunking specific medical claims.
*   **Does**: Cross-references claims against peer-reviewed consensus.
*   **Does NOT**: Act as a real-time conversational lie detector.
*   **Example**: `medkit-medical facts "Vaccines cause autism"`

### 7. `faq`
*   **Problem**: Creating patient-facing documentation is repetitive.
*   **Usage**: Automating patient education materials.
*   **Does**: Generates common questions and plain-language professional answers.
*   **Does NOT**: Answer patient-specific physiological questions.
*   **Example**: `medkit-medical faq "Asthma"`

### 8. `implant`
*   **Problem**: Unknown implant specs pose risks (e.g., in MRI suites).
*   **Usage**: Reference for surgical hardware and medical devices.
*   **Does**: Lists materials, indications, and MRI safety protocols.
*   **Does NOT**: Provide real-time device tracking or battery status.
*   **Example**: `medkit-medical implant "Pacemaker"`

### 9. `myth`
*   **Problem**: Harmful medical myths persist despite scientific evidence.
*   **Usage**: Educating patients and debunking persistent misconceptions.
*   **Does**: Explains the myth's origin and the science that refutes it.
*   **Does NOT**: Debate non-scientific conspiracy theories.
*   **Example**: `medkit-medical myth "We use 10% of our brain"`

### 10. `procedure`
*   **Problem**: Residents and students need step-by-step guidance for non-surgical tasks.
*   **Usage**: Educational breakdown of clinical procedures.
*   **Does**: Lists equipment, technique steps, and complications.
*   **Does NOT**: Certify competence or allow untrained performance.
*   **Example**: `medkit-medical procedure "Lumbar Puncture"`

### 11. `eval-procedure`
*   **Problem**: Procedure documentation quality varies significantly.
*   **Usage**: Auditing and evaluating medical procedure reports.
*   **Does**: Scores documentation based on completeness and safety.
*   **Does NOT**: Evaluate the *skill* of the operator, only the documentation.
*   **Example**: `medkit-medical eval-procedure "report.json"`

### 12. `quiz`
*   **Problem**: Assessing clinical knowledge requires high-quality question sets.
*   **Usage**: Generating MCQ assessments for students or staff.
*   **Does**: Creates questions, distractors, and rationales.
*   **Does NOT**: Store student records or manage LMS integration.
*   **Example**: `medkit-medical quiz "Cardiology"`

### 13. `refer`
*   **Problem**: Symptoms often fall between multiple medical specialties.
*   **Usage**: Identifying the correct specialty for a clinical presentation.
*   **Does**: Maps complex symptoms to board-certified specialties.
*   **Does NOT**: Schedule appointments or provide doctor lists.
*   **Example**: `medkit-medical refer "Chest pain and dyspnea"`

### 14. `roles`
*   **Problem**: Healthcare professional roles vary by jurisdiction and specialty.
*   **Usage**: Clarifying scope of practice and clinical responsibilities.
*   **Does**: Defines responsibilities for specialists (e.g., Surgeon vs. PA).
*   **Does NOT**: Handle specific state-by-state licensing law variations.
*   **Example**: `medkit-medical roles "Neurosurgeon"`

### 15. `topic`
*   **Problem**: General medical topics are often searched too broadly.
*   **Usage**: Rapid synthesis of any general medical subject.
*   **Does**: Provides high-level clinical summaries and key facts.
*   **Does NOT**: Replace deep-dive modules like `disease` or `anatomy`.
*   **Example**: `medkit-medical topic "Telemedicine Ethics"`

### 16. `organ`
*   **Problem**: Systemic diseases are best understood via organ-specific roles.
*   **Usage**: Physiological summaries of human organs.
*   **Does**: Covers primary functions and systemic impact.
*   **Does NOT**: Provide surgical-level topographical anatomy.
*   **Example**: `medkit-medical organ "Pancreas"`

### 17. `surgery`
*   **Problem**: Major operations require exhaustive pre- and post-op protocols.
*   **Usage**: Detailed monographs for surgical operations.
*   **Does**: Covers prep, technical approach, and recovery benchmarks.
*   **Does NOT**: Provide a guide for untrained individuals to operate.
*   **Example**: `medkit-medical surgery "Appendectomy"`

### 18. `pose`
*   **Problem**: Incorrect patient positioning leads to pressure sores and nerve injury.
*   **Usage**: Reference for surgical patient positioning.
*   **Does**: Describes positions and lists safety risks (e.g., ulnar nerve).
*   **Does NOT**: Replace the physical check by the surgical team.
*   **Example**: `medkit-medical pose "Prone"`

### 19. `tool`
*   **Problem**: Identifying specialized surgical tools is difficult for trainees.
*   **Usage**: Reference for instruments and clinical hardware.
*   **Does**: Lists tool function, variants, and sterilization needs.
*   **Does NOT**: Interface with hospital inventory systems.
*   **Example**: `medkit-medical tool "Scalpel"`

### 20. `tray`
*   **Problem**: Inconsistent tray setups lead to delays in the OR.
*   **Usage**: Standardizing surgical instrument tray configurations.
*   **Does**: Lists every required instrument for a standard operation.
*   **Does NOT**: Account for individual surgeon "preference cards."
*   **Example**: `medkit-medical tray "Orthopedic"`

### 21. `case`
*   **Problem**: Realistic patient cases are needed for medical training.
*   **Usage**: Generating synthetic medical case reports.
*   **Does**: Creates a coherent history, exam, and laboratory narrative.
*   **Does NOT**: Represent a real, identifiable patient.
*   **Example**: `medkit-medical case "Type 2 Diabetes"`

### 22. `ethics`
*   **Problem**: Ethical dilemmas require structured, multi-pillar analysis.
*   **Usage**: Analyzing complex bioethical scenarios.
*   **Does**: Applies frameworks like Autonomy and Justice.
*   **Does NOT**: Provide legally binding rulings.
*   **Example**: `medkit-medical ethics "Patient confidentiality vs public safety"`

### 23. `history`
*   **Problem**: Unstructured intake results in missing clinical data.
*   **Usage**: Standardizing targeted history-taking questions.
*   **Does**: Tailors questions to age, gender, and purpose.
*   **Does NOT**: Record answers directly into an EMR.
*   **Example**: `medkit-medical history -e "Physical" -a 45 -g "Male"`

### 24. `flashcard`
*   **Problem**: Dense jargon on medical labels is inaccessible to many.
*   **Usage**: Extraction and explanation of medical labels from images.
*   **Does**: Uses OCR to find terms and provides professional definitions.
*   **Does NOT**: Identify pills by their physical appearance.
*   **Example**: `medkit-medical flashcard "label_image.jpg"`

---

## 💊 `medkit-drug` (Pharmacology & Safety)
**9 Specialized Subcommands for Medication Management**

### 1. `info`
*   **Problem**: Clinicians need deeper monographs than simple definitions.
*   **Usage**: Professional medication reference.
*   **Does**: MOA, pharmacokinetics, and standard adult dosing.
*   **Does NOT**: Perform pediatric weight-based dosing.
*   **Example**: `medkit-drug info "Lisinopril"`

### 2. `interact`
*   **Problem**: Multidrug regimens (polypharmacy) increase interaction risks.
*   **Usage**: Screening for drug-drug interactions.
*   **Does**: Identifies Major, Moderate, and Minor severity interactions.
*   **Does NOT**: Account for specific time-of-administration effects.
*   **Example**: `medkit-drug interact "Warfarin" "Aspirin"`

### 3. `food`
*   **Problem**: Dietary choices can nullify or amplify drug effects.
*   **Usage**: Identifying drug-food interactions.
*   **Does**: Identifies interactions with items like grapefruit or dairy.
*   **Does NOT**: Provide a complete personalized meal plan.
*   **Example**: `medkit-drug food "Metformin" "Grapefruit"`

### 4. `disease`
*   **Problem**: Certain drugs are contraindicated in specific comorbidities.
*   **Usage**: Checking drug-disease safety.
*   **Does**: Flags risks like Beta-blockers in Asthma patients.
*   **Does NOT**: Provide a final "Green Light" for prescribing.
*   **Example**: `medkit-drug disease "Ibuprofen" "Kidney Disease"`

### 5. `similar`
*   **Problem**: Medication shortages require therapeutic substitutions.
*   **Usage**: Finding therapeutic alternatives or drug class peers.
*   **Does**: Lists drugs with similar mechanisms or indications.
*   **Does NOT**: Guarantee equal efficacy for a specific patient.
*   **Example**: `medkit-drug similar "Ozempic"`

### 6. `compare`
*   **Problem**: Choosing between two similar drugs requires side-by-side data.
*   **Usage**: Professional medication comparison.
*   **Does**: Compares efficacy, half-life, and side-effect profiles.
*   **Does NOT**: Recommend which drug is "better" for a patient.
*   **Example**: `medkit-drug compare "Tylenol" "Advil"`

### 7. `symptoms`
*   **Problem**: Identifying common pharmacological treatments for a symptom set.
*   **Usage**: Mapping clinical symptoms to drug categories.
*   **Does**: Suggests OTC and prescription categories for reference.
*   **Does NOT**: Prescribe medication to the user.
*   **Example**: `medkit-drug symptoms "Migraine with aura"`

### 8. `addiction`
*   **Problem**: SUD management requires evidence-based withdrawal data.
*   **Usage**: Researching substance use and recovery.
*   **Does**: Provides withdrawal timelines and treatment options.
*   **Does NOT**: Provide active crisis or suicide counseling.
*   **Example**: `medkit-drug addiction "Oxycodone"`

### 9. `explain`
*   **Problem**: Complex pharmacology is often unintelligible to patients.
*   **Usage**: Plain-language patient education.
*   **Does**: Translates technical jargon into 5th-grade level terms.
*   **Does NOT**: Include high-level biochemical pathways.
*   **Example**: `medkit-drug explain "Amoxicillin"`

---

## 📊 `medkit-graph` (Logic Visualization)
**Maps 10 Domains into Knowledge Triples**

*   **Subcommands**: `anatomy`, `disease`, `genetic`, `medicine`, `pathophysiology`, `pharmacology`, `procedure`, `surgery`, `symptoms`, `test`.
*   **Primary Usage**: Converting medical text into structured Entity-Relation maps.
*   **Does**: Extracts triples (Subject -> Relation -> Object) and creates graphs.
*   **Does NOT**: Verify the medical truth of the input text.
*   **Edge Case**: Pronouns ("it", "this") may break logical links in the graph.
*   **Example**: `medkit-graph pathophysiology "Fever resets the hypothalamus."`

---

## 🔍 `medkit-recognizer` (Medical NER)
**19 Identifiers for Unstructured Text Extraction**

*   **Subcommands**: `abbreviation`, `anatomy`, `clinical_sign`, `coding`, `condition`, `device`, `disease`, `drug`, `genetic`, `imaging`, `lab_unit`, `med_class`, `pathogen`, `procedure`, `specialty`, `supplement`, `symptom`, `test`, `vaccine`.
*   **Primary Usage**: Extracting structured medical data from clinical notes.
*   **Does**: Identifies entities, categorizes them, and normalizes forms.
*   **Does NOT**: Understand clinical negation (e.g., "denies fever").
*   **Edge Case**: Typos in raw notes significantly degrade accuracy.
*   **Example**: `medkit-recognizer drug "Patient taking 10mg Lisinopril."`

---

## 🛡️ `medkit-privacy` (HIPAA Compliance)
**Automated Data Protection Workflows**

*   **Subcommands**: `audit`, `consent`, `mask`, `report`.
*   **Primary Usage**: Automating HIPAA compliance for medical applications.
*   **Does**: Logs access, captures consent, and scrubs PII from text.
*   **Does NOT**: Replace legal counsel or physical security.
*   **Example**: `medkit-privacy mask "Patient John Doe at 555-0199"`
