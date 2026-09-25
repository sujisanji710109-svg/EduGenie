from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from qna import answer_question_with_gemini
from explanation_module import explain_topic
from summary_module import summarize_text
from quiz_module import generate_quiz
from learning_path import get_learning_recommendations


# ============================================================
# Base Directory
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="EduGenie",
    description="AI-powered Educational Assistant",
    version="2.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Static / Templates
# ============================================================

static_dir = BASE_DIR / "static"
templates_dir = BASE_DIR / "templates"

if static_dir.exists():
    app.mount(
        "/static",
        StaticFiles(directory=str(static_dir)),
        name="static"
    )


# ============================================================
# Home
# ============================================================

@app.get("/")
async def serve_home():

    index_file = templates_dir / "index.html"

    if not index_file.exists():
        return JSONResponse(
            content={
                "error": "templates/index.html not found."
            },
            status_code=404
        )

    return FileResponse(str(index_file))


# ============================================================
# 1. Q&A
# ============================================================

@app.get("/qa")
async def qa_get(
    question: str = Query(...)
):

    if not question.strip():
        return JSONResponse(
            content={
                "error": "Please enter a question."
            },
            status_code=400
        )

    answer = answer_question_with_gemini(question)

    return {
        "question": question,
        "answer": answer
    }


@app.post("/qa")
async def qa_post(request: Request):

    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            content={
                "error": "Invalid JSON request."
            },
            status_code=400
        )

    question = data.get("question", "")

    if not question or not question.strip():
        return JSONResponse(
            content={
                "error": "Please enter a question."
            },
            status_code=400
        )

    answer = answer_question_with_gemini(question)

    return {
        "question": question,
        "answer": answer
    }


# ============================================================
# 2. Explanation
# ============================================================

@app.post("/explain/")
async def explain_api(request: Request):

    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            content={
                "error": "Invalid JSON request."
            },
            status_code=400
        )

    topic = data.get("topic", "")

    if not topic or not topic.strip():
        return JSONResponse(
            content={
                "error": "Please provide a topic."
            },
            status_code=400
        )

    explanation = explain_topic(topic)

    return {
        "topic": topic,
        "explanation": explanation
    }


# Also support /explain without trailing slash
@app.post("/explain")
async def explain_api_without_slash(request: Request):

    return await explain_api(request)


# ============================================================
# 3. Summary
# ============================================================

@app.post("/summarize/")
async def summarize_api(request: Request):

    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            content={
                "error": "Invalid JSON request."
            },
            status_code=400
        )

    text = data.get("text", "")

    if not text or not text.strip():
        return JSONResponse(
            content={
                "error": "Please provide text to summarize."
            },
            status_code=400
        )

    summary = summarize_text(text)

    return {
        "summary": summary
    }


@app.post("/summarize")
async def summarize_api_without_slash(request: Request):

    return await summarize_api(request)


# ============================================================
# 4. Quiz
# ============================================================

@app.post("/quiz")
async def quiz_api(request: Request):

    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            content={
                "error": "Invalid JSON request."
            },
            status_code=400
        )

    text = data.get("text", "")

    if not text or not text.strip():
        return JSONResponse(
            content={
                "error": "Please provide text for quiz."
            },
            status_code=400
        )

    quiz_data = generate_quiz(text)

    return {
        "quiz": quiz_data
    }


# ============================================================
# 5. Learning Path
# ============================================================

@app.get("/learn/recommendations")
async def learning_recommendation_api(
    topic: str = Query(...)
):

    if not topic.strip():
        return JSONResponse(
            content={
                "error": "Please provide a topic."
            },
            status_code=400
        )

    recommendation = get_learning_recommendations(topic)

    return {
        "topic": topic,
        "recommendation": recommendation
    }


@app.post("/learn/recommendations")
async def learning_recommendation_post(request: Request):

    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            content={
                "error": "Invalid JSON request."
            },
            status_code=400
        )

    topic = data.get("topic", "")

    if not topic or not topic.strip():
        return JSONResponse(
            content={
                "error": "Please provide a topic."
            },
            status_code=400
        )

    recommendation = get_learning_recommendations(topic)

    return {
        "topic": topic,
        "recommendation": recommendation
    }


# ============================================================
# Health Check
# ============================================================

@app.get("/health")
async def health_check():

    return {
        "status": "online",
        "application": "EduGenie",
        "modules": [
            "Q&A",
            "Explanation",
            "Summary",
            "Quiz",
            "Learning Path"
        ]
    }


# ============================================================
# Run Server
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )