#!/usr/bin/env python3
# codesense - quick python code checker i built to stop making the same mistakes
# started this after getting roasted in a code review lol

import argparse
import sys
import os
from analyzer.code_analyzer import run_analysis
from analyzer.report import show_report, show_summary


def collect_files(path):
    """given a file or folder, return a list of .py files to check"""
    if os.path.isfile(path):
        if not path.endswith(".py"):
            print(f"warning: '{path}' doesn't look like a python file, skipping")
            return []
        return [path]

    if os.path.isdir(path):
        found = []
        for root, _, files in os.walk(path):
            for f in files:
                if f.endswith(".py"):
                    found.append(os.path.join(root, f))
        return sorted(found)

    return []


def main():
    parser = argparse.ArgumentParser(description="codesense: check your python files before you commit")
    parser.add_argument("path", nargs="?", help="python file or folder to check")
    parser.add_argument("--score", action="store_true", help="just show the score, nothing else")
    parser.add_argument("--json", action="store_true", help="output as json (useful for piping)")

    args = parser.parse_args()

    if not args.path:
        print("usage: python main.py <file.py>")
        print("       python main.py <folder/>")
        print("  python main.py mycode.py --score")
        print("  python main.py src/ --json")
        sys.exit(0)

    files = collect_files(args.path)

    if not files:
        print(f"no python files found in '{args.path}'")
        sys.exit(1)

    all_results = []
    for filepath in files:
        try:
            results = run_analysis(filepath)
            show_report(results, score_only=args.score, as_json=args.json)
            all_results.append(results)
        except FileNotFoundError:
            print(f"can't find '{filepath}', skipping")
        except Exception as e:
            print(f"error analyzing '{filepath}': {e}")

    # only show summary when checking multiple files
    if len(all_results) > 1 and not args.json:
        show_summary(all_results)


if __name__ == "__main__":
    main()
