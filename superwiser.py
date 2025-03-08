from agents.cv_parser_agent import CVParserAgent
from agents.rag_agent import RAGAgent
from agents.cv_generator_agent import CVGeneratorAgent
from agents.cv_feedback_agent import CVFeedbackAgent
from agents.email_formulator_agent import EmailFormulatorAgent
import json


class SuperWiser:
    def __init__(self):
        self.cv_parser_agent = CVParserAgent()
        self.rag_agent = RAGAgent()
        self.cv_generator_agent = CVGeneratorAgent()
        self.cv_feedback_agent = CVFeedbackAgent()
        self.email_formulator_agent = EmailFormulatorAgent()
        self.satisfied = False

    def process(self):
        self.user_input = input("Welcome to SuperWiser! Your AI research supervisor assistant. Please provide a brief description of your research interests and academic background: ")
        self.pdf_path = input("Enter the name of your CV in the CVs folder (without .pdf): ")
        self.pdf_path = f"CVs/{self.pdf_path}.pdf"
        self.process_cv()

        while not self.satisfied:
            self.process_rag()
            self.process_cv_generator_and_feedback()
            self.process_email_formulator()

            print(f"SUPERVISOR RECOMMENDATION:\n{self.response_rag}")
            print(f"GENERATED CV:\n{self.cv_generator_response}")
            print(f"FORMULATED E-MAIL:\n{self.response_email_formulator}")

            is_satisfied = input("Are you satisfied with the suggested supervisor, generated CV and E-mail? (yes/no): ")
            if is_satisfied.lower() == "yes":
                self.satisfied = True
            else:
                self.user_input = input("Please provide a clearer description of your research interests and academic background: ")

    def process_cv(self):
        self.response_cv_parser = self.cv_parser_agent.generate_response_with_pdf(self.pdf_path)
        print(f"PARSED CV:\n{self.response_cv_parser}")
        return self.response_cv_parser
    
    def process_rag(self):
        self.response_rag = self.rag_agent.generate_response(self.user_input, self.response_cv_parser)
        return self.response_rag
    
    def process_cv_generator_and_feedback(self):
        # count = 0
        # feedback = ""
        # while count < 2:
        #     # generate CV
        #     self.response_cv_generator = self.cv_generator_agent.generate_response(self.user_input, self.response_cv_parser, self.response_rag, feedback=feedback)
        #     # print(response_cv_generator)

        #     # get feedback
        #     self.response_cv_feedback = self.cv_feedback_agent.generate_response(self.user_input, self.response_cv_parser, self.response_cv_generator)
        #     # print(response_cv_feedback)

        #     # load response_cv_feedback into json
        #     json_response_cv_feedback = json.loads(self.response_cv_feedback)
        #     decision = json_response_cv_feedback["decision"]
        #     feedback = json_response_cv_feedback["feedback"]
        #     if decision == "accept":
        #         break

        #     print("Rejected CV, generating new one")
        #     count += 1
        accepted = False
        feedback = None
        counter = 0
        self.cv_generator_agent.add_human_message(self.user_input)
        self.cv_generator_agent.add_human_message(self.response_rag)
        self.cv_generator_agent.add_human_message(self.response_cv_parser)
        while not accepted and counter < 3:
            counter += 1
            self.cv_generator_response = self.cv_generator_agent.generate_response(feedback=feedback)
            print(f"Generated CV: {self.cv_generator_response}")
            self.cv_feedback_response = self.cv_feedback_agent.generate_response(self.user_input, self.response_cv_parser, self.cv_generator_response)
            print(f"Feedback: {self.cv_feedback_response}")
            cv_feedback = json.loads(self.cv_feedback_response)
            decision = cv_feedback["decision"]
            feedback = cv_feedback["feedback"]
            consistency = cv_feedback["consistency"]
            # print(f"Desicion: {decision}")
            # print(f"Feedback: {feedback}")
            # print(f"Consistency: {consistency}")
            if decision == "accept":
                accepted = True
            else:
                print("REJECTED CV, GENERATING NEW ONE...")

        return self.cv_generator_response
    
    def process_email_formulator(self):
        self.response_email_formulator = self.email_formulator_agent.generate_response(self.user_input, self.cv_generator_response, self.response_rag)
        return self.response_email_formulator