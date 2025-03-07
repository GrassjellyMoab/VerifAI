import pinecone
from app.utils.config import PINECONE_API_KEY

pinecone.init(api_key=PINECONE_API_KEY, environment="us-west1-gcp")  # example env

# Then create or connect to an index
index = pinecone.Index("my-index")
