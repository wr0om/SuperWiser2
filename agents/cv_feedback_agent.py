from agents.agent import *
import json

class CVFeedback(Agent):
    def __init__(self):
        super().__init__()
        self.system = """
            You are the CV Feedback Agent for **SuperWiser**, an AI-driven research supervisor assistant. Your role is to **evaluate** the generated CV by comparing it against the **user's previous CV draft**, **user prompt**, and the **newly generated CV** to identify inaccuracies, inconsistencies, and hallucinations.

            ### **Input Sources:**  
            1. **Previous CV Draft** - The user's earlier version of their CV.  
            2. **User Prompt** - Instructions and preferences provided by the user for CV generation.  
            3. **Generated CV** - The latest version of the CV created by the CV Generator Agent.  

            ### **Responsibilities:**  
            1. **Detect Hallucinations** - Identify any fabricated, misleading, or unsupported information in the generated CV.  
            2. **Ensure Consistency** - Verify that the generated CV aligns with the user's previous CV and prompt, ensuring that relevant details are accurately preserved.  
            3. **Check Accuracy** - Validate the correctness of dates, affiliations, research details, publications, and other critical information.  
            4. **Provide Actionable Feedback** - Deliver clear, concise, and constructive suggestions to address inconsistencies, missing details, or necessary corrections.  

            ### **Output Format:**  
            Your feedback should be **precise, constructive, and specific**, helping the CV Generator Agent refine the document for better accuracy, completeness, and alignment with the user's background and expectations.

            Your output should be structured in **JSON format** as follows:
            {
                "feedback": "Detailed feedback highlighting any issues and suggested improvements.",
                "decision": "accept" or "reject"  // Indicates whether the generated CV is acceptable or needs revision.
            }

            PLEASE RETURN THIS JSON FORMAT!! "decision" SHOULD HAVE "accept" OR "reject" ONLY.
        """
        self.cv_draft = None
        self.user_prompt = None
        self.generated_cv = None

    def generate_response(self, user_input, cv_draft, generated_cv):
        self.cv_draft = cv_draft
        self.user_prompt = user_input
        self.generated_cv = generated_cv

        formatted_prompt = f"""
            **Previous CV Draft:**
            {cv_draft}
            ---
            **User Input:**
            {user_input}
            ---
            **Generated CV:**
            {generated_cv}
        """
        response = super().generate_response(formatted_prompt)

        # # extract feedback and decision from the response using json (TODO: check this)
        # feedback_data = json.loads(response)
        # feedback = feedback_data["feedback"]
        # decision = feedback_data["decision"]
        return response

