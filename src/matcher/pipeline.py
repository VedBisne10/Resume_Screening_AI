from src.parser.pdf_parser import (extract_text_from_pdf)
from src.parser.text_cleaner import (clean_text)
from src.extractor.skill_extractor import (extract_skills)
from src.matcher.embedding_matcher import (generate_embedding)
from src.matcher.scorer import (rank_jobs)
from src.utils.helpers import (load_job_descriptions)


def process_resume(resume_path):

    # Extract resume text from pdf
    resume_text = extract_text_from_pdf(resume_path)

    # Clean text from the extracted resume text
    cleaned_text = clean_text(resume_text)

    # Extract skills from the cleaned text
    resume_skills = extract_skills(cleaned_text)

    # Generate embedding of the cleaned_text so nothing is left out
    resume_embedding = (generate_embedding(cleaned_text))

    # Load all JDs in the job_descriptions folder
    job_descriptions = (load_job_descriptions("data/job_descriptions"))

    # Rank jobs
    ranked_jobs = rank_jobs(cleaned_text, resume_embedding, job_descriptions)

    return ranked_jobs