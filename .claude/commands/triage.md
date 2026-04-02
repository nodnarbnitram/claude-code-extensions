---
description: Start a Linear-backed triage workflow for a new issue
argument-hint: <issue-description> [--team <team-id>]
allowed-tools: AskUserQuestion, Skill
---

# Linear Triage Workflow

You are initiating a triage workflow. Your job is to gather information and then activate the `linear` skill.

## Input Provided

**Arguments:** $ARGUMENTS

## Step 1: Parse Arguments

Check if arguments include:
- Issue description (required)
- Team identifier (optional, e.g., `--team IAI`)

If no team is specified, default to **IAI**.

## Step 2: Gather Missing Information

If the issue description is unclear or missing details, use **AskUserQuestion** to clarify:

- What is the issue or feature being triaged?
- What is the priority? (1=urgent, 2=high, 3=medium, 4=low)
- Any specific labels to apply?

## Step 3: Confirm Details

Before proceeding, confirm with the user:

**Issue:** [parsed description]
**Team:** [team identifier]
**Priority:** [if specified]

## Step 4: Activate Skill

Once you have all the information, invoke the **linear** skill and tell it to create a ticket using the wrapper scripts.

> "Use the linear skill to create a Linear ticket for: [issue description] in team [team], with priority [priority] and labels [labels if any]."

The linear skill should be the source of truth for ticket creation and ticket lookup. After ticket creation, the agent can continue with branch, proposal, commit, and PR workflows as needed.

## Example Usage

```
/triage Users can't log in with SSO
/triage Add dark mode support --team IAI
/triage Fix payment timeout --team ICE
```
