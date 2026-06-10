from openai import OpenAI       # OpenAI library used to talk to GPT models via API
from dotenv import load_dotenv  # load_dotenv reads the .env file and loads the API key into the environment
import os                       # os is used to read environment variables like the API key
import time                     # time is used to add a delay between retries when rate limited

# Load the .env file so we can access OPENROUTER_API_KEY stored inside it
load_dotenv()

# Create a connection to OpenRouter (which gives us access to GPT models)
# api_key: our secret key stored in .env file — never hardcode this in the code
# base_url: OpenRouter's API address instead of the default OpenAI address
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def call_llm(prompt, retries=3, delay=10):
    # This function takes a text prompt and sends it to the LLM, then returns the response
    # retries: how many times to retry if rate limited (default 3)
    # delay: how many seconds to wait between retries (default 10 seconds)

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b:free",   # Free model on OpenRouter
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
    