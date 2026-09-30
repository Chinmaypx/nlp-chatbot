# Multitask Marathi NLP Chatbot with English Support

## Project objective

Build a college-level chatbot foundation that will eventually support multiple NLP tasks in Marathi and English. Phase 0 established a modular API and frontend. Phase 1 adds a lightweight language identification heuristic and reusable Marathi/English preprocessing foundation. **No trained NLP models or model-backed task behavior are implemented.** Other task routes intentionally remain HTTP 501 placeholders.

## Planned NLP capabilities

- Language detection and preprocessing foundation (Phase 1)
- Sentiment analysis
- Text summarization
- Marathi-English translation
- Text classification and intent detection
- Question answering
- Keyword extraction
- Conversation history

## Technology stack

- Backend: Python, FastAPI, Uvicorn
- Frontend: React, Vite
- Tests: pytest, FastAPI TestClient
- No database or ML model libraries are needed in Phase 1.

## Project structure

```text
backend/       FastAPI app, modular API routes, NLP/database placeholders, tests, data/model directories
frontend/      Minimal React and Vite application
notebooks/     Reserved notebooks for later NLP phases
README.md      Project overview and setup
```

## Phase-wise development plan

- **Phase 0:** Project architecture, health endpoint, explicit API placeholders, minimal frontend, and test foundation.
- **Phase 1 (current):** Language detection and Marathi/English preprocessing, tokenization, and optional stopword handling.
- **Phase 2:** Implement and evaluate NLP capabilities incrementally.
- **Phase 3:** Connect task services to the chatbot experience and persistence.
- **Phase 4:** Integration, broader testing, documentation, and deployment preparation.

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

## Phase 1 NLP foundation

The language detector uses Unicode script heuristics: Devanagari letters are reported as `Marathi`, Latin letters as `English`, both as `Mixed`, and text without either as `Unknown`. This is a lightweight rule-based baseline, **not** a trained language identifier. Devanagari alone cannot distinguish Marathi from other Devanagari languages, and mixed-language detection is approximate.

Preprocessing applies Unicode NFC normalization, removes control and common invisible formatting artifacts, normalizes whitespace, and collapses repeated punctuation while retaining sentence punctuation. Sentence splitting recognizes `.`, `?`, `!`, danda (`।`) and double danda (`॥`). Word tokenization preserves Devanagari and Latin words, numeric groups, and punctuation. Small editable Marathi and English stopword lists live in `backend/nlp/resources/`; stopword removal is opt-in. No stemming or lemmatization is performed.

### API endpoints

`POST /api/language-detect`

Request:

```json
{"text": "मला अभ्यास करायला आवडतो."}
```

Response:

```json
{"language": "Marathi"}
```

`POST /api/preprocess`

Request (stopword removal is optional and defaults to false):

```json
{"text": "मला आज college ला जायचे आहे!", "remove_stopwords": true}
```

Response includes `original_text`, `detected_language`, `normalized_text`, `cleaned_text`, `sentences`, `tokens`, and `processed_tokens`. Blank text, missing `text`, and invalid JSON receive HTTP 422 validation errors.

The previous `/api/language-detection/` URL remains available as a compatibility alias. `/health` is unchanged. Other NLP endpoints remain placeholders.

Phase 1 provides reusable language detection and preprocessing; it does not claim model accuracy or implement sentiment analysis, summarization, translation, question answering, classification, keyword extraction, chatbot intelligence, or persistence.

## Run the frontend

In another terminal:

```powershell
cd frontend
npm install
npm run dev
```

For a production build, run `npm run build` from `frontend/`.

## Testing

From the repository root, install backend dependencies as above, then run the complete backend suite. It covers health, language detection, preprocessing/tokenization, stopword behavior, Unicode preservation, and API validation:

```powershell
python -m pytest backend/tests -q
```
