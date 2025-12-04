---
description: Start SOC II triage workflow (Linear ticket → branch → OpenSpec → commit → PR)
argument-hint: <issue-description> [--team <team-id>]
allowed-tools: AskUserQuestion, Skill
---

# SOC II Triage Workflow

You are initiating a triage workflow. Your job is to gather information and then activate the `triage-workflow` skill.

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

Once you have all the information, invoke the **triage-workflow** skill by stating:

> "Starting triage workflow for: [issue description] in team [team]"

This will trigger the skill which handles:
1. Creating the Linear ticket
2. Creating the branch
3. Running `/openspec:proposal`
4. Validating with user
5. Running `/openspec:apply`
6. Committing with `/git-commit`
7. Optionally pushing and creating PR

## Example Usage

```
/triage Users can't log in with SSO
/triage Add dark mode support --team IAI
/triage Fix payment timeout --team ICE
```
