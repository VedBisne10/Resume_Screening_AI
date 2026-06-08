from sklearn.metrics.pairwise import cosine_similarity
from src.matcher.embedding_matcher import (generate_embedding)

def semantic_skill_matching(resume_skills, jd_skills, threshold=0.70):
    matched_skills = []
    missing_skills = []

    for jd_skill in jd_skills:

        jd_embedding = generate_embedding(jd_skill)
        best_similarity = 0
        for resume_skill in resume_skills:
            resume_embedding = (generate_embedding(resume_skill))

            similarity = cosine_similarity([jd_embedding], [resume_embedding])[0][0]

            best_similarity = max(best_similarity, similarity)

        if best_similarity >= threshold:
            matched_skills.append(jd_skill)

        else:
            missing_skills.append(jd_skill)

    return {
        "matched_skills":
            matched_skills,
        "missing_skills":
            missing_skills
    }