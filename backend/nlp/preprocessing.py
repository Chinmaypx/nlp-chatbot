"""Reusable, conservative Marathi/English text preprocessing helpers."""

from functools import lru_cache
from pathlib import Path
import re
import unicodedata

from nlp.language_detection import detect_language
from nlp.tokenizer import sentence_tokenize, word_tokenize

_RESOURCE_DIR = Path(__file__).parent / "resources"
_REPEATED_PUNCTUATION = re.compile(r"([.!?,;:।॥])\1{1,}")


def _replace_invalid_scalars(text: str) -> str:
    return "".join("\ufffd" if unicodedata.category(char) == "Cs" else char for char in text)


def normalize_unicode(text: str) -> str:
    """Use NFC canonical composition while retaining valid Devanagari text."""
    # Lone surrogate code points are invalid Unicode scalar values and cannot
    # be safely emitted as UTF-8 JSON. Replace them with the standard marker.
    return unicodedata.normalize("NFC", _replace_invalid_scalars(text))


def clean_text(text: str) -> str:
    """Remove control/format artifacts and normalize spacing and repeated marks."""
    text = normalize_unicode(text)
    kept: list[str] = []
    for char in text:
        category = unicodedata.category(char)
        if category == "Cc":
            if char.isspace():
                kept.append(" ")
            continue
        # Keep join controls that can occur in Indic text; discard invisible
        # formatting artifacts such as BOM and zero-width space.
        if category == "Cf" and char not in ("\u200c", "\u200d"):
            continue
        kept.append(char)
    text = "".join(kept)
    text = _REPEATED_PUNCTUATION.sub(r"\1", text)
    return " ".join(text.split())


@lru_cache(maxsize=2)
def _load_stopwords(language: str) -> frozenset[str]:
    filename = "stopwords_mr.txt" if language == "Marathi" else "stopwords_en.txt"
    path = _RESOURCE_DIR / filename
    return frozenset(
        line.strip().casefold()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    )


def get_stopwords(language: str) -> frozenset[str]:
    """Load the small, editable stopword resource for a supported language."""
    if language == "Marathi":
        return _load_stopwords("Marathi")
    if language == "English":
        return _load_stopwords("English")
    # Mixed text can contain terms from either list.
    if language == "Mixed":
        return _load_stopwords("Marathi") | _load_stopwords("English")
    return frozenset()


def remove_stopwords(tokens: list[str], language: str) -> list[str]:
    """Remove configured stopwords, preserving punctuation and other tokens."""
    stopwords = get_stopwords(language)
    return [token for token in tokens if token.casefold() not in stopwords]


def conservative_normalize(text: str) -> str:
    """Apply only safe canonical Unicode and whitespace normalization."""
    return " ".join(normalize_unicode(text).split())


def preprocess_text(text: str, remove_stopwords_option: bool = False) -> dict[str, object]:
    """Run the language-agnostic preprocessing pipeline and return its stages."""
    normalized_text = normalize_unicode(text)
    cleaned_text = conservative_normalize(clean_text(normalized_text))
    language = detect_language(cleaned_text)
    sentences = sentence_tokenize(cleaned_text)
    tokens = word_tokenize(cleaned_text)
    processed_tokens = (
        remove_stopwords(tokens, language) if remove_stopwords_option else list(tokens)
    )
    return {
        "original_text": _replace_invalid_scalars(text),
        "detected_language": language,
        "normalized_text": normalized_text,
        "cleaned_text": cleaned_text,
        "sentences": sentences,
        "tokens": tokens,
        "processed_tokens": processed_tokens,
    }
