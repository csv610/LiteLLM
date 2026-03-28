import logging
from typing import Optional

logger = logging.getLogger(__name__)

class HITLManager:
    """Manages Human-in-the-loop interactions for clinical approval."""
    
    @staticmethod
    def request_approval(agent_name: str, content: str) -> str:
        """
        Request approval or edits for an agent's output.
        In a CLI context, this prompts the user.
        In a web context, this would wait for an API callback.
        """
        print(f"\n--- HITL APPROVAL REQUIRED: {agent_name} ---")
        print(f"Content:\n{content}")
        print("-" * 40)
        
        user_choice = input("Approve as is? (y/n/edit): ").lower().strip()
        
        if user_choice == 'y':
            return content
        elif user_choice == 'edit':
            print("Enter your edits (end with a single line containing 'END'):")
            lines = []
            while True:
                line = input()
                if line.strip() == 'END':
                    break
                lines.append(line)
            return "\n".join(lines)
        else:
            print("Rejecting content. Please provide required changes/feedback (will be appended to context):")
            feedback = input("> ")
            return f"REJECTED BY CLINICIAN. Feedback: {feedback}\nOriginal Content: {content}"
