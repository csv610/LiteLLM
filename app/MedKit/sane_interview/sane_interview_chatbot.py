from sane_interview_models import SANEInterviewRecord, YesNoUnsure


class ConsoleInterviewIO:
    def display(self, text):
        print(text)

    def ask(self, prompt):
        return input(prompt)

    def wait_for_user(self, text):
        input(text)


class SANEInterviewer:
    """Base class for SANE Interviewer (Mock/Placeholder)"""

    def __init__(self, io_handler=None):
        self.io = io_handler or ConsoleInterviewIO()
        self.interview = SANEInterviewRecord()

    def get_yes_no(self, question: str) -> YesNoUnsure:
        self.io.display(f"\n{question}")
        self.io.display("(yes/no/skip/unsure)")
        ans = self.io.ask("Response: ").strip().lower()
        if ans in ["y", "yes"]:
            return YesNoUnsure.YES
        if ans in ["n", "no"]:
            return YesNoUnsure.NO
        if ans in ["u", "unsure"]:
            return YesNoUnsure.UNSURE
        return YesNoUnsure.DECLINE

    def get_response(self, question: str) -> str:
        self.io.display(f"\n{question}")
        return self.io.ask("Response: ").strip()

    def conduct_interview(self):
        # This would be overridden or implemented here
        return self.interview

    def save_interview(self, filename: str):
        with open(filename, "w") as f:
            f.write(self.interview.model_dump_json(indent=2))
