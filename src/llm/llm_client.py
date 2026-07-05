from openai import OpenAI       # OpenAI library used to talk to LLM models via API
import streamlit as st          # Streamlit is used to access secrets stored in Streamlit Cloud
import time                     # time is used to add a delay between retries when rate limited

# Read the API key from Streamlit Secrets
# On Streamlit Cloud: add OPENROUTER_API_KEY in Settings -> Secrets
# For local development: add it to .streamlit/secrets.toml file
client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],   # API key loaded from Streamlit secrets — never hardcode this
    base_url="https://openrouter.ai/api/v1"     # OpenRouter's API address
)


def call_llm(prompt, retries=3, delay=30):
    # This function takes a text prompt and sends it to the LLM, then returns the response
    # retries: how many times to retry if rate limited (default 3)
    # delay: how many seconds to wait between retries (default 10 seconds)

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b:free",   # Free model on OpenRouter
                temperature=0,                      # Temperature 0 means consistent, deterministic answers
                max_tokens=2000,                    # Max tokens for the response
                messages=[{"role": "user", "content": prompt}]  # Send the prompt as a user message
            )

            # Extract and return the text content from the response
            return response.choices[0].message.content

        except Exception as e:
            error_str = str(e)

            # Check if the error is a rate limit (429) error
            if "429" in error_str or "rate" in error_str.lower():
                if attempt < retries - 1:
                    # If we still have retries left, wait and try again
                    print(f"Rate limited. Waiting {delay} seconds before retry {attempt + 2}/{retries}...")
                    time.sleep(delay)
                else:
                    # If all retries are exhausted, print error and return None
                    print(f"Rate limit exceeded after {retries} attempts. Skipping this call.")
                    return None
            else:
                # If it's a different error (not rate limit), don't retry — just return None
                print(f"LLM error: {e}")
                return None
