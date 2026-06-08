from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def call_llm(prompt):
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        temperature = 0,
        max_tokens= 1000,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content