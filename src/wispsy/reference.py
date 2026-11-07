"""Ordinary typed functions shared by every reference invocation surface."""

import argparse
import json
from typing import TypedDict


class TextReport(TypedDict):
    text: str
    words: int
    characters: int


def normalize(text: str) -> str:
    """Collapse Unicode whitespace and casefold text."""
    return " ".join(text.split()).casefold()


def report(text: str) -> TextReport:
    """Report words and Unicode code points in the supplied text."""
    return {"text": text, "words": len(text.split()), "characters": len(text)}


def run_reference(text: str) -> TextReport:
    """Compose the same functions directly, with an explicit argument mapping."""
    return report(text=normalize(text=text))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", help="Text to normalize and report.")
    arguments = parser.parse_args()
    print(json.dumps(run_reference(arguments.text), ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
