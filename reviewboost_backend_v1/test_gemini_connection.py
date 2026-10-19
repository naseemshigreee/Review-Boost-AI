"""Send a simple test prompt using GEMINI_API_KEY from the environment or backend .env."""

import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

load_dotenv(Path(__file__).with_name(".env"))

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("GEMINI_API_KEY is not set. Add it to .env or your environment.")

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model=os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
    contents="Hello, kaise ho?",
)

if not response.text:
    raise RuntimeError("Gemini returned an empty response.")

print(response.text)
