import json
from src.llm.prompts import (document_extraction_prompt)
from src.llm.llm_client import (call_llm)


def extract_document_data(text):
    # Generate prompt containing extraction instruction and the resume content
    prompt = document_extraction_prompt(text)

    # Sends the prompt to LLM (openai/gpt-3.5-turbo) and receive the response as JSON string 
    response = call_llm(prompt)

    # Converts the JSON string returned by the LLM into a python dictionary and returns it
    data = json.loads(response)

    if "skills" in data:
        data["skills"] = [ skill.lower().strip()
                            for skill in data["skills"]
                         ]  
    return data