# Acknowledgement: The following prompt has been copied verbatim from Dimitrios A. Karras’ Post on Linkedln.


from litellm import completion

MODEL = "ollama/gemma3"

SYSTEM_PROMPT = """
You are a master explainer who channels Richard Feynman’s ability to break complex ideas into simple, intuitive truths.
Your goal is to help the user understand any topic through analogy, questioning, and iterative refinement until they can teach it back confidently.
"""

CONTEXT = """
The user wants to deeply learn a topic using a step-by-step Feynman learning loop:
• simplify
• identify gaps
• question assumptions
• refine understanding
• apply the concept
• compress it into a teachable insight
"""

INSTRUCTIONS = """
Follow this exact structure:

Step 1: Simple Explanation
- Use a clean analogy
- No jargon
- Define any technical term simply

Step 2: Confusion Check
- Highlight common confusion points
- Ask 3–5 targeted questions to reveal gaps

Step 3: Refinement Cycles
- Re-explain 2–3 times
- Each time more intuitive
- Each time simpler
- Use a new analogy if needed

Step 4: Understanding Challenge
- Ask the user to apply it or teach it back

Step 5: Teaching Snapshot
- Compress the idea into a short, teachable insight

Constraints:
• Always use analogies
• No jargon early
• Define terms simply
• Each cycle must be clearer
• Prioritize understanding over recall
"""

def ask_llm(messages):
    response = completion(
        model=MODEL,
        messages=messages,
        temperature=0.4
    )
    return response["choices"][0]["message"]["content"]

def feynman_tutor():
    print("\n🧠 Feynman-Style AI Tutor\n")

    topic = input("📌 Topic: ")
    level = input("📊 Your current understanding (beginner/intermediate/advanced): ")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": CONTEXT},
        {"role": "system", "content": INSTRUCTIONS},
        {
            "role": "user",
            "content": f"My topic is: {topic}. My understanding level is: {level}. Begin Step 1."
        }
    ]

    # Step 1–2–3 initial response
    response = ask_llm(messages)
    print("\n" + response)
    messages.append({"role": "assistant", "content": response})

    # Refinement cycles
    for i in range(2):
        feedback = input("\n🤔 What feels unclear, confusing, or shaky? ")
        messages.append({"role": "user", "content": feedback})

        refinement_prompt = "Refine the explanation using a clearer analogy and simpler language."
        messages.append({"role": "user", "content": refinement_prompt})

        response = ask_llm(messages)
        print("\n" + response)
        messages.append({"role": "assistant", "content": response})

    # Step 4: Understanding challenge
    challenge_prompt = "Now perform Step 4: Test my understanding by asking me to apply or teach the idea."
    messages.append({"role": "user", "content": challenge_prompt})

    response = ask_llm(messages)
    print("\n" + response)
    messages.append({"role": "assistant", "content": response})

    user_answer = input("\n✍️ Your answer: ")
    messages.append({"role": "user", "content": user_answer})

    # Step 5: Teaching snapshot
    snapshot_prompt = "Now perform Step 5: Create my final Teaching Snapshot."
    messages.append({"role": "user", "content": snapshot_prompt})

    response = ask_llm(messages)
    print("\n" + response)

    print("\n🎉 Learning loop complete.\n")

if __name__ == "__main__":
    feynman_tutor()

