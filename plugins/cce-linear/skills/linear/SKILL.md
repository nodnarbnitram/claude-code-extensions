---
name: linear
description: Manage Linear tickets, projects, milestones, and documents. Use for coordinating work across skills (orca-security, multi-repo) or tracking remediation progress.
license: MIT
compatibility: Requires linearis CLI and LINEAR_API_TOKEN.
metadata:
  author: security-cleanup
  version: "2.0"
---

# Linear Project & Ticket Management

Comprehensive skill for Linear operations including tickets, projects, milestones, and documents.

## Prerequisites

### Required: linearis CLI

```bash
npm install -g linearis
```

### Required: API Token

```bash
export LINEAR_API_TOKEN='lin_api_xxxxx'
```

Get token from: Linear → Settings → Security & Access → Personal API keys

### Verify Setup

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/read-ticket.py ICE-2041
```

If this returns ticket JSON, you're good to go.

## IMPORTANT: Use Scripts Only

**NEVER call the `linearis` CLI directly. Always use the wrapper scripts below.**

The scripts are in `${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/`. They handle CLI quirks, parse output, and give consistent JSON results. If you need raw CLI details for debugging, see `references/linearis-reference.md`.

## When to Use This Skill

- **Create tickets** for security issues or feature work
- **Create projects** to group related tickets with goals and timelines
- **Create milestones** to track project phases with due dates
- **Create documents** to attach reference material to projects
- **Track progress** by updating ticket status and adding comments

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `list-issues.py` | List issues for a team |
| `search-issues.py` | Search issues by query |
| `create-ticket.py` | Create a ticket |
| `read-ticket.py` | Read ticket details |
| `update-ticket.py` | Update ticket status |
| `add-comment.py` | Add comment to ticket |
| `create-project.py` | Create a project |
| `add-issues-to-project.py` | Add tickets to a project |
| `create-milestone.py` | Create a project milestone |
| `add-issues-to-milestone.py` | Add tickets to a milestone |
| `create-document.py` | Create a document attached to project |

---

## Ticket Operations

### List Issues

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/list-issues.py --team ICE-T
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/list-issues.py --team ICE-T --limit 100
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/list-issues.py --team ICE-T --status "Todo,In Progress"
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/list-issues.py --team ICE-T --project "Orca Security Remediation"
```

**Options:**
- `--team` - Filter by team key or name (e.g., `ICE-T`)
- `--limit`, `-l` - Max issues to fetch (default: 50)
- `--status`, `-s` - Filter by status (comma-separated, e.g., `Todo,In Progress`)
- `--project` - Filter by project name or ID

### Search Issues

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/search-issues.py "Orca Security"
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/search-issues.py "CVE" --team ICE-T
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/search-issues.py "Privileged Role" --status "Todo,Triage"
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/search-issues.py "Docker" --team ICE-T --limit 20
```

**Options:**
- `query` (required) - Search query string
- `--team` - Filter by team key or name
- `--status`, `-s` - Filter by status (comma-separated)
- `--project` - Filter by project name or ID
- `--assignee`, `-a` - Filter by assignee user ID
- `--limit`, `-l` - Max results (default: 25)

### Create Ticket

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/create-ticket.py "Fix CVE-2024-1234" \
  --team ICE-T \
  --description "Critical vulnerability in production" \
  --priority 1 \
  --labels "security" \
  --json
```

**Options:**
- `title` (required) - Ticket title
- `--team` (required) - Team key (e.g., `ICE-T`)
- `--description`, `-d` - Description
- `--priority`, `-p` - 1=urgent, 2=high, 3=normal, 4=low
- `--labels` - Comma-separated labels
- `--json` - Output full JSON

### Read Ticket

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/read-ticket.py ICE-2021
```

### Update Ticket

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/update-ticket.py ICE-2021 --status "In Progress"
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/update-ticket.py ICE-2021 --status "Done"
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/update-ticket.py ICE-2021 --status "Done" --priority 2
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/update-ticket.py ICE-2021 --labels "security,urgent"
```

**Options (at least one required):**
- `--status` - New status (e.g., `Triage`, `Todo`, `In Progress`, `In Review`, `Done`, `Canceled`)
- `--priority` - 1=urgent, 2=high, 3=normal, 4=low
- `--assignee` - User ID
- `--labels` - Comma-separated label names
- `--project` - Project name or ID
- `--project-milestone` - Milestone name or ID
- `--title` - New title
- `--description` - New description

### Add Comment

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/add-comment.py ICE-2021 "Fixed in PR #123"
```

---

## Project Operations

### Create Project

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/create-project.py "Security Remediation Q1" \
  --team ICE-T \
  --description "Eliminate all High severity alerts" \
  --priority 1 \
  --json
```

**Options:**
- `name` (required) - Project name
- `--team` (required) - Team key
- `--description` - Short summary (max 255 chars, shown in list views)
- `--content` - Full markdown content (shown on project page)
- `--priority` - 0=none, 1=urgent, 2=high, 3=normal, 4=low
- `--target-date` - Target date (YYYY-MM-DD)
- `--json` - Output full JSON

**Important:** Linear has two description fields:
- `description` - Short summary (255 char limit), shown in project lists
- `content` - Full markdown document, shown on project detail page

### Add Issues to Project

```bash
# Single issue
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/add-issues-to-project.py PROJECT_UUID ICE-2027

# Multiple issues
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/add-issues-to-project.py PROJECT_UUID ICE-2027 ICE-2028 ICE-2029

# Comma-separated
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/add-issues-to-project.py PROJECT_UUID --issues ICE-2027,ICE-2028
```

---

## Milestone Operations

### Create Milestone

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/create-milestone.py "P1: Critical Fixes" \
  --project PROJECT_UUID \
  --description "RCE and exposed secrets" \
  --target-date 2026-02-09 \
  --json
```

**Options:**
- `name` (required) - Milestone name
- `--project` (required) - Project name or UUID
- `--description` - Milestone description
- `--target-date` - Due date (YYYY-MM-DD)
- `--json` - Output full JSON

### Add Issues to Milestone

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/add-issues-to-milestone.py MILESTONE_UUID ICE-2027 ICE-2028
```

**Note:** linearis CLI does not support milestone operations. Use the scripts above or GraphQL API directly.

---

## Document Operations

### Create Document

```bash
# With inline content
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/create-document.py \
  --title "Security Findings Report" \
  --project PROJECT_UUID \
  --content "# Report\n\nDetails here..."

# From file
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/create-document.py \
  --title "Security Findings Report" \
  --project PROJECT_UUID \
  --content-file ./report.md \
  --json
```

**Options:**
- `--title` (required) - Document title
- `--project` (required) - Project name or UUID
- `--content` - Markdown content
- `--content-file` - Read content from file
### List/Read Documents

No wrapper script yet. Use the `linearis` CLI directly (see `references/linearis-reference.md`):

```bash
linearis documents list --project <project>
linearis documents read <document-id>
```

---

## Common Workflows

### Create Project with Milestones and Issues

```bash
# 1. Create project
PROJECT_ID=$(uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/create-project.py \
  "Security Remediation" \
  --team ICE-T \
  --description "Eliminate all security vulnerabilities")

# 2. Create milestones
P1_ID=$(uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/create-milestone.py \
  "P1: Critical" \
  --project $PROJECT_ID \
  --target-date 2026-02-09)

# 3. Create tickets
TICKET_ID=$(uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/create-ticket.py \
  "Patch CVE-2024-1234" \
  --team ICE-T \
  --priority 1)

# 4. Add tickets to project and milestone
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/add-issues-to-project.py $PROJECT_ID $TICKET_ID
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/add-issues-to-milestone.py $P1_ID $TICKET_ID

# 5. Attach documentation
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/create-document.py \
  --title "Findings Report" \
  --project $PROJECT_ID \
  --content-file ./report.md
```

### Batch Add Issues to Project

```bash
# Get project ID
PROJECT_ID="9e05263f-ed01-4b85-9c74-569fd1a0ce13"

# Add range of issues
uv run ${CLAUDE_PLUGIN_ROOT}/skills/linear/scripts/add-issues-to-project.py $PROJECT_ID \
  --issues ICE-2027,ICE-2028,ICE-2029,ICE-2030
```

---

## GraphQL API Reference

For operations not supported by linearis CLI, use the Linear GraphQL API directly.

### Authentication

```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_TOKEN" \
  -d '{"query": "{ viewer { id name } }"}'
```

**Note:** Do NOT use `Bearer` prefix - Linear uses the raw token.

### Create Project

```graphql
mutation CreateProject($input: ProjectCreateInput!) {
  projectCreate(input: $input) {
    success
    project { id name url }
  }
}
```

Variables:
```json
{
  "input": {
    "teamIds": ["team-uuid"],
    "name": "Project Name",
    "description": "Short description (max 255 chars)",
    "priority": 1
  }
}
```

### Update Project Content

```graphql
mutation UpdateProject($id: String!, $input: ProjectUpdateInput!) {
  projectUpdate(id: $id, input: $input) {
    success
  }
}
```

Variables:
```json
{
  "id": "project-uuid",
  "input": {
    "content": "# Full markdown content here"
  }
}
```

### Add Issue to Project

```graphql
mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
  issueUpdate(id: $id, input: $input) {
    success
  }
}
```

Variables:
```json
{
  "id": "issue-uuid",
  "input": {
    "projectId": "project-uuid"
  }
}
```

### Add Issue to Milestone

```json
{
  "id": "issue-uuid",
  "input": {
    "projectMilestoneId": "milestone-uuid"
  }
}
```

### Get Team ID

```graphql
{ teams { nodes { id name key } } }
```

### Get Issue UUID from Identifier

```graphql
{ issue(id: "ICE-2027") { id } }
```

---

## Known Limitations

- **Projects:** Create/update via `create-project.py` script (uses GraphQL under the hood)
- **Due dates:** Cannot be set on tickets — use Linear UI
- **Custom labels:** May not exist in workspace; use existing labels or create via UI
- **Description field:** Max 255 characters (use `content` for full text on projects)

---

## Error Handling

All scripts exit with code 1 on errors:

- **Missing token:** `Error: LINEAR_API_TOKEN not set and ~/.linear_api_token not found`
- **Ticket not found:** `Error: Ticket ICE-9999 not found`
- **Invalid team:** `Error: Team 'INVALID' not found`
- **linearis not installed:** `Error: linearis CLI not found. Install with: npm install -g linearis`

---

## Version

- **Skill version:** 2.0
- **linearis version:** latest
