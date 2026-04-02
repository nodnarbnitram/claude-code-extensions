# Linearis CLI Reference

Complete reference for the `linearis` CLI. Generated from `linearis usage` output.

**IMPORTANT:** Prefer using wrapper scripts in `.claude/skills/linear/scripts/` over calling linearis directly. The scripts handle edge cases and output parsing.

## Authentication

```bash
export LINEAR_API_TOKEN=<your-token>
```

Get token from: Linear → Settings → Security & Access → Personal API keys

---

## Issues

### Read Issue

```bash
linearis issues read <issueId>
```

Accepts UUID or identifiers like `ICE-2041`.

### Create Issue

```bash
linearis issues create <title> [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `<title>` | | Yes | Issue title (positional) |
| `--team <team>` | | Yes | Team key, name, or ID |
| `--description <desc>` | `-d` | No | Issue description |
| `--priority <priority>` | `-p` | No | 1=urgent, 2=high, 3=medium, 4=low |
| `--labels <labels>` | | No | Comma-separated label names or IDs |
| `--project <project>` | | No | Project name or ID |
| `--status <status>` | | No | Status name or ID |
| `--assignee <assigneeId>` | `-a` | No | Assign to user ID |
| `--project-milestone <milestone>` | | No | Milestone name or ID (requires --project) |
| `--cycle <cycle>` | | No | Cycle name or ID (requires --team) |
| `--parent-ticket <parentId>` | | No | Parent issue ID or identifier |

### Update Issue

```bash
linearis issues update <issueId> [options]
```

| Option | Short | Description |
|--------|-------|-------------|
| `--status <status>` | `-s` | New status name or ID |
| `--title <title>` | `-t` | New title |
| `--description <desc>` | `-d` | New description |
| `--priority <priority>` | `-p` | New priority (1-4) |
| `--assignee <assigneeId>` | | New assignee ID |
| `--project <project>` | | New project (name or ID) |
| `--labels <labels>` | | Labels (comma-separated names or IDs) |
| `--label-by <mode>` | | How to apply labels: `adding` (default) or `overwriting` |
| `--clear-labels` | | Remove all labels |
| `--parent-ticket <parentId>` | | Set parent issue ID or identifier |
| `--clear-parent-ticket` | | Clear parent relationship |
| `--project-milestone <milestone>` | | Set milestone (name or ID) |
| `--clear-project-milestone` | | Clear milestone |
| `--cycle <cycle>` | | Set cycle (name or ID) |
| `--clear-cycle` | | Clear cycle |

**Common status values:** `Triage`, `Todo`, `In Progress`, `In Review`, `Done`, `Canceled`

### Search Issues

```bash
linearis issues search <query> [options]
```

| Option | Description |
|--------|-------------|
| `--team <team>` | Filter by team key, name, or ID |
| `--assignee <assigneeId>` | Filter by assignee ID |
| `--project <project>` | Filter by project name or ID |
| `--status <status>` | Filter by status (comma-separated) |
| `--limit <number>` | Limit results (default: 10) |

### List Issues

```bash
linearis issues list [options]
```

| Option | Short | Description |
|--------|-------|-------------|
| `--limit <number>` | `-l` | Limit results (default: 25) |

---

## Comments

### Create Comment

```bash
linearis comments create <issueId> --body <body>
```

| Option | Required | Description |
|--------|----------|-------------|
| `<issueId>` | Yes | Issue ID or identifier (positional) |
| `--body <body>` | Yes | Comment body text |

**WARNING:** There is NO `-b` shorthand. You MUST use `--body`.

---

## Projects

```bash
linearis projects list [--limit <number>]
```

**Note:** linearis only supports listing projects. Use GraphQL API or wrapper scripts for create/update.

---

## Project Milestones

### Create Milestone

```bash
linearis project-milestones create <name> [options]
```

| Option | Short | Description |
|--------|-------|-------------|
| `--project <project>` | | Project name or ID |
| `--description <desc>` | `-d` | Milestone description |
| `--target-date <date>` | | Target date (YYYY-MM-DD) |

### List Milestones

```bash
linearis project-milestones list --project <project> [--limit <number>]
```

### Read Milestone

```bash
linearis project-milestones read <milestoneIdOrName> [--project <project>] [--issues-first <n>]
```

### Update Milestone

```bash
linearis project-milestones update <milestoneIdOrName> [options]
```

| Option | Short | Description |
|--------|-------|-------------|
| `--project <project>` | | Project scope for name lookup |
| `--name <name>` | `-n` | New name |
| `--description <desc>` | `-d` | New description |
| `--target-date <date>` | | New target date (YYYY-MM-DD) |
| `--sort-order <number>` | | New sort order |

---

## Documents

### Create Document

```bash
linearis documents create [options]
```

| Option | Description |
|--------|-------------|
| `--title <title>` | Document title |
| `--content <content>` | Markdown content |
| `--project <project>` | Project name or ID |
| `--team <team>` | Team key or name |
| `--icon <icon>` | Document icon |
| `--color <color>` | Icon color |
| `--attach-to <issue>` | Attach document to issue (e.g., `ICE-2041`) |

### List Documents

```bash
linearis documents list [--project <project>] [--issue <issue>] [--limit <limit>]
```

### Read Document

```bash
linearis documents read <documentId>
```

### Update Document

```bash
linearis documents update <documentId> [--title <title>] [--content <content>] [--project <project>]
```

### Delete Document

```bash
linearis documents delete <documentId>
```

---

## Cycles

```bash
linearis cycles list [--team <team>] [--active] [--around-active <n>]
linearis cycles read <cycleIdOrName> [--team <team>] [--issues-first <n>]
```

---

## Teams, Users & Labels

```bash
linearis teams list
linearis users list [--active]
linearis labels list [--team <team>]
```

---

## Embeds (File Upload/Download)

```bash
linearis embeds upload <file>
linearis embeds download <url> [--output <path>] [--overwrite]
```

---

## GraphQL API (for unsupported operations)

### Create Project

```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_TOKEN" \
  -d '{
    "query": "mutation($input: ProjectCreateInput!) { projectCreate(input: $input) { success project { id name url } } }",
    "variables": {
      "input": {
        "teamIds": ["team-uuid"],
        "name": "Project Name",
        "description": "Short description"
      }
    }
  }'
```

### Update Project Content

```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_TOKEN" \
  -d '{
    "query": "mutation($id: String!, $input: ProjectUpdateInput!) { projectUpdate(id: $id, input: $input) { success } }",
    "variables": {
      "id": "project-uuid",
      "input": { "content": "# Markdown content" }
    }
  }'
```

### Add Issue to Project / Milestone

```bash
curl -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_TOKEN" \
  -d '{
    "query": "mutation($id: String!, $input: IssueUpdateInput!) { issueUpdate(id: $id, input: $input) { success } }",
    "variables": {
      "id": "issue-uuid",
      "input": { "projectId": "project-uuid", "projectMilestoneId": "milestone-uuid" }
    }
  }'
```

**Important:** Do NOT use `Bearer` prefix with Linear API token.

---

## Known Limitations

| Feature | CLI Support | Workaround |
|---------|-------------|------------|
| Create project | No | Use GraphQL API |
| Update project | No | Use GraphQL API |
| Set due dates | No | Use Linear UI |
| Custom labels | Partial | Use existing labels |

---

## Common Mistakes

| Wrong | Right | Why |
|-------|-------|-----|
| `linearis ticket get ICE-2041` | `linearis issues read ICE-2041` | No `ticket` command; subcommand is `read` not `get` |
| `linearis issues update ... --state` | `linearis issues update ... --status` | Flag is `--status` or `-s` |
| `linearis comments create ... -b` | `linearis comments create ... --body` | No `-b` shorthand exists |
