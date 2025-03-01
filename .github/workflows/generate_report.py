from github import Github
import os
from datetime import datetime, timedelta

# Authenticate to GitHub
g = Github(os.getenv('GITHUB_TOKEN'))

# Get the repository
repo = g.get_repo("Vishal-Bhaliya/your-repo-name")

# Get the date 24 hours ago
since = datetime.utcnow() - timedelta(days=1)

# Collect comments from issues and pull requests
comments = repo.get_issues_comments(since=since)
pr_comments = repo.get_pulls_comments(since=since)

# Generate the report
report = "# Daily Commented Tasks Report\n\n"
report += f"Report generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

report += "## Issue Comments\n\n"
for comment in comments:
    report += f"- **{comment.user.login}** commented on issue **#{comment.issue.number}**: {comment.body[:100]}...\n"

report += "\n## Pull Request Comments\n\n"
for comment in pr_comments:
    report += f"- **{comment.user.login}** commented on pull request **#{comment.pull_request_url.split('/')[-1]}**: {comment.body[:100]}...\n"

# Save the report to a file
with open("report.md", "w") as f:
    f.write(report)
