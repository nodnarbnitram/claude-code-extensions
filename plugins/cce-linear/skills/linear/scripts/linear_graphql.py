from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib import error, request

LINEAR_GRAPHQL_ENDPOINT = "https://api.linear.app/graphql"

ISSUE_LIST_FIELDS = """
id
identifier
title
description
branchName
priority
createdAt
updatedAt
url
state {
  id
  name
}
assignee {
  id
  name
}
team {
  id
  key
  name
}
project {
  id
  name
}
projectMilestone {
  id
  name
  targetDate
}
labels {
  nodes {
    id
    name
  }
}
""".strip()

ISSUE_DETAIL_FIELDS = f"""
{ISSUE_LIST_FIELDS}
parent {{
  id
  identifier
  title
}}
children {{
  nodes {{
    id
    identifier
    title
  }}
}}
comments {{
  nodes {{
    id
    body
    createdAt
    updatedAt
    user {{
      id
      name
    }}
  }}
}}
""".strip()

DOCUMENT_FIELDS = """
id
title
content
slugId
url
icon
color
createdAt
updatedAt
trashed
""".strip()


class LinearError(RuntimeError):
    """Raised when a Linear GraphQL operation fails."""


def get_api_token() -> str | None:
    if token := os.environ.get("LINEAR_API_TOKEN"):
        return token.strip()

    token_file = Path.home() / ".linear_api_token"
    if token_file.exists():
        return token_file.read_text().strip()

    return None


def require_api_token() -> str:
    token = get_api_token()
    if token:
        return token

    raise LinearError(
        "LINEAR_API_TOKEN not set and ~/.linear_api_token not found"
    )


def is_uuid(value: str) -> bool:
    if len(value) != 36:
        return False

    parts = value.split("-")
    return len(parts) == 5 and [len(part) for part in parts] == [8, 4, 4, 4, 12]


def parse_issue_identifier(value: str) -> tuple[str, int] | None:
    if "-" not in value:
        return None

    team_key, issue_number = value.rsplit("-", 1)
    if not team_key or not issue_number.isdigit():
        return None

    return team_key, int(issue_number)


def graphql_request(query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    token = require_api_token()
    payload = json.dumps(
        {
            "query": query,
            "variables": variables or {},
        }
    ).encode("utf-8")

    http_request = request.Request(
        LINEAR_GRAPHQL_ENDPOINT,
        data=payload,
        headers={
            "Authorization": token,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(http_request) as response:
            raw_body = response.read().decode("utf-8")
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace").strip()
        raise LinearError(body or f"HTTP {exc.code} from Linear API") from exc
    except error.URLError as exc:
        raise LinearError(f"Unable to reach Linear API: {exc.reason}") from exc

    try:
        data = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise LinearError(f"Invalid JSON from Linear API: {exc}") from exc

    errors_list = data.get("errors") or []
    if errors_list:
        first_error = errors_list[0]
        if isinstance(first_error, dict):
            message = first_error.get("message", "Linear GraphQL request failed")
        else:
            message = str(first_error)
        raise LinearError(message)

    return data.get("data") or {}


def _single_node(nodes: list[dict[str, Any]], entity_name: str, value: str) -> dict[str, Any]:
    if not nodes:
        raise LinearError(f"{entity_name} '{value}' not found")
    return nodes[0]


def resolve_team(team_key_or_name_or_id: str) -> dict[str, Any]:
    if is_uuid(team_key_or_name_or_id):
        return {"id": team_key_or_name_or_id, "key": None, "name": None}

    data = graphql_request(
        """
        query ResolveTeam($value: String!) {
          byKey: teams(filter: { key: { eq: $value } }, first: 2) {
            nodes { id key name }
          }
          byName: teams(filter: { name: { eq: $value } }, first: 2) {
            nodes { id key name }
          }
        }
        """,
        {"value": team_key_or_name_or_id},
    )

    nodes = []
    seen_ids: set[str] = set()
    for bucket in (data.get("byKey", {}), data.get("byName", {})):
        for node in bucket.get("nodes", []):
            node_id = node.get("id")
            if node_id and node_id not in seen_ids:
                seen_ids.add(node_id)
                nodes.append(node)

    return _single_node(nodes, "Team", team_key_or_name_or_id)


def resolve_project(project_name_or_id: str) -> dict[str, Any]:
    if is_uuid(project_name_or_id):
        return {"id": project_name_or_id, "name": None, "url": None}

    data = graphql_request(
        """
        query ResolveProject($value: String!) {
          projects(filter: { name: { eqIgnoreCase: $value } }, first: 2) {
            nodes { id name url }
          }
        }
        """,
        {"value": project_name_or_id},
    )
    return _single_node(data.get("projects", {}).get("nodes", []), "Project", project_name_or_id)


def resolve_label_ids(label_names_or_ids: list[str]) -> list[str]:
    label_ids: list[str] = []

    for label in label_names_or_ids:
        if not label:
            continue
        if is_uuid(label):
            label_ids.append(label)
            continue

        data = graphql_request(
            """
            query ResolveLabel($value: String!) {
              issueLabels(filter: { name: { eqIgnoreCase: $value } }, first: 2) {
                nodes { id name }
              }
            }
            """,
            {"value": label},
        )
        label_ids.append(
            _single_node(data.get("issueLabels", {}).get("nodes", []), "Label", label)["id"]
        )

    return label_ids


def resolve_user_id(user_name_or_email_or_id: str) -> str:
    if is_uuid(user_name_or_email_or_id):
        return user_name_or_email_or_id

    data = graphql_request(
        """
        query ResolveUser($value: String!) {
          byDisplayName: users(
            filter: { displayName: { eqIgnoreCase: $value } }
            first: 10
          ) {
            nodes { id name displayName email }
          }
          byEmail: users(filter: { email: { eqIgnoreCase: $value } }, first: 2) {
            nodes { id name displayName email }
          }
        }
        """,
        {"value": user_name_or_email_or_id},
    )

    by_name = data.get("byDisplayName", {}).get("nodes", [])
    if len(by_name) == 1:
        return by_name[0]["id"]
    if len(by_name) > 1:
        matches = ", ".join(
            sorted(
                {
                    f"{node.get('displayName') or node.get('name') or 'Unknown'} <{node.get('email', 'no-email')}>"
                    for node in by_name
                }
            )
        )
        raise LinearError(
            f"User '{user_name_or_email_or_id}' matched multiple users ({matches}). Use email or UUID to disambiguate."
        )

    by_email = data.get("byEmail", {}).get("nodes", [])
    if len(by_email) == 1:
        return by_email[0]["id"]

    raise LinearError(f"User '{user_name_or_email_or_id}' not found")


def resolve_workflow_state_ids(
    statuses: list[str], team_id: str | None = None
) -> list[str]:
    state_ids: list[str] = []

    for status in statuses:
        if not status:
            continue
        if is_uuid(status):
            state_ids.append(status)
            continue

        if team_id:
            query = """
            query ResolveWorkflowState($value: String!, $teamId: String!) {
              workflowStates(
                filter: {
                  name: { eqIgnoreCase: $value }
                  team: { id: { eq: $teamId } }
                }
                first: 2
              ) {
                nodes { id name }
              }
            }
            """
            variables = {"value": status, "teamId": team_id}
        else:
            query = """
            query ResolveWorkflowState($value: String!) {
              workflowStates(filter: { name: { eqIgnoreCase: $value } }, first: 2) {
                nodes { id name }
              }
            }
            """
            variables = {"value": status}

        data = graphql_request(query, variables)
        state_ids.append(
            _single_node(
                data.get("workflowStates", {}).get("nodes", []), "Status", status
            )["id"]
        )

    return state_ids


def resolve_issue(issue_id_or_identifier: str) -> dict[str, Any]:
    if is_uuid(issue_id_or_identifier):
        data = graphql_request(
            f"""
            query GetIssueById($id: String!) {{
              issue(id: $id) {{
                {ISSUE_DETAIL_FIELDS}
              }}
            }}
            """,
            {"id": issue_id_or_identifier},
        )
        issue = data.get("issue")
        if not issue:
            raise LinearError(f"Ticket {issue_id_or_identifier} not found")
        return issue

    parsed = parse_issue_identifier(issue_id_or_identifier)
    if not parsed:
        raise LinearError(
            f"'{issue_id_or_identifier}' is not a valid ticket identifier or UUID"
        )

    team_key, issue_number = parsed
    data = graphql_request(
        f"""
        query GetIssueByIdentifier($teamKey: String!, $number: Float!) {{
          issues(
            filter: {{ team: {{ key: {{ eq: $teamKey }} }}, number: {{ eq: $number }} }}
            first: 1
          ) {{
            nodes {{
              {ISSUE_DETAIL_FIELDS}
            }}
          }}
        }}
        """,
        {"teamKey": team_key, "number": issue_number},
    )
    nodes = data.get("issues", {}).get("nodes", [])
    return _single_node(nodes, "Ticket", issue_id_or_identifier)


def resolve_issue_id(issue_id_or_identifier: str) -> str:
    if is_uuid(issue_id_or_identifier):
        return issue_id_or_identifier
    return resolve_issue(issue_id_or_identifier)["id"]


def resolve_milestone_id(
    milestone_name_or_id: str,
    project_name_or_id: str | None = None,
) -> str:
    if is_uuid(milestone_name_or_id):
        return milestone_name_or_id

    if project_name_or_id:
        project = resolve_project(project_name_or_id)
        data = graphql_request(
            """
            query FindScopedMilestone($projectId: String!, $name: String!) {
              project(id: $projectId) {
                projectMilestones(filter: { name: { eq: $name } }, first: 10) {
                  nodes {
                    id
                    name
                    project { id name }
                  }
                }
              }
            }
            """,
            {"projectId": project["id"], "name": milestone_name_or_id},
        )
        scoped_nodes = data.get("project", {}).get("projectMilestones", {}).get("nodes", [])
        if scoped_nodes:
            return _single_node(scoped_nodes, "Milestone", milestone_name_or_id)["id"]

    data = graphql_request(
        """
        query FindGlobalMilestone($name: String!) {
          projectMilestones(filter: { name: { eq: $name } }, first: 10) {
            nodes {
              id
              name
              project { id name }
            }
          }
        }
        """,
        {"name": milestone_name_or_id},
    )
    nodes = data.get("projectMilestones", {}).get("nodes", [])
    if len(nodes) > 1:
        project_names = ", ".join(
            sorted(
                {
                    node.get("project", {}).get("name", "unknown project")
                    for node in nodes
                }
            )
        )
        raise LinearError(
            f"Milestone '{milestone_name_or_id}' matched multiple projects ({project_names}). Provide the milestone ID or scope it with --project."
        )
    return _single_node(nodes, "Milestone", milestone_name_or_id)["id"]


def build_issue_filter(
    *,
    team_id: str | None = None,
    project_id: str | None = None,
    assignee_id: str | None = None,
    state_ids: list[str] | None = None,
) -> dict[str, Any]:
    fragments: list[dict[str, Any]] = []

    if state_ids:
        fragments.append({"state": {"id": {"in": state_ids}}})
    else:
        fragments.append({"state": {"type": {"neq": "completed"}}})

    if team_id:
        fragments.append({"team": {"id": {"eq": team_id}}})
    if project_id:
        fragments.append({"project": {"id": {"eq": project_id}}})
    if assignee_id:
        fragments.append({"assignee": {"id": {"eq": assignee_id}}})

    if len(fragments) == 1:
        return fragments[0]
    return {"and": fragments}


def list_issues(
    *,
    team: str | None = None,
    limit: int = 50,
    status: str | None = None,
    project: str | None = None,
    assignee: str | None = None,
) -> list[dict[str, Any]]:
    team_id = resolve_team(team)["id"] if team else None
    project_id = resolve_project(project)["id"] if project else None
    assignee_id = resolve_user_id(assignee) if assignee else None
    state_ids = (
        resolve_workflow_state_ids([part.strip() for part in status.split(",")], team_id)
        if status
        else None
    )

    data = graphql_request(
        f"""
        query ListIssues($first: Int!, $filter: IssueFilter) {{
          issues(first: $first, filter: $filter, includeArchived: false) {{
            nodes {{
              {ISSUE_LIST_FIELDS}
            }}
          }}
        }}
        """,
        {
            "first": limit,
            "filter": build_issue_filter(
                team_id=team_id,
                project_id=project_id,
                assignee_id=assignee_id,
                state_ids=state_ids,
            ),
        },
    )

    return data.get("issues", {}).get("nodes", [])


def search_issues(
    term: str,
    *,
    team: str | None = None,
    status: str | None = None,
    project: str | None = None,
    assignee: str | None = None,
    limit: int = 25,
) -> list[dict[str, Any]]:
    team_id = resolve_team(team)["id"] if team else None
    project_id = resolve_project(project)["id"] if project else None
    assignee_id = resolve_user_id(assignee) if assignee else None
    state_ids = (
        resolve_workflow_state_ids([part.strip() for part in status.split(",")], team_id)
        if status
        else None
    )

    data = graphql_request(
        f"""
        query SearchIssues($term: String!, $first: Int!, $filter: IssueFilter) {{
          searchIssues(
            term: $term
            first: $first
            filter: $filter
            includeArchived: false
          ) {{
            nodes {{
              {ISSUE_LIST_FIELDS}
            }}
          }}
        }}
        """,
        {
            "term": term,
            "first": limit,
            "filter": build_issue_filter(
                team_id=team_id,
                project_id=project_id,
                assignee_id=assignee_id,
                state_ids=state_ids,
            ),
        },
    )

    return data.get("searchIssues", {}).get("nodes", [])


def create_ticket(
    title: str,
    team: str,
    *,
    description: str | None = None,
    priority: int | None = None,
    labels: str | None = None,
) -> dict[str, Any]:
    team_node = resolve_team(team)
    label_ids = resolve_label_ids([part.strip() for part in labels.split(",")]) if labels else None

    input_data: dict[str, Any] = {"title": title, "teamId": team_node["id"]}
    if description:
        input_data["description"] = description
    if priority is not None:
        input_data["priority"] = priority
    if label_ids:
        input_data["labelIds"] = label_ids

    data = graphql_request(
        f"""
        mutation CreateIssue($input: IssueCreateInput!) {{
          issueCreate(input: $input) {{
            success
            issue {{
              {ISSUE_DETAIL_FIELDS}
            }}
          }}
        }}
        """,
        {"input": input_data},
    )

    issue = data.get("issueCreate", {}).get("issue")
    if not issue:
        raise LinearError("Failed to create issue")
    return issue


def update_ticket(issue_id_or_identifier: str, updates: dict[str, Any]) -> dict[str, Any]:
    issue = resolve_issue(issue_id_or_identifier)
    issue_id = issue["id"]

    input_data: dict[str, Any] = {}

    if updates.get("status") is not None:
        state_ids = resolve_workflow_state_ids([updates["status"]], issue.get("team", {}).get("id"))
        input_data["stateId"] = state_ids[0]

    if updates.get("priority") is not None:
        input_data["priority"] = updates["priority"]

    if updates.get("assignee") is not None:
        input_data["assigneeId"] = resolve_user_id(updates["assignee"])

    if updates.get("project") is not None:
        input_data["projectId"] = resolve_project(updates["project"])["id"]

    if updates.get("project_milestone") is not None:
        milestone_scope = updates.get("project") or issue.get("project", {}).get("id") or issue.get("project", {}).get("name")
        input_data["projectMilestoneId"] = resolve_milestone_id(
            updates["project_milestone"],
            milestone_scope,
        )

    if updates.get("title") is not None:
        input_data["title"] = updates["title"]

    if updates.get("description") is not None:
        input_data["description"] = updates["description"]

    if updates.get("labels") is not None:
        new_label_ids = resolve_label_ids(
            [part.strip() for part in str(updates["labels"]).split(",") if part.strip()]
        )
        current_label_ids = [
            node["id"] for node in issue.get("labels", {}).get("nodes", []) if node.get("id")
        ]
        input_data["labelIds"] = sorted(set(current_label_ids + new_label_ids))

    data = graphql_request(
        f"""
        mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {{
          issueUpdate(id: $id, input: $input) {{
            success
            issue {{
              {ISSUE_DETAIL_FIELDS}
            }}
          }}
        }}
        """,
        {"id": issue_id, "input": input_data},
    )

    updated_issue = data.get("issueUpdate", {}).get("issue")
    if not updated_issue:
        raise LinearError("Failed to update issue")
    return updated_issue


def add_comment(issue_id_or_identifier: str, body: str) -> dict[str, Any]:
    issue = resolve_issue(issue_id_or_identifier)
    data = graphql_request(
        """
        mutation CreateComment($input: CommentCreateInput!) {
          commentCreate(input: $input) {
            success
            comment {
              id
            }
          }
        }
        """,
        {"input": {"issueId": issue["id"], "body": body}},
    )

    comment = data.get("commentCreate", {}).get("comment")
    if not comment:
        raise LinearError("Failed to create comment")

    return {
        "ticket": issue.get("identifier", issue_id_or_identifier),
        "commented": True,
        "commentId": comment.get("id", ""),
        "url": issue.get("url", ""),
    }


def create_project(
    name: str,
    team: str,
    *,
    description: str | None = None,
    content: str | None = None,
    priority: int | None = None,
    target_date: str | None = None,
) -> dict[str, Any]:
    team_node = resolve_team(team)
    input_data: dict[str, Any] = {"name": name, "teamIds": [team_node["id"]]}

    if description:
        if len(description) > 255:
            print(
                f"Warning: Description truncated to 255 chars (was {len(description)})",
                file=sys.stderr,
            )
            description = description[:252] + "..."
        input_data["description"] = description
    if priority is not None:
        input_data["priority"] = priority
    if target_date:
        input_data["targetDate"] = target_date

    data = graphql_request(
        """
        mutation CreateProject($input: ProjectCreateInput!) {
          projectCreate(input: $input) {
            success
            project {
              id
              name
              description
              content
              state
              url
            }
          }
        }
        """,
        {"input": input_data},
    )
    project_node = data.get("projectCreate", {}).get("project")
    if not project_node:
        raise LinearError("Failed to create project")

    if content:
        graphql_request(
            """
            mutation UpdateProject($id: String!, $input: ProjectUpdateInput!) {
              projectUpdate(id: $id, input: $input) {
                success
              }
            }
            """,
            {"id": project_node["id"], "input": {"content": content}},
        )
        project_node["content"] = content

    return project_node


def create_milestone(
    name: str,
    project_id: str,
    *,
    description: str | None = None,
    target_date: str | None = None,
) -> dict[str, Any]:
    input_data: dict[str, Any] = {"name": name, "projectId": project_id}
    if description:
        input_data["description"] = description
    if target_date:
        input_data["targetDate"] = target_date

    data = graphql_request(
        """
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
        """,
        {"input": input_data},
    )

    milestone = data.get("projectMilestoneCreate", {}).get("projectMilestone")
    if not milestone:
        raise LinearError("Failed to create milestone")
    return milestone


def set_issue_project(issue_id_or_identifier: str, project_id: str) -> bool:
    issue_id = resolve_issue_id(issue_id_or_identifier)
    data = graphql_request(
        """
        mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
          issueUpdate(id: $id, input: $input) {
            success
          }
        }
        """,
        {"id": issue_id, "input": {"projectId": project_id}},
    )
    return bool(data.get("issueUpdate", {}).get("success"))


def set_issue_milestone(issue_id_or_identifier: str, milestone_id: str) -> bool:
    issue_id = resolve_issue_id(issue_id_or_identifier)
    data = graphql_request(
        """
        mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
          issueUpdate(id: $id, input: $input) {
            success
          }
        }
        """,
        {"id": issue_id, "input": {"projectMilestoneId": milestone_id}},
    )
    return bool(data.get("issueUpdate", {}).get("success"))


def create_document(
    *,
    title: str,
    project: str,
    content: str | None = None,
) -> dict[str, Any]:
    project_node = resolve_project(project)
    input_data: dict[str, Any] = {
        "title": title,
        "projectId": project_node["id"],
    }
    if content:
        input_data["content"] = content

    data = graphql_request(
        f"""
        mutation CreateDocument($input: DocumentCreateInput!) {{
          documentCreate(input: $input) {{
            success
            document {{
              {DOCUMENT_FIELDS}
            }}
          }}
        }}
        """,
        {"input": input_data},
    )

    document = data.get("documentCreate", {}).get("document")
    if not document:
        raise LinearError("Failed to create document")

    document["project"] = project_node.get("name") or project
    return document


def list_documents(*, project: str | None = None, limit: int = 50) -> dict[str, Any]:
    filter_input = None
    if project:
        project_node = resolve_project(project)
        filter_input = {"project": {"id": {"eq": project_node["id"]}}}

    data = graphql_request(
        f"""
        query ListDocuments($first: Int!, $filter: DocumentFilter) {{
          documents(first: $first, filter: $filter) {{
            nodes {{
              {DOCUMENT_FIELDS}
            }}
            pageInfo {{
              hasNextPage
              endCursor
            }}
          }}
        }}
        """,
        {"first": limit, "filter": filter_input},
    )

    return data.get("documents", {"nodes": [], "pageInfo": {"hasNextPage": False, "endCursor": None}})


def read_document(document_id: str) -> dict[str, Any]:
    data = graphql_request(
        f"""
        query GetDocument($id: String!) {{
          document(id: $id) {{
            {DOCUMENT_FIELDS}
          }}
        }}
        """,
        {"id": document_id},
    )
    document = data.get("document")
    if not document:
        raise LinearError(f"Document {document_id} not found")
    return document
