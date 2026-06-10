import json                                          # json is used to convert GPT's text response into a Python dictionary
from src.llm.prompts import document_extraction_prompt  # Import the function that builds the extraction instruction for GPT
from src.llm.llm_client import call_llm                 # Import the function that sends prompts to GPT and returns the response


def extract_document_data(text):
    # This function takes any text (resume or JD) and uses GPT to extract
    # structured information like skills, education, experience, and certifications

    # Build the prompt — this creates the full instruction we send to GPT
    # It tells GPT exactly what to extract and in what JSON format
    prompt = document_extraction_prompt(text)

    # Send the prompt to GPT and get back a response
    # GPT will return a JSON string like: {"skills": [...], "education": [...], ...}
    response = call_llm(prompt)

    # Try to convert GPT's JSON string response into a Python dictionary
    try:
        # If response is None (model returned no content), treat it as a failed extraction
        if not response:
            raise ValueError("LLM returned empty response")

        # Strip markdown code blocks if the model wrapped the JSON in ```json ... ```
        # Some models return ```json\n{...}\n``` instead of raw JSON
        cleaned = response.strip()
        if cleaned.startswith("```"):
            # Remove the opening ```json or ``` line
            cleaned = cleaned.split("\n", 1)[-1]
        if cleaned.endswith("```"):
            # Remove the closing ``` line
            cleaned = cleaned.rsplit("```", 1)[0]

        # .strip() removes any remaining extra spaces or newlines before parsing
        data = json.loads(cleaned.strip())

    except (json.JSONDecodeError, ValueError):
        # If GPT returns something unexpected that is not valid JSON, dont crash
        # Instead print a warning and return an empty structure with all keys present
        print(f"Warning: Could not parse LLM response: {response}")
        data = {
            "skills": [],
            "education": [],
            "experience": [],
            "certifications": []
        }

    # If skills were extracted, clean them up
    # .lower() makes all skills lowercase so "Python" and "python" are treated the same
    # .strip() removes any extra spaces around each skill
    if "skills" in data:
        data["skills"] = [skill.lower().strip() for skill in data["skills"]]

    # Return the final structured dictionary with all extracted information
    return data
