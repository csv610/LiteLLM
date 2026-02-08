from sane_interview import SANEInterview, Question
from sane_interview_models import YesNoUnsure
from lite.utils import save_model_response

def cli():
    """Main entry point for SANE Interview System"""
    print("="*60)
    print("🩺 SANE INTERVIEW SYSTEM")
    print("Sexual Assault Nurse Examiner - Trauma-Informed Interview")
    print("="*60)
    print("\nKey Principles:")
    print("• Patient has the right to decline any question")
    print("• Maintain nonjudgmental, supportive tone")
    print("• Document exact words when possible")
    print("• Allow pauses and breaks as needed")
    print("="*60 + "\n")

    interviewer = SANEInterview()
    last_answer = None
    
    try:
        while True:
            question = interviewer.get_next_question(last_answer)
            
            if question is None:
                break
                
            # Display the question text
            if question.type == "info":
                print(f"{question.text}")
                # If it's an informational pause
                if "Press Enter" in question.text:
                    input("")
                last_answer = ""
            else:
                while True:
                    print(f"\n{question.text}")
                    if question.type == "yes_no":
                        print("(yes/no/skip/explain)")
                    elif question.allow_skip:
                        print("(Type 'skip' to decline answering, or 'explain' for more info)")
                    else:
                        print("(Type 'explain' for more info)")
                    
                    response = input("Response: ").strip()
                    
                    if response.lower() == 'explain':
                        if question.explanation:
                            print(f"\n💡 EXPLANATION: {question.explanation}")
                        else:
                            print("\n💡 This question helps us gather necessary medical or forensic information to provide you with the best care and support.")
                        continue
                    
                    last_answer = response
                    break

        print("\n" + "="*60)
        print("✅ INTERVIEW COMPLETE")
        print("="*60)

        save = input("\nWould you like to save this interview record? (yes/no): ").strip().lower()
        if save in ['y', 'yes']:
            filename = input("Enter filename (default: interview_record.json): ").strip()
            if not filename:
                filename = "interview_record.json"
            
            # Helper to save
            save_model_response(interviewer.interview, filename)
            print(f"\n💾 Interview saved to {filename}")
        
        print("\n🙏 Thank you for your courage and trust.")
        print("Remember: This was not your fault.")
        print("Support is available 24/7.")

    except KeyboardInterrupt:
        print("\n\n⚠️  Interview interrupted by user.")
        print("Patient safety is priority. Provide immediate support.")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        # import traceback
        # traceback.print_exc()
        print("Ensure patient safety and wellbeing first.")

if __name__ == "__main__":
    cli()
