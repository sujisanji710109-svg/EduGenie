# Phase 5: Project Development Phase - EduGenie

## 1. Technical Stack & Implementation Highlights
- **FastAPI Core**: Leveraged FastAPI's asynchronous routing capabilities to handle incoming requests concurrently without blocking the server loop.
- **Direct REST Integration**: Adopted direct HTTP calls to the Google Generative Language v1/v1beta endpoint over standard Python wrapper packages to avoid library version mismatches.
- **HTTPX Integration**: Implemented persistent client sessions using `httpx.Client` equipped with custom user-agents, automatic redirects, and strict 30-second timeouts.
- **Defensive Model Fallback**: Implemented sequential endpoint polling (`gemini-1.5-flash` -> `gemini-1.5-pro`) to ensure high availability even if a specific model tag undergoes cloud maintenance.

---

## 2. Core Implementation Artifacts

### Core Engine (`call_gemini` Architecture)
```python
def call_gemini(prompt: str) -> str:
    if not api_key:
        return "⚠️ Gemini API key is missing. Check your .env file."
    
    endpoints = [
        f"[https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=](https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=){api_key}",
        f"[https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key=](https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key=){api_key}",
        f"[https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=](https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=){api_key}"
    ]
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) EduGenie/1.0"
    }
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    with httpx.Client(timeout=30.0, verify=True) as client:
        for url in endpoints:
            res = client.post(url, json=payload, headers=headers)
            if res.status_code == 200:
                data = res.json()
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
Assessment Deserialization Logic
Python
# Cleaning raw LLM output to guarantee valid JSON formatting
cleaned_json = re.sub(r"^```(?:json)?\n?", "", raw_response.strip(), flags=re.IGNORECASE)
cleaned_json = re.sub(r"\n?```$", "", cleaned_json.strip())
quiz_data = json.loads(cleaned_json)
3. Directory Layout
EduGenie/
├── static/
│   └── style.css            # Custom responsive styles & typography
├── templates/
│   └── index.html           # Unified interactive single page dashboard
├── .env                     # Private environmental variable credentials
├── .gitignore               # Excludes secrets, caches, and venv files
├── main.py                  # Main API gateway, module handlers, and runners
├── explanation_module.py    # Specialized concept expansion routines
├── learning_path.py         # Roadmap recommendation generators
├── qna.py                   # Direct question resolution services
├── quiz_module.py           # Multiple-choice quiz generator
├── requirements.txt         # Pinned project dependencies
└── summary_module.py        # Text condensation and extraction module
