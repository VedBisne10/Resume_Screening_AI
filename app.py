from src.parser.pdf_parser import extract_text_from_pdf

pdf_path = "data/resumes/Resume.pdf"
text = extract_text_from_pdf(pdf_path)
print(text)