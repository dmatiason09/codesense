"""
core analysis logic - reads a python file and finds common problems
nothing fancy, just ast + regex
"""

import ast
import re


def run_analysis(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        src = f.read()

    lines = src.splitlines()

    issues = []
    issues += _long_lines(lines)
    issues += _naming(src)
    issues += _missing_docs(src)
    issues += _bare_excepts(src)
    issues += _unused_imports(src)
    issues += _todos(lines)
    issues += _magic_numbers(src)

    metrics = _get_metrics(src, lines)
    score = _score(issues)

    return {
        "file": filepath,
        "issues": issues,
        "metrics": metrics,
        "score": score
    }


def _long_lines(lines, limit=79):
    found = []
    for i, line in enumerate(lines, 1):
        if len(line) > limit:
            found.append({
                "type": "style",
                "severity": "warning",
                "line": i,
                "message": f"line is {len(line)} chars (pep8 says max {limit})"
            })
    return found


def _naming(src):
    issues = []
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        # if we can't parse it there's bigger problems
        return [{"type": "syntax", "severity": "error", "line": 1, "message": str(e)}]

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            name = node.name
            # skip dunder methods like __init__, __str__ etc
            if name.startswith("__"):
                continue
            if not re.match(r'^[a-z_][a-z0-9_]*$', name):
                issues.append({
                    "type": "naming",
                    "severity": "warning",
                    "line": node.lineno,
                    "message": f"'{name}' - functions should be snake_case"
                })

        if isinstance(node, ast.ClassDef):
            if not re.match(r'^[A-Z][a-zA-Z0-9]+$', node.name):
                issues.append({
                    "type": "naming",
                    "severity": "warning",
                    "line": node.lineno,
                    "message": f"'{node.name}' - classes should be PascalCase"
                })

    return issues


def _missing_docs(src):
    # only checks functions and classes, not every little thing
    issues = []
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            continue
        has_doc = (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
        )
        if not has_doc:
            issues.append({
                "type": "docs",
                "severity": "info",
                "line": node.lineno,
                "message": f"'{node.name}' has no docstring"
            })

    return issues


def _bare_excepts(src):
    issues = []
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return []

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            issues.append({
                "type": "bad_practice",
                "severity": "warning",
                "line": node.lineno,
                # bare except swallows KeyboardInterrupt and SystemExit which is bad
                "message": "bare except catches everything including keyboard interrupts - be specific"
            })
    return issues


def _unused_imports(src):
    issues = []
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return []

    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                n = alias.asname or alias.name.split(".")[0]
                imported.append((n, node.lineno))
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                n = alias.asname or alias.name
                imported.append((n, node.lineno))

    used = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used.add(node.id)
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            used.add(node.value.id)

    for name, lineno in imported:
        if name not in used and name != "*":
            issues.append({
                "type": "unused",
                "severity": "warning",
                "line": lineno,
                "message": f"'{name}' imported but never used"
            })
    return issues


def _todos(lines):
    # track leftover notes so they don't get forgotten
    issues = []
    pattern = re.compile(r'#\s*(TODO|FIXME|HACK|XXX)', re.IGNORECASE)
    for i, line in enumerate(lines, 1):
        if pattern.search(line):
            issues.append({
                "type": "todo",
                "severity": "info",
                "line": i,
                "message": line.strip()
            })
    return issues


def _magic_numbers(src):
    issues = []
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return []

    ok_numbers = {0, 1, -1, 2, 100}  # these are fine as-is

    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            if node.value not in ok_numbers:
                issues.append({
                    "type": "magic_number",
                    "severity": "info",
                    "line": getattr(node, 'lineno', 0),
                    "message": f"magic number {node.value} - give it a name so it's clear what it means"
                })
    return issues


def _get_metrics(src, lines):
    total = len(lines)
    blank = sum(1 for l in lines if not l.strip())
    comments = sum(1 for l in lines if l.strip().startswith("#"))
    code = total - blank - comments

    fns = classes = 0
    try:
        tree = ast.parse(src)
        fns = sum(1 for n in ast.walk(tree) if isinstance(n, ast.FunctionDef))
        classes = sum(1 for n in ast.walk(tree) if isinstance(n, ast.ClassDef))
    except SyntaxError:
        pass

    return {
        "total": total,
        "code": code,
        "comments": comments,
        "blank": blank,
        "functions": fns,
        "classes": classes,
    }


def _score(issues):
    s = 100
    for issue in issues:
        if issue["severity"] == "error":
            s -= 15
        elif issue["severity"] == "warning":
            s -= 5
        else:
            s -= 1
    return max(0, s)
