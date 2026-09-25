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


def explain_topic(topic: str) -> str:
    """Explains an educational topic using Gemini."""

    if not API_KEY:
        return "⚠️ Gemini API key is missing. Check your .env file."

    if not topic or not topic.strip():
        return "⚠️ Please enter a topic."

    prompt = f"""
You are EduGenie, an expert educational tutor.

Explain this topic to a student:

Topic:
{topic.strip()}

Structure the explanation like this:

1. Simple Definition
2. How It Works
3. Important Points
4. Simple Real-World Example
5. Short Summary

Rules:
- Use simple language.
- Explain step by step.
- Avoid unnecessary technical complexity.
- Make it useful for a school or college student.
"""

    last_error = ""

    for attempt, model_name in enumerate(GEMINI_MODELS, start=1):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.4,
                    max_output_tokens=2500,
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