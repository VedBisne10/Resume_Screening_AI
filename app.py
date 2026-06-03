from src.parser.pdf_parser import extract_text_from_pdf         # Importing the text extraction function from parser folder

pdf_path = "data/resumes/Resume.pdf"                    # Specifying which resume's text should be extracted
text = extract_text_from_pdf(pdf_path)                  # Calling the function of text extraction
print(text)                                             # Printing the extracted text
