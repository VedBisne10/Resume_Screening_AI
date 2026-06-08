from sklearn.metrics.pairwise import cosine_similarity
from src.extractor.skill_extractor import extract_skills
from src.matcher.embedding_matcher import generate_embedding
from src.llm.extractor import extract_document_data
from src.matcher.semantic_matcher import semantic_skill_matching
from src.llm.skill_matcher import llm_skill_match

def calculate_skill_match_score(resume_summary, jd_skills):
    # Convert resume skills to lowercase and store in a set to make comparison case-insensitive and remove duplicates
    resume_summary = set(skill.lower() for skill in resume_summary)

    # Convert JD skills to lowercase and store in a set to make comparison case-insensitive and remove duplicates
    jd_skills = set(skill.lower()for skill in jd_skills)

    # Find skills that are common in both resume and job description
    skill_details = llm_skill_match(resume_summary, jd_skills)

    matched_count = len(skill_details["matched_skills"])

    # It prevents division by zero if no skills are found in the job description
    if len(jd_skills) == 0:
        return 0

    # Calculate skill match percentage
    score = (matched_skills / len(jd_skills)) * 100

    return round(score, 2)


def calculate_embedding_similarity(resume_embedding, jd_embedding):
    # Calculate the cosine similarity between the resume embedding and jd embedding
    similarity = cosine_similarity([resume_embedding], [jd_embedding])[0][0]
    
    # Convert similarity score into percentage and round it to 2 decimal places
    return round(similarity * 100, 2)


def calculate_final_score(skill_score, embedding_score):
    # Calulate the final match score using weighted averaging of 40% skill match score and 60% embedding similarity score
    final_score = (
        (0.4 * skill_score) + (0.6 * embedding_score)
    )

    return round(final_score, 2)


def get_skill_match_details(resume_text, jd_skills):
    print("Using LLM matcher")
    return llm_skill_match(jd_skills, resume_text)


def rank_jobs(resume_text, resume_embedding, job_descriptions):
    ranked_jobs = []

    # Process each job description
    for job_id, job_text in job_descriptions.items():

        # Extract skills from JD by using extract_skills function
        jd_data = extract_document_data(job_text)
        
        jd_skills = jd_data["skills"]

        # Generate JD embeddings by using generate_embedding function
        jd_embedding = generate_embedding(job_text)

        # Calculate skill match score by using calculate_skill_match_score function
        skill_score = calculate_skill_match_score(resume_text, jd_skills)

        # Calculate embedding similarity score by using calculate_embedding_similarity function
        embedding_score = calculate_embedding_similarity(resume_embedding, jd_embedding)

        # Calculate final hybrid score by using calculate_final_score function
        final_score = calculate_final_score(skill_score, embedding_score)

        # Find matched and missing skills between the resume and the job description
        skill_details = get_skill_match_details(resume_text, jd_skills)

        # Store all details in ranked_jobs as dictionaries
        ranked_jobs.append(
            {
                "job_id": job_id,
                "skill_score": skill_score,
                "embedding_score": embedding_score,
                "final_score": final_score,
                "matched_skills": skill_details["matched_skills"],
                "missing_skills":skill_details["missing_skills"]
            }
        )

        # Sort jobs by final score in descending order (without reverse=True, it will sort in ascending order)
        # Lambda function used because only final_score is to be extracted from each dictionary that will be created in ranked_jobs
        ranked_jobs.sort(key = lambda job: job["final_score"], reverse=True)
    
    return ranked_jobs


