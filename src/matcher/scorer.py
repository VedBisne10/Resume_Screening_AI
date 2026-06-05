def calculate_skill_match_score(resume_skills, jd_skills):

    # Convert resume skills to lowercase and store in a set to make comparison case-insensitive and remove duplicates
    resume_skills = set(skill.lower() for skill in resume_skills)

    # Convert JD skills to lowercase and store in a set to make comparison case-insensitive and remove duplicates
    jd_skills = set(skill.lower()for skill in jd_skills)

    # Find skills that are common in both resume and job description
    matched_skills = (resume_skills.intersection(jd_skills))

    # Prevent division by zero if no skills are found in the job description
    if len(jd_skills) == 0:
        return 0

    # Calculate skill match percentage
    score = (len(matched_skills) / len(jd_skills)) * 100

    return round(score, 2)
