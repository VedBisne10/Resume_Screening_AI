from PyPDF2 import PdfReader     # Importing PyPDF2 for reading and extracting texts from PDF.

def extract_text_from_pdf(pdf_path: str) -> str:       # Function for text extraction with type hints
    try:
        reader = PdfReader(pdf_path)        # Opens the pdf file using pdfReader
        extracted_text = ""                 # Creates an empty string to store text extracted from all the pages

        for page in reader.pages:           # Loop through every page in the pdf
            page_text = page.extract_text()     # Extract text from the current page

            if page_text:        # Check if any text is extracted from the pdf
                extracted_text += page_text + "\n"       # Adds extracted page text to the final text and '\n' adds a new line after each page 
        
        return extracted_text       # Returns the complete extracted text from pdf

    except Exception as e:          # Handles any error that occur while reading the pdf
        print(f"Error reading PDF: {e}")
        return ""               # Returns empty string if extraction fails.