from sentence_transformers import SentenceTransformer

# Load embedding model once
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def generate_embedding(text):
    # Generate Embeddings
    embedding = model.encode(text)

    return embedding