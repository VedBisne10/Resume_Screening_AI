from src.parser.pdf_parser import extract_text_from_pdf         # Importing the text extraction function from parser folder
from src.parser.text_cleaner import clean_text          

# Specifying which resume's text should be extracted
pdf_path = "data/resumes/Resume.pdf"       

# Calling the function of text extraction
raw_text = extract_text_from_pdf(pdf_path)      

# function to remove special characters, spaces, and convert all the text into lower case
cleaned_text = clean_text(raw_text)       

# Printing the extracted text
print(cleaned_text)        
