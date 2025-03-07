from agents.agent import Agent
from langchain.schema import HumanMessage, SystemMessage, AIMessage

class CVGeneratorAgent(Agent):
    def __init__(self, user_input=None, supervisor_recommendations=None, parced_cv=None):
        super().__init__()
        self.system = """
            You are the CV Generator Agent for **SuperWiser**, an AI-driven research supervisor assistant. Your role is to create a structured, professional CV. The generated CV is then sent to a feedback agent for review and feedback.
            1. The conversation history with the feedback agent.
            2. **CV Parser Data** - Extracted details from the user's existing CV draft.    
            3. **Supervisor's Recommendations** - A description of the recommended supervisor.

            ### **Output:**  
            You should base the generated CV on the **CV Parser Data**. If the draft is not too detailed, you can output it as it is. If you think it may have irrelevant information, you should focus on the relevant parts.
            Use the same format as in the draft CV, but ensure the content is accurate, well-organized, and professional.
            Output only the generated CV, don't add anything beyond that.

            ### **CV Format:**  

            ---

            Education:
            - [Degree] | [Institution] | [Years]  
            - [Degree] | [Institution] | [Years]  

            Research Experience:
            - [Position] | [Institution] | [Years]  
            Description: [Brief description of research work]  
            - [Position] | [Institution] | [Years]  
            Description: [Brief description of research work]  

            Work Experience:
            - [Job Title] | [Company/Institution] | [Years]  
            Description: [Brief summary of responsibilities]  

            Volunteer Experience:
            - [Position] | [Organization] | [Years]
            Description: [Brief summary of responsibilities]

            Publications:
            - "[Title]" | [Authors] | [Conference/Journal] | [Year]  
            - "[Title]" | [Authors] | [Conference/Journal] | [Year]  

            Skills:
            - [Skill 1], [Skill 2], [Skill 3], ...

            Awards & Achievements:
            - [Award Name] | [Institution] | [Year]  

            Contact Information:
            - Name: [Full Name]  
            - Email: [Email Address]  
            - Phone: [Phone Number]  
            - LinkedIn: [Profile URL] (if available)  
            - Website: [Personal Website] (if available)  

            ---

            ### **Guidelines:**  
            - Personalize the CV to the supervisor's expectations without making up new information.
            - Base the CV on CV Parser Data.  
            - Retain detailed and relevant content.  
            - Filter out irrelevant information.  
            - Follow the same format as the draft CV.  
            - Ensure accuracy, clarity, and professionalism. 
            - DO NOT add a message explaining the output, only the generated CV.
            - DO NOT invent, assume, or generate any new information!!!
            """
        self.messages = [SystemMessage(content=self.system)]
        if user_input:
            self.add_human_message(user_input)
        if supervisor_recommendations:
            self.add_human_message(supervisor_recommendations)
        if parced_cv:
            self.add_human_message(parced_cv)

    def add_human_message(self, content):
        self.messages.append(HumanMessage(content=content))

    def add_AI_message(self, content):
        self.messages.append(AIMessage(content=content))

    def generate_response(self, parsed_cv=None, supervisor_recommendations=None, feedback=None, user_input=None):
        if parsed_cv:
            self.add_human_message(parsed_cv)

        if supervisor_recommendations:
            self.add_human_message(supervisor_recommendations)

        if user_input:
            self.add_human_message(user_input)

        if feedback:
            self.add_AI_message(feedback)

        response = super().generate_response_from_messages(messages=self.messages)
        self.add_AI_message("Generated CV: " + response)
        return response

            

        



            