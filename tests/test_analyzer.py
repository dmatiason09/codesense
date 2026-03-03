"""
tests for codesense - added these after breaking the magic number check
by accident and not noticing for like a week lol
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analyzer.code_analyzer import (
    run_analysis,
    _long_lines,
    _naming,
    _bare_excepts,
    _unused_imports,
    _magic_numbers,
    _long_functions,
    _short_varnames,
)


# ── helpers ──────────────────────────────────────────────────────────────────

def issues_of_type(issues, type_):
    return [i for i in issues if i["type"] == type_]


# ── _long_lines ───────────────────────────────────────────────────────────────

def test_long_lines_catches_violation():
    lines = ["x = 1", "a" * 80]
    found = _long_lines(lines)
    assert len(found) == 1
    assert found[0]["line"] == 2


def test_long_lines_clean():
    lines = ["x = 1", "y = 2"]
    assert _long_lines(lines) == []


def test_long_lines_exactly_at_limit():
    # 79 chars should be fine, 80 should not
    lines = ["a" * 79, "b" * 80]
    found = _long_lines(lines)
    assert len(found) == 1


# ── _naming ───────────────────────────────────────────────────────────────────

def test_naming_bad_function():
    src = "def MyFunction(): pass"
    issues = _naming(src)
    assert any(i["type"] == "naming" for i in issues)


def test_naming_good_function():
    src = "def my_function(): pass"
    issues = _naming(src)
    assert issues == []


def test_naming_bad_class():
    src = "class my_class: pass"
    issues = _naming(src)
    assert any(i["type"] == "naming" for i in issues)


def test_naming_good_class():
    src = "class MyClass: pass"
    issues = _naming(src)
    assert issues == []


def test_naming_ignores_dunder():
    src = "def __init__(self): pass"
    issues = _naming(src)
    assert issues == []


# ── _bare_excepts ─────────────────────────────────────────────────────────────

def test_bare_except_caught():
    src = "try:\n    pass\nexcept:\n    pass"
    issues = _bare_excepts(src)
    assert len(issues) == 1


def test_specific_except_ok():
    src = "try:\n    pass\nexcept ValueError:\n    pass"
    issues = _bare_excepts(src)
    assert issues == []


# ── _unused_imports ───────────────────────────────────────────────────────────

def test_unused_import_caught():
    src = "import os\n"
    issues = _unused_imports(src)
    assert any(i["type"] == "unused" for i in issues)


def test_used_import_ok():
    src = "import os\nos.getcwd()"
    issues = _unused_imports(src)
    assert issues == []


# ── _magic_numbers ────────────────────────────────────────────────────────────

def test_magic_number_caught():
    src = "x = 42\n"
    issues = _magic_numbers(src)
    assert any(i["type"] == "magic_number" for i in issues)


def test_allowed_numbers_ok():
    for n in [0, 1, -1, 2, 100]:
        src = f"x = {n}\n"
        issues = _magic_numbers(src)
        assert issues == [], f"number {n} should be allowed"


# ── _long_functions ───────────────────────────────────────────────────────────

def test_long_function_caught():
    # build a function with 35 lines
    body = "\n".join(["    x = 1"] * 35)
    src = f"def big_func():\n{body}\n"
    issues = _long_functions(src)
    assert any(i["type"] == "complexity" for i in issues)


def test_short_function_ok():
    src = "def small_func():\n    return 1\n"
    issues = _long_functions(src)
    assert issues == []


# ── _short_varnames ───────────────────────────────────────────────────────────

def test_short_varname_caught():
    src = "x = some_value\n"
    issues = _short_varnames(src)
    assert any(i["type"] == "naming" for i in issues)


def test_underscore_ok():
    # _ is a common throwaway variable
    src = "_ = something\n"
    issues = _short_varnames(src)
    assert issues == []


# ── run_analysis (integration) ────────────────────────────────────────────────

def test_run_analysis_returns_expected_keys(tmp_path):
    f = tmp_path / "sample.py"
    f.write_text("x = 1\n")
    result = run_analysis(str(f))
    assert "file" in result
    assert "issues" in result
    assert "metrics" in result
    assert "score" in result


def test_run_analysis_score_between_0_and_100(tmp_path):
    f = tmp_path / "sample.py"
    f.write_text("import os\nimport sys\nimport json\nx=1\n")
    result = run_analysis(str(f))
    assert 0 <= result["score"] <= 100


def test_run_analysis_file_not_found():
    with pytest.raises(FileNotFoundError):
        run_analysis("definitely_does_not_exist.py")
