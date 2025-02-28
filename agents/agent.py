from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

import os
from dotenv import load_dotenv

load_dotenv()

class Agent:
    def __init__(self, system=""):
        AZURE_OPENAI_API_KEY = os.getenv("API_KEY")
        DEOLOYMENT_NAME = "team5-gpt4o" # team5-embedding
        AZURE_OPENAI_ENDPOINT = "https://096290-oai.openai.azure.com"
        API_VERSION = "2023-05-15"

        # Initialize the Azure OpenAI chat model
        self.chat = AzureChatOpenAI(
            azure_deployment=DEOLOYMENT_NAME,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
            openai_api_type="azure",
            openai_api_version=API_VERSION,
            temperature=0.7
        )
        self.system = system

    def generate_response(self, user_input: str) -> str:
        # Render the final prompt
        if self.system:
            messages = [
                SystemMessage(content=self.system),
                HumanMessage(content=user_input)
            ]
        else:
            messages = [
                HumanMessage(content=user_input)
            ]
        # Call the chat model
        response = self.chat(messages=messages)
        return response.content
    
    def generate_response_from_messages(self, messages: list) -> str:
        response = self.chat(messages=messages)
        return response.content
    
    def generate_response_with_pdf(self, pdf_path: str, user_input="") -> str:
        loader = PyPDFLoader(file_path=pdf_path, mode="single")
        document = loader.load()
        document_text = document[0].page_content

        if user_input:
            model_input = f"User: {user_input}\nDocument: {document_text}"
        else:
            model_input = f"Document: {document_text}"
        response = self.generate_response(model_input)
        return response
