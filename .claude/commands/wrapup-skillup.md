---
allowed-tools: Read, Write, Bash(git log:*), Bash(git diff:*)
argument-hint: [topic-slug]
description: Generate session report capturing learnings, tools, pitfalls, and extension recommendations
---

# Session Wrapup & Skillup

Generate a session report for topic: $ARGUMENTS

## Your Task

Analyze this conversation session and create a comprehensive report that captures learnings, documents pitfalls, and recommends extensions that could help in future similar sessions.

## Instructions

1. **Analyze the session context** - Review the entire conversation from start to finish
2. **Extract the original request** - Identify the first user message that started this session
3. **Summarize tool usage** - Document which tools were used, how, and why
4. **Identify key learnings** - What discoveries, patterns, or insights emerged?
5. **Document pitfalls** - What problems were encountered? How were they resolved?
6. **Note outcomes** - What was accomplished?
7. **Find ticket references** - Look for any Linear, GitHub, or other ticket IDs mentioned
8. **Recommend extensions** - Based on the session, suggest which extension types would be most valuable

## Output Format

Write the report to: `.claude/session-reports/YYYY-MM-DD-HH-MM-{topic}.md`

Where `{topic}` is the topic-slug argument (use "session" if not provided).

Use this template structure:

```markdown
# Session Report: {Topic Title}

## Metadata
- **Date**: YYYY-MM-DD HH:MM
- **Duration**: ~X minutes (estimate based on conversation length)
- **Related Tickets**: [ticket-ids or "None"]

## Original Request

> [Quote the first user message that initiated this session]

## Tools Used

| Tool | Purpose | Key Usage |
|------|---------|-----------|
| Tool1 | Why it was used | How it was applied |
| Tool2 | Why it was used | How it was applied |

## Key Learnings

- **Learning 1**: Description of what was discovered
- **Learning 2**: Description of pattern identified
- **Learning 3**: Description of insight gained

## Pitfalls & Solutions

### Pitfall: [Issue Name]
- **Problem**: What went wrong or was difficult
- **Solution**: How it was resolved
- **Prevention**: How to avoid this in the future

### Pitfall: [Another Issue]
- **Problem**: Description
- **Solution**: Resolution
- **Prevention**: Future avoidance strategy

## Results & Outcomes

- **Outcome 1**: What was accomplished
- **Outcome 2**: What was delivered
- **Files Changed**: List key files created or modified

## Extension Recommendations

Based on this session, the following extensions would help in similar future work:

### Recommended: [Skill/Command/Hook/Agent]

**Name**: `suggested-name`

**Purpose**: Why this extension would be valuable

**Type Justification**: Why this type (skill vs command vs hook vs agent) is appropriate

**Template**:
```yaml
---
name: suggested-name
description: Description for discovery
---

# Extension content template
```
```

## Extension Type Selection Guide

When recommending extensions, use these criteria:

### Skill (Model-invoked, automatic)
- Workflows Claude should auto-discover based on context
- Reusable expertise that applies to many situations
- Complex multi-step processes
- Example: PDF processing, code review checklists

### Command (User-invoked, explicit)
- Operations user explicitly triggers with `/command`
- Quick actions with specific parameters
- Tasks user wants control over when to run
- Example: `/git-commit`, `/security-scan`

### Hook (Lifecycle automation)
- Actions that must happen deterministically
- Safety checks, logging, formatting
- Response to specific tool calls or events
- Example: Auto-lint on file save, block dangerous commands

### Agent (Specialized expertise)
- Deep domain expertise with isolated context
- Complex problem-solving in specific area
- Tasks requiring specialized knowledge
- Example: Django expert, Temporal troubleshooter

## Guidelines

1. **Be specific** - Use concrete examples from the session
2. **Be actionable** - Extension recommendations should be ready to implement
3. **Be honest** - Document real pitfalls, not just successes
4. **Be concise** - Keep each section focused and scannable
5. **Prioritize** - If multiple extensions recommended, order by impact

## After Writing the Report

1. Confirm the file was written successfully
2. Summarize key findings to the user
3. Highlight the most impactful extension recommendation
4. Ask if they want help creating any recommended extensions
