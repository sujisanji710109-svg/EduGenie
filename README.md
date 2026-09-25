# Phase 3: Project Design Phase - EduGenie

## 1. System Architecture Overview
EduGenie employs a decoupled client-server architecture. The presentation layer communicates with the high-performance asynchronous FastAPI backend via standard RESTful endpoints. The backend acts as an orchestration gateway, transforming client payloads into conditioned prompt schemas before querying the Google Generative Language inference engine.
+-------------------------------------------------------------+
|                     Client Web Browser                      |
|  (Responsive HTML5 / CSS3 / ES6 Fetch API / DOM Rendering)  |
+------------------------------+------------------------------+
|  HTTP / REST (JSON)
v
+-------------------------------------------------------------+
|                 FastAPI Application Gateway                 |
|                   (Uvicorn ASGI Listener)                   |
|  - Route Dispatcher (/qa, /explain, /summarize, /quiz)      |
|  - Input Validation & CORS Middleware                       |
|  - Static Asset Delivery Engine                             |
+------------------------------+------------------------------+
|
v
+-------------------------------------------------------------+
|                  Gemini Connector Service                   |
|  - Environment Secret Ingestion (.env)                      |
|  - HTTPX Async Connection Pool                              |
|  - Multi-Endpoint Fallback Router                           |
|  - Response Validation & Regex JSON Sanitizer               |
+------------------------------+------------------------------+
|  HTTPS / REST (TLS 1.3)
v
+-------------------------------------------------------------+
|             Google Generative Language Platform             |
|                  (gemini-1.5-flash Engine)                  |
+-------------------------------------------------------------+


---

## 2. API Design & Endpoint Specification

### `GET /qa`
- **Description**: Ingests student question queries and returns real-time conceptual explanations.
- **Query Parameter**: `question` (string, required)
- **Response**: `{"answer": "string"}`

### `POST /explain/`
- **Description**: Breaks down an academic subject into an intuitive pedagogical explanation.
- **Payload**: `{"topic": "string"}`
- **Response**: `{"topic": "string", "explanation": "string"}`

### `POST /summarize/`
- **Description**: Synthesizes dense passages into key actionable bulleted points.
- **Payload**: `{"text": "string"}`
- **Response**: `{"summary": "string"}`

### `POST /quiz`
- **Description**: Generates a structured 3-question multiple choice assessment based on text.
- **Payload**: `{"text": "string"}`
- **Response**:
```json
{
  "quiz": [
    {
      "question": "string",
      "options": ["string", "string", "string", "string"],
      "answer": "string"
    }
  ]
}
GET /learn/recommendations
Description: Synthesizes a structured, milestone-driven learning roadmap.

Query Parameter: topic (string, required)

Response: {"topic": "string", "recommendation": "string"}

3. UI/UX & Layout Design
Single Page Application (SPA) Paradigm: Seamless navigation through dynamic DOM manipulation avoiding complete page reloads.

Visual Hierarchy: Modern card-based UI container layout utilizing clean border-radius, distinct drop-shadow elevations, and ergonomic input spacing.

Status Indicators & Feedback: Interactive loading states and error notifications to keep the user informed during asynchronous remote calls.
