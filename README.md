### Phase 4: `04-project-planning`

```markdown
# Phase 4: Project Planning & Management Phase - EduGenie

## 1. Work Breakdown Structure (WBS)

EduGenie Engineering Lifecycle
├── 1. Foundation & Environment Setup
│   ├── Virtual Environment Configuration (venv)
│   ├── Package Dependency Ingestion (FastAPI, Uvicorn, HTTPX, python-dotenv)
│   └── Google Cloud Console API Registration & Access Management
├── 2. Core Service Development
│   ├── Asynchronous Network Client Setup
│   ├── Model Routing & Redundant Failover Logic
│   └── Prompt Engineering & Sanitization Handlers
├── 3. Module Encapsulation
│   ├── Q&A Router Implementation
│   ├── Concept Explainer Service
│   ├── Passage Summarizer Engine
│   ├── Dynamic Assessment/Quiz Parser
│   └── Strategic Learning Path Synthesizer
├── 4. Frontend Integration
│   ├── HTML5 Semantic Structure
│   ├── Modern CSS3 Design & Component Styling
│   └── Asynchronous JavaScript Fetch Pipelines
├── 5. Verification & Testing
│   ├── Local Integration & API Connectivity Testing
│   ├── Exception Handling & Error Message Verification
│   └── Boundary & Malformed Input Testing
└── 6. Version Control & Release
├── Local Git Tracking Configuration
├── Secret Isolation (.gitignore Enforcement)
└── GitHub Remote Mirroring & Branch Topology Creation


---

## 2. Project Milestone Timeline

| Milestone ID | Task / Phase Deliverable | Target Duration | Status |
| :--- | :--- | :--- | :--- |
| **M1** | Project Initialization & Cloud Credential Provisioning | Day 1 | Complete |
| **M2** | FastAPI Skeleton, Static Routes & CORS Config | Day 2 | Complete |
| **M3** | HTTPX Engine & Gemini Endpoint Integration | Day 3 | Complete |
| **M4** | Education Module Synthesis (Q&A, Quiz, Explainer) | Day 4 | Complete |
| **M5** | User Interface Polish & Client DOM Wiring | Day 5 | Complete |
| **M6** | End-to-End Stress & Exception Testing | Day 6 | Complete |
| **M7** | Git Lifecycle, Branch Topology & Remote Deployment | Day 7 | Complete |

---

## 3. Risk Mitigation & Contingency Strategy
- **Issue**: Google deprecates legacy SDK endpoints resulting in runtime 404/403 errors.
  - **Remedy**: Replaced brittle wrapper libraries with raw REST calls via standard HTTPX clients using Google's direct stable `v1` endpoints.
- **Issue**: Accidental public exposure of secret API keys.
  - **Remedy**: Enforced rigorous `.gitignore` shielding rules and runtime `dotenv` variable injection.
- **Issue**: Invalid JSON response structures from generative models during quiz synthesis.
  - **Remedy**: Implemented defensive regular expressions (`re.sub`) to strip Markdown code backticks before deserializing payloads.
