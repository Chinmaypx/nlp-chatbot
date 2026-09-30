from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator

from nlp.preprocessing import preprocess_text

router = APIRouter()


class PreprocessRequest(BaseModel):
    text: str
    remove_stopwords: bool = False

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text must not be empty or whitespace-only")
        return value


class PreprocessResponse(BaseModel):
    original_text: str
    detected_language: str
    normalized_text: str
    cleaned_text: str
    sentences: list[str] = Field(default_factory=list)
    tokens: list[str] = Field(default_factory=list)
    processed_tokens: list[str] = Field(default_factory=list)


@router.post("", response_model=PreprocessResponse)
def preprocess(request: PreprocessRequest) -> PreprocessResponse:
    """Normalize, clean, tokenize, and optionally remove stopwords."""
    return PreprocessResponse(
        **preprocess_text(request.text, remove_stopwords_option=request.remove_stopwords)
    )
