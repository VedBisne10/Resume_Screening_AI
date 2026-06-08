import chromadb
from src.matcher.embedding_matcher import (generate_embedding)

client = chromadb.PersistentClient(path="./chroma_db") # Client is the connection to the database
                                                       # And it creates a folder chroma_db inside the project

# The use of this function is to use the pre-existing collection of JD's or create a new one
collection = client.get_or_create_collection(  
    name="job_descriptions"
)

# 
def add_job_description(job_id, job_text, embedding):

    # Check if this JD already exists in ChromaDB using its job_id
    # This prevents a duplicate ID error if you run the app more than once
    existing = collection.get(ids=[job_id])

    # existing["ids"] will be an empty list if the JD is not stored yet
    if not existing["ids"]:
        # Only store if it doesn't already exist
        collection.add(
            ids=[job_id],   # Every record needs a unique identifier
            documents=[job_text],   # Stores the actual JD text
            embeddings=[embedding.tolist()]     # Create embeddings of the JD  
        )

# Function for searching the vector database
def search_similar_jobs(resume_embedding, top_k=5):

    # Converts the array of embeddings into list of embeddings and gives top_k results as output from all the similar results
    results = collection.query(query_embeddings=[
        resume_embedding.tolist()
        ], n_results=top_k)
    return results


# Function for looping through all loaded Job Descriptions
def index_job_descriptions(job_descriptions):

    # Loop through all loaded job descriptions
    for job_id, job_text in (job_descriptions.items()):

        # Generate embedding vector for the job description text
        embedding = generate_embedding(job_text)

        # Store the job description and its embedding inside the chromadb collection
        add_job_description(job_id, job_text, embedding)

    print("All job descriptions indexed successfully.")