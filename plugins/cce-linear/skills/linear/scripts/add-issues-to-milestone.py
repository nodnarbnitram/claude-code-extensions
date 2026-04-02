#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Add issues to a Linear project milestone.

Usage:
    uv run scripts/add-issues-to-milestone.py MILESTONE_ID ISSUE_ID [ISSUE_ID ...]
    uv run scripts/add-issues-to-milestone.py MILESTONE_ID --issues ICE-2027,ICE-2028

Options:
    MILESTONE_ID    Milestone UUID
    ISSUE_ID        Issue identifiers (e.g., ICE-2027) or UUIDs
    --issues        Comma-separated list of issue identifiers

Returns:
    Count of successfully added issues
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def get_api_token() -> str | None:
    if token := os.environ.get("LINEAR_API_TOKEN"):
        return token
    token_file = Path.home() / ".linear_api_token"
    if token_file.exists():
        return token_file.read_text().strip()
    return None


def get_issue_uuid(identifier: str, token: str) -> str | None:
    if len(identifier) == 36 and identifier.count("-") == 4:
        return identifier

    query = '{ issue(id: "%s") { id } }' % identifier
    payload = json.dumps({"query": query})

    try:
        result = subprocess.run(
            [
                "curl",
                "-s",
                "-X",
                "POST",
                "https://api.linear.app/graphql",
                "-H",
                "Content-Type: application/json",
                "-H",
                f"Authorization: {token}",
                "-d",
                payload,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(result.stdout)
        if data.get("data", {}).get("issue"):
            return data["data"]["issue"]["id"]
        return None
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return None


def add_issue_to_milestone(token: str, issue_uuid: str, milestone_id: str) -> bool:
    mutation = """
    mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
      issueUpdate(id: $id, input: $input) { success }
    }
    """
    variables = {"id": issue_uuid, "input": {"projectMilestoneId": milestone_id}}
    payload = json.dumps({"query": mutation, "variables": variables})

    try:
        result = subprocess.run(
            [
                "curl",
                "-s",
                "-X",
                "POST",
                "https://api.linear.app/graphql",
                "-H",
                "Content-Type: application/json",
                "-H",
                f"Authorization: {token}",
                "-d",
                payload,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(result.stdout)
        return data.get("data", {}).get("issueUpdate", {}).get("success", False)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return False


def main():
    parser = argparse.ArgumentParser(description="Add issues to a project milestone")
    parser.add_argument("milestone_id", help="Milestone UUID")
    parser.add_argument("issue_ids", nargs="*", help="Issue identifiers")
    parser.add_argument("--issues", help="Comma-separated issue identifiers")

    args = parser.parse_args()

    issue_ids = list(args.issue_ids) if args.issue_ids else []
    if args.issues:
        issue_ids.extend(args.issues.split(","))

    if not issue_ids:
        print("Error: No issue IDs provided", file=sys.stderr)
        sys.exit(1)

    token = get_api_token()
    if not token:
        print("Error: LINEAR_API_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    success_count = 0
    fail_count = 0

    for issue_id in issue_ids:
        issue_id = issue_id.strip()
        if not issue_id:
            continue

        issue_uuid = get_issue_uuid(issue_id, token)
        if not issue_uuid:
            print(f"Warning: Issue '{issue_id}' not found", file=sys.stderr)
            fail_count += 1
            continue

        if add_issue_to_milestone(token, issue_uuid, args.milestone_id):
            success_count += 1
        else:
            print(f"Warning: Failed to add '{issue_id}'", file=sys.stderr)
            fail_count += 1

    print(f"Added {success_count} issues to milestone ({fail_count} failed)")

    if fail_count > 0 and success_count == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
