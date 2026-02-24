import argparse
import sys
from pathlib import Path

def list_exams():
    exams = [
        "abstract_reasoning", "anal_rectum_prostate", "arithmetic_calculation", "attention_span",
        "blood_vessels", "breast_axillae", "depression_screening", "ears_nose_throat",
        "emotional_stability", "female_genitalia", "head_and_neck", "heart", "judgement",
        "lungs_cheast", "lymphatic_system", "male_genitalia", "memory_ability",
        "musculoskeletal_core", "musculoskeletal_mvp", "musculoskeletal", "neurological",
        "neurology_system", "nutrition_growth", "skin_hair_nails", "writing_ability"
    ]
    print("\n📋 Available Physical Examination Protocols:\n")
    for exam in sorted(exams):
        print(f" - {exam.replace('_', ' ').title()}")
    print("\nUsage: These protocols are currently available as data models for clinical assessment.")

def main():
    parser = argparse.ArgumentParser(description="MedKit Physical Examinations CLI")
    parser.add_argument("-l", "--list", action="store_true", help="List available exam protocols")
    
    args = parser.parse_args()
    
    if args.list or len(sys.argv) == 1:
        list_exams()
    else:
        print("Use --list to see available examination protocols.")

if __name__ == "__main__":
    main()
