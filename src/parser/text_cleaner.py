import re   # re is Python's built-in library for working with regular expressions (pattern matching in text)


def clean_text(text):
    # This function cleans up raw text extracted from a PDF
    # It is used ONLY for generating embeddings — NOT for sending to GPT
    # (Sending cleaned text to GPT would destroy technical terms like C++, scikit-learn, .NET)

    # Convert all text to lowercase so "Python" and "python" are treated the same
    text = text.lower()

    # Remove all special characters except letters, numbers, and spaces
    # This removes things like @, #, !, /, etc. that add noise to embeddings
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # Replace multiple spaces or newlines with a single space
    # This cleans up messy formatting from PDF extraction
    text = re.sub(r"\s+", " ", text)

    # Remove any leading or trailing spaces from the final text
    text = text.strip()

    # Return the cleaned text
    return text
