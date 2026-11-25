#!/usr/bin/env python3
"""Fortune Cookie for the Liquidated Trader — make.fun bounty entry.

Writes one fortune-cookie line for a crypto trader who has just been
liquidated to /output/entry.txt, then self-checks the bounty gate before
exiting: UTF-8 text, a single line, 1 to 160 characters, at most 20 words,
no leading or trailing white space, no control characters.

The line itself is a fixed, hand-written fortune: the oracle voice opens
("Your fortune is not lost"), the loss is softened rather than mocked
("merely redistributed"), and the punchline lands on the very people the
money went to ("traders with worse jokes") — rueful, warm, and aimed at
the trader, not at the loss.
"""

import os
import sys

FORTUNE = "Your fortune is not lost, merely redistributed to traders with worse jokes."

# The grader runs the entry with no environment set, so this is always
# /output/entry.txt there; the override exists only so the entry can be
# smoke-tested on a machine where /output is not writable.
OUTPUT_PATH = os.environ.get("FORTUNE_OUTPUT", "/output/entry.txt")

MAX_CHARS = 160
MAX_WORDS = 20


def check_gate(text: str) -> None:
    """Raise SystemExit with a reason if the text would fail the gate."""
    if not text or not text.strip():
        raise SystemExit("gate failed: entry is empty or only white space")
    if text != text.strip():
        raise SystemExit("gate failed: entry has leading or trailing white space")
    if "\n" in text or "\r" in text:
        raise SystemExit("gate failed: entry is not a single line")
    if any(ord(ch) < 0x20 for ch in text):
        raise SystemExit("gate failed: entry contains control characters")
    if len(text) > MAX_CHARS:
        raise SystemExit(
            f"gate failed: entry is {len(text)} chars, max is {MAX_CHARS}"
        )
    if len(text.split()) > MAX_WORDS:
        raise SystemExit(
            f"gate failed: entry is {len(text.split())} words, max is {MAX_WORDS}"
        )
    text.encode("utf-8")  # raises if the text is not valid UTF-8-encodable


def main() -> int:
    check_gate(FORTUNE)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(FORTUNE)
    with open(OUTPUT_PATH, "rb") as handle:
        written = handle.read()
    if written != FORTUNE.encode("utf-8"):
        raise SystemExit("gate failed: file bytes differ from the fortune")
    check_gate(written.decode("utf-8"))
    print(f"wrote {OUTPUT_PATH} ({len(FORTUNE)} chars, {len(FORTUNE.split())} words)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
