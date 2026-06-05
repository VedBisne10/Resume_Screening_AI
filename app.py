from src.matcher.pipeline import process_resume
from src.llm.extractor import extract_document_data
from src.parser.text_cleaner import clean_text
from src.parser.pdf_parser import extract_text_from_pdf
from src.utils.helpers import load_job_descriptions

job_descriptions = (load_job_descriptions("data/job_descriptions/"))

text = extract_text_from_pdf("data/resumes/Resume.pdf")

cleaned_text = clean_text(text)

resume_data = extract_document_data(cleaned_text)

for job_id, job_text in (job_descriptions.items()):
    print("\n" + "=" * 50)
    print(f"Job: {job_id}")
    jd_data = (extract_document_data(job_text))
    print("\nExtracted JD Skills:")
    print(jd_data["skills"])


print("\nExtracted Resume Skills: ")
print("Skills:", resume_data["skills"])
print("\nEducation:", resume_data["education"])
print("\nExperience:", resume_data["experience"])
print("\nCertifications:", resume_data["certifications"])

# results = process_resume(
#     "data/resumes/Resume.pdf"
# )

# for job in results:
#     print("\n---------------------")
#     print(f"Job: {job['job_id']}")
#     print(f"Skill Score: {job['skill_score']}")
#     print(f"Embedding Score: {job['embedding_score']}")
#     print(f"Final Score: {job['final_score']}")
#     print("\nMatched Skills: ")
#     for skill in job["matched_skills"]:
#         print(f"✓ {skill}")
#     print("\nMissing Skills:")
#     for skill in job["missing_skills"]:
#         print(f"✗ {skill}")