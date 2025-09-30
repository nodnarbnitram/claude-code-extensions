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

#### Option 1: Interactive CLI Installer (Recommended)

The easiest way to install extensions is using the included CLI tool:

```bash
# Clone this repository
git clone <repo-url>
cd claude-code-extensions

# Run the interactive installer
./install_extensions.py install ~/my-project
```

The installer provides:
- **Interactive selection**: Choose which extensions to install by type or category
- **Smart settings.json merging**: Automatically configures hooks without breaking existing settings
- **Dependency handling**: Copies hook utilities automatically
- **Dry-run mode**: Preview changes before applying

**Usage examples:**

```bash
# Interactive mode (default) - choose what to install
./install_extensions.py install ~/my-project

# Install all core agents non-interactively
./install_extensions.py install --type agent --category core --no-interactive ~/my-project

# Install all hooks
./install_extensions.py install --type hook ~/my-project

# Dry run to see what would be installed
./install_extensions.py install --dry-run ~/my-project

# List available extensions
./install_extensions.py list

# Get info about a specific extension
./install_extensions.py info code-reviewer

# See all options
./install_extensions.py install --help
```

#### Option 2: Manual Installation

1. **Clone this repository**:
   ```bash
   git clone <repo-url>
   cd claude-code-extensions
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

## Commands

| Command | Description | Arguments |
|---------|-------------|-----------|
| [`/agent-from-docs`](.claude/commands/agent-from-docs.md) | Create a specialized agent by analyzing documentation URLs | `<doc-url>` `[additional-urls...]` |
| [`/prime`](.claude/commands/prime.md) | Load context for a new agent session by analyzing codebase structure, documentation and README | - |
| [`/git-status`](.claude/commands/git-status.md) | Understand the current state of the git repository | - |
| [`/git-commit`](.claude/commands/git-commit.md) | Create well-formatted commits with conventional commit format and emoji | `[message]` \| `--no-verify` \| `--amend` |
| [`/frontend-mode`](.claude/commands/frontend-mode.md) | Load Ultracite rules for JS/TS development | - |
| [`/security-scan`](.claude/commands/security-scan.md) | Run security scans on project files (Python/Go/JS/TS) | `[path]` |

## Agents

### Meta Agent

| Agent | Description |
|-------|-------------|
| [`meta-agent`](.claude/agents/meta-agent.md) | Generates new, complete Claude Code sub-agent configuration files from descriptions. Uses Opus model for high-quality agent generation. |

### Core Agents

Quality assurance and analysis specialists:

| Agent | Description |
|-------|-------------|
| [`code-reviewer`](.claude/agents/core/code-reviewer.md) | Rigorous, security-aware code review after features, bug-fixes, or pull-requests. Delivers severity-tagged reports and routes issues to specialists. |
| [`code-archaeologist`](.claude/agents/core/code-archaeologist.md) | Explores and documents unfamiliar, legacy, or complex codebases. Produces comprehensive reports with architecture, metrics, risks, and action plans. |
| [`fact-checker`](.claude/agents/core/fact-checker.md) | Validates outputs from other agents to prevent hallucinations and ensure accuracy. Cross-references claims against codebase, web sources, and documentation. |
| [`documentation-specialist`](.claude/agents/core/documentation-specialist.md) | Crafts and updates project documentation including READMEs, API specs, architecture guides, and user manuals. |
| [`performance-optimizer`](.claude/agents/core/performance-optimizer.md) | Identifies bottlenecks, profiles workloads, and applies optimizations for high-performance systems. |

### Deep Research Agents

Specialized researchers for comprehensive analysis:

| Agent | Description |
|-------|-------------|
| [`research-coordinator`](.claude/agents/deep-research/research-coordinator.md) | Strategically plans and coordinates complex research tasks across multiple specialist researchers. |
| [`academic-researcher`](.claude/agents/deep-research/academic-researcher.md) | Searches scholarly sources, peer-reviewed papers, and academic literature with citation tracking. |
| [`data-analyst`](.claude/agents/deep-research/data-analyst.md) | Provides quantitative analysis, statistical insights, trend identification, and data visualization recommendations. |
| [`technical-researcher`](.claude/agents/deep-research/technical-researcher.md) | Analyzes code repositories, technical documentation, implementation details, and evaluates technical solutions. |
| [`web-researcher`](.claude/agents/deep-research/web-researcher.md) | Researches current news, industry reports, blogs, market trends, and real-time web intelligence. |

### Orchestrator Agents

Project coordination and team management:

| Agent | Description |
|-------|-------------|
| [`tech-lead-orchestrator`](.claude/agents/orchestrators/tech-lead-orchestrator.md) | Analyzes complex software projects and provides strategic recommendations. Coordinates multi-step tasks and assigns work to sub-agents. |
| [`project-analyst`](.claude/agents/orchestrators/project-analyst.md) | Analyzes new or unfamiliar codebases to detect frameworks, tech stacks, and architecture for proper specialist routing. |
| [`team-configurator`](.claude/agents/orchestrators/team-configurator.md) | Sets up AI development teams for projects. Detects stack, selects specialist sub-agents, and updates CLAUDE.md configuration. |

### Specialized Agents

#### Data & AI

| Agent | Description |
|-------|-------------|
| [`ai-engineer`](.claude/agents/specialized/data-ai/ai-engineer.md) | AI system design, model implementation, and production deployment across multiple frameworks. |
| [`llm-architect`](.claude/agents/specialized/data-ai/llm-architect.md) | LLM architecture, deployment, optimization, fine-tuning, and production serving. |
| [`machine-learning-engineer`](.claude/agents/specialized/data-ai/machine-learning-engineer.md) | Production model deployment, serving infrastructure, optimization, and edge deployment. |
| [`nlp-engineer`](.claude/agents/specialized/data-ai/nlp-engineer.md) | Natural language processing, transformer models, text pipelines, and multilingual support. |
| [`prompt-engineer`](.claude/agents/specialized/data-ai/prompt-engineer.md) | Prompt design, optimization, evaluation frameworks, and production prompt systems. |

#### React

| Agent | Description |
|-------|-------------|
| [`react-component-architect`](.claude/agents/specialized/react/react-component-architect.md) | Modern React patterns, component design, hooks implementation, and React 19+ architecture. |
| [`react-nextjs-expert`](.claude/agents/specialized/react/react-nextjs-expert.md) | Next.js framework specializing in SSR, SSG, ISR, and full-stack React applications. |
| [`tanstack-start-expert`](.claude/agents/specialized/react/tanstack-start-expert.md) | TanStack Start framework, TanStack Router integration, server functions, and type-safe development. |

#### Vue

| Agent | Description |
|-------|-------------|
| [`vue-component-architect`](.claude/agents/specialized/vue/vue-component-architect.md) | Vue 3 Composition API, component patterns, composables, and Vue architecture decisions. |
| [`vue-nuxt-expert`](.claude/agents/specialized/vue/vue-nuxt-expert.md) | Nuxt.js framework specializing in SSR, SSG, and full-stack Vue applications. |

#### Django

| Agent | Description |
|-------|-------------|
| [`django-backend-expert`](.claude/agents/specialized/django/django-backend-expert.md) | Django backend development: models, views, services, and Django-specific implementations. |
| [`django-api-developer`](.claude/agents/specialized/django/django-api-developer.md) | Django REST Framework and GraphQL API development with DRF serializers and viewsets. |
| [`django-orm-expert`](.claude/agents/specialized/django/django-orm-expert.md) | Django ORM optimization, complex queries, database performance, and migrations. |

#### Python

| Agent | Description |
|-------|-------------|
| [`typer-expert`](.claude/agents/specialized/python/typer-expert.md) | Typer CLI development specialist for type-hint driven CLIs, command structure, validation, testing, and distribution. |

#### Temporal.io

| Agent | Description |
|-------|-------------|
| [`temporal-core`](.claude/agents/specialized/temporal/temporal-core.md) | Universal Temporal.io expert for core concepts, architecture patterns, and determinism across all SDKs. |
| [`temporal-python`](.claude/agents/specialized/temporal/temporal-python.md) | Python SDK specialist for Temporal.io (v1.18.0+) covering async/await patterns, pytest testing, and AsyncIO. |
| [`temporal-go`](.claude/agents/specialized/temporal/temporal-go.md) | Go SDK specialist for Temporal.io (v1.36.0+) covering workflow-safe primitives, context patterns, and determinism. |
| [`temporal-typescript`](.claude/agents/specialized/temporal/temporal-typescript.md) | TypeScript SDK specialist for Temporal.io (v1.13.0+) covering proxyActivities patterns, type safety, and Jest testing. |
| [`temporal-testing`](.claude/agents/specialized/temporal/temporal-testing.md) | Testing specialist for Temporal.io covering testing strategies, time-skipping, activity mocking, and CI/CD integration. |
| [`temporal-troubleshooting`](.claude/agents/specialized/temporal/temporal-troubleshooting.md) | Troubleshooting specialist for diagnosing errors, non-determinism issues, performance problems, and production incidents. |

#### Go

| Agent | Description |
|-------|-------------|
| [`go-google-style-expert`](.claude/agents/specialized/go/go-google-style-expert.md) | Google Go style guide expert covering naming, error handling, concurrency, testing, interfaces, and Go 1.25 features. Enforces strict Google conventions. |

#### Other Frameworks

| Agent | Description |
|-------|-------------|
| [`cloudflare-workers-expert`](.claude/agents/specialized/cloudflare/cloudflare-workers-expert.md) | Cloudflare Workers development, serverless edge computing, and platform integrations. |
| [`crossplane-upgrade-agent`](.claude/agents/specialized/crossplane/crossplane-upgrade-agent.md) | Crossplane upgrade specialist for YAML and code migrations from v1 to v2. |

### Universal Agents

Framework-agnostic developers:

| Agent | Description |
|-------|-------------|
| [`api-architect`](.claude/agents/universal/api-architect.md) | Universal API designer for RESTful design, GraphQL schemas, OpenAPI specs, and modern contract standards. |
| [`backend-developer`](.claude/agents/universal/backend-developer.md) | Production-ready server-side code across any language or stack when no framework-specific agent exists. |
| [`frontend-developer`](.claude/agents/universal/frontend-developer.md) | Responsive, accessible, high-performance UIs with vanilla JS/TS, React, Vue, Angular, Svelte, or Web Components. |
| [`tailwind-css-expert`](.claude/agents/universal/tailwind-css-expert.md) | Tailwind CSS styling, utility-first refactors, and responsive component work. |

## Hooks

All hooks use Python with `uv run --script` for dependency management.

| Hook | Event | Purpose |
|------|-------|---------|
| [`pre_tool_use.py`](.claude/hooks/pre_tool_use.py) | PreToolUse | Blocks dangerous commands (`rm -rf`), prevents `.env` access, and logs all tool calls for audit. |
| [`post_tool_use.py`](.claude/hooks/post_tool_use.py) | PostToolUse | Logs all tool executions to `logs/post_tool_use.json`. Triggers lint checking on Edit/Write operations. |
| [`session_start.py`](.claude/hooks/session_start.py) | SessionStart | Injects git status and project context at session start. Logs session information. |
| [`user_prompt_submit.py`](.claude/hooks/user_prompt_submit.py) | UserPromptSubmit | Logs user prompts and can validate/block them before processing. |
| [`pre_compact.py`](.claude/hooks/pre_compact.py) | PreCompact | Executes before context compaction to preserve important information. |
| [`stop.py`](.claude/hooks/stop.py) | Stop | Runs when the main agent finishes responding. |
| [`subagent_stop.py`](.claude/hooks/subagent_stop.py) | SubagentStop | Executes when a subagent completes its task. |
| [`notification.py`](.claude/hooks/notification.py) | Notification | Handles notification events from Claude Code. |
| [`lint/check.py`](.claude/hooks/lint/check.py) | (Invoked by PostToolUse) | Automatically runs language-specific linters: `ruff` (Python), `golangci-lint` (Go), `biome`/`prettier` (JS/TS). |

### Hook Utilities

Shared utilities in `.claude/hooks/utils/`:

**LLM Integrations:**
- [`llm/anth.py`](.claude/hooks/utils/llm/anth.py) - Anthropic API integration
- [`llm/oai.py`](.claude/hooks/utils/llm/oai.py) - OpenAI API integration
- [`llm/ollama.py`](.claude/hooks/utils/llm/ollama.py) - Ollama local LLM integration

**Text-to-Speech:**
- [`tts/pyttsx3_tts.py`](.claude/hooks/utils/tts/pyttsx3_tts.py) - Local TTS using pyttsx3
- [`tts/openai_tts.py`](.claude/hooks/utils/tts/openai_tts.py) - OpenAI TTS API
- [`tts/elevenlabs_tts.py`](.claude/hooks/utils/tts/elevenlabs_tts.py) - ElevenLabs TTS API

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