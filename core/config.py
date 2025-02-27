# core/config.py
import os
import openai
from dotenv import load_dotenv

# Load from .env file (and system environment variables)
load_dotenv()

# Read environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
NAMESPACE = os.getenv("PINECONE_NAMESPACE")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
EMBED_DIMENSIONS = int(os.getenv("EMBED_DIMENSIONS", "3072"))  # fallback for int is okay

# Validate critical keys
if not OPENAI_API_KEY:
    raise ValueError("Missing environment variable: OPENAI_API_KEY")
if not PINECONE_API_KEY:
    raise ValueError("Missing environment variable: PINECONE_API_KEY")

# Set up OpenAI
openai.api_key = OPENAI_API_KEY
