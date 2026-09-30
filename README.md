# Multitask Marathi NLP Chatbot with English Support

## Project objective

Build a college-level chatbot foundation that will eventually support multiple NLP tasks in Marathi and English. Phase 0 establishes a modular API, a minimal web frontend, and a health check. **NLP models and NLP task behavior are not implemented yet.** API task routes intentionally return HTTP 501 placeholders.

## Planned NLP capabilities

- Sentiment analysis
- Text summarization
- Marathi–English translation
- Text classification and intent detection
- Question answering
- Keyword extraction
- Language detection
- Conversation history

## Technology stack

- Backend: Python, FastAPI, Uvicorn
- Frontend: React, Vite
- Tests: pytest, FastAPI TestClient
- Persistence and model libraries are deferred until their needs are defined.

## Project structure

```text
backend/       FastAPI app, modular API routes, NLP/database placeholders, tests, data/model directories
frontend/      Minimal React and Vite application
notebooks/     Reserved notebooks for later NLP phases
tests/         Reserved for cross-project tests
README.md      Project overview and setup
```

## Phase-wise development plan

- **Phase 0 (current):** Project architecture, health endpoint, explicit API placeholders, minimal frontend, and test foundation.
- **Phase 1:** Define datasets and preprocessing/evaluation approach.
- **Phase 2:** Implement and evaluate NLP capabilities incrementally.
- **Phase 3:** Connect task services to the chatbot experience and persistence.
- **Phase 4:** Integration, broader testing, documentation, and deployment preparation.

No model results are generated or implied in Phase 0.

## Run the backend

From the repository root, create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend/requirements.txt
```

Run the API from the `backend` directory:

```powershell
cd backend
python -m uvicorn main:app --reload
```

The health endpoint is at `http://127.0.0.1:8000/health`; interactive API documentation is at `/docs`.

## Run the frontend

In another terminal:

```powershell
cd frontend
npm install
npm run dev
```

For a production build, run `npm run build` from `frontend/`.

## Testing

From the repository root, install backend dependencies as above, then:

```powershell
python -m pytest backend/tests -q
```

The health test checks HTTP 200 and the expected status and service fields.
