# codesense

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Static analysis tool for Python files. Checks for common style issues, bad practices, and things that will come back to bite you later.

Built this because I kept making the same mistakes (unused imports, magic numbers, bare excepts) and wanted something lightweight I could run from the terminal without pulling in a million dependencies.

## install

No dependencies needed, just Python 3.8+.

```bash
git clone https://github.com/dmatiason09/codesense.git
cd codesense
```

## usage

```bash
python main.py yourfile.py           # check a single file
python main.py src/                  # check an entire folder
python main.py yourfile.py --score   # just the score
python main.py yourfile.py --json    # json output (useful for piping)
```

## what it checks

- lines over 79 chars (pep8)
- function/class naming (snake_case / PascalCase)
- missing docstrings
- bare `except:` clauses
- unused imports
- TODO/FIXME comments left in code
- magic numbers without names
- functions over 30 lines (usually means it needs splitting up)
- single-letter variable names outside of loops

## example

```
codesense → examples/bad_code.py
  37 lines  (31 code / 1 comments / 5 blank)
  5 functions, 1 classes

  issues (20)

  WARNING × 9
  • [naming] 'CalculateDiscount' - functions should be snake_case  (line 5)
  • [bad_practice] bare except catches everything  (line 24)
  • [unused] 'os' imported but never used  (line 1)
  ...

  score: 44/100 — poor
```

when checking a folder, you also get a summary at the end:

```
──────────────────────────────────────────────────
summary — 4 files checked
  total issues : 31
  average score: 67/100 — needs work
  best file    : src/utils.py (91/100)
  worst file   : src/legacy.py (44/100)
──────────────────────────────────────────────────
```

## running tests

```bash
pip install pytest
pytest tests/
```

## project structure

```
codesense/
├── main.py
├── analyzer/
│   ├── code_analyzer.py   # all the checks live here
│   └── report.py          # terminal output formatting
├── tests/
│   └── test_analyzer.py
└── examples/
    ├── good_code.py
    └── bad_code.py
```

## notes

- doesn't execute your code, all static analysis via the `ast` module
- false positives happen with magic numbers, use your judgment
- single-letter variable check skips loop variables (i, j, k etc are fine)
- TODO: maybe add a --fix flag someday that auto-corrects simple stuff

## license

MIT
