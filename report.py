"""
report.py
Formats and prints the analysis results to the terminal or as JSON.
"""

import json


SEVERITY_COLORS = {
    "error":   "\033[91m",  # Red
    "warning": "\033[93m",  # Yellow
    "info":    "\033[94m",  # Blue
}
RESET = "\033[0m"
BOLD  = "\033[1m"
GREEN = "\033[92m"


def _score_label(score: int) -> str:
    if score >= 90:
        return f"{GREEN}Excellent ✓{RESET}"
    elif score >= 75:
        return f"\033[92mGood{RESET}"
    elif score >= 50:
        return f"\033[93mNeeds Work{RESET}"
    else:
        return f"\033[91mPoor ✗{RESET}"


def generate_report(results: dict, score_only: bool = False, output_format: str = "text"):
    """Print the analysis report in the requested format."""
    if output_format == "json":
        print(json.dumps(results, indent=2))
        return

    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}  CodeSense — Code Quality Report{RESET}")
    print(f"{'='*60}")
    print(f"  File   : {results['file']}")
    print(f"  Lines  : {results['metrics']['total_lines']} total  "
          f"({results['metrics']['code_lines']} code, "
          f"{results['metrics']['comment_lines']} comments, "
          f"{results['metrics']['blank_lines']} blank)")
    print(f"  Functions : {results['metrics']['functions']}   "
          f"Classes : {results['metrics']['classes']}   "
          f"Comment ratio : {results['metrics']['comment_ratio']}%")

    if not score_only:
        print(f"\n{BOLD}  Issues Found ({len(results['issues'])}){RESET}")
        print(f"  {'-'*56}")

        if not results["issues"]:
            print(f"  {GREEN}No issues found! Clean code 🎉{RESET}")
        else:
            grouped = {"error": [], "warning": [], "info": []}
            for issue in results["issues"]:
                grouped[issue["severity"]].append(issue)

            for severity in ["error", "warning", "info"]:
                group = grouped[severity]
                if group:
                    color = SEVERITY_COLORS[severity]
                    print(f"\n  {color}{BOLD}[{severity.upper()}] ({len(group)}){RESET}")
                    for issue in group:
                        line_ref = f"line {issue['line']}" if issue.get("line") else ""
                        print(f"  {color}•{RESET} [{issue['type']}] {issue['message']}"
                              + (f"  {BOLD}→ {line_ref}{RESET}" if line_ref else ""))

    score = results["score"]
    label = _score_label(score)
    print(f"\n{BOLD}  Quality Score : {score}/100  —  {label}{RESET}")
    print(f"{'='*60}\n")
