"""The One-Line Laugh — entry program.

Writes exactly one funny line (a single sentence, at most 200
characters) to /output/entry.txt.

The program keeps a small curated list of original one-liners and
picks the strongest one with a deterministic scoring function, so
every run — local or in the grader sandbox — produces the same
output. Scoring rewards what the house judge weighs most: a real
surprise at the end, an everyday truth people recognise, and
economy of words.

Usage:
    python3 main.py [--output PATH]

Defaults to /output/entry.txt (the path the grader expects). For a
local test run, pass --output to point at a scratch directory.
"""

import argparse
import os
import sys

# Original one-liners, each a single sentence of at most 200 chars.
# The twist (the surprise) is deliberately placed in the final third
# of each line, so the laugh lands at the end.
CANDIDATES = [
    "My smartwatch congratulated me on standing up, which is the only promotion I have had in three years.",
    "I finally cleaned out my inbox, and my reward was forty-seven new emails thanking me for the space.",
    "My plants died despite all my love, which makes them the most honest relationship I have ever had.",
    "I bought a standing desk to get healthier, and now I just sit in a taller chair.",
    "My phone's screen time report reads like a performance review from a boss I never hired.",
]

# Words that carry the twist in each line. The scorer checks how late
# in the line the twist lands: a punchline at the end scores best.
TWIST_WORDS = [
    "promotion",
    "thanking",
    "honest",
    "taller chair",
    "never hired",
]

MAX_CHARS = 200


def score_line(line: str, twist: str) -> float:
    """Score one candidate line. Higher is funnier by the judge's brief.

    - Length sweet spot: 70-130 chars (economy of words).
    - Twist position: the later the twist word appears, the better
      (a real surprise at the end).
    - Single sentence: exactly one sentence-ending mark.
    """
    score = 0.0
    length = len(line)

    if not 1 <= length <= MAX_CHARS:
        return -1.0
    if line != line.strip() or not line:
        return -1.0

    # Economy: prefer the 70-130 char sweet spot, penalise bloat.
    if 70 <= length <= 130:
        score += 3.0
    elif 40 <= length < 70:
        score += 1.5
    else:
        score += 0.5

    # Surprise at the end: twist word in the final third scores best.
    pos = line.lower().find(twist.lower())
    if pos < 0:
        return -1.0
    frac = (pos + len(twist)) / length
    if frac >= 0.85:
        score += 4.0
    elif frac >= 0.66:
        score += 3.0
    elif frac >= 0.5:
        score += 1.5
    else:
        score += 0.5

    # Single sentence: exactly one terminal punctuation mark, at the end.
    terminals = sum(line.count(mark) for mark in ".!?")
    if terminals == 1 and line.endswith("."):
        score += 2.0
    else:
        score -= 2.0

    # Freshness guard: no tired opener.
    if line.lower().startswith(("why did the", "a man walks into")):
        score -= 5.0

    return score


def pick_line() -> str:
    """Return the highest-scoring candidate line.

    Ties break on punch density (the twist phrase's share of the
    line: the punch should carry weight), then on the shorter line.
    """
    best_line = None
    best_key = None
    for line, twist in zip(CANDIDATES, TWIST_WORDS):
        score = score_line(line, twist)
        punch_density = len(twist) / len(line) if line else 0.0
        key = (score, punch_density, -len(line))
        if best_key is None or key > best_key:
            best_key = key
            best_line = line
    if best_line is None:
        raise RuntimeError("no valid candidate line")
    return best_line


def main() -> int:
    parser = argparse.ArgumentParser(description="Write one funny line.")
    parser.add_argument(
        "--output",
        default=os.environ.get("MAKEFUN_OUTPUT", "/output/entry.txt"),
        help="path of the output text file (default: /output/entry.txt)",
    )
    args = parser.parse_args()

    line = pick_line()

    # Gate: the same contract the sealed scorer checks.
    if not 1 <= len(line) <= MAX_CHARS:
        print(f"line is {len(line)} chars, outside 1-{MAX_CHARS}", file=sys.stderr)
        return 1
    if not line.strip():
        print("line is blank", file=sys.stderr)
        return 1

    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as handle:
        handle.write(line)

    print(f"wrote {len(line)} chars to {args.output}")
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
