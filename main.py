#!/usr/bin/env python3
"""Seventeen Syllables of Debugging.

Writes one haiku about debugging (5-7-5 syllables, 66 characters) to
/output/entry.txt and prints it to stdout.

The haiku:

    The stack trace ends here
    a thousand frames of maybe
    one semicolon

A thousand frames of doubt, and the whole hunt ends on a single
semicolon. Pure standard library, fully deterministic.
"""

import os

# The haiku: three lines, 5-7-5 syllables.
LINES = (
    "The stack trace ends here",
    "a thousand frames of maybe",
    "one semicolon",
)

# Per-word syllable table (verified by hand against the 5-7-5 shape).
# Line 1 (5): The(1) stack(1) trace(1) ends(1) here(1)
# Line 2 (7): a(1) thousand(2) frames(1) of(1) maybe(2)
# Line 3 (5): one(1) semicolon(4)
SYLLABLES = {
    "The": 1,
    "stack": 1,
    "trace": 1,
    "ends": 1,
    "here": 1,
    "a": 1,
    "thousand": 2,
    "frames": 1,
    "of": 1,
    "maybe": 2,
    "one": 1,
    "semicolon": 4,
}

EXPECTED_COUNTS = (5, 7, 5)
MAX_CHARS = 200


def count_line(line: str) -> int:
    """Count syllables in one line using the per-word table.

    A word missing from the table is a bug in this program, not a
    guessable count, so fail loudly instead of silently miscounting.
    """
    total = 0
    for word in line.split():
        if word not in SYLLABLES:
            raise ValueError(f"no syllable count recorded for word {word!r}")
        total += SYLLABLES[word]
    return total


def build_text() -> str:
    """Return the haiku, asserting the 5-7-5 shape and the 200-char cap."""
    counts = tuple(count_line(line) for line in LINES)
    assert counts == EXPECTED_COUNTS, f"syllable counts {counts} != {EXPECTED_COUNTS}"
    text = "\n".join(LINES)
    assert 1 <= len(text) <= MAX_CHARS, f"haiku is {len(text)} chars, must be 1-200"
    assert text.strip(), "haiku must not be only whitespace"
    return text


def output_path() -> str:
    """Resolve the output path: $MAKEFUN_OUTPUT, then $MAKEFUN_OUTPUT_DIR, else /output/entry.txt."""
    direct = os.environ.get("MAKEFUN_OUTPUT")
    if direct:
        return direct
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if directory:
        return os.path.join(directory, "entry.txt")
    return "/output/entry.txt"


def main() -> None:
    text = build_text()
    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    print(text)


if __name__ == "__main__":
    main()
