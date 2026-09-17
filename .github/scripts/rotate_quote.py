#!/usr/bin/env python3
"""Swap the quote shown between the QUOTE markers in README.md."""

import json
import pathlib
import random
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
QUOTES = ROOT / ".github" / "quotes.json"

START = "<!-- QUOTE:START -->"
END = "<!-- QUOTE:END -->"


def render(quote):
    return f'> *"{quote["text"]}"*\n>\n> — **{quote["author"]}**'


def main():
    quotes = json.loads(QUOTES.read_text(encoding="utf-8"))
    readme = README.read_text(encoding="utf-8")

    block = re.compile(f"{re.escape(START)}.*?{re.escape(END)}", re.DOTALL)
    current = block.search(readme)
    if current is None:
        sys.exit(f"Could not find {START} ... {END} in README.md")

    # Exclude the quote on display so the block always changes.
    candidates = [q for q in quotes if render(q) not in current.group(0)] or quotes
    chosen = random.choice(candidates)

    replacement = f"{START}\n{render(chosen)}\n{END}"
    README.write_text(block.sub(lambda _: replacement, readme, count=1), encoding="utf-8")
    print(f'{chosen["author"]}: "{chosen["text"]}"')


if __name__ == "__main__":
    main()
