# SANE Interview Assistant (Trauma-Informed)

A specialized command-line interface (CLI) tool designed to assist Sexual Assault Nurse Examiners (SANE) in conducting comprehensive, trauma-informed medical-forensic interviews.

This tool ensures a structured yet flexible interview process, prioritizing patient consent, comfort, and data integrity.

## Project Structure

*   **`sane_interview_cli.py`**: The main entry point for the application. It handles user input/output and runs the interview loop.
*   **`sane_interview.py`**: Contains the core logic for the interview flow (`SANEInterview` class) and state management. It defines the sequence of questions and conditional logic based on patient responses.
*   **`sane_interview_models.py`**: Defines the data structures (Pydantic models) used to store the interview record securely and consistently.
*   **`llm_sane_interview.py`**: An advanced version of the interview logic that utilizes Large Language Models (LLM) to assist with suggestions and narrative generation.

## Question Reference & Explanations

The following reference details every question in the interview protocol. Specifically, it lists the **Explanation** text provided to the patient if they type `explain` (or ask for clarification) for that specific question.

### 1. Introduction and Consent

| Question | Explanation (Context Provided) |
| :--- | :--- |
| **"Do you understand the purpose of this examination and your rights during the process?"** | "The SANE exam is a specialized medical-forensic examination designed to provide you with medical care and to collect evidence if you choose to report the assault." |
| **"Do I have your permission to proceed with the medical examination?"** | "Your consent is required for the exam to proceed. You can stop or skip any part of the exam at any time." |
| **"Would you like someone (advocate, friend, or family member) to be with you during the exam?"** | "Having a support person can help you feel safer and more comfortable during the examination process." |

### 2. General Medical History

*   *Note: Standard medical history questions (allergies, medications) generally do not require complex explanations but can be skipped if the patient is uncomfortable.*

### 3. Incident History

| Question | Explanation (Context Provided) |
| :--- | :--- |
| **"Can you tell me, in your own words, what happened?"** | "Your narrative helps us understand the context of the assault, which guides both your medical care and the collection of forensic evidence." |
| **"Were any weapons used or threats made?"** | "Information about weapons or threats is important for assessing your safety and for legal documentation of the assault." |
| **"Did you lose consciousness at any point?"** | "Loss of consciousness can indicate head trauma or the use of substances, which requires specific medical evaluation." |
| **"Were you forced to drink alcohol, take drugs, or any substances?"** | "This helps us determine if toxicology testing is needed and if any substances might interact with medications we provide today." |

### 4. Sexual Contact Details

| Question | Explanation (Context Provided) |
| :--- | :--- |
| **"What parts of your body were touched or penetrated?"** | "Knowing the specific types of contact helps us identify where to collect DNA evidence and where to check for potential injuries." |
| **"Did the person finish (ejaculate)?"** | "This information is critical for locating and collecting potential DNA evidence." |

### 5. Injury and Pain Assessment

| Question | Context |
| :--- | :--- |
| **"Do you have any pain right now?"** | Used to triage immediate pain management needs. |
| **"Did the person hit, slap, kick, bite, or strangle (choke) you?"** | Identifies specific mechanisms of injury to guide the physical exam. |

### 6. Forensic Evidence Collection

*   *Note: Questions about post-assault activities (showering, changing clothes) are used to determine if evidence may have been washed away or contaminated.*

### 7. Treatment Discussion

*   *Note: Questions regarding STI prophylaxis and emergency contraception are standard medical care discussions.*

### 8. Emotional & Psychological Assessment

*   *Note: These questions screen for acute distress and safety planning needs (e.g., suicide risk).*

### 9. Legal & Follow-Up

| Question | Explanation (Context Provided) |
| :--- | :--- |
| **"Would you like me to explain how reporting works?"** | **Detailed Text:** "There are different ways to report what happened... 1. Forensic Medical Report (Non-Reporting)... 2. Police Report... 3. Anonymous/Jane Doe Report... Regardless of your choice, you are entitled to medical care." |

### 10. Closure

| Question | Explanation (Context Provided) |
| :--- | :--- |
| **"Would you like me to review your next steps...?"** | **Detailed Text:** "Let's review the next steps for your care: 1. Medical Follow-up... 2. STI Testing... 3. Support Services... 4. Evidence... 5. Safety..." |

## AI-Assisted Features (`llm_sane_interview.py`)

The advanced version of the tool incorporates LLM-powered assistance to improve documentation quality:

*   **Contextual Suggestions:** Based on the patient's narrative, the AI suggests specific follow-up questions (e.g., if "choking" is mentioned, it suggests asking about breathing difficulties).
*   **Priority Ranking:** Suggestions are categorized as CRITICAL, High, Medium, or Low priority.
*   **Nurse-in-the-Loop:** All AI suggestions must be reviewed and accepted by the nurse before being asked.
*   **Safety Detection:** Automatically flags potential indicators of trafficking or self-harm for immediate clinical attention.

## Interaction Guide & Commands

| Command | Short | Description | Action Taken |
| :--- | :--- | :--- | :--- |
| **YES** | `yes`, `y` | **Affirmative** | Records `YES` and triggers relevant follow-ups. |
| **NO** | `no`, `n` | **Negative** | Records `NO` and skips irrelevant follow-ups. |
| **UNSURE** | `unsure`, `u` | **Uncertainty** | Records `UNSURE`. |
| **SKIP** | `skip` | **Decline** | Records `DECLINED` and moves to next section. |
| **EXPLAIN** | `explain` | **Info Request** | Displays context/rationale without recording an answer. |

## Data Privacy & Safety

*   **Anonymity:** Uses patient identifiers instead of names.
*   **Local Processing:** Designed for local execution to protect sensitive health information (PHI).
*   **Empowerment:** The "Skip" feature ensures the patient maintains agency over their story.
