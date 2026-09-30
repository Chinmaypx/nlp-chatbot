"""Lightweight script-based language identification for Marathi and English.

This is a heuristic foundation, not a trained language identification model.
Devanagari script does not uniquely identify Marathi, so script-only results
should be treated as approximate for unsupported Devanagari languages.
"""

from enum import Enum
import unicodedata


class Language(str, Enum):
    MARATHI = "Marathi"
    ENGLISH = "English"
    MIXED = "Mixed"
    UNKNOWN = "Unknown"


def detect_language(text: str) -> str:
    """Classify text by the presence of Devanagari and Latin letters."""
    has_devanagari = False
    has_latin = False

    for char in text:
        if not unicodedata.category(char).startswith("L"):
            continue
        codepoint = ord(char)
        if 0x0900 <= codepoint <= 0x097F:
            has_devanagari = True
        elif (0x0041 <= codepoint <= 0x005A) or (0x0061 <= codepoint <= 0x007A):
            has_latin = True

    if has_devanagari and has_latin:
        return Language.MIXED.value
    if has_devanagari:
        return Language.MARATHI.value
    if has_latin:
        return Language.ENGLISH.value
    return Language.UNKNOWN.value
