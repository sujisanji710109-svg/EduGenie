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


def get_learning_recommendations(topic: str) -> str:
    """Generates a structured learning roadmap."""

    if not API_KEY:
        return "⚠️ Gemini API key is missing. Check your .env file."

    if not topic or not topic.strip():
        return "⚠️ Please enter a topic."

    prompt = f"""
You are EduGenie, an expert AI tutor.

The student wants to learn:

{topic.strip()}

Create a practical learning roadmap.

Include:

1. Prerequisites
2. Beginner Level
3. Intermediate Level
4. Advanced Level
5. Suggested timeline
6. Practice exercises
7. Mini projects
8. Final project
9. Recommended learning resources
10. Suggested order of study

Keep the roadmap realistic for a student.

Use clear headings and bullet points.
"""

    last_error = ""

    for attempt, model_name in enumerate(GEMINI_MODELS, start=1):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.4,
                    max_output_tokens=3000,
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