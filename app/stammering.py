from __future__ import annotations

import re
import unicodedata

WORD_RE = re.compile(r"\b\w+\b", re.UNICODE)


def _normalize_text(text: str) -> str:
    return unicodedata.normalize("NFKC", text.lower())


def _tokens(text: str) -> list[str]:
    return WORD_RE.findall(_normalize_text(text))


def _max_consecutive_word_repeats(tokens: list[str]) -> int:
    if not tokens:
        return 0

    best = 1
    current = 1
    for idx in range(1, len(tokens)):
        if tokens[idx] == tokens[idx - 1]:
            current += 1
            best = max(best, current)
        else:
            current = 1
    return best


def _max_consecutive_ngram_repeats(tokens: list[str], n: int) -> int:
    best = 1
    total = len(tokens)

    for start in range(total - n + 1):
        gram = tokens[start : start + n]
        repeats = 1
        cursor = start + n
        while cursor + n <= total and tokens[cursor : cursor + n] == gram:
            repeats += 1
            cursor += n
        best = max(best, repeats)

    return best


def _max_character_run(text: str) -> int:
    normalized = _normalize_text(text)
    best = 1
    current = 1
    previous = None

    for char in normalized:
        if char.isalpha():
            if char == previous:
                current += 1
                best = max(best, current)
            else:
                current = 1
            previous = char
        else:
            previous = None
            current = 1

    return best


def has_stammering(source_sentence: str, translated_sentence: str) -> bool:
    source_tokens = _tokens(source_sentence)
    translated_tokens = _tokens(translated_sentence)

    source_word_repeat = _max_consecutive_word_repeats(source_tokens)
    target_word_repeat = _max_consecutive_word_repeats(translated_tokens)

    if target_word_repeat >= 4 and target_word_repeat > source_word_repeat + 1:
        return True

    for n in (4, 3, 2, 1):
        source_ngram_repeat = _max_consecutive_ngram_repeats(source_tokens, n)
        target_ngram_repeat = _max_consecutive_ngram_repeats(translated_tokens, n)

        if n >= 2 and target_ngram_repeat >= 3 and target_ngram_repeat > source_ngram_repeat:
            return True

        if n == 1 and target_ngram_repeat >= 4 and target_ngram_repeat > source_ngram_repeat + 1:
            return True

    if len(source_tokens) <= 4 and len(translated_tokens) >= max(8, len(source_tokens) * 4):
        return True

    source_char_run = _max_character_run(source_sentence)
    target_char_run = _max_character_run(translated_sentence)
    if target_char_run >= 10 and target_char_run > source_char_run + 3:
        return True

    return False
