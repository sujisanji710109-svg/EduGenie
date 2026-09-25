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


def answer_question_with_gemini(question: str) -> str:
    """Answers general and academic questions using Gemini."""

    if not API_KEY:
        return "⚠️ Gemini API key is missing. Check your .env file."

    if not question or not question.strip():
        return "⚠️ Please enter a question."

    prompt = f"""
You are EduGenie, an AI educational assistant.

Answer the student's question clearly and accurately.

Student question:
{question.strip()}

Instructions:
- Give the direct answer first.
- Explain in simple student-friendly language.
- Use examples when helpful.
- Use headings and bullet points when appropriate.
- For academic questions, explain step by step.
- Do not unnecessarily make the answer too long.
"""

    last_error = ""

    for attempt, model_name in enumerate(GEMINI_MODELS, start=1):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.4,
                    max_output_tokens=2048,
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