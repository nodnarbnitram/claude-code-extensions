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
import sys

from linear_graphql import LinearError, set_issue_milestone


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

    success_count = 0
    fail_count = 0

    for issue_id in issue_ids:
        issue_id = issue_id.strip()
        if not issue_id:
            continue

        try:
            if set_issue_milestone(issue_id, args.milestone_id):
                success_count += 1
            else:
                print(f"Warning: Failed to add '{issue_id}'", file=sys.stderr)
                fail_count += 1
        except LinearError as exc:
            print(f"Warning: {exc}", file=sys.stderr)
            fail_count += 1


    print(f"Added {success_count} issues to milestone ({fail_count} failed)")

    if fail_count > 0 and success_count == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
