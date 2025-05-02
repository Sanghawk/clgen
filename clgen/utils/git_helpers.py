import subprocess
from pathlib import Path
from typing import Dict, List, Optional


def get_commits(
    path: Path, since: Optional[str] = None, until: str = "HEAD"
) -> List[Dict[str, str]]:
    """
    Retrieve git commits in structured format.

    Returns a list of dicts with keys:
      - commit: full commit hash
      - author: author name/email
      - date: commit date
      - summary: commit summary (subject)
      - body: commit body (message excluding subject)

    :param path: path to the git repository
    :param since: optional starting revision (e.g. 'v1.0.0')
    :param until: ending revision (defaults to HEAD)
    :return: list of commit dicts
    """
    # Format each commit as: hash, author, date, summary, body; record separator: \x1e; field separator: \x1f
    fmt = "%H%x1f%an%x1f%ad%x1f%s%x1f%B%x1e"
    args = ["git", "-C", str(path), "log", f"--pretty=format:{fmt}"]
    if since:
        args.append(f"{since}..{until}")

    raw = subprocess.check_output(args, text=True)
    entries = [entry for entry in raw.split("\x1e") if entry.strip()]

    commits: List[Dict[str, str]] = []
    for entry in entries:
        parts = entry.split("\x1f")
        if len(parts) < 5:
            # Skip malformed entries
            continue
        commit_hash, author, date, summary, body = (
            parts[0],
            parts[1],
            parts[2],
            parts[3],
            parts[4].rstrip(),
        )
        commits.append(
            {
                "commit": commit_hash,
                "author": author,
                "date": date,
                "summary": summary,
                "body": body,
            }
        )

    return commits
