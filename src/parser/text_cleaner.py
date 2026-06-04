import re

def clean_text(text):
    # Convert all text to lowercase
    text = text.lower()        

    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)       

    # Remove multiple spaces and newlines 
    text = re.sub(r"\s+", " ", text)       

    # Remove leading and trailing spaces 
    text = text.strip()         

    return text
