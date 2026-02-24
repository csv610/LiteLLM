# MedKit Exhaustive CLI Reference

This manual is the definitive technical guide for MedKit. Every subcommand is detailed from an end-user perspective, focusing on clinical utility, safety boundaries, and technical parameters.

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
**9 Specialized Subcommands for Medication Management**

*   **Global Arguments**:
    *   **`-s, --structured`**: Returns drug data in a machine-readable JSON format.

### `interact`
*   **Problem**: Multidrug regimens increase life-threatening interaction risks.
*   **Usage**: Screening for drug-drug interactions.
*   **Does**: Identifies Major, Moderate, and Minor severity interactions.
*   **Example**: `medkit-drug interact "Warfarin" "Aspirin" --structured`

### `disease`
*   **Problem**: Certain drugs are lethal if the patient has a secondary disease.
*   **Usage**: Checking drug-disease safety.
*   **Does**: Flags risks like Beta-blockers in Asthma patients.
*   **Example**: `medkit-drug disease "Ibuprofen" "Kidney Disease" -s`

### `info`
*   **Problem**: Clinicians need deeper monographs than simple definitions.
*   **Usage**: Professional medication reference.
*   **Does**: MOA, pharmacokinetics, and standard adult dosing.
*   **Example**: `medkit-drug info "Lisinopril" --structured`

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

## 🧪 `medkit-diagnostics` (Tests & Devices)
**Laboratory and Diagnostic Hardware Reference**

*   **Global Arguments**:
    *   **`-s, --structured`**: Forces JSON output.

### `test`
*   **Usage**: Understanding the clinical utility and normal ranges of lab tests.
*   **Example**: `medkit-diagnostics test "HbA1c" -s`

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
