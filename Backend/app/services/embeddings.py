# app/services/embeddings.py

import pinecone
import os

# Suppose you load your Pinecone key from an env variable
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", None)

# Initialize pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment="us-west1-gcp")  # example env
index = pinecone.Index("my-hackathon-index")

def embed_text_and_upsert(text_chunks, metadata=None):
    """
    Embeds text chunks and inserts them into Pinecone with optional metadata.
    """
    # Example: using OpenAI embeddings -> embed, then upsert to Pinecone
    pass

def query_similar_passages(query_text, top_k=5):
    """
    Embeds 'query_text' and queries Pinecone for the top_k similar chunks.
    """
    pass
