from sentence_transformers import SentenceTransformer   # SentenceTransformer is the library that converts text into embedding vectors

# Load the embedding model once when this file is imported
# "all-MiniLM-L6-v2" is a lightweight but accurate model for generating text embeddings
# Loading it once here avoids reloading it every time generate_embedding is called
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text):
    # This function takes any text and converts it into a vector (list of numbers)
    # These numbers capture the meaning of the text so similar texts have similar vectors
    # This is what allows ChromaDB to find similar job descriptions for a given resume

    # model.encode() converts the text into a numpy array of numbers (the embedding)
    embedding = model.encode(text)

    # Return the embedding vector
    return embedding
