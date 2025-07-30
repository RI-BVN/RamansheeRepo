from github import Github
import os
import pandas as pd
from datetime import datetime, timedelta

# Authenticate using GitHub token
g = Github(os.getenv('GH_PAT') or os.getenv('GITHUB_TOKEN'))  # Fallback to GITHUB_TOKEN if GH_PAT not set

# Set your repo
repo = g.get_repo("RI-BVN/RamansheeRepo")

# Get comments from the last 24 hours
since = datetime.utcnow() - timedelta(days=1)

issue_comments = repo.get_issues_comments(since=since)
pr_comments = repo.get_pulls_comments(since=since)

rows = []
sr_no = 1

for comment in issue_comments:
    issue_number = int(comment.issue_url.split('/')[-1])
    issue = repo.get_issue(issue_number)
    rows.append({
        "Sr.No": sr_no,
        "Type": "Issue",
        "Task Title": issue.title,
        "Assignees": ', '.join([a.login for a in issue.assignees]) or "Unassigned",
        "Status": issue.state,
        "Commented By": comment.user.login,
        "Comment": comment.body[:200],
        "Date": comment.created_at.strftime("%Y-%m-%d")
    })
    sr_no += 1

for comment in pr_comments:
    pr_number = int(comment.pull_request_url.split('/')[-1])
    pr = repo.get_pull(pr_number)
    rows.append({
        "Sr.No": sr_no,
        "Type": "Pull Request",
        "Task Title": pr.title,
        "Assignees": ', '.join([a.login for a in pr.assignees]) or "Unassigned",
        "Status": pr.state,
        "Commented By": comment.user.login,
        "Comment": comment.body[:200],
        "Date": comment.created_at.strftime("%Y-%m-%d")
    })
    sr_no += 1

# Create DataFrame and save to Excel
df = pd.DataFrame(rows, columns=[
    "Sr.No", "Type", "Task Title", "Assignees", "Status", "Commented By", "Comment", "Date"
])

today = datetime.today().strftime('%Y-%m-%d')
df.to_excel(f"daily_commented_tasks_{today}.xlsx", index=False)
print("✅ Report generated and saved.")
