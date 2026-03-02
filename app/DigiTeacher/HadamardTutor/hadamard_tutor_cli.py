from hadamard_tutor import HadamardTutor

def run_cli():
    print("\n🧠 Hadamard Discovery Tutor")
    print("Guiding you through Preparation, Incubation, Illumination, and Verification.\n")

    topic = input("📌 Topic or Problem: ")
    level = input("📊 Your current level/context (e.g., beginner, researching, stuck): ")

    tutor = HadamardTutor(topic, level)

    print("\n--- [Beginning Discovery Loop] ---")
    response = tutor.get_preparation_phase()
    print(f"\n🧠 Hadamard: {response}")

    # For Hadamard, we follow the phases but allow conversational interaction
    # In this dynamic version, we'll use a loop and cycle through phases or stay in one
    phases = [
        tutor.get_incubation_phase,
        tutor.get_illumination_phase,
        tutor.get_verification_phase
    ]
    phase_idx = 0

    while not tutor.is_convinced:
        user_input = input("\n👤 You: ")
        
        if user_input.lower() in ["exit", "quit", "goodbye"]:
            print("\n👋 Hadamard: May your intuition stay sharp!\n")
            break
            
        print("\n--- [Thinking...] ---")
        
        # We advance phases based on user input or stay in the current one
        # For this implementation, we'll advance until verification, then stay there
        current_phase_fn = phases[min(phase_idx, len(phases)-1)]
        response = current_phase_fn(user_input)
        print(f"\n🧠 Hadamard: {response}")
        
        phase_idx += 1

        if tutor.is_convinced:
            print("\n--- [Discovery Complete] ---")
            print(f"📊 Summary of Breakthrough: {tutor.summary}")
            print("\n🎉 Hadamard: Brilliant! You have navigated the psychological path to invention.\n")
            break

if __name__ == "__main__":
    run_cli()
