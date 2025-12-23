---
allowed-tools: Bash, Read
description: Load context for a new agent session by analyzing codebase structure, documentation and README
---

# Prime

Run the commands under the `Execute` section to gather information about the project, and then review *ALL* the files listed under `Read` to understand the project's purpose and functionality then `Report` your findings.

## Execute
- `git ls-files`

## Read (ALL OF THEM ARE IMPORTANT CONTEXT)
- @README.md
- @./docs/claude-code/hooks.md
- @./docs/uv-scripts.md
- @./docs/claude-code/commands-reference.md
- @./docs/claude-code/sub-agents.md
- @./docs/claude-code/plugins.md
- @./docs/claude-code/agent-skills.md

## Report

- Provide a summary of your understanding of the project
