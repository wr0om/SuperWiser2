from qdrant_client import QdrantClient
from agents.agent import *
from qdrant_client.models import Distance, VectorParams, PointStruct, Batch
import numpy as np
from transformers import AutoTokenizer, AutoModel
import tqdm
import os
import torch
import pickle


class RAGAgent(Agent):
    def __init__(self, system=""):
        super().__init__(system=system)
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.qdrant_endpoint = "https://be736619-417f-4ba8-9088-eafbd3c5cc51.us-east4-0.gcp.cloud.qdrant.io:6333"
        self.qdrant_client = QdrantClient(api_key=self.qdrant_api_key, url=self.qdrant_endpoint)
        self.embedding_size = 768
        print(self.qdrant_client.get_collections())
        self.load_embedder()

    def load_embedder(self, model_str="answerdotai/ModernBERT-base"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_str)
        self.model = AutoModel.from_pretrained(model_str)
        researcher_data ="Mitzi is a cat that likes to run in the Technion annual"
        researcher_data_embedding = self.embed_text(researcher_data)
        self.embedding_size = len(researcher_data_embedding)
        print(f"Embedding size: {self.embedding_size}")

    def embed_text(self, text):
        return self.model(**self.tokenizer(text, return_tensors="pt")).last_hidden_state[0, -1].detach().numpy()

    def delete_collection(self, collection_name):
        self.qdrant_client.delete_collection(collection_name)

    def retrieve_documents(self, collection_name, query, limit=1):
        # Embed the query
        query_vector = self.embed_text(query)

        # Perform the search
        search_result = self.qdrant_client.search(
            collection_name=collection_name,
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

    def load_data(self, collection_name, documents, embedding_size=768):
        # Create the collection if it doesn't exist
        if not self.qdrant_client.collection_exists(collection_name):
            self.qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=embedding_size, distance=Distance.COSINE),  # Adjust size and distance as needed
            )

        # Upsert points into the collection
        ids = [doc["id"] for doc in documents]
        vectors = [doc["vector"] for doc in documents]
        payloads = [doc["payload"] for doc in documents]

        self.qdrant_client.upsert(
            collection_name=collection_name,
            points=Batch(ids=ids, vectors=vectors, payloads=payloads)
        )

        stored_points = self.qdrant_client.scroll(collection_name=collection_name, limit=10, with_payload=True, with_vectors=True)
        print(stored_points)

    def load_documents(self, collection_name, doc_path="web_scraping/researchers_db"):
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

        self.load_data(collection_name, documents)

        # save the documents (just in case)
        with open("web_scraping/documents.pkl", "wb") as f:
            pickle.dump(documents, f)