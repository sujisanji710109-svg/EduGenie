import os
import json
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


def clean_json(text: str) -> str:
    """Removes markdown code fences from JSON response."""

    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    return text


def generate_quiz(text: str) -> list:
    """Generates exactly 3 MCQs with 4 options each."""

    if not API_KEY:
        return [{
            "error": "⚠️ Gemini API key is missing."
        }]

    if not text or not text.strip():
        return [{
            "error": "⚠️ Please provide text for the quiz."
        }]

    prompt = f"""
You are EduGenie Quiz Generator.

Create exactly 3 multiple-choice questions from the passage below.

Each question MUST contain:
- question
- options: exactly 4 options
- answer: the correct option text

Return ONLY a JSON array.

Required format:

[
  {{
    "question": "Question here",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "answer": "Option 1"
  }}
]

Rules:
- Exactly 3 questions.
- Exactly 4 options per question.
- One correct answer per question.
- The answer must exactly match one option.
- Questions must be based only on the provided text.
- No markdown.
- No explanation outside JSON.

Passage:
{text.strip()}
"""

    last_error = ""

    for attempt, model_name in enumerate(GEMINI_MODELS, start=1):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=2000,
                    response_mime_type="application/json",
                ),
            )

            if not response or not response.text:
                last_error = (
                    f"Attempt {attempt} ({model_name}): Empty response."
                )
                continue

            cleaned = clean_json(response.text)

            quiz_data = json.loads(cleaned)

            if not isinstance(quiz_data, list):
                raise ValueError("Gemini returned invalid quiz format.")

            if len(quiz_data) != 3:
                raise ValueError("Gemini did not generate exactly 3 questions.")

            for question in quiz_data:
                if not isinstance(question, dict):
                    raise ValueError("Invalid question format.")

                if "question" not in question:
                    raise ValueError("Missing question field.")

                if "options" not in question:
                    raise ValueError("Missing options field.")

                if "answer" not in question:
                    raise ValueError("Missing answer field.")

                if len(question["options"]) != 4:
                    raise ValueError("Each question must have 4 options.")

                if question["answer"] not in question["options"]:
                    raise ValueError(
                        "Answer does not match one of the options."
                    )

            return quiz_data

        except Exception as e:
            last_error = (
                f"Attempt {attempt} ({model_name}): {str(e)}"
            )

    return [{
        "error": (
            "⚠️ Quiz generation failed.\n"
            f"{last_error}"
        )
    }]