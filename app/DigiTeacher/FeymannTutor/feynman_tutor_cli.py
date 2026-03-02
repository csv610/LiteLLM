from feynman_tutor import FeynmanTutor

def run_cli():
    print("\n🧠 Feynman-Style AI Tutor\n")

    topic = input("📌 Topic: ")
    level = input("📊 Your current understanding (beginner/intermediate/advanced): ")

    tutor = FeynmanTutor(topic, level)

    print("\n--- [Beginning Learning Loop] ---")
    response = tutor.get_initial_explanation()
    print(f"\n🧠 Feynman: {response}")

    while not tutor.is_convinced:
        user_input = input("\n👤 You: ")
        
        if user_input.lower() in ["exit", "quit", "goodbye"]:
            print("\n👋 Feynman: Keep exploring! The more you simplify, the more you understand.\n")
            break
            
        print("\n--- [Thinking...] ---")
        # Decide which step to take based on history or just use refinement
        # For simplicity in this conversational version, we use refine_explanation
        response = tutor.refine_explanation(user_input)
        print(f"\n🧠 Feynman: {response}")

        if tutor.is_convinced:
            print("\n--- [Learning Complete] ---")
            print(f"📊 Summary of Understanding: {tutor.summary}")
            print("\n🎉 Feynman: Excellent! You've simplified this concept to its core. You're ready to teach it!\n")
            break

if __name__ == "__main__":
    run_cli()
