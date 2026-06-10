from PyPDF2 import PdfReader     # PdfReader is used to open and read text content from PDF files


def extract_text_from_pdf(pdf_path: str) -> str:
    # This function takes the path to a PDF file and returns all its text as a single string
    # pdf_path: the location of the PDF file (e.g. "data/resumes/Resume.pdf")

    try:
        # Open the PDF file using PdfReader
        reader = PdfReader(pdf_path)

        # Start with an empty string — we will add each page's text to this
        extracted_text = ""

        # Loop through every page in the PDF one by one
        for page in reader.pages:

            # Extract the text from the current page
            page_text = page.extract_text()

            # Only add the text if the page actually has some text (not a blank page)
            if page_text:
                # Add this page's text to the full text, with a new line after each page
                extracted_text += page_text + "\n"

        # Return the complete text from all pages combined
        return extracted_text

    except Exception as e:
        # If anything goes wrong while reading the PDF (file not found, corrupted, etc.)
        # print the error and return an empty string instead of crashing
        print(f"Error reading PDF: {e}")
        return ""
