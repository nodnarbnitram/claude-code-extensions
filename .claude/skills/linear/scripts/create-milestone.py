#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Create a Linear project milestone using the GraphQL API.

Usage:
    uv run scripts/create-milestone.py "Milestone name" --project PROJECT_ID [options]

Options:
    --project       Project UUID (required)
    --description   Milestone description
    --target-date   Target date (YYYY-MM-DD)
    --json          Output full JSON instead of just ID

Returns:
    Without --json: Prints the milestone ID
    With --json: Prints full JSON with id, name, targetDate, etc.

Note:
    The linearis CLI does not support milestone creation.
    This script uses the Linear GraphQL API directly.

Schema Reference:
    https://studio.apollographql.com/public/Linear-API/variant/current/schema/reference
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def get_api_token() -> str | None:
    """Get Linear API token from environment or file."""
    if token := os.environ.get("LINEAR_API_TOKEN"):
        return token
    token_file = Path.home() / ".linear_api_token"
    if token_file.exists():
        return token_file.read_text().strip()
    return None


def create_milestone(
    name: str,
    project_id: str,
    description: str | None = None,
    target_date: str | None = None,
    output_json: bool = False,
) -> None:
    """Create a Linear project milestone using GraphQL API."""

    token = get_api_token()
    if not token:
        print(
            "Error: LINEAR_API_TOKEN not set and ~/.linear_api_token not found",
            file=sys.stderr,
        )
        sys.exit(1)

    # Build GraphQL mutation
    mutation = """
    mutation CreateProjectMilestone($input: ProjectMilestoneCreateInput!) {
      projectMilestoneCreate(input: $input) {
        success
        projectMilestone {
          id
          name
          description
          targetDate
        }
      }
    }
    """

    variables = {
        "input": {
            "projectId": project_id,
            "name": name,
        }
    }

    if description:
        variables["input"]["description"] = description

    if target_date:
        variables["input"]["targetDate"] = target_date

    # Make GraphQL request
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

        if "errors" in data:
            print(f"Error: {data['errors'][0]['message']}", file=sys.stderr)
            sys.exit(1)

        milestone = data["data"]["projectMilestoneCreate"]["projectMilestone"]
        milestone_id = milestone["id"]

        if output_json:
            print(json.dumps(milestone, separators=(",", ":")))
        else:
            print(milestone_id)

    except subprocess.CalledProcessError as e:
        print(f"Error making API request: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Create a Linear project milestone and return its ID"
    )
    parser.add_argument("name", help="Milestone name")
    parser.add_argument("--project", required=True, help="Project UUID")
    parser.add_argument("--description", "-d", help="Milestone description")
    parser.add_argument("--target-date", help="Target date (YYYY-MM-DD)")
    parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Output full JSON instead of just ID",
    )

    args = parser.parse_args()

    create_milestone(
        name=args.name,
        project_id=args.project,
        description=args.description,
        target_date=args.target_date,
        output_json=args.output_json,
    )


if __name__ == "__main__":
    main()
