# app/core/pinecone_client.py
import time
from typing import List
from pinecone import Pinecone, ServerlessSpec

from core.config import (
    PINECONE_API_KEY,
    PINECONE_ENV,
    INDEX_NAME,
    EMBEDDING_MODEL,
    EMBED_DIMENSIONS,
    NAMESPACE,
)

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Ensure the index exists
indexes = pc.list_indexes().names()
if INDEX_NAME not in indexes:
    pc.create_index(
        name=INDEX_NAME,
        dimension=EMBED_DIMENSIONS,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=PINECONE_ENV),
    )

# Get a reference to the Pinecone index
index = pc.Index(INDEX_NAME)
