import os
import time
from google import genai
from google.genai.errors import ServerError

# Initialize the Gemini client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Set the active model gemini-3.5-flash-lite
MODEL = "gemini-3.5-flash-lite"


# Robust retry helper function using e.code instead of status_code
def generate_with_retry(client, model, contents, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(model=model, contents=contents)
        except ServerError as e:
            # Check e.code for 503 (server overloaded/unavailable)
            if e.code == 503 and attempt < max_retries - 1:
                wait_time = 2 * (attempt + 1)
                print(f"Model busy (503). Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e


# Prompt 1: Simple prompt
simple_prompt = """
Explain Artificial Intelligence.
"""

# Prompt 2: Detailed prompt
detailed_prompt = """
You are an experienced technology teacher.

Explain Artificial Intelligence to a beginner
who has no programming experience.

Requirements:
1. Use simple English.
2. Explain what Artificial Intelligence means.
3. Give three practical examples.
4. Keep the explanation under 200 words.
5. Include a short summary at the end.
"""

# Send the first prompt
print("\n========== SIMPLE PROMPT ==========\n")
response1 = generate_with_retry(client, MODEL, simple_prompt)
print(response1.text)

# Send the second prompt
print("\n========== DETAILED PROMPT ==========\n")
response2 = generate_with_retry(client, MODEL, detailed_prompt)
print(response2.text)
