"""Unicode-aware sentence and word tokenizers for Marathi and English."""

import re


_SENTENCE_END = re.compile(r"(?<=[.!?\u0964\u0965])\s+|(?<=[.!?\u0964\u0965])(?=[^\s])")
# Devanagari letters/marks, Latin words, numbers, and punctuation are retained.
_WORD = re.compile(
    r"[\u0900-\u0963\u0966-\u097f]+(?:[\u200c\u200d]?[\u0900-\u0963\u0966-\u097f]+)*"
    r"|[A-Za-z]+(?:['’][A-Za-z]+)*"
    r"|\d+(?:[.,]\d+)*"
    r"|[^\w\s]",
    re.UNICODE,
)


def sentence_tokenize(text: str) -> list[str]:
    """Split on common English and Devanagari sentence terminators."""
    return [part.strip() for part in _SENTENCE_END.split(text.strip()) if part.strip()]


def word_tokenize(text: str) -> list[str]:
    """Return words, number groups, and punctuation without losing script."""
    return _WORD.findall(text)
