from fastapi import APIRouter
from pydantic import BaseModel, field_validator

from nlp.language_detection import detect_language

router = APIRouter()


class TextRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text must not be empty or whitespace-only")
        return value


class LanguageResponse(BaseModel):
    language: str


@router.post("", response_model=LanguageResponse)
@router.post("/", response_model=LanguageResponse, include_in_schema=False)
def language_detect(request: TextRequest) -> LanguageResponse:
    """Detect supported script language heuristically; this is not a model."""
    return LanguageResponse(language=detect_language(request.text))
