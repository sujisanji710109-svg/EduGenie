import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.5-flash-lite",
]

client = genai.Client(api_key=API_KEY) if API_KEY else None


def summarize_text(text: str) -> str:
    """Summarizes educational text using Gemini."""

    if not API_KEY:
        return "⚠️ Gemini API key is missing. Check your .env file."

    if not text or not text.strip():
        return "⚠️ Please provide text to summarize."

    prompt = f"""
You are EduGenie, an educational AI assistant.

Summarize the following text.

Requirements:
- Keep the important information.
- Remove unnecessary repetition.
- Use simple language.
- Use bullet points when useful.
- Preserve important facts.
- Make it easy for a student to revise.

Text:
{text.strip()}
"""

    last_error = ""

    for attempt, model_name in enumerate(GEMINI_MODELS, start=1):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=2000,
                ),
            )

            if response and response.text:
                return response.text.strip()

            last_error = f"Attempt {attempt} ({model_name}): Empty response."

        except Exception as e:
            last_error = f"Attempt {attempt} ({model_name}): {str(e)}"

    return (
        "⚠️ Gemini AI is temporarily unavailable.\n\n"
        f"Last error: {last_error}"
    )