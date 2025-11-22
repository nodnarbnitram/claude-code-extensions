# Linearis CLI Reference

Quick reference for Linear ticket management via CLI.

## Authentication

```bash
# Option 1: Environment variable
export LINEAR_API_TOKEN=<your-token>

# Option 2: Token file (recommended)
echo "<your-token>" > ~/.linear_api_token
```

Get token from: Linear → Settings → Security & Access → Personal API keys

## Create Issue

```bash
linearis issues create "Title" \
  --team Backend \
  --description "Description" \
  --priority 2 \
  --labels "Bug,Critical" \
  --project "Project Name" \
  --assignee user-id
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<title>` | Yes | Issue title |
| `--team` | Yes | Team key/name/ID |
| `--description` | No | Issue description |
| `--priority` | No | 1=urgent, 2=high, 3=medium, 4=low |
| `--labels` | No | Comma-separated label names |
| `--project` | No | Project name/ID |
| `--assignee` | No | User ID |

### Response

Returns JSON with `identifier` field (e.g., `ICE-1965`):

```json
{
  "id": "uuid",
  "identifier": "ICE-1965",
  "title": "Issue Title",
  "state": { "name": "Backlog" },
  "team": { "key": "ICE" }
}
```

## Other Commands

```bash
# List issues
linearis issues list -l 10

# Search issues
linearis issues search "query" --team Platform

# Read issue details
linearis issues read ICE-1965

# Update issue
linearis issues update ICE-1965 --state "In Review"

# Add comment
linearis comments create ICE-1965 --body "Comment text"
```

## Extract Identifier

```bash
# Using jq
linearis issues create "Title" --team Backend | jq -r '.identifier'
```
