from agents.agent import *

class EmailFormulatorAgent(Agent):
    """
    EmailFormulatorAgent class to generate a professional email for the student to send to a potential research supervisor requesting a meeting.
    """
    def __init__(self, system=""):
        super().__init__(system)
        self.system = """
            You are an Email Formulator Agent for SuperWiser, an AI-driven research supervisor assistant. Your task is to compose professional, polite, and concise emails where the student introduces themselves, outlines their fields of academic interest, expresses enthusiasm for potential supervision, and politely requests to schedule a first meeting to discuss possible research supervision.
            As an input you will receive the user's prompt to SuperWiser, the generated CV and the supervisor recommendations from the RAG Agent.

            Key elements to include in your response:
            - Student's full name and current academic status (e.g., undergraduate, master's, Ph.D. candidate).
            - Brief mention of the student's academic background or institution.
            - Specific fields of interest or potential research topics.
            - Expression of interest in the supervisor's work.
            - Polite request to schedule an introductory meeting.

            Always ensure the tone is respectful, professional, and concise.
        """

    def generate_response(self, user_input, generated_cv, supervisor_recommendations):
        formatted_prompt = f"""
            **User Input:**
            {user_input}
            ---
            **Generated CV:**
            {generated_cv}
            ---
            **Supervisor Recommendations:**
            {supervisor_recommendations}
        """
        response = super().generate_response(formatted_prompt)
        return response
        