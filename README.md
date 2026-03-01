# 🔍 CodeSense — Python Code Quality Analyzer

A lightweight command-line tool that analyzes Python source files and reports
quality issues, style violations, and best-practice warnings — with a final
quality score out of 100.

---

## ✨ Features

- **Style checks** — line length (PEP 8 compliant)
- **Naming conventions** — enforces snake_case for functions, PascalCase for classes
- **Documentation checks** — flags missing docstrings
- **Best practices** — detects bare `except`, magic numbers, unused imports
- **Maintenance flags** — surfaces TODO / FIXME / HACK comments
- **Quality score** — a single 0–100 score summarizing the file's health
- **Multiple output formats** — human-readable text or JSON

---

## 📦 Installation

No external dependencies required — pure Python standard library.

```bash
git clone https://github.com/YOUR_USERNAME/codesense.git
cd codesense
python main.py --help
```

> Python 3.8 or higher is required.

---

## 🚀 Usage

```bash
# Analyze a file (full report)
python main.py examples/bad_code.py

# Show only the score
python main.py examples/good_code.py --score-only

# Output as JSON (great for piping into other tools)
python main.py examples/bad_code.py --output json
```

---

## 📊 Example Output

```
============================================================
  CodeSense — Code Quality Report
============================================================
  File   : examples/bad_code.py
  Lines  : 28 total  (22 code, 3 comments, 3 blank)
  Functions : 3   Classes : 1   Comment ratio : 10.7%

  Issues Found (14)
  --------------------------------------------------------

  [WARNING] (6)
  • [style] Line too long (80 chars, max 79)  → line 32
  • [naming] Function 'CalculateDiscount' should use snake_case  → line 4
  • [naming] Function 'processData' should use snake_case  → line 21
  • [naming] Class 'account_manager' should use PascalCase  → line 9
  • [best_practice] Bare 'except:' found  → line 19
  • [unused] Import 're' appears to be unused  → line 3

  [INFO] (8)
  • [documentation] 'withdraw' is missing a docstring  → line 14
  • [maintenance] Unresolved comment: # TODO: fix this logic
  ...

  Quality Score : 48/100  —  Poor ✗
============================================================
```

---

## 🗂️ Project Structure

```
codesense/
├── main.py               # CLI entry point
├── requirements.txt      # Dependencies (none required)
├── analyzer/
│   ├── __init__.py
│   ├── code_analyzer.py  # Core analysis logic (AST-based)
│   └── report.py         # Report formatting (text & JSON)
└── examples/
    ├── good_code.py      # Clean code demo
    └── bad_code.py       # Problematic code demo
```

---

## 🧠 How It Works

CodeSense uses Python's built-in `ast` (Abstract Syntax Tree) module to parse
and inspect source files without executing them. This allows safe, fast, and
accurate static analysis of:

- Function and class definitions
- Import statements
- Exception handlers
- Numeric literals
- And more

---

## 🔧 Checks Performed

| Check | Severity | Description |
|---|---|---|
| Line length | Warning | Lines over 79 characters (PEP 8) |
| Function naming | Warning | Non-snake_case function names |
| Class naming | Warning | Non-PascalCase class names |
| Missing docstrings | Info | Functions/classes without docstrings |
| Bare except | Warning | `except:` without a specific exception type |
| Unused imports | Warning | Imported modules not referenced in code |
| TODO comments | Info | Unresolved TODO/FIXME/HACK markers |
| Magic numbers | Info | Unexplained numeric literals in code |

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to
discuss what you would like to change.

---

## 📄 License

[MIT](https://choosealicense.com/licenses/mit/)
