# embeddings.py
import time
import openai
from typing import List

from core.config import EMBEDDING_MODEL, NAMESPACE
from core.pinecone_client import index

def get_embedding(text: str) -> List[float]:
    """Get a text embedding from OpenAI with basic retry logic."""
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = openai.Embedding.create(input=[text], model=EMBEDDING_MODEL)
            return response["data"][0]["embedding"]
        except openai.error.RateLimitError:
            print("Rate limit reached in get_embedding; retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"Error in get_embedding: {e}")
            time.sleep(5)
    raise Exception("Exceeded maximum retries in get_embedding.")

def query_pinecone(embedding: List[float], top_k: int) -> List[dict]:
    """Query the Pinecone index for the top_k matches using the provided embedding."""
    max_retries = 5
    for attempt in range(max_retries):
        try:
            result = index.query(
                vector=embedding, 
                top_k=top_k, 
                namespace=NAMESPACE, 
                include_metadata=True
            )
            return result.get("matches", [])
        except Exception as e:
            print(f"Error in query_pinecone (attempt {attempt+1}): {e}")
            time.sleep(5)
    raise Exception("Exceeded maximum retries in query_pinecone.")
