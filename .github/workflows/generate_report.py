from github import Github
import os
import pandas as pd
from datetime import datetime, timedelta

# No need to import 'timezone' explicitly from datetime if you're using utcnow()
# from datetime import datetime, timedelta, timezone # <--- REMOVE timezone here if using utcnow()

g = Github(os.getenv('GH_PAT'))

repo = g.get_repo("RI-BVN/RamansheeRepo")

# Corrected line: Use datetime.utcnow() for a naive UTC datetime
since = datetime.utcnow() - timedelta(days=1) # This will give you a naive UTC datetime

issue_comments = repo.get_issues_comments(since=since)
pr_comments = repo.get_pulls_comments(since=since)

rows = []
sr_no = 1

for comment in issue_comments:
    # Fetch the issue object from the issue_url
    # The issue_url looks like "https://api.github.com/repos/owner/repo/issues/123"
    # We need to extract the issue number from the URL
    issue_number = int(comment.issue_url.split('/')[-1])
    issue = repo.get_issue(issue_number) # Get the actual Issue object

    rows.append({
        "Sr.No": sr_no,
        "Type": "Issue",
        "Task Title": issue.title,
        "Assignees": ', '.join([assignee.login for assignee in issue.assignees]) or "Unassigned",
        "Status": issue.state,
        "Commented By": comment.user.login,
        "Comment": comment.body[:200], # Short preview
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
        "Assignees": ', '.join([assignee.login for assignee in pr.assignees]) or "Unassigned",
        "Status": pr.state,
        "Commented By": comment.user.login,
        "Comment": comment.body[:200],
        "Date": comment.created_at.strftime("%Y-%m-%d")
    })
    sr_no += 1

df = pd.DataFrame(rows, columns=[
    "Sr.No", "Type", "Task Title", "Assignees", "Status", "Commented By", "Comment", "Date"
])

today = datetime.today().strftime('%Y-%m-%d')
df.to_excel(f"daily_commented_tasks_{today}.xlsx", index=False)
print("Report generated: Excel saved.")
