from sentence_transformers import SentenceTransformer

# Load embedding model once
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def generate_embedding(text):
    # It Generate Embeddings of the text present in the pdf
    embedding = model.encode(text)

    return embedding