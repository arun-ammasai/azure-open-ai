from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key= "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"
)

response = client.responses.create(
    model="gpt-4o-mini",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)