"""
code_analyzer.py
Core module that reads and analyzes Python source files.
"""

import ast
import re


class CodeAnalyzer:
    def __init__(self, filepath: str):
        self.filepath = filepath
        with open(filepath, "r", encoding="utf-8") as f:
            self.source = f.read()
        self.lines = self.source.splitlines()

    def analyze(self) -> dict:
        """Run all checks and return a results dictionary."""
        results = {
            "file": self.filepath,
            "lines_of_code": self._count_lines(),
            "issues": [],
            "metrics": {}
        }

        results["issues"] += self._check_line_length()
        results["issues"] += self._check_naming_conventions()
        results["issues"] += self._check_missing_docstrings()
        results["issues"] += self._check_bare_except()
        results["issues"] += self._check_unused_imports()
        results["issues"] += self._check_todo_comments()
        results["issues"] += self._check_magic_numbers()

        results["metrics"] = self._compute_metrics()
        results["score"] = self._compute_score(results["issues"])

        return results

    # ── Line length ──────────────────────────────────────────────────────────
    def _check_line_length(self, max_length: int = 79) -> list:
        issues = []
        for i, line in enumerate(self.lines, start=1):
            if len(line) > max_length:
                issues.append({
                    "type": "style",
                    "severity": "warning",
                    "line": i,
                    "message": f"Line too long ({len(line)} chars, max {max_length})"
                })
        return issues

    # ── Naming conventions ───────────────────────────────────────────────────
    def _check_naming_conventions(self) -> list:
        issues = []
        try:
            tree = ast.parse(self.source)
        except SyntaxError:
            return [{"type": "syntax", "severity": "error", "line": 1,
                     "message": "Syntax error — could not parse file"}]

        for node in ast.walk(tree):
            # Functions should be snake_case
            if isinstance(node, ast.FunctionDef):
                if not re.match(r'^[a-z_][a-z0-9_]*$', node.name) and not node.name.startswith('__'):
                    issues.append({
                        "type": "naming",
                        "severity": "warning",
                        "line": node.lineno,
                        "message": f"Function '{node.name}' should use snake_case"
                    })
            # Classes should be PascalCase
            if isinstance(node, ast.ClassDef):
                if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                    issues.append({
                        "type": "naming",
                        "severity": "warning",
                        "line": node.lineno,
                        "message": f"Class '{node.name}' should use PascalCase"
                    })
        return issues

    # ── Docstrings ───────────────────────────────────────────────────────────
    def _check_missing_docstrings(self) -> list:
        issues = []
        try:
            tree = ast.parse(self.source)
        except SyntaxError:
            return []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not (node.body and isinstance(node.body[0], ast.Expr)
                        and isinstance(node.body[0].value, ast.Constant)
                        and isinstance(node.body[0].value.value, str)):
                    issues.append({
                        "type": "documentation",
                        "severity": "info",
                        "line": node.lineno,
                        "message": f"'{node.name}' is missing a docstring"
                    })
        return issues

    # ── Bare except ──────────────────────────────────────────────────────────
    def _check_bare_except(self) -> list:
        issues = []
        try:
            tree = ast.parse(self.source)
        except SyntaxError:
            return []

        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                issues.append({
                    "type": "best_practice",
                    "severity": "warning",
                    "line": node.lineno,
                    "message": "Bare 'except:' found — catch specific exceptions instead"
                })
        return issues

    # ── Unused imports ───────────────────────────────────────────────────────
    def _check_unused_imports(self) -> list:
        issues = []
        try:
            tree = ast.parse(self.source)
        except SyntaxError:
            return []

        imported_names = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname or alias.name
                    imported_names.append((name.split(".")[0], node.lineno))
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    name = alias.asname or alias.name
                    imported_names.append((name, node.lineno))

        # Collect all names actually used in the code
        used_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                used_names.add(node.id)
            elif isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name):
                    used_names.add(node.value.id)

        for name, lineno in imported_names:
            if name not in used_names and name != "*":
                issues.append({
                    "type": "unused",
                    "severity": "warning",
                    "line": lineno,
                    "message": f"Import '{name}' appears to be unused"
                })
        return issues

    # ── TODO comments ────────────────────────────────────────────────────────
    def _check_todo_comments(self) -> list:
        issues = []
        for i, line in enumerate(self.lines, start=1):
            if re.search(r'#\s*(TODO|FIXME|HACK|XXX)', line, re.IGNORECASE):
                issues.append({
                    "type": "maintenance",
                    "severity": "info",
                    "line": i,
                    "message": f"Unresolved comment: {line.strip()}"
                })
        return issues

    # ── Magic numbers ────────────────────────────────────────────────────────
    def _check_magic_numbers(self) -> list:
        issues = []
        try:
            tree = ast.parse(self.source)
        except SyntaxError:
            return []

        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                if node.value not in (0, 1, -1, 2, 100):
                    issues.append({
                        "type": "best_practice",
                        "severity": "info",
                        "line": node.lineno if hasattr(node, 'lineno') else 0,
                        "message": f"Magic number '{node.value}' — consider using a named constant"
                    })
        return issues

    # ── Metrics ──────────────────────────────────────────────────────────────
    def _count_lines(self) -> int:
        return len([l for l in self.lines if l.strip() and not l.strip().startswith("#")])

    def _compute_metrics(self) -> dict:
        comment_lines = sum(1 for l in self.lines if l.strip().startswith("#"))
        blank_lines = sum(1 for l in self.lines if not l.strip())
        total = len(self.lines)
        try:
            tree = ast.parse(self.source)
            functions = sum(1 for n in ast.walk(tree) if isinstance(n, ast.FunctionDef))
            classes = sum(1 for n in ast.walk(tree) if isinstance(n, ast.ClassDef))
        except SyntaxError:
            functions = classes = 0

        return {
            "total_lines": total,
            "code_lines": self._count_lines(),
            "comment_lines": comment_lines,
            "blank_lines": blank_lines,
            "functions": functions,
            "classes": classes,
            "comment_ratio": round(comment_lines / total * 100, 1) if total else 0
        }

    def _compute_score(self, issues: list) -> int:
        score = 100
        for issue in issues:
            if issue["severity"] == "error":
                score -= 15
            elif issue["severity"] == "warning":
                score -= 5
            elif issue["severity"] == "info":
                score -= 1
        return max(0, score)
