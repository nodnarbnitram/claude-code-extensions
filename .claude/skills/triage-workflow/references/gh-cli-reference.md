# GitHub CLI Reference

Quick reference for branch and PR management.

## Authentication

```bash
gh auth login          # Interactive login
gh auth status         # Check current status
gh auth token          # Get current token
```

## Get GitHub Username

```bash
gh auth status --json hosts | jq -r '.hosts["github.com"].user'
```

## Create Pull Request

```bash
gh pr create \
  --title "ICE-1965: Fix authentication bug" \
  --body "Fixes ICE-1965

## Summary
- Fixed the bug

## Test Plan
- [ ] Tests pass" \
  --base main \
  --reviewer user1,user2 \
  --assignee @me \
  --label bug
```

### Options

| Flag | Description |
|------|-------------|
| `--title` | PR title |
| `--body` | PR description |
| `--base` | Target branch (default: repo default) |
| `--draft` | Create as draft |
| `--reviewer` | Request reviewers |
| `--assignee` | Assign users |
| `--label` | Add labels |
| `--fill` | Auto-fill from commits |
| `--web` | Open in browser |

## Linking Issues

Include in body to auto-close on merge:
- `Fixes #123`
- `Closes #123`
- `Fixes ICE-1965`

## Other Commands

```bash
# List PRs
gh pr list

# View PR
gh pr view 123 --web

# Checkout PR locally
gh pr checkout 123

# Check PR status
gh pr status
```

## Branch Workflow

```bash
# Create and push branch
git checkout -b username/ICE-1965
git push -u origin username/ICE-1965

# Create PR (will prompt to push if needed)
gh pr create --fill
```
