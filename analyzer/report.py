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
            # group by severity
            for sev in ["error", "warning", "info"]:
                group = [x for x in issues if x["severity"] == sev]
                if not group:
                    continue
                c = SEV_COLOR[sev]
                print(f"\n  {c}{sev.upper()} × {len(group)}{RESET}")
                for issue in group:
                    ln = f"  (line {issue['line']})" if issue.get("line") else ""
                    print(f"  {c}•{RESET} [{issue['type']}] {issue['message']}{BOLD}{ln}{RESET}")

    # score label
    if score >= 90:
        label = f"{GREEN}excellent{RESET}"
    elif score >= 75:
        label = f"{GREEN}good{RESET}"
    elif score >= 50:
        label = f"{YELLOW}needs work{RESET}"
    else:
        label = f"{RED}poor{RESET}"

    print(f"\n  score: {BOLD}{score}/100{RESET} — {label}\n")
