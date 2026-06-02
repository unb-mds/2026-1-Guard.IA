import json
import os
from datetime import datetime, timezone
from github import Github

REPO_NAME   = "unb-mds/2026-1-Guard.IA"
OUTPUT_PATH = "docs/productivity/metrics.json"

BRANCHES_IGNORADAS = {"gh-pages"}


def _iso(dt):
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def descobrir_branches(repo):
    branches_ativas = set()
    for branch in repo.get_branches():
        if branch.name not in BRANCHES_IGNORADAS:
            branches_ativas.add(branch.name)

    branches_deletadas = set()
    for pr in repo.get_pulls(state="closed"):
        if pr.merged_at and pr.head.ref not in branches_ativas:
            branches_deletadas.add(pr.head.ref)

    todas = sorted(branches_ativas) + sorted(branches_deletadas)
    print(f"   Branches ativas   : {sorted(branches_ativas)}")
    print(f"   Branches deletadas: {sorted(branches_deletadas)}")
    return todas, branches_ativas, branches_deletadas


def collect_branch(repo, branch_name, sha=None):
    try:
        ref = sha or branch_name
        commits_raw = list(repo.get_commits(sha=ref))
    except Exception as e:
        print(f"  Branch '{branch_name}' não encontrada ou sem commits: {e}")
        return {
            "branch":             branch_name,
            "status":             "deleted",
            "total_commits":      0,
            "commits_per_author": {},
            "commit_timeline":    [],
            "recent_commits":     [],
        }

    commits            = []
    commits_per_author = {}
    commits_per_day    = {}

    for c in commits_raw:
        login    = (c.author.login if c.author else None) or c.commit.author.name or "unknown"
        date_str = _iso(c.commit.author.date)
        day_key  = (date_str or "unknown")[:10]
        msg      = c.commit.message or ""

        commits.append({
            "sha":        c.sha[:7],
            "author":     login,
            "date":       date_str,
            "message":    msg.split("\n")[0][:120],
            "char_count": len(msg),
        })
        commits_per_author[login] = commits_per_author.get(login, 0) + 1
        commits_per_day[day_key]  = commits_per_day.get(day_key, 0) + 1

    commit_timeline = [
        {"date": d, "count": v}
        for d, v in sorted(commits_per_day.items())
    ]

    return {
        "branch":             branch_name,
        "total_commits":      len(commits),
        "commits_per_author": commits_per_author,
        "commit_timeline":    commit_timeline,
        "recent_commits":     commits[:40],
    }


def collect_branch_deletada(repo, pr):
    branch_name = pr.head.ref
    try:
        commits_raw = list(repo.get_commits(sha=pr.head.sha))
    except Exception as e:
        print(f"   Branch deletada '{branch_name}' sem acesso via SHA: {e}")
        return {
            "branch":             branch_name,
            "status":             "deleted",
            "merged_into":        pr.base.ref,
            "merged_at":          _iso(pr.merged_at),
            "pr_number":          pr.number,
            "pr_title":           pr.title[:120],
            "total_commits":      0,
            "commits_per_author": {},
            "commit_timeline":    [],
            "recent_commits":     [],
        }

    commits            = []
    commits_per_author = {}
    commits_per_day    = {}

    for c in commits_raw:
        login    = (c.author.login if c.author else None) or c.commit.author.name or "unknown"
        date_str = _iso(c.commit.author.date)
        day_key  = (date_str or "unknown")[:10]
        msg      = c.commit.message or ""

        commits.append({
            "sha":        c.sha[:7],
            "author":     login,
            "date":       date_str,
            "message":    msg.split("\n")[0][:120],
            "char_count": len(msg),
        })
        commits_per_author[login] = commits_per_author.get(login, 0) + 1
        commits_per_day[day_key]  = commits_per_day.get(day_key, 0) + 1

    commit_timeline = [
        {"date": d, "count": v}
        for d, v in sorted(commits_per_day.items())
    ]

    return {
        "branch":             branch_name,
        "status":             "deleted",
        "merged_into":        pr.base.ref,
        "merged_at":          _iso(pr.merged_at),
        "pr_number":          pr.number,
        "pr_title":           pr.title[:120],
        "total_commits":      len(commits),
        "commits_per_author": commits_per_author,
        "commit_timeline":    commit_timeline,
        "recent_commits":     commits[:40],
    }


def collect_issues(repo):
    all_issues = list(repo.get_issues(state="all"))
    issues                = []
    issues_open_per_day   = {}
    issues_closed_per_day = {}

    for issue in all_issues:
        if issue.pull_request:
            continue
        open_day   = (_iso(issue.created_at) or "")[:10] or None
        closed_day = (_iso(issue.closed_at)  or "")[:10] or None

        issues.append({
            "number":     issue.number,
            "title":      issue.title[:120],
            "state":      issue.state,
            "created_at": _iso(issue.created_at),
            "closed_at":  _iso(issue.closed_at),
            "labels":     [lb.name for lb in issue.labels],
        })
        if open_day:
            issues_open_per_day[open_day] = issues_open_per_day.get(open_day, 0) + 1
        if closed_day:
            issues_closed_per_day[closed_day] = issues_closed_per_day.get(closed_day, 0) + 1

    all_dates = sorted(set(list(issues_open_per_day) + list(issues_closed_per_day)))
    issue_timeline = [
        {"date": d,
         "opened": issues_open_per_day.get(d, 0),
         "closed": issues_closed_per_day.get(d, 0)}
        for d in all_dates
    ]

    return {
        "total":    len(issues),
        "open":     sum(1 for i in issues if i["state"] == "open"),
        "closed":   sum(1 for i in issues if i["state"] == "closed"),
        "timeline": issue_timeline,
        "list":     issues[:200],
    }


def collect_prs(repo):
    prs = []
    for pr in repo.get_pulls(state="all"):
        prs.append({
            "number":     pr.number,
            "title":      pr.title[:120],
            "state":      pr.state,
            "base":       pr.base.ref,
            "head":       pr.head.ref,
            "author":     pr.user.login if pr.user else "unknown",
            "created_at": _iso(pr.created_at),
            "merged_at":  _iso(pr.merged_at),
        })
    return prs[:100]


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise EnvironmentError("Defina a variável de ambiente GITHUB_TOKEN.")

    g    = Github(token)
    repo = g.get_repo(REPO_NAME)

    print(f" Repositório: {REPO_NAME}")
    print(" Descobrindo branches...")

    _, branches_ativas, branches_deletadas = descobrir_branches(repo)
    branches_data = {}
    for branch_name in sorted(branches_ativas):
        print(f" Coletando branch ativa '{branch_name}'…")
        branches_data[branch_name] = collect_branch(repo, branch_name)

    prs_merged = {}
    for pr in repo.get_pulls(state="closed"):
        if pr.merged_at and pr.head.ref not in branches_ativas:
            nome = pr.head.ref
            if nome not in prs_merged or pr.merged_at > prs_merged[nome].merged_at:
                prs_merged[nome] = pr

    for branch_name, pr in sorted(prs_merged.items()):
        print(f"  Coletando branch deletada '{branch_name}' (PR #{pr.number})…")
        branches_data[branch_name] = collect_branch_deletada(repo, pr)

    print(" Coletando issues…")
    issues_data = collect_issues(repo)

    print(" Coletando pull requests…")
    prs_data = collect_prs(repo)

    all_authors = {}
    for bd in branches_data.values():
        for author, count in bd["commits_per_author"].items():
            all_authors[author] = all_authors.get(author, 0) + count

    branches_ativas_list  = sorted(branches_ativas)
    branches_deletadas_list = sorted(prs_merged.keys())

    data = {
        "generated_at": _iso(datetime.now(timezone.utc)),
        "repo":         REPO_NAME,
        "branches":          branches_ativas_list,
        "branches_deletadas": branches_deletadas_list,
        "summary": {
            "total_commits":       sum(bd["total_commits"] for bd in branches_data.values()),
            "open_issues":         issues_data["open"],
            "closed_issues":       issues_data["closed"],
            "contributors":        len(all_authors),
            "open_prs":            sum(1 for p in prs_data if p["state"] == "open"),
            "branches_ativas":     len(branches_ativas_list),
            "branches_deletadas":  len(branches_deletadas_list),
        },
        "branches_data":  branches_data,
        "issues":         issues_data,
        "pull_requests":  prs_data,
        "all_authors":    all_authors,
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)

    s = data["summary"]
    print(f"\n  metrics.json gerado → {OUTPUT_PATH}")
    print(f"   Commits totais      : {s['total_commits']}")
    print(f"   Branches ativas     : {s['branches_ativas']}")
    print(f"   Branches deletadas  : {s['branches_deletadas']}")
    for b_name, bd in sorted(branches_data.items()):
        status = " [deletada]" if bd.get("status") == "deleted" else ""
        print(f"   ├─ {b_name}{status}: {bd['total_commits']} commits")
    print(f"   Issues              : open={s['open_issues']}  closed={s['closed_issues']}")
    print(f"   PRs abertos         : {s['open_prs']}")
    print(f"   Membros únicos      : {s['contributors']}")


if __name__ == "__main__":
    main()