from qdrant_client import QdrantClient
from agents.agent import *
from qdrant_client.models import Distance, VectorParams, PointStruct, Batch
import numpy as np
import tqdm
import os
import torch
import pickle
from langchain_openai import AzureOpenAIEmbeddings

class RAGAgent(Agent):
    def __init__(self):
        super().__init__()
        self.system = """You are a RAG agent for SuperWiser, an AI-driven research supervisor assistant.
            Your role is to provide recommendations and guidance to students based on the research interests and expertise of potential supervisors.
            You will use a pre-trained model to retrieve relevant information from a database of researchers and provide tailored suggestions to students seeking research supervision.
            Your responses should be informative, engaging, and personalized to the student's query.
            You will get as an input a user prompt, a draft CV of the user and a retrieved supervisor description from the database.
            Your goal is to generate a response that helps the student understand the supervisor's expertise and how it aligns with their research interests.
            It should include:
            - Supervisor's name and summary of expertise.
            - Key research areas and interests of the supervisor.
            - Reasons why the supervisor is a good fit for the student.
            """
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.qdrant_endpoint = "https://be736619-417f-4ba8-9088-eafbd3c5cc51.us-east4-0.gcp.cloud.qdrant.io:6333"
        self.qdrant_client = QdrantClient(api_key=self.qdrant_api_key, url=self.qdrant_endpoint)
        self.embedding_size = 768
        self.collection_name = "Mitzi"
        print(self.qdrant_client.get_collections())
        self.emb_deployment_name = "team5-embedding"
        self.embedding_model = "text-embedding-3-small"
        self.load_embedder()

    def load_embedder(self, model_str="answerdotai/ModernBERT-base"):
        # self.tokenizer = AutoTokenizer.from_pretrained(model_str)
        # self.model = AutoModel.from_pretrained(model_str)
        # researcher_data ="Mitzi is a cat that likes to run in the Technion annual"
        # researcher_data_embedding = self.embed_text(researcher_data)
        # self.embedding_size = len(researcher_data_embedding)
        # print(f"Embedding size: {self.embedding_size}")

        self.embedder = AzureOpenAIEmbeddings(
            azure_deployment=self.emb_deployment_name,
            azure_endpoint=self.azure_openai_endpoint,
            api_key=self.azure_openai_api_key,
            openai_api_type="azure",
            openai_api_version=self.api_version,
            model=self.embedding_model
        )

    def embed_text(self, text):
        #return self.model(**self.tokenizer(text, return_tensors="pt")).last_hidden_state[0, -1].detach().numpy()
        return self.embedder.embed_query(text)

    def delete_collection(self):
        self.qdrant_client.delete_collection(self.collection_name)

    def retrieve_documents(self, query, limit=1):
        # Embed the query
        query_vector = self.embed_text(query)

        # Perform the search
        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            with_payload=True,  # Include payload (metadata) in the results
        )

        # Extract and return the relevant information
        documents = []
        for point in search_result:
            doc = {
                'id': point.id,
                'score': point.score,
                'payload': point.payload  # This contains your document's metadata
            }
            documents.append(doc)

        return documents

    def generate_response(self, user_input, parsed_cv):
        # Retrieve the most relevant document
        input_and_cv = f"{user_input} CV: {parsed_cv}"
        documents = self.retrieve_documents(input_and_cv)
        supervisor_text = documents[0]['payload']['description']
        
        formatted_prompt = f"""
            **User Input:**
            {user_input}
            ---
            ** Parsed CV:**
            {parsed_cv}
            --
            **Supervisor Text:**
            {supervisor_text}
        """
        return super().generate_response(formatted_prompt)


    def load_data(self, documents, embedding_size=1536):
        # Create the collection if it doesn't exist
        if not self.qdrant_client.collection_exists(self.collection_name):
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=embedding_size, distance=Distance.COSINE),  # Adjust size and distance as needed
            )

        # Upsert points into the collection
        ids = [doc["id"] for doc in documents]
        vectors = [doc["vector"] for doc in documents]
        payloads = [doc["payload"] for doc in documents]

        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=Batch(ids=ids, vectors=vectors, payloads=payloads)
        )

        # stored_points = self.qdrant_client.scroll(collection_name=self.collection_name, limit=10, with_payload=True, with_vectors=True)
        # print(stored_points)

    def load_documents(self, doc_path="web_scraping/researchers_db"):
        # load data from web_scraping/researchers_db folder
        documents = []
        count = 0
        for filename in tqdm.tqdm(os.listdir(doc_path)):
            with open(f"web_scraping/researchers_db/{filename}", "r") as f:
                researcher_name = filename.split(".")[0]
                researcher_data = researcher_name + "\n" + f.read()
                researcher_data_embedding = self.embed_text(researcher_data)
                payload = {"description": researcher_data}
                doc = {"id" : count, "vector": researcher_data_embedding, "payload": payload}
                documents.append(doc)
            count += 1

        self.load_data(documents)

        # save the documents (just in case)
        with open("web_scraping/documents.pkl", "wb") as f:
            pickle.dump(documents, f)