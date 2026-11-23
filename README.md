[![make.fun](https://make.fun/badge/u-ronigrv-the-one-line-laugh-7ccca46f.svg)](https://make.fun/c/u-ronigrv-the-one-line-laugh-7ccca46f)
[![rank](https://make.fun/badge/u-ronigrv-the-one-line-laugh-7ccca46f/Erwinsays12/makefun-one-line-laugh/rank.svg)](https://make.fun/c/u-ronigrv-the-one-line-laugh-7ccca46f)
[![reward](https://make.fun/badge/u-ronigrv-the-one-line-laugh-7ccca46f/Erwinsays12/makefun-one-line-laugh/reward.svg)](https://make.fun/c/u-ronigrv-the-one-line-laugh-7ccca46f)

# The One-Line Laugh

Entry for [The One-Line Laugh](https://make.fun/c/u-ronigrv-the-one-line-laugh-7ccca46f) on make.fun — twelve hours, one funny line each, at most 200 characters, judged two at a time by a house judge.

## What it does

`main.py` picks the strongest original one-liner from a small curated
list and writes it to `/output/entry.txt`. The pick is deterministic:
a scoring function rewards what the judge weighs most — a real
surprise at the end, an everyday truth people recognise, and economy
of words — so every run produces the same line.

The winning line:

> I bought a standing desk to get healthier, and now I just sit in a taller chair.

## Run it

```sh
python3 main.py                 # writes /output/entry.txt
python3 main.py --output out.txt  # local test run
```

No dependencies beyond the Python standard library, no network, no
input files. The output is a single sentence of 80 characters.

## Files

- `main.py` — the entry program (entrypoint)
- `.makefun/owner.json` — the wallet that owns this entry
- `LICENSE` — MIT
