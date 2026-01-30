# CCE Core Plugin

Essential Claude Code extensions providing core agents, hooks, commands, and universal tools.

## Overview

The **cce-core** plugin is the foundational plugin that provides essential automation, safety hooks, and universal development agents. **Everyone should install this plugin** as it contains the core functionality needed for safe and productive Claude Code usage.

## Features

- **8 Lifecycle Hooks**: Safety guards, logging, context loading, and automation
- **13 Core Agents**: Code reviewers, orchestrators, meta-agents, and universal specialists
- **8 Slash Commands**: Git workflows, project analysis, security scanning, and more
- **2 Essential Skills**: Commit message generation and code review automation

## Plugin Components

### Agents (13)

**Core Agents:**
- `code-archaeologist`: Explore unfamiliar/legacy codebases
- `code-reviewer`: Rigorous security-aware code review
- `documentation-specialist`: Project documentation creation
- `performance-optimizer`: Performance analysis and optimization

**Orchestrators:**
- `tech-lead-orchestrator`: Strategic project planning
- `project-analyst`: Codebase analysis and tech stack detection
- `team-configurator`: AI team setup for projects

**Universal Agents:**
- `api-architect`: RESTful/GraphQL API design
- `frontend-developer`: Framework-agnostic UI development
- `backend-developer`: Server-side development across stacks
- `tailwind-frontend-expert`: Tailwind CSS styling
- `fact-checker`: Verification and accuracy validation
- `meta-agent`: Generate new Claude Code agents

### Skills (2)

- `commit-helper`: Smart commit message generation
- `code-reviewer`: Automated code quality checks

### Commands (8)

- `/cce:git-commit`: Intelligent git commit workflow
- `/cce:git-status`: Repository state analysis
- `/cce:prime`: Load project context
- `/cce:agent-from-docs`: Create agents from documentation URLs
- `/cce:agent-intent-from-docs`: Create specialized agents with specific intent
- `/cce:security-scan`: Run security scans on code
- `/cce:wrapup-skillup`: Generate session learning reports
- `/cce:frontend-mode`: Load frontend development rules

### Hooks (8 Lifecycle Events)

- **PreToolUse**: Block dangerous commands, prevent .env commits
- **PostToolUse**: Log tool executions
- **SessionStart**: Load project context
- **UserPromptSubmit**: Mandatory skill activation
- **Stop**: Session cleanup
- **SubagentStop**: Subagent completion tracking
- **PreCompact**: Context compaction logging
- **Notification**: System notifications

## Installation

### From Marketplace (Recommended)

```bash
# Add the CCE marketplace
/plugin marketplace add github:nodnarbnitram/claude-code-extensions

# Install core plugin
/plugin install cce-core@cce-marketplace
```

### From Local Source

```bash
git clone https://github.com/nodnarbnitram/claude-code-extensions.git
/plugin marketplace add /path/to/claude-code-extensions
/plugin install cce-core@cce-marketplace
```

## Usage

### Commands (Namespaced)

```bash
/cce:git-commit           # Smart commit with conventional format
/cce:prime               # Load project context and structure
/cce:security-scan       # Scan for security vulnerabilities
```

### Agents (Automatic Activation)

```bash
> Review this code for security issues
# Automatically uses code-reviewer agent

> Create an agent for working with GraphQL
# Automatically uses meta-agent

> Optimize the slow database queries
# Automatically uses performance-optimizer
```

## Requirements

- **Claude Code**: Latest version
- **Python**: 3.11+ (for hooks)
- **uv**: Python package manager (for hook dependencies)

## Safety Features

The core plugin includes critical safety hooks:

✅ **Blocks dangerous rm commands**
✅ **Prevents .env file commits**
✅ **Logs all tool executions**
✅ **Validates security-sensitive operations**

## License

MIT License - see [LICENSE](../../../LICENSE) for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/nodnarbnitram/claude-code-extensions/issues)
- **Documentation**: [Repository README](../../../README.md)
