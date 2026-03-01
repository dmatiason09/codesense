#!/usr/bin/env python3
# codesense - quick python code checker i built to stop making the same mistakes
# started this after getting roasted in a code review lol

import argparse
import sys
from analyzer.code_analyzer import run_analysis
from analyzer.report import show_report


def main():
    parser = argparse.ArgumentParser(description="codesense: check your python files before you commit")
    parser.add_argument("file", nargs="?", help="python file to check")
    parser.add_argument("--score", action="store_true", help="just show the score, nothing else")
    parser.add_argument("--json", action="store_true", help="output as json (useful for piping)")

    args = parser.parse_args()

    if not args.file:
        print("usage: python main.py <file.py>")
        print("  python main.py mycode.py")
        print("  python main.py mycode.py --score")
        sys.exit(0)

    try:
        results = run_analysis(args.file)
        show_report(results, score_only=args.score, as_json=args.json)
    except FileNotFoundError:
        print(f"can't find '{args.file}', double check the path")
        sys.exit(1)


if __name__ == "__main__":
    main()
