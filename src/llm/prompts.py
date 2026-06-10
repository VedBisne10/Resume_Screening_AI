def document_extraction_prompt(text):
    # This function builds the instruction we send to GPT for extracting information
    # from any document — works for both resumes and job descriptions
    # It returns a formatted string (the prompt) that tells GPT exactly what to do

    return f"""
You are an expert ATS (Applicant Tracking System) parser.

Analyze the following document and extract:
1. Technical Skills
2. Education
3. Experience
4. Certifications

IMPORTANT RULES:

- Extract ONLY actual technical skills, tools, technologies,
  programming languages, frameworks, libraries, databases,
  cloud platforms, and software.

- Do NOT include category names such as:
  Programming
  Libraries
  Frameworks
  Tools
  Technologies
  Skills

- Do NOT include soft skills such as:
  Communication
  Teamwork
  Leadership
  Problem Solving
  Time Management

- Return skills as individual items.

- Extract all the education and experience present in the resume

- Extract experience with its details about the experience

Bad Examples:
Programming
Libraries
Frameworks
Technical Skills
Analytical Skills
Problem Solving Skills

Return ONLY valid JSON.

Schema:

{{
    "skills": [],
    "education": [],
    "experience": [],
    "certifications": []
}}

Document:

{text}
"""


def skill_validation_prompt(jd_skills, resume_summary):
    # This function builds the instruction we send to GPT for matching skills
    # It takes the list of required JD skills and the candidate's resume summary
    # and asks GPT to evaluate ALL skills at once and return YES or NO for each

    # Convert the list of JD skills into a formatted bullet list for the prompt
    # Example: ["Python", "Docker"] becomes "- Python\n- Docker"
    skills_list = "\n".join(f"- {skill}" for skill in jd_skills)

    return f"""
You are an expert technical recruiter evaluating a candidate's resume.

Resume Summary:
{resume_summary}

Required Skills from Job Description:
{skills_list}

Instructions:
- For each skill, return YES if the candidate demonstrates that competency
  either directly (skill is mentioned) OR indirectly (they have used
  technologies/built projects that prove that skill).
- Return NO only if there is genuinely no evidence of that skill.

Good inference examples:
- Resume has PyTorch, scikit-learn, built regression model -> "Machine Learning" = YES
- Resume has React, built frontend dashboards -> "JavaScript" = YES
- Resume has Docker, deployed on AWS EC2 -> "DevOps" = YES

Bad inference examples:
- Resume has Python -> "Java" = NO
- Resume has SQL -> "Hibernate" = NO
- Resume has Excel -> "Power BI" = NO

Return ONLY valid JSON where keys are skill names and values are YES or NO.

Example output format:
{{
    "Machine Learning": "YES",
    "Java": "NO",
    "REST APIs": "YES"
}}
"""
