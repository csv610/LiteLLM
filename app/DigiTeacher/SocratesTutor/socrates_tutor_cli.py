from socrates_tutor import SocratesTutor

def run_cli():
    print("\n🏛️  Socrates AI Tutor")
    print("Welcome to our inquiry. I will help you find the truth through dialogue.\n")

    topic = input("📌 What concept or problem shall we explore? ")
    level = input("📊 Tell me a bit about your current understanding (e.g., student, expert, confused): ")

    tutor = SocratesTutor(topic, level)

    print("\n--- [Beginning Inquiry] ---")
    response = tutor.begin_inquiry()
    print(f"\n🧠 Socrates: {response}")

    while not tutor.is_convinced:
        user_input = input("\n👤 You: ")
        
        if user_input.lower() in ["exit", "quit", "goodbye"]:
            print("\n👋 Socrates: Farewell, seeker of wisdom. May your questions never cease!\n")
            break
            
        print("\n--- [Thinking...] ---")
        response = tutor.provide_response(user_input)
        print(f"\n🧠 Socrates: {response}")

        if tutor.is_convinced:
            print("\n--- [Inquiry Complete] ---")
            print(f"📊 Summary of Understanding: {tutor.summary}")
            print("\n🎉 Socrates: Our dialogue has reached its end. You have discovered the truth through your own reason.\n")
            break

if __name__ == "__main__":
    run_cli()
