"""update_question_ids - Batch update JSON question files to standardize field names.

This module processes JSON exam question files and standardizes field names for consistency.
It replaces deprecated field names (question_number, answer_method, follow_up_prompts) with
current standard names (id, responder, followup_questions). Processes entire outputs directory
in batch, generating default follow-up questions if none exist, enabling seamless schema
migration and data consistency across question files.

QUICK START:
    Update all question JSON files in the outputs directory:

    $ python update_question_ids.py

    The script will:
    - Replace question_number with id
    - Replace answer_method with responder
    - Replace/update follow_up_prompts with followup_questions
    - Generate default questions if none provided
    - Report count of updated files

    Or use programmatically:

    >>> from update_question_ids import update_json_file
    >>> updated = update_json_file("exam_file.json")
    >>> print(f"Updated: {updated}")

COMMON USES:
    1. Schema migration - updating to new question field names
    2. Batch updates - processing multiple exam files consistently
    3. Data standardization - ensuring uniform question structure
    4. Question generation - populating missing follow-up questions
    5. File processing - automated bulk field renaming

KEY FEATURES AND COVERAGE AREAS:
    - Field Renaming: question_number → id, answer_method → responder
    - Follow-up Questions: manages follow_up_prompts/followup_questions field
    - Default Generation: creates 5 generic follow-up questions if missing
    - Batch Processing: updates all JSON files in outputs directory
    - Structure Detection: identifies and processes question_data format
    - Error Handling: catches JSON and data structure errors gracefully
    - Flexible Updates: preserves existing data while adding defaults
    - Status Reporting: logs all processed files and update count
"""

import json
import os


def update_json_file(file_path):
    """Update a single JSON file to replace 'question_number' with 'id'."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if this is a questions file with the expected structure
        if 'questions_data' in data and 'questions' in data['questions_data']:
            updated = False
            for question in data['questions_data']['questions']:
                # Rename fields if they exist
                if 'question_number' in question:
                    question['id'] = question.pop('question_number')
                    updated = True
                if 'answer_method' in question:
                    question['responder'] = question.pop('answer_method')
                    updated = True
                # Handle follow-up questions
                if 'follow_up_prompts' in question:
                    # If there are existing follow-up prompts, use them as followup_questions
                    if question['follow_up_prompts'] and len(question['follow_up_prompts']) > 0:
                        question['followup_questions'] = question.pop('follow_up_prompts')
                    else:
                        # Generate 5 generic follow-up questions if none exist
                        question['followup_questions'] = [
                            "Can you tell me more about that?",
                            "How does this affect your daily activities?",
                            "When did you first notice this?",
                            "What makes it better or worse?",
                            "Have you discussed this with your healthcare provider before?"
                        ]
                        question.pop('follow_up_prompts', None)
                    updated = True
                elif 'followup_questions' not in question:
                    # If neither follow_up_prompts nor followup_questions exist, add default ones
                    question['followup_questions'] = [
                        "Can you tell me more about that?",
                        "How does this affect your daily activities?",
                        "When did you first notice this?",
                        "What makes it better or worse?",
                        "Have you discussed this with your healthcare provider before?"
                    ]
                    updated = True
            
            if updated:
                # Save the updated data back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                return True
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error processing {file_path}: {e}")
    return False

def cli():
    # Get the outputs directory path
    outputs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    
    if not os.path.exists(outputs_dir):
        print(f"Error: Outputs directory not found at {outputs_dir}")
        return
    
    # Process all JSON files in the outputs directory
    updated_count = 0
    for filename in os.listdir(outputs_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(outputs_dir, filename)
            if update_json_file(file_path):
                print(f"Updated: {filename}")
                updated_count += 1
    
    print(f"\nUpdate complete. {updated_count} files were updated.")

if __name__ == "__main__":
    cli()
