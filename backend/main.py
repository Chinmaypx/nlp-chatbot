from fastapi import FastAPI

from api import (
    chat, classification, history, keywords, language_detect, preprocessing,
    question_answering, sentiment, summarization, translation,
)

app = FastAPI(
    title="Multitask Marathi NLP Chatbot",
    description="Phase 1 language detection and preprocessing foundation; model-based NLP capabilities remain placeholders.",
    version="0.1.0",
)

app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(sentiment.router, prefix="/api/sentiment", tags=["sentiment"])
app.include_router(summarization.router, prefix="/api/summarization", tags=["summarization"])
app.include_router(translation.router, prefix="/api/translation", tags=["translation"])
app.include_router(classification.router, prefix="/api/classification", tags=["classification"])
app.include_router(question_answering.router, prefix="/api/question-answering", tags=["question-answering"])
app.include_router(keywords.router, prefix="/api/keywords", tags=["keywords"])
app.include_router(language_detect.router, prefix="/api/language-detection", tags=["language-detection"])
app.include_router(language_detect.router, prefix="/api/language-detect", tags=["language-detection"])
app.include_router(preprocessing.router, prefix="/api/preprocess", tags=["preprocessing"])
app.include_router(history.router, prefix="/api/history", tags=["history"])


@app.get("/health")
def health() -> dict[str, str]:
    """Report whether the API process is responding."""
    return {"status": "ok", "service": "marathi-nlp-chatbot"}
