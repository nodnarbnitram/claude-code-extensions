# Claude Code Extensions

A comprehensive collection of agents, hooks, commands, and output styles for extending [Claude Code](https://claude.ai/code).

## What's Inside

This repository provides production-ready extensions for Claude Code:

- **Agents**: Specialized AI assistants with separate context for specific tasks
- **Hooks**: Lifecycle automation scripts for safety, logging, and workflow control
- **Commands**: Reusable slash commands for common workflows
- **Output Styles**: Custom system prompts to change Claude Code's behavior

## Quick Start

### Using These Extensions

1. **Clone this repository**:
   ```bash
   git clone <repo-url>
   cd platform-claude-code
   ```

2. **Copy extensions to your project**:
   ```bash
   # Copy specific agents
   cp .claude/agents/core/code-reviewer.md ~/my-project/.claude/agents/

   # Copy hooks
   cp -r .claude/hooks ~/my-project/.claude/

   # Copy settings configuration
   cp .claude/settings.json ~/my-project/.claude/
   ```

3. **Or use as a template**: Fork this repo and customize for your needs.

### Creating New Extensions

This repository is also a **working environment** for creating new extensions:

#### Creating Agents

Use the meta-agent to generate new agents:

```
> Use the meta-agent to create a test automation specialist agent
```

The meta-agent will:
- Fetch latest Claude Code documentation
- Generate a complete agent definition
- Write the file to `.claude/agents/`

#### Creating Hooks

See the Python templates in `.claude/hooks/` and the [CLAUDE.md](./CLAUDE.md) guide.

#### Creating Commands

Create markdown files in `.claude/commands/`:

```markdown
---
description: Your command description
argument-hint: [arg1] [arg2]
---

Your command prompt using $1, $2, or $ARGUMENTS
```

#### Creating Output Styles

Create markdown files in `.claude/output-styles/`:

```markdown
---
name: Style Name
description: What this style does
---

Your custom system prompt
```

## Featured Extensions

### Agents

- **meta-agent**: Generates new agents from descriptions (uses Opus model)
- **code-reviewer**: Security-aware code review with severity ratings
- **code-archaeologist**: Legacy codebase exploration
- **performance-optimizer**: Performance analysis and optimization
- **tech-lead-orchestrator**: Coordinates complex multi-agent workflows

Plus specialized agents for React, Django, Vue, AI/ML, and more in `.claude/agents/specialized/`.

### Hooks

All hooks use Python with `uv run --script` for dependency management:

- **PreToolUse**: Blocks dangerous commands (rm -rf), prevents .env access
- **PostToolUse**: Logs all tool executions; includes lint checking on Edit/Write operations
- **SessionStart**: Injects git status and project context
- **UserPromptSubmit**: Logs prompts and can validate/block them

The **lint hook** (PostToolUse) automatically runs language-specific linters after file edits:
- **Python**: `ruff check` (if installed)
- **Go**: `golangci-lint run` (if installed)
- **JS/TS**: `biome check` or `prettier --check` (if installed)

Utilities in `.claude/hooks/utils/`:
- LLM integrations (OpenAI, Anthropic, Ollama)
- TTS implementations (pyttsx3, OpenAI, ElevenLabs)

### Safety Features

The `pre_tool_use.py` hook includes:
- **Dangerous command blocking**: Prevents destructive `rm -rf` operations (ENABLED)
- **.env file protection**: Blocks access to sensitive environment files (ENABLED)
- **Audit logging**: All tool calls logged to `logs/`

## Documentation

- **[CLAUDE.md](./CLAUDE.md)**: Complete guide for creating extensions
- **[docs/claude-code/](./docs/claude-code/)**: Official Claude Code documentation
  - [sub-agents.md](./docs/claude-code/sub-agents.md)
  - [hooks.md](./docs/claude-code/hooks.md)
  - [hooks-reference.md](./docs/claude-code/hooks-reference.md)
  - [commands-reference.md](./docs/claude-code/commands-reference.md)
  - [output-styles.md](./docs/claude-code/output-styles.md)

## Requirements

- [Claude Code](https://claude.ai/code) CLI
- [uv](https://github.com/astral-sh/uv) (for Python hooks)
- Python 3.11+ (for hooks)

## Project Structure

```
.claude/
├── settings.json          # Hook configuration
├── agents/                # Agent definitions
│   ├── core/             # Quality/analysis agents
│   ├── orchestrators/    # Coordination agents
│   ├── universal/        # Framework-agnostic agents
│   └── specialized/      # Framework-specific agents
├── hooks/                # Lifecycle automation
│   └── utils/           # Shared utilities
└── commands/            # Slash commands (create as needed)

docs/claude-code/        # Official documentation
logs/                    # Runtime logs (generated)
```

## Usage Examples

### Using the Code Reviewer

The code reviewer agent automatically reviews changes:

```bash
# Make code changes
git add .

# Ask Claude to review
> Review my recent changes
```

### Custom Notifications

The notification hook can be configured for desktop alerts:

```json
{
  "hooks": {
    "Notification": [{
      "hooks": [{
        "type": "command",
        "command": "notify-send 'Claude Code' 'Ready for input'"
      }]
    }]
  }
}
```

### Testing Hooks

```bash
# Create test input
echo '{"tool_name": "Bash", "tool_input": {"command": "ls"}}' > test.json

# Test hook
uv run ./.claude/hooks/pre_tool_use.py < test.json
echo $?  # 0 = allowed, 2 = blocked
```

## Contributing

When adding new extensions:

1. Use the meta-agent for creating agents
2. Follow existing patterns in `.claude/hooks/`
3. Test incrementally
4. Update CLAUDE.md if adding new patterns
5. Version control in `.claude/agents/` and `.claude/commands/`

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)