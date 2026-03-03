import json

# terminal colors - keeping it simple
RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
GREEN  = "\033[92m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

SEV_COLOR = {"error": RED, "warning": YELLOW, "info": BLUE}


def show_report(results, score_only=False, as_json=False):
    if as_json:
        print(json.dumps(results, indent=2))
        return

    f = results["file"]
    m = results["metrics"]
    score = results["score"]
    issues = results["issues"]

    print(f"\n{BOLD}codesense → {f}{RESET}")
    print(f"  {m['total']} lines  ({m['code']} code / {m['comments']} comments / {m['blank']} blank)")
    print(f"  {m['functions']} functions, {m['classes']} classes")

    if not score_only:
        print(f"\n  {BOLD}issues ({len(issues)}){RESET}")
        if not issues:
            print(f"  {GREEN}clean! no issues found{RESET}")
        else:
            for sev in ["error", "warning", "info"]:
                group = [x for x in issues if x["severity"] == sev]
                if not group:
                    continue
                c = SEV_COLOR[sev]
                print(f"\n  {c}{sev.upper()} × {len(group)}{RESET}")
                for issue in group:
                    ln = f"  (line {issue['line']})" if issue.get("line") else ""
                    print(f"  {c}•{RESET} [{issue['type']}] {issue['message']}{BOLD}{ln}{RESET}")

    print(f"\n  score: {BOLD}{score}/100{RESET} — {_score_label(score)}\n")


def show_summary(all_results):
    """print an overall summary when analyzing multiple files"""
    total_issues = sum(len(r["issues"]) for r in all_results)
    total_files = len(all_results)
    avg_score = sum(r["score"] for r in all_results) // total_files

    worst = min(all_results, key=lambda r: r["score"])
    best = max(all_results, key=lambda r: r["score"])

    print(f"\n{BOLD}{'─' * 50}{RESET}")
    print(f"{BOLD}summary — {total_files} files checked{RESET}")
    print(f"  total issues : {total_issues}")
    print(f"  average score: {BOLD}{avg_score}/100{RESET} — {_score_label(avg_score)}")
    print(f"  best file    : {GREEN}{best['file']}{RESET} ({best['score']}/100)")
    print(f"  worst file   : {RED}{worst['file']}{RESET} ({worst['score']}/100)")
    print(f"{BOLD}{'─' * 50}{RESET}\n")


def _score_label(score):
    if score >= 90:
        return f"{GREEN}excellent{RESET}"
    elif score >= 75:
        return f"{GREEN}good{RESET}"
    elif score >= 50:
        return f"{YELLOW}needs work{RESET}"
    else:
        return f"{RED}poor{RESET}"
