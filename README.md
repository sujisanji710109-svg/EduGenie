# Phase 2: Requirement Analysis Phase - EduGenie

## 1. Functional Requirements (FR)
- **FR-01: Q&A Ingestion & Resolution**: The system must accept natural language queries via HTTP GET/POST and return structured, context-rich responses within 3 seconds.
- **FR-02: Pedagogical Concept Explanation**: The system must break down abstract topics into intuitive definitions, real-world analogies, and step-by-step illustrations.
- **FR-03: Text Summarization**: The platform must accept up to 10,000 characters of raw educational text and output high-yield bulleted summaries retaining critical definitions.
- **FR-04: Dynamic Assessment Generation**: The system must extract core concepts from submitted text and generate a structured JSON array containing exactly 3 multi-choice questions, options, and accurate answer indices.
- **FR-05: Learning Roadmap Synthesis**: The system must generate tiered roadmaps covering beginner, intermediate, and advanced milestones based on topic queries.

---

## 2. Non-Functional Requirements (NFR)
- **NFR-01: Latency & Performance**: API response latency for direct inference must not exceed 2.5 seconds under standard broadband conditions.
- **NFR-02: Availability & Fault Tolerance**: The system must implement graceful fallbacks across model endpoints (`gemini-1.5-flash`, `gemini-1.5-pro`) to ensure high uptime.
- **NFR-03: Security & Secret Isolation**: API credentials must never be committed to source control; all secrets must be managed strictly through environmental variables (`.env`).
- **NFR-04: Cross-Platform Accessibility**: The frontend interface must be responsive across desktop, tablet, and mobile viewport resolutions without horizontal overflow.
- **NFR-05: Modularity & Maintainability**: Backend logic must be segregated into standalone modular handlers to allow independent testing and zero regression during updates.

---

## 3. Hardware & Software Requirements

### Software Environment
- **Operating System**: Windows 10/11 64-bit / Linux Ubuntu 22.04 LTS
- **Runtime**: Python 3.10+
- **Backend Framework**: FastAPI (Asynchronous ASGI server powered by Uvicorn)
- **HTTP Client**: HTTPX (Asynchronous HTTP/1.1 and HTTP/2 client)
- **Frontend Engine**: Semantic HTML5, Modern CSS3 Flexbox/Grid, Vanilla JavaScript (ES6+)
- **Large Language Model Service**: Google Cloud Generative Language API (Gemini family)

### Hardware Environment (Local Development)
- **CPU**: Intel Core i3 / AMD Ryzen 3 or higher
- **RAM**: 8 GB minimum
- **Disk Space**: 500 MB free space for virtual environments and runtime caches
- **Network**: Broadband Internet connectivity (minimum 5 Mbps for live API inference)

---

## 4. Stakeholder & Persona Matrix
- **Primary Persona - The Self-Directed Learner**: High school or undergraduate students preparing for examinations needing fast explanations and dynamic self-testing.
- **Secondary Persona - The Educator/Content Creator**: Teachers seeking to generate quick quizzes and lecture summaries from raw textbook excerpts.
- **System Administrator**: Developers deploying and maintaining the FastAPI instance and monitoring API quotas.
