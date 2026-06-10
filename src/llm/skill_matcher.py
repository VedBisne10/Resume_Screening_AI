from src.llm.prompts import skill_validation_prompt      # Import the prompt builder function that creates the instruction for GPT
from src.llm.llm_client import call_llm                  # Import the function that actually sends the prompt to GPT and gets a response
import json                                              # Import json so we can convert GPT's text response into a Python dictionary


def llm_skill_match(jd_skills, resume_summary):
    # Build the prompt by passing all JD skills and the resume summary to the prompt function
    # This creates one single instruction that asks GPT to evaluate ALL skills at once
    prompt = skill_validation_prompt(jd_skills, resume_summary)

    # Send the prompt to GPT and store the response
    # GPT will return a JSON string like: {"Machine Learning": "YES", "Java": "NO"}
    response = call_llm(prompt)

    # Try to convert GPT's text response into a Python dictionary
    try:
        # If response is None (model returned no content), treat it as a failed match
        if not response:
            raise ValueError("LLM returned empty response")

        # Strip markdown code blocks if the model wrapped the JSON in ```json ... ```
        cleaned = response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[-1]
        if cleaned.endswith("```"):
            cleaned = cleaned.rsplit("```", 1)[0]

        # json.loads() converts a JSON string into a Python dictionary
        results = json.loads(cleaned.strip())

    except (json.JSONDecodeError, ValueError):
        # If GPT returned something unexpected that is not valid JSON, we handle the error here
        # Instead of crashing the program, we default every skill to "NO"
        print(f"Warning: Could not parse LLM response: {response}")

        # Create a dictionary where every skill from JD is marked as "NO" as a safe fallback
        results = {skill: "NO" for skill in jd_skills}

    # Create an empty list to store skills that the candidate HAS
    matched_skills = []

    # Create an empty list to store skills that the candidate is MISSING
    missing_skills = []

    # Loop through each skill and its verdict (YES or NO) from the parsed results
    for skill, verdict in results.items():

        # .strip() removes extra spaces, .upper() converts to uppercase so "yes", "Yes", "YES" all work
        if verdict.strip().upper() == "YES":
            # If GPT said YES, the candidate has this skill — add it to matched list
            matched_skills.append(skill)

        else:
            # If GPT said NO, the candidate is missing this skill — add it to missing list
            missing_skills.append(skill)

    # Return both lists as a dictionary so the caller can use matched and missing skills separately
    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }
