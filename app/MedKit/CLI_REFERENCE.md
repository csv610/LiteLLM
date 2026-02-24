# MedKit: Clinical Reference & Operations Manual

This document is the authoritative guide for MedKit. It is written from the perspective of the end-user (clinician, researcher, or developer) to ensure maximum utility and safety.

---

## 🤖 `medkit-agent` (The Orchestrator)
**"The Central Brain for Multi-Domain Queries"**

### 1. The Clinical Problem
Medical queries are rarely one-dimensional. A patient isn't just "a disease"; they are a collection of medications, symptoms, and history. Traditional tools require you to look up each piece separately.

### 2. Primary Usage
Use this when you have a complex scenario that requires "connecting the dots" between multiple MedKit tools (e.g., Drugs + Symptoms + Specialists).

### 3. Detailed Workflow (What it DOES)
*   **Intent Analysis**: Parses your natural language query to identify the underlying medical goals.
*   **Tool Selection**: Dynamically decides which sub-tools (e.g., `medkit-drug`, `medkit-medical`) are needed.
*   **Execution Loop**: Runs a multi-step "Reasoning" loop, feeding the output of one tool into the next.
*   **Synthesis**: Consolidates technical data into a coherent, professional response.

### 4. Technical Boundaries (What it DOES NOT Do)
*   **Legal Liability**: It does not assume liability for clinical decisions.
*   **Physical Monitoring**: It cannot interact with real-time patient monitors or hardware.

### 5. Failure Handling & Edge Cases
*   **Conflicting Data**: If `medkit-drug` says a drug is safe but `medkit-medical` notes a rare side effect, the agent will flag the discrepancy for human review rather than picking a "winner."
*   **Tool Failure**: If a sub-tool (like PubMed) is down, the agent will explicitly state: "I could not access research papers, but based on my static knowledge base..."

### 6. Real-World Scenario
> **User**: "Patient is a 70yo on Warfarin with a new persistent cough. Check for interactions and suggest if they should see a Pulmonologist."
> **Result**: The agent calls `medkit-drug` to check Warfarin interactions, `medkit-medical disease` to analyze the cough, and `medkit-medical refer` to validate the specialty.

---

## 🏥 `medkit-medical` (Knowledge Engine)
**"The Ultimate Clinical Fact-Checker"**

### `anatomy`
*   **The Problem**: Searching textbooks for blood supply or nerve innervation is slow.
*   **Primary Usage**: Instant retrieval of structured anatomical profiles.
*   **Does**: Provides official names, classifications, body systems, and functional mechanisms.
*   **Does NOT**: Analyze user-uploaded medical images (e.g., "Is this bone broken?").
*   **Edge Case**: Variations like "Situs Inversus" (mirrored organs) are handled as "Rare Variants" rather than standard anatomy.
*   **Example**: `medkit-medical anatomy "Left Ventricle"`

### `ethics`
*   **The Problem**: Healthcare professionals often face "gray area" decisions where there is no clear right answer.
*   **Primary Usage**: Structuring an ethical argument for a hospital committee or review board.
*   **Does**: Evaluates a scenario against the four pillars: Autonomy, Beneficence, Non-maleficence, and Justice.
*   **Does NOT**: Provide a "Pass/Fail" or "Legal/Illegal" judgment.
*   **Handling Failure**: If the scenario is too vague, it will ask for the "Stakeholders" involved before proceeding.
*   **Example**: `medkit-medical ethics "Withholding treatment from a non-compliant patient"`

### `flashcard`
*   **The Problem**: Reading medication bottles or medical labels with dense jargon.
*   **Primary Usage**: Converting visual labels into understandable clinical definitions.
*   **Does**: Uses OCR to extract terms from a photo and generates a 2-sentence "Flashcard" explanation for each.
*   **Does NOT**: Identify the *pill* itself by color/shape (only reads text).
*   **Failure Mode**: If the image is blurry, it returns "Unreadable Label" rather than guessing.
*   **Example**: `medkit-medical flashcard "/path/to/prescription_bottle.jpg"`

---

## 💊 `medkit-drug` (Pharmacology)
**"Safety First Medication Management"**

### `interact`
*   **The Problem**: Polypharmacy (taking multiple drugs) is a leading cause of hospitalizations due to unknown interactions.
*   **Primary Usage**: Safety-screening a patient’s entire medication list in one command.
*   **Does**: Identifies Major (Life-threatening), Moderate, and Minor interactions.
*   **Does NOT**: Account for the *time of day* meds are taken unless specified.
*   **Edge Case**: "Cumulative Toxicity"—where three drugs all have a small effect on the kidneys that adds up to a large problem.
*   **Example**: `medkit-drug interact "Lisinopril" "Spironolactone" "Ibuprofen"`

### `disease`
*   **The Problem**: Some drugs are "good" for a condition but "lethal" if the patient has a secondary disease (e.g., Beta-blockers in Asthma).
*   **Primary Usage**: Checking if a drug is safe for a specific patient's comorbidities.
*   **Does**: Flags absolute contraindications and "Use with Caution" warnings.
*   **Does NOT**: Calculate pediatric weight-based dosages.
*   **Failure Handling**: If the disease is misspelled, it uses medical-weighted fuzzy matching (e.g., "Astma" -> "Asthma").
*   **Example**: `medkit-drug disease "Propranolol" "Asthma"`

---

## 📊 `medkit-graph` (Reasoning Engine)
**"Visualizing the Logic of Medicine"**

*   **The Problem**: Medical text is dense. It’s hard to see the causal links between a gene, a protein, and a symptom.
*   **Primary Usage**: Converting a research paper or clinical note into a visual map.
*   **Does**: Extracts "Triples" (Subject -> Action -> Object) and creates a clickable graph.
*   **Does NOT**: Verify if the input text is a lie; it only maps what you tell it.
*   **Edge Case**: Circular reasoning in text (e.g., "A causes B, B causes A") is visualized as a loop.
*   **Example**: `medkit-graph pathophysiology "Fever triggers cytokine release which resets the hypothalamus."`

---

## 🛡️ `medkit-privacy` (Compliance)
**"The HIPAA Safeguard"**

*   **The Problem**: Developing medical apps is risky due to data privacy laws.
*   **Primary Usage**: Automating the administrative overhead of HIPAA compliance.
*   **Does**: Generates audit logs, captures formal consent, and scrubs PII (Names/SSNs) from data.
*   **Does NOT**: Replace your lawyer or your server's firewall.
*   **Failure Mode**: If the "mask" command sees a name that is also a common word (e.g., "Patient Joy"), it flags it for "Manual Verification" to ensure it doesn't accidentally delete medical meaning.
*   **Example**: `medkit-privacy mask "Patient John Doe (DOB 01/01/1980) presents with chest pain."`

---

## 📋 `medkit-exam` (Clinical Protocols)
**"Standardizing the Physical Touch"**

*   **The Problem**: Skipping a step in a physical exam can lead to a missed diagnosis.
*   **Primary Usage**: A digital checklist for residents, students, or nurses performing exams.
*   **Does**: Provides the standardized sequence (Inspection -> Palpation -> Percussion -> Auscultation).
*   **Does NOT**: Sense the patient's body; it is a reference guide for the human performing the exam.
*   **Handling Failure**: Provides "Red Flag" warnings for every exam (e.g., "If patient has X, stop exam and call 911").
*   **Example**: `medkit-exam --list` (Lists 28+ protocols like Cardiac, Neuro, Ortho)

---

## 🔍 `medkit-recognizer` (NER)
**"Turning Notes into Data"**

*   **The Problem**: 80% of medical data is "trapped" in unstructured text notes.
*   **Primary Usage**: Cleaning up messy doctor notes into a format a database can understand.
*   **Does**: Extracts 19 types of entities including `Pathogens`, `Lab Units`, and `Genetic Variants`.
*   **Does NOT**: Understand context like "I thought about giving the drug but didn't." It only extracts the mention of the drug.
*   **Edge Case**: "Acronym Overlap"—it uses LLM context to decide if "PE" means "Pulmonary Embolism" or "Physical Exam."
*   **Example**: `medkit-recognizer med_class "Patient needs to start a high-intensity statin."`
