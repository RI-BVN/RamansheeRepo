from github import Github
import os
import pandas as pd
from datetime import datetime, timedelta

# Authenticate using your GitHub token
g = Github(os.getenv('GITHUB_TOKEN'))  # From GitHub Actions or env

# Set your repo
repo = g.get_repo("RI-BVN/RamansheeRepo")  # 🔁 Replace with your org/repo

# Get all issue and PR comments from the last 24 hours
since = datetime.utcnow() - timedelta(days=1)

# Collect all comments
issue_comments = repo.get_issues_comments(since=since)
pr_comments = repo.get_pulls_comments(since=since)

# Store rows
rows = []
sr_no = 1

# Handle Issue Comments
for comment in issue_comments:
    issue = comment.issue
    rows.append({
        "Sr.No": sr_no,
        "Type": "Issue",
        "Task Title": issue.title,
        "Assignees": ', '.join([assignee.login for assignee in issue.assignees]) or "Unassigned",
        "Status": issue.state,
        "Commented By": comment.user.login,
        "Comment": comment.body[:200],  # Short preview
        "Date": comment.created_at.strftime("%Y-%m-%d")
    })
    sr_no += 1

# Handle PR Comments
for comment in pr_comments:
    pr_number = int(comment.pull_request_url.split('/')[-1])
    pr = repo.get_pull(pr_number)
    rows.append({
        "Sr.No": sr_no,
        "Type": "Pull Request",
        "Task Title": pr.title,
        "Assignees": ', '.join([assignee.login for assignee in pr.assignees]) or "Unassigned",
        "Status": pr.state,
        "Commented By": comment.user.login,
        "Comment": comment.body[:200],
        "Date": comment.created_at.strftime("%Y-%m-%d")
    })
    sr_no += 1

# Create DataFrame and export to Excel
df = pd.DataFrame(rows, columns=[
    "Sr.No", "Type", "Task Title", "Assignees", "Status", "Commented By", "Comment", "Date"
])

today = datetime.today().strftime('%Y-%m-%d')
df.to_excel(f"daily_commented_tasks_{today}.xlsx", index=False)
print("Report generated: Excel saved.")
