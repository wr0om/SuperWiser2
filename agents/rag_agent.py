from qdrant_client import QdrantClient
from agents.agent import *
from qdrant_client.models import Distance, VectorParams, PointStruct, Batch
import numpy as np

class RAGAgent(Agent):
    def __init__(self, system=""):
        super().__init__(system=system)
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.qdrant_endpoint = "https://be736619-417f-4ba8-9088-eafbd3c5cc51.us-east4-0.gcp.cloud.qdrant.io:6333"
        self.qdrant_client = QdrantClient(api_key=self.qdrant_api_key, url=self.qdrant_endpoint)
        print(self.qdrant_client.get_collections())

    def delete_collection(self, collection_name):
        self.qdrant_client.delete_collection(collection_name)

    def load_data(self, collection_name, documents):
        # Create the collection if it doesn't exist
        if not self.qdrant_client.collection_exists(collection_name):
            self.qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=3, distance=Distance.COSINE),  # Adjust size and distance as needed
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


    def retrieve_documents(self, collection_name, query_vector, limit=1):
        """
        Retrieve documents from Qdrant based on the similarity to the query vector.

        Args:
            collection_name (str): The name of the collection to search in.
            query_vector (list): The vector representation of the query.
            limit (int): The number of top results to return.

        Returns:
            list: A list of dictionaries containing the retrieved documents and their metadata.
        """
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

