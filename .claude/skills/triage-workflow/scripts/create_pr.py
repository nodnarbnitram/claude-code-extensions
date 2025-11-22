#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Create a GitHub PR with ticket reference.

Usage:
    uv run scripts/create_pr.py ICE-1965 "PR title" --body "Description"
    uv run scripts/create_pr.py ICE-1965 "PR title" --draft

Options:
    --body        PR body/description
    --base        Base branch (default: main)
    --draft       Create as draft PR
    --reviewer    Request reviewers (comma-separated)
    --assignee    Assign users (comma-separated)
    --label       Add labels (comma-separated)

Returns:
    Prints the PR URL to stdout
"""

import argparse
import subprocess
import sys


def create_pr(
    identifier: str,
    title: str,
    body: str = None,
    base: str = "main",
    draft: bool = False,
    reviewer: str = None,
    assignee: str = None,
    label: str = None,
) -> str:
    """Create a GitHub PR and return its URL."""

    # Prefix title with ticket identifier
    full_title = f"{identifier}: {title}"

    # Build body with ticket reference
    if body:
        full_body = f"Fixes {identifier}\n\n{body}"
    else:
        full_body = f"Fixes {identifier}\n\n## Summary\n\n## Test Plan\n- [ ] Tests pass\n- [ ] Manual verification"

    cmd = [
        "gh", "pr", "create",
        "--title", full_title,
        "--body", full_body,
        "--base", base
    ]

    if draft:
        cmd.append("--draft")
    if reviewer:
        cmd.extend(["--reviewer", reviewer])
    if assignee:
        cmd.extend(["--assignee", assignee])
    if label:
        cmd.extend(["--label", label])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        # gh pr create outputs the URL
        pr_url = result.stdout.strip()
        return pr_url

    except subprocess.CalledProcessError as e:
        print(f"Error creating PR: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: gh CLI not found. Install from: https://cli.github.com/", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Create a GitHub PR with ticket reference"
    )
    parser.add_argument("identifier", help="Ticket identifier (e.g., ICE-1965)")
    parser.add_argument("title", help="PR title (will be prefixed with identifier)")
    parser.add_argument("--body", "-b", help="PR body/description")
    parser.add_argument("--base", default="main", help="Base branch (default: main)")
    parser.add_argument("--draft", action="store_true", help="Create as draft PR")
    parser.add_argument("--reviewer", "-r", help="Request reviewers (comma-separated)")
    parser.add_argument("--assignee", "-a", help="Assign users (comma-separated)")
    parser.add_argument("--label", "-l", help="Add labels (comma-separated)")

    args = parser.parse_args()

    pr_url = create_pr(
        identifier=args.identifier,
        title=args.title,
        body=args.body,
        base=args.base,
        draft=args.draft,
        reviewer=args.reviewer,
        assignee=args.assignee,
        label=args.label,
    )

    print(pr_url)


if __name__ == "__main__":
    main()
