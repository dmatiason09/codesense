#!/usr/bin/env python3
"""
CodeSense - Python Code Quality Analyzer
Author: Your Name
Description: Analyzes Python code files for quality, style, and common issues.
"""

import argparse
import sys
from analyzer.code_analyzer import CodeAnalyzer
from analyzer.report import generate_report


def main():
    parser = argparse.ArgumentParser(
        description="CodeSense: Analyze the quality of Python code files.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to the Python file to analyze"
    )
    parser.add_argument(
        "--score-only",
        action="store_true",
        help="Show only the final quality score"
    )
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="Output format: text (default) or json"
    )

    args = parser.parse_args()

    if not args.file:
        parser.print_help()
        print("\nExample usage:")
        print("  python main.py examples/good_code.py")
        print("  python main.py examples/bad_code.py --output json")
        sys.exit(0)

    try:
        analyzer = CodeAnalyzer(args.file)
        results = analyzer.analyze()
        generate_report(results, score_only=args.score_only, output_format=args.output)
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
