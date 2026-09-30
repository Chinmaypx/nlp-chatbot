import unicodedata

import pytest
from fastapi.testclient import TestClient

from main import app
from nlp.language_detection import detect_language
from nlp.preprocessing import normalize_unicode, preprocess_text, remove_stopwords
from nlp.tokenizer import sentence_tokenize, word_tokenize

client = TestClient(app)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("मला अभ्यास करायला आवडतो.", "Marathi"),
        ("I like studying.", "English"),
        ("मला आज college ला जायचे आहे.", "Mixed"),
        ("123 !!!", "Unknown"),
    ],
)
def test_language_detection(text: str, expected: str) -> None:
    assert detect_language(text) == expected


def test_devanagari_characters_survive_preprocessing() -> None:
    result = preprocess_text("हा चित्रपट खूप छान आहे.")

    assert result["detected_language"] == "Marathi"
    assert "चित्रपट" in result["tokens"]
    assert all(any("\u0900" <= char <= "\u097f" for char in token) for token in result["tokens"] if token.isalpha())


def test_unicode_nfc_normalization() -> None:
    decomposed = "म" + "\u093e" + "झ" + "\u0940"
    assert normalize_unicode(decomposed) == unicodedata.normalize("NFC", decomposed)
    assert preprocess_text(decomposed)["normalized_text"] == "माझी"
    assert preprocess_text(decomposed)["original_text"] == decomposed


def test_malformed_surrogate_is_handled_safely() -> None:
    result = preprocess_text("मराठी\ud800 text")
    assert result["normalized_text"] == "मराठी\ufffd text"
    assert result["original_text"] == "मराठी\ufffd text"


def test_cleaning_preserves_meaningful_punctuation_and_collapses_repeats() -> None:
    result = preprocess_text("  नमस्कार!!!\nकसे आहात??  ")
    assert result["cleaned_text"] == "नमस्कार! कसे आहात?"
    assert result["tokens"][-1] == "?"


def test_sentence_tokenization_supports_english_and_danda() -> None:
    text = "मला अभ्यास आवडतो. आज माझी परीक्षा आहे! पुढचा भाग आहे। ठीक?"
    assert sentence_tokenize(text) == [
        "मला अभ्यास आवडतो.", "आज माझी परीक्षा आहे!", "पुढचा भाग आहे।", "ठीक?"
    ]


def test_word_tokenization_keeps_words_numbers_and_punctuation() -> None:
    tokens = word_tokenize("मला आज कॉलेजला जायचे आहे! Room 12.5?")
    assert "कॉलेजला" in tokens
    assert "12.5" in tokens
    assert "!" in tokens
    assert "?" in tokens


def test_optional_marathi_and_english_stopword_removal() -> None:
    assert "मला" not in remove_stopwords(["मला", "अभ्यास", "आवडतो"], "Marathi")
    assert remove_stopwords(["I", "like", "the", "study"], "English") == ["like", "study"]
    assert preprocess_text("मला अभ्यास आवडतो.")["processed_tokens"] == ["मला", "अभ्यास", "आवडतो", "."]


def test_multiple_sentences_and_optional_removal_in_pipeline() -> None:
    result = preprocess_text("I like the book. It is good!", remove_stopwords_option=True)
    assert len(result["sentences"]) == 2
    assert result["processed_tokens"] == ["like", "book", ".", "good", "!"]


@pytest.mark.parametrize("text", ["", "   ", "\n\t"])
def test_empty_or_whitespace_text_is_rejected_by_api(text: str) -> None:
    assert client.post("/api/language-detect", json={"text": text}).status_code == 422
    assert client.post("/api/preprocess", json={"text": text}).status_code == 422


def test_language_detection_api_and_compatibility_alias() -> None:
    response = client.post("/api/language-detect", json={"text": "मला अभ्यास आवडतो."})
    assert response.status_code == 200
    assert response.json() == {"language": "Marathi"}

    old_path = client.post("/api/language-detection/", json={"text": "I like studying."})
    assert old_path.status_code == 200
    assert old_path.json() == {"language": "English"}


def test_preprocessing_api_returns_structured_result() -> None:
    response = client.post(
        "/api/preprocess",
        json={"text": "मला आज college ला जायचे आहे!", "remove_stopwords": True},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["detected_language"] == "Mixed"
    assert body["original_text"] == "मला आज college ला जायचे आहे!"
    assert "college" in body["tokens"]
    assert "मला" not in body["processed_tokens"]


def test_invalid_api_bodies_are_rejected() -> None:
    for path in ("/api/language-detect", "/api/preprocess"):
        assert client.post(path, json={}).status_code == 422
        assert client.post(path, content=b"not json", headers={"content-type": "application/json"}).status_code == 422

