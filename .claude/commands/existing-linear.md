---
description: Create a PR for an existing Linear ticket (for additional related changes)
argument-hint: <ticket-id> [--skip-validation]
allowed-tools: Bash(linearis issues read:*), Bash(git checkout:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git branch:*), Bash(gh pr create:*), Bash(rm:*)
---

# Existing Linear PR Workflow

Create a new PR for an existing Linear ticket when additional related code changes are required.

## Context

- Current git status: !`git status --short`
- Current branch: !`git branch --show-current`
- Staged changes: !`git diff --cached --stat`
- Unstaged changes: !`git diff --stat`

## Arguments

- `$1` - Linear ticket identifier (e.g., `ICE-2004`)
- `--skip-validation` - Optional flag in `$ARGUMENTS` to skip success criteria validation

If ticket ID is missing, ask the user for it.

## Prerequisites

- Changes should already be made to files (staged or unstaged)
- `linearis` CLI must be configured
- `gh` CLI must be authenticated

## Steps

Track these steps as TODOs and complete them one by one.

1. **Parse arguments** - Extract ticket ID (`$1`) and check for `--skip-validation` in `$ARGUMENTS`.

2. **Read Linear ticket** - Fetch ticket details:
   ```bash
   linearis issues read $1
   ```
   - Extract: `identifier`, `title`, `description`, `branchName`, `state`
   - If ticket not found, stop and inform the user.

3. **Validate success criteria** (skip if `--skip-validation` is present)
   - Present the ticket details:
     ```
     ## Ticket: <identifier>
     **Title:** <title>
     **Status:** <state.name>

     **Description:**
     <description>
     ```
   - Ask: "Does this match the work you're committing? (yes/no)"
   - If no, ask for clarification and document for PR description.

4. **Review changes** - Analyze the context above.
   - If no changes exist, stop and inform the user.
   - Summarize what will be committed.

5. **Create or checkout branch** - Use the Linear branch name:
   ```bash
   git checkout -b <branchName>
   ```
   - If branch exists locally: `git checkout <branchName>`
   - If already on correct branch, continue.

6. **Stage and commit** - Commit with ticket ID prefix:
   ```bash
   git add <relevant files>
   git commit -m "$(cat <<'EOF'
   <TICKET-ID>: <brief description derived from changes>

   <detailed description>

   Part of: <ticket title from Linear>
   EOF
   )"
   ```
   - Derive a concise commit title from the changes being committed.
   - Commit message describes THIS specific change, not the full ticket.

7. **Push branch** - Push to origin:
   ```bash
   git push -u origin <branch-name>
   ```
   - If remote branch exists: `git push`

8. **Create PR** - Open pull request:
   ```bash
   gh pr create --title "<TICKET-ID>: <brief description derived from changes>" --body "$(cat <<'EOF'
   ## Summary
   <what this specific PR adds/changes>

   ## Context
   Additional changes for [<TICKET-ID>](https://linear.app/axios-hq/issue/<TICKET-ID>): <ticket title from Linear>

   ## Test Plan
   - [ ] <verification steps>

   Linear: <TICKET-ID>
   EOF
   )"
   ```

9. **Output summary** - Display results:
   ```
   | Item | Details |
   |------|---------|
   | **Linear Ticket** | [<TICKET-ID>](https://linear.app/axios-hq/issue/<TICKET-ID>) |
   | **Branch** | `<branch-name>` |
   | **PR** | <PR URL> |
   | **Note** | Additional PR for existing ticket |
   ```

## Error Handling

- If `git add` fails due to lock file, run `rm -f .git/index.lock` and retry.
- If no changes to commit, stop and inform the user.
- If ticket doesn't exist, stop and inform the user.

## Examples

```bash
# With validation (default)
/existing-linear ICE-2004

# Skip validation
/existing-linear ICE-2004 --skip-validation
```
