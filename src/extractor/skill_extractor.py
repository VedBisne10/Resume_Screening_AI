import spacy
from src.utils.constants import SKILLS

# Load SpaCy English NLP model
nlp = spacy.load("en_core_web_sm")

def extract_skills(text):
 
    # Process the text containing tokens, entities, sentences, etc with SpaCy 
    doc = nlp(text)
    extracted_skills = set()       # Used set instead of list because, list allows duplicate values and set does not

    # Convert all tokens to lowercase
    tokens = []
    for token in doc:
        tokens.append(token.text.lower())

    # Check single-word skills
    for skill in SKILLS:
        if " " not in  skill:
            if skill.lower() in tokens:
                extracted_skills.add(skill)

    # Check multi-word skills
    text_lower = text.lower()
    for skill in SKILLS:
        if " " in skill:
            if skill.lower() in text_lower:
                extracted_skills.add(skill)

    return list(extracted_skills)