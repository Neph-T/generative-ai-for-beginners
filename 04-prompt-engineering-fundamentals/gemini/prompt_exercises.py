import os
from google import genai

# Initialize the Gemini client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-3.5-flash-lite"

print("==========================================")
print("1. ZERO-SHOT PROMPTING")
print("==========================================")
# Zero-shot: Giving a direct instruction with no prior examples
zero_shot_prompt = "Summarize the main security challenges faced by South African farmers."

response_zero = client.models.generate_content(model=MODEL, contents=zero_shot_prompt)
print(response_zero.text)


print("\n==========================================")
print("2. FEW-SHOT PROMPTING")
print("==========================================")
# Few-shot: Providing examples to guide the model's output format and tone
few_shot_prompt = """
Classify the following farm incident reports as either 'Critical Threat' or 'Routine Notice'.

Example 1:
Input: Motion detected on fence line zone 4 at 2:00 AM, thermal camera shows human figures.
Output: Critical Threat

Example 2:
Input: Scheduled drone battery check completed successfully at 10:00 AM.
Output: Routine Notice

Target Input:
Input: Vibration sensor triggered near cattle kraal, two unknown vehicles spotted parked on dirt road.
Output:
"""

response_few = client.models.generate_content(model=MODEL, contents=few_shot_prompt)
print(response_few.text)


print("\n==========================================")
print("3. SYSTEM PROMPTS & TEMPLATES")
print("==========================================")
# Using System instructions to anchor persona and guardrails, and templates for user input
system_instruction = (
    "You are an expert AI agricultural security consultant for South African farms. "
    "Provide concise, actionable, and safety-focused recommendations."
)

user_template = f"""
Analyze the following farm setup and recommend the best drone patrol frequency:
- Farm Size: {500} hectares
- Primary Stock: Cattle and Sheep
- Risk Level: High stock theft zone
"""

# In the google-genai SDK, system instructions can be passed via config
from google.genai import types

config = types.GenerateContentConfig(system_instruction=system_instruction, temperature=0.2)

response_system = client.models.generate_content(model=MODEL, contents=user_template, config=config)
print(response_system.text)
