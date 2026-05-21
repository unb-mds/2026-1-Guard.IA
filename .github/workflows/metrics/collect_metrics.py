#!/usr/bin/env python3
"""
Coletor de métricas Guard.IA — duas branches
Gera docs/productivity/metrics.json com dados de dev-projeto e estudos.
Dependência: PyGithub  (pip install PyGithub)
"""
 
import json
import os
from datetime import datetime, timezone
from github import Github
 
REPO_NAME   = "unb-mds/2026-1-Guard.IA"
BRANCHES    = ["dev-projeto", "estudos"]
OUTPUT_PATH = "docs/productivity/metrics.json"
 
 
def _iso(dt):
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()
 
 
def collect_branch(repo, branch_name):
    """Coleta commits de uma branch específica."""
    try:
        commits_raw = list(repo.get_commits(sha=branch_name))
    except Exception as e:
        print(f"  ⚠️  Branch '{branch_name}' não encontrada ou sem commits: {e}")
        return {
            "branch": branch_name,
            "total_commits": 0,
            "commits_per_author": {},
            "commit_timeline": [],
            "recent_commits": [],
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
        "branch":              branch_name,
        "total_commits":       len(commits),
        "commits_per_author":  commits_per_author,
        "commit_timeline":     commit_timeline,
        "recent_commits":      commits[:40],
    }
 
 
def collect_issues(repo):
    """Coleta issues do repositório (não são por branch)."""
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
    """Coleta pull requests abertos e fechados."""
    prs = []
    for pr in repo.get_pulls(state="all"):
        prs.append({
            "number":    pr.number,
            "title":     pr.title[:120],
            "state":     pr.state,
            "base":      pr.base.ref,
            "head":      pr.head.ref,
            "author":    pr.user.login if pr.user else "unknown",
            "created_at":_iso(pr.created_at),
            "merged_at": _iso(pr.merged_at),
        })
    return prs[:100]
 
 
def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise EnvironmentError("Defina a variável de ambiente GITHUB_TOKEN.")
 
    g    = Github(token)
    repo = g.get_repo(REPO_NAME)
 
    print(f"📦 Repositório: {REPO_NAME}")
 
    # Coleta por branch
    branches_data = {}
    for branch in BRANCHES:
        print(f"🔍 Coletando branch '{branch}'…")
        branches_data[branch] = collect_branch(repo, branch)
 
    # Issues e PRs (globais)
    print("🔍 Coletando issues…")
    issues_data = collect_issues(repo)
 
    print("🔍 Coletando pull requests…")
    prs_data = collect_prs(repo)
 
    # Consolida membros únicos entre as duas branches
    all_authors = {}
    for bd in branches_data.values():
        for author, count in bd["commits_per_author"].items():
            all_authors[author] = all_authors.get(author, 0) + count
 
    data = {
        "generated_at": _iso(datetime.now(timezone.utc)),
        "repo":         REPO_NAME,
        "branches":     BRANCHES,
        "summary": {
            "total_commits":  sum(bd["total_commits"] for bd in branches_data.values()),
            "open_issues":    issues_data["open"],
            "closed_issues":  issues_data["closed"],
            "contributors":   len(all_authors),
            "open_prs":       sum(1 for p in prs_data if p["state"] == "open"),
        },
        "branches_data": branches_data,
        "issues":        issues_data,
        "pull_requests": prs_data,
        "all_authors":   all_authors,
    }
 
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
 
    s = data["summary"]
    print(f"\n✅  metrics.json gerado → {OUTPUT_PATH}")
    print(f"   Commits totais : {s['total_commits']}")
    for b in BRANCHES:
        print(f"   ├─ {b}: {branches_data[b]['total_commits']} commits")
    print(f"   Issues         : open={s['open_issues']}  closed={s['closed_issues']}")
    print(f"   PRs abertos    : {s['open_prs']}")
    print(f"   Membros únicos : {s['contributors']}")
 
 
if __name__ == "__main__":
    main()