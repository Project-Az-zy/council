import os
import string
import random

from google import genai
from pydantic import BaseModel

print("\033[H\033[J", end="")
print("[ RESOURCES ]")
print("YouTube transcript: https://www.youtube-transcript.io")
print("[ AWAITING INPUT... ]\n> ", end="")
personality_base = input()
print("[ PROCESSING... ]")

class PersonalityParsed(BaseModel):
    keywords: list[str]
    worldview: str
    alignment: str
    key_notes: str
    things_to_remember: str

client = genai.Client(api_key=os.environ['KEY_GENAI'])
response = client.models.generate_content(
    model="gemini-2.5-flash-preview-05-20",
    contents=f"Extract from the text below the represented worldview, alignment, key notes and important things to remember. Afterwards, summarize everything with three keywords.\n\n{personality_base}",
    config={
        "response_mime_type": "application/json",
        "response_schema": PersonalityParsed,
    },
)

print("\n")
print(response.text)

class PersonalityFile(BaseModel):
    source: str
    keywords: list[str]
    personality: str

personality = PersonalityFile(
    source = personality_base,
    keywords = response.parsed.keywords,
    personality = f"Worldview:\n{response.parsed.worldview}\n\nAlignment:\n{response.parsed.alignment}\n\nKey notes:\n{response.parsed.key_notes}\n\nThings to remember:\n{response.parsed.things_to_remember}"
)
filename = ('-'.join(personality.keywords[:3])+'-'+''.join(random.choices(string.ascii_lowercase + string.digits, k=6))+'.person').lower().replace(" ", "-")
print(filename)
with open(f"/personalities/{filename}", "w") as f:
  f.write(personality.model_dump_json())
print("\n\n[ PERSONALITY GENERATED :) ]")