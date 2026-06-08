from src.parser.pdf_parser import extract_text_from_pdf      # Import function that reads a PDF file and returns its text
from src.parser.text_cleaner import clean_text               # Import function that cleans text by removing special chars and lowercasing
from src.llm.extractor import extract_document_data          # Import function that uses GPT to extract skills, experience, education from text
from src.llm.skill_matcher import llm_skill_match            # Import function that uses GPT to match JD skills against resume summary
from src.utils.helpers import load_job_descriptions          # Import function that loads all job description text files from a folder
from src.matcher.vector_store import index_job_descriptions, search_similar_jobs  # Import ChromaDB functions for storing and searching JDs
from src.matcher.embedding_matcher import generate_embedding  # Import function that converts text into embedding vectors


# Extract raw text from the resume PDF file
# This gives us the original unmodified text exactly as it appears in the PDF
resume_text = extract_text_from_pdf("data/resumes/Resume.pdf")

# Keep the original resume text separately for sending to the LLM
# We do NOT clean this because cleaning would destroy terms like C++, scikit-learn, .NET
resume_text_raw = resume_text

# Create a cleaned version of the resume text for use with embeddings only
# clean_text lowercases everything and removes special characters which is good for vector similarity
resume_text_clean = clean_text(resume_text)

# Load all job description files from the job_descriptions folder
# Returns a dictionary where key is the filename and value is the text content of that JD
job_descriptions = load_job_descriptions("data/job_descriptions")

# Extract structured data from the resume ONCE before the loop using raw unmodified text
# This gives us skills and experience as clean lists instead of one big noisy text block
resume_data = extract_document_data(resume_text_raw)

# Combine the skills list and experience list from the resume into one summary list
# This structured summary is much better for GPT to reason about than the full resume text
resume_summary = resume_data["skills"] + resume_data["experience"]

# Store all JDs in ChromaDB with their embeddings — only stores if not already stored
index_job_descriptions(job_descriptions)

# Convert the raw resume text into an embedding vector for ChromaDB similarity search
resume_embedding = generate_embedding(resume_text_raw)

# Query ChromaDB to find the top 3 most similar JDs to this resume
# This filters out completely irrelevant jobs before sending to GPT
similar_jobs = search_similar_jobs(resume_embedding, top_k=3)

# Loop only over the top matching JDs returned by ChromaDB, not all JDs
for job_id, job_text, distance in zip(
    similar_jobs["ids"][0],           # list of matched job ids
    similar_jobs["documents"][0],     # list of matched job texts
    similar_jobs["distances"][0]      # list of similarity distances (lower = more similar)
):
    # Skip jobs that are too different from the resume (distance above 1.5 means very low similarity)
    if distance > 1.5:
        print(f"\nSkipping {job_id} — too different from resume (distance: {distance})")
        continue

    # Print a separator line and the job name so output is easy to read
    print("\n" + "=" * 60)
    print(f"Job: {job_id}")

    # Use GPT to extract structured data from the job description text
    # This gives us a clean list of required skills from the JD
    jd_data = extract_document_data(job_text)

    # Get only the skills list from the extracted JD data
    jd_skills = jd_data["skills"]

    # Print the skills required by this job so we can see what GPT extracted
    print("\nJD Skills:")
    print(jd_skills)

    # Use GPT to compare JD skills against the resume summary
    # Passing resume_summary (structured list) instead of full resume text for better accuracy
    # GPT will return which skills are matched and which are missing
    results = llm_skill_match(jd_skills, resume_summary)

    # Print the skills that the candidate has (directly or through related technologies)
    print("\nMatched Skills:")
    print(results["matched_skills"])

    # Print the skills that the candidate is missing or has no evidence of
    print("\nMissing Skills:")
    print(results["missing_skills"])

    # Calculate ATS score based on how many JD skills the candidate matched
    matched_count = len(results["matched_skills"])   # number of skills the candidate has
    total_skills = len(jd_skills)                    # total skills the job requires

    # Calculate percentage, avoid division by zero if JD has no skills
    ats_score = round((matched_count / total_skills) * 100, 2) if total_skills > 0 else 0

    print(f"\nATS Score: {ats_score}%")
    print(f"Matched {matched_count} out of {total_skills} skills")
