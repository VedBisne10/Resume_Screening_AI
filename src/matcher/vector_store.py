import chromadb                                          # chromadb is the vector database we use to store and search job descriptions
from src.matcher.embedding_matcher import generate_embedding  # Import the function that converts text into embedding vectors (numbers)

# Create a persistent connection to ChromaDB
# PersistentClient means the data is saved to disk in the "chroma_db" folder
# So even if you restart the app, the stored JDs are still there
client = chromadb.PersistentClient(path="./chroma_db")

# Get or create a collection called "job_descriptions"
# A collection is like a table in a database — it holds all our JD vectors
# If it already exists from a previous run, it reuses it. If not, it creates a new one.
collection = client.get_or_create_collection(
    name="job_descriptions"
)


def add_job_description(job_id, job_text, embedding):
    # This function stores a single job description into ChromaDB
    # job_id: unique name for the JD (we use the filename like "JavaDeveloper.txt")
    # job_text: the full text content of the JD
    # embedding: the vector representation of the JD text

    # First check if this JD is already stored in ChromaDB using its job_id
    # This prevents a "duplicate ID" error if the app is run more than once
    existing = collection.get(ids=[job_id])

    # existing["ids"] will be an empty list [] if the JD is NOT stored yet
    if not existing["ids"]:
        # Only store the JD if it doesnt already exist in the database
        collection.add(
            ids=[job_id],                       # Unique identifier for this JD
            documents=[job_text],               # The actual text of the JD
            embeddings=[embedding.tolist()]     # The vector of the JD (converted to list for ChromaDB)
        )


def search_similar_jobs(resume_embedding, top_k=5):
    # This function takes a resume embedding and finds the most similar JDs in ChromaDB
    # resume_embedding: the vector of the resume text
    # top_k: how many similar JDs to return (default is 5)

    # Query ChromaDB with the resume vector and get the top_k most similar JDs
    # ChromaDB compares the resume vector against all stored JD vectors and returns the closest ones
    results = collection.query(
        query_embeddings=[resume_embedding.tolist()],   # Resume vector converted to list
        n_results=top_k                                  # Number of results to return
    )

    # Returns a dictionary with keys: "ids", "documents", "distances"
    # ids: list of matched JD filenames
    # documents: list of matched JD texts
    # distances: how different each JD is from the resume (lower = more similar)
    return results


def index_job_descriptions(job_descriptions):
    # This function loops through all loaded JDs and stores them in ChromaDB
    # job_descriptions: dictionary where key = filename, value = JD text

    for job_id, job_text in job_descriptions.items():

        # Convert the JD text into a vector (embedding) so ChromaDB can compare it
        embedding = generate_embedding(job_text)

        # Store this JD in ChromaDB (skips if already stored)
        add_job_description(job_id, job_text, embedding)

    print("All job descriptions indexed successfully.")
