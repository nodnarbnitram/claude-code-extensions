---
name: linear
description: Manage Linear tickets, projects, milestones, and documents. Use for coordinating work across skills (orca-security, multi-repo) or tracking remediation progress.
license: MIT
compatibility: Requires LINEAR_API_TOKEN.
metadata:
  author: security-cleanup
  version: "3.0"
---

# Linear Project & Ticket Management

This skill manages Linear through the GraphQL endpoint only. Do not use `linearis` or any other CLI wrapper. The project scripts in `.claude/skills/linear/scripts/` share a single GraphQL client and hit `https://api.linear.app/graphql` directly.

## Prerequisites

### Required: API Token

```bash
export LINEAR_API_TOKEN='lin_api_xxxxx'
```

Get the token from Linear → Settings → Security & Access → Personal API keys.

### Verify Setup

```bash
uv run .claude/skills/linear/scripts/read-ticket.py ICE-2041
```

If this returns ticket JSON, auth and GraphQL access are working.

## IMPORTANT: Use Scripts First

Prefer the scripts in `.claude/skills/linear/scripts/` over ad hoc `curl` calls. They resolve names to IDs, normalize errors, and keep output JSON-shaped for agent workflows. If you need raw queries for debugging or unsupported operations, use `references/graphql-reference.md`.

## When to Use This Skill

- Create or update tickets for feature work, bugs, or remediation
- Create projects and milestones to organize work
- Add comments with progress or review notes
- Create, list, or read project documents
- Move issues into projects or milestones

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `list-issues.py` | List issues with optional team, status, and project filters |
| `search-issues.py` | Full-text search issues |
| `create-ticket.py` | Create a ticket |
| `read-ticket.py` | Read ticket details by identifier or UUID |
| `update-ticket.py` | Update ticket fields |
| `add-comment.py` | Add a comment to a ticket |
| `create-project.py` | Create a project |
| `add-issues-to-project.py` | Add tickets to a project |
| `create-milestone.py` | Create a project milestone |
| `add-issues-to-milestone.py` | Add tickets to a milestone |
| `create-document.py` | Create a project document |
| `list-documents.py` | List documents, optionally by project |
| `read-document.py` | Read a document by UUID |

---

## Ticket Operations

### List Issues

```bash
uv run .claude/skills/linear/scripts/list-issues.py --team ICE-T
uv run .claude/skills/linear/scripts/list-issues.py --team ICE-T --limit 100
uv run .claude/skills/linear/scripts/list-issues.py --team ICE-T --status "Todo,In Progress"
uv run .claude/skills/linear/scripts/list-issues.py --team ICE-T --project "Orca Security Remediation"
```

Options:
- `--team` filter by team key or name
- `--limit`, `-l` max issues to fetch, default `50`
- `--status`, `-s` comma-separated workflow states
- `--project` project name or UUID

### Search Issues

```bash
uv run .claude/skills/linear/scripts/search-issues.py "Orca Security"
uv run .claude/skills/linear/scripts/search-issues.py "CVE" --team ICE-T
uv run .claude/skills/linear/scripts/search-issues.py "Privileged Role" --status "Todo,Triage"
uv run .claude/skills/linear/scripts/search-issues.py "Docker" --team ICE-T --limit 20
```

Options:
- `query` required search text
- `--team` filter by team key or name
- `--status`, `-s` comma-separated workflow states
- `--project` project name or UUID
- `--assignee`, `-a` assignee user ID
- `--limit`, `-l` max results, default `25`

### Create Ticket

```bash
uv run .claude/skills/linear/scripts/create-ticket.py "Fix CVE-2024-1234" \
  --team ICE-T \
  --description "Critical vulnerability in production" \
  --priority 1 \
  --labels "security" \
  --json
```

Options:
- `title` required ticket title
- `--team` required team key or name
- `--description`, `-d` description
- `--priority`, `-p` `1=urgent`, `2=high`, `3=normal`, `4=low`
- `--labels` comma-separated label names or UUIDs
- `--json` print structured JSON instead of just the identifier

### Read Ticket

```bash
uv run .claude/skills/linear/scripts/read-ticket.py ICE-2021
uv run .claude/skills/linear/scripts/read-ticket.py 9e05263f-ed01-4b85-9c74-569fd1a0ce13
```

### Update Ticket

```bash
uv run .claude/skills/linear/scripts/update-ticket.py ICE-2021 --status "In Progress"
uv run .claude/skills/linear/scripts/update-ticket.py ICE-2021 --status "Done" --priority 2
uv run .claude/skills/linear/scripts/update-ticket.py ICE-2021 --labels "security,urgent"
```

Options, at least one required:
- `--status` new status name or UUID
- `--priority` `1=urgent`, `2=high`, `3=normal`, `4=low`
- `--assignee` assignee user ID
- `--labels` comma-separated label names or UUIDs; labels are added to the existing set
- `--project` project name or UUID
- `--project-milestone` milestone name or UUID
- `--title` new title
- `--description` new description

### Add Comment

```bash
uv run .claude/skills/linear/scripts/add-comment.py ICE-2021 "Fixed in PR #123"
```

---

## Project Operations

### Create Project

```bash
uv run .claude/skills/linear/scripts/create-project.py "Security Remediation Q1" \
  --team ICE-T \
  --description "Eliminate all High severity alerts" \
  --priority 1 \
  --json
```

Options:
- `name` required project name
- `--team` required team key or name
- `--description` short summary, max 255 chars
- `--content` full markdown content for the project page
- `--priority` `0=none`, `1=urgent`, `2=high`, `3=normal`, `4=low`
- `--target-date` `YYYY-MM-DD`
- `--json` print full project JSON

### Add Issues to Project

```bash
uv run .claude/skills/linear/scripts/add-issues-to-project.py PROJECT_UUID ICE-2027
uv run .claude/skills/linear/scripts/add-issues-to-project.py PROJECT_UUID ICE-2027 ICE-2028 ICE-2029
uv run .claude/skills/linear/scripts/add-issues-to-project.py PROJECT_UUID --issues ICE-2027,ICE-2028
```

---

## Milestone Operations

### Create Milestone

```bash
uv run .claude/skills/linear/scripts/create-milestone.py "P1: Critical Fixes" \
  --project PROJECT_UUID \
  --description "RCE and exposed secrets" \
  --target-date 2026-02-09 \
  --json
```

Options:
- `name` required milestone name
- `--project` required project UUID
- `--description` milestone description
- `--target-date` due date in `YYYY-MM-DD`
- `--json` print full milestone JSON

### Add Issues to Milestone

```bash
uv run .claude/skills/linear/scripts/add-issues-to-milestone.py MILESTONE_UUID ICE-2027 ICE-2028
```

---

## Document Operations

### Create Document

```bash
uv run .claude/skills/linear/scripts/create-document.py \
  --title "Security Findings Report" \
  --project PROJECT_UUID \
  --content-file ./report.md \
  --json
```

Options:
- `--title` required document title
- `--project` required project name or UUID
- `--content` markdown content
- `--content-file` read content from file
- `--json` print structured JSON

### List Documents

```bash
uv run .claude/skills/linear/scripts/list-documents.py --project PROJECT_UUID
uv run .claude/skills/linear/scripts/list-documents.py --project "Security Remediation" --limit 100
```

### Read Document

```bash
uv run .claude/skills/linear/scripts/read-document.py DOCUMENT_UUID
```

---

## Common Workflow

```bash
# 1. Create project
PROJECT_ID=$(uv run .claude/skills/linear/scripts/create-project.py \
  "Security Remediation" \
  --team ICE-T \
  --description "Eliminate all security vulnerabilities")

# 2. Create milestone
MILESTONE_ID=$(uv run .claude/skills/linear/scripts/create-milestone.py \
  "P1: Critical" \
  --project "$PROJECT_ID" \
  --target-date 2026-02-09)

# 3. Create ticket
TICKET_ID=$(uv run .claude/skills/linear/scripts/create-ticket.py \
  "Patch CVE-2024-1234" \
  --team ICE-T \
  --priority 1)

# 4. Link ticket into the plan
uv run .claude/skills/linear/scripts/add-issues-to-project.py "$PROJECT_ID" "$TICKET_ID"
uv run .claude/skills/linear/scripts/add-issues-to-milestone.py "$MILESTONE_ID" "$TICKET_ID"

# 5. Attach supporting documentation
uv run .claude/skills/linear/scripts/create-document.py \
  --title "Findings Report" \
  --project "$PROJECT_ID" \
  --content-file ./report.md
```

---

## Direct GraphQL Usage

If a needed operation does not have a wrapper yet, call the GraphQL endpoint directly rather than introducing a CLI dependency.

```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_TOKEN" \
  -d '{"query":"{ viewer { id name } }"}'
```

Do not use a `Bearer` prefix. Linear expects the raw token.

For reusable queries and resolver examples, see `references/graphql-reference.md`.

---

## Known Limitations

- Due dates are not handled by the current project wrappers; use the UI if you need fields not exposed here
- Labels must already exist in the workspace
- Project `description` is capped at 255 characters; use `content` for long-form project docs

---

## Error Handling

All scripts exit with code `1` on errors.

Common failures:
- `Error: LINEAR_API_TOKEN not set and ~/.linear_api_token not found`
- `Error: Ticket ICE-9999 not found`
- `Error: Team 'INVALID' not found`
- `Error: Milestone 'Release 1' matched multiple projects (...)`

---

## Version

- Skill version: `3.0`
- Transport: `Linear GraphQL endpoint only`
