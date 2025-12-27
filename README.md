# Claude Code Extensions

> A comprehensive collection of production-ready agents, hooks, commands, and output styles for [Claude Code](https://claude.ai/code)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple.svg)](https://claude.ai/code)

Supercharge your Claude Code experience with **55+ specialized agents**, **7 skills**, **8 lifecycle hooks**, **8 slash commands**, and powerful automation tools—all ready to install and customize.

## ✨ Highlights

- **🤖 55+ Expert Agents** - From code reviewers to deep research specialists (React, Django, Temporal, Cloudflare, Research, and more)
- **🎯 Model-Invoked Skills** - Capabilities Claude discovers and uses automatically based on context
- **🔒 Safety-First Hooks** - Block dangerous commands, protect sensitive files, audit all operations
- **⚡ Auto-Linting** - Integrated Python, Go, and JS/TS linters that run automatically
- **🎯 Smart Orchestration** - Tech-lead agents that coordinate multi-step tasks across specialists
- **📦 Easy Installation** - Interactive CLI installer with settings.json merging
- **🧪 Battle-Tested** - Production patterns from real-world Claude Code workflows

## 📦 Available Plugins

The repository provides **8 focused plugins** (Phase 1) with 10+ more coming in future releases:

| Plugin | Description | What's Included |
|--------|-------------|-----------------|
| **cce-core** | Essential foundation | 13 agents (core, orchestrators, universal), 8 hooks, 2 skills, 8 commands |
| **cce-kubernetes** | Kubernetes operations | 6 K8s health agents, 2 skills, 1 command |
| **cce-cloudflare** | Cloudflare development | 5 Workers/AI/Workflows agents, 1 VPC skill |
| **cce-esphome** | ESPHome IoT | 6 ESPHome agents, 2 skills (config, Box-3) |
| **cce-web-react** | React ecosystem | 3 React/Next.js/TanStack agents |
| **cce-django** | Django backend | 3 Django agents (backend, API, ORM) |
| **cce-research** | Deep research coordination | 5 research agents (coordinator, academic, web, technical, data) |
| **cce-grafana** | Grafana observability | 1 plugin expert agent, 2 skills (scaffolding, billing metrics) |

**Coming Soon:** `cce-web-vue`, `cce-temporal`, `cce-devops`, `cce-ai`, `cce-homeassistant`, `cce-go`, `cce-python`, `cce-typescript`, `cce-anthropic`

**Install only what you need** - no need to load 50+ agents if you only work with React!

## 🚀 Quick Start

### Installation

**Option 1: Plugin (Recommended for Multiple Projects)**

Install as modular plugins via Claude Code's plugin system - pick only what you need for your tech stack:

```bash
# In any Claude Code session:
/plugin marketplace add github:nodnarbnitram/claude-code-extensions
```

Then install the plugins you need:

```bash
# Essential foundation (everyone needs this)
/plugin install cce-core@cce-marketplace

# Add plugins for your tech stack:
/plugin install cce-kubernetes@cce-marketplace    # For Kubernetes development
/plugin install cce-cloudflare@cce-marketplace    # For Cloudflare Workers/AI
/plugin install cce-esphome@cce-marketplace       # For ESPHome IoT
/plugin install cce-web-react@cce-marketplace     # For React/Next.js/TanStack
/plugin install cce-django@cce-marketplace        # For Django backend development
/plugin install cce-grafana@cce-marketplace       # For Grafana plugin development & billing
/plugin install cce-research@cce-marketplace      # For deep research tasks
```

**Benefits:**
- ✅ Modular - install only what you need
- ✅ Automatic updates across all projects
- ✅ Centralized management
- ✅ No repository cloning needed

**Command namespaces:**
- Core: `/cce:git-commit`, `/cce:prime`
- Kubernetes: `/cce-kubernetes:health`
- (Other plugins currently provide agents/skills only)

**Option 2: Standalone (For Single Project or Custom Setup)**

```bash
git clone https://github.com/nodnarbnitram/claude-code-extensions.git
cd claude-code-extensions
./install_extensions.py install ~/my-project
```

The installer lets you:
- ✅ Choose extensions interactively by type or category
- ✅ Preview changes with `--dry-run` before applying
- ✅ Merge settings.json safely without conflicts
- ✅ Copy dependencies automatically

```bash
# Common usage patterns
./install_extensions.py list                    # See all available extensions
./install_extensions.py info code-reviewer      # Get details on specific extension
./install_extensions.py install --dry-run ~/my-project   # Preview what will be installed
./install_extensions.py install --type agent --category core ~/my-project  # Install specific category
```

**Option 3: Manual Copy**

```bash
# Copy specific items manually
cp .claude/agents/core/code-reviewer.md ~/my-project/.claude/agents/
cp -r .claude/hooks ~/my-project/.claude/
cp .claude/settings.json ~/my-project/.claude/
```

### Which Installation Method Should I Use?

| Mode | Best For | Pros | Cons |
|------|----------|------|------|
| **Plugin** | Multiple projects, team distribution | Auto-updates, centralized, modular | Namespaced commands |
| **Standalone** | Single project, custom setup | Full control, unprefixed commands | Manual updates, per-project install |
| **Manual** | Cherry-picking specific extensions | Maximum control | No automation, manual merging |

### Creating New Extensions

**Agents** - Use the built-in meta-agent:
```
> Use the meta-agent to create a [domain] specialist agent
```

**Hooks** - Use Python with uv script format (see [CLAUDE.md](./CLAUDE.md) for templates)

**Commands** - Create `.md` files in `.claude/commands/` with frontmatter

**Output Styles** - Create `.md` files in `.claude/output-styles/` with custom prompts

📖 **Full guide**: See [CLAUDE.md](./CLAUDE.md) for detailed patterns and examples

## 💡 Why Use This?

**For Teams**
- Share consistent workflows across your organization
- Enforce code quality standards automatically
- Onboard developers faster with specialized agents
- Version control your Claude Code configuration

**For Solo Developers**
- Automate repetitive tasks with hooks and commands
- Get expert-level assistance across multiple frameworks
- Keep your main Claude context focused with subagents
- Protect yourself from mistakes with safety hooks

**For Learning**
- Explore production-ready extension patterns
- Learn from 50+ agent examples across different domains
- Understand hook lifecycle and automation
- See how to structure complex AI workflows

## 📚 Extension Reference

### Commands

| Command | Description | Arguments |
|---------|-------------|-----------|
| [`/agent-from-docs`](.claude/commands/agent-from-docs.md) | Create a specialized agent by analyzing documentation URLs | `<doc-url>` `[additional-urls...]` |
| [`/prime`](.claude/commands/prime.md) | Load context for a new agent session by analyzing codebase structure, documentation and README | - |
| [`/git-status`](.claude/commands/git-status.md) | Understand the current state of the git repository | - |
| [`/git-commit`](.claude/commands/git-commit.md) | Analyze changes and create well-formatted commits with emoji conventional format | `[message]` `[--amend]` (Optional)|
| [`/frontend-mode`](.claude/commands/frontend-mode.md) | Load Ultracite rules for JS/TS development | - |
| [`/security-scan`](.claude/commands/security-scan.md) | Run security scans on project files (Python/Go/JS/TS) | `[path]` |
| [`/wrapup-skillup`](.claude/commands/wrapup-skillup.md) | Generate session report capturing learnings, tools, pitfalls, and extension recommendations | `[topic-slug]` |
| [`/k8s-health`](.claude/commands/k8s-health.md) | Run comprehensive Kubernetes cluster health diagnostics with dynamic operator discovery | `[--operator <name>]` `[--output json\|summary\|detailed]` |

### Skills

Model-invoked capabilities that Claude automatically discovers and uses based on task context.

| Skill | Description |
|-------|-------------|
| [`commit-helper`](.claude/skills/commit-helper/) | Generate clear, conventional commit messages from git diffs |
| [`code-reviewer`](.claude/skills/code-reviewer/) | Review code for best practices, security issues, and potential bugs (read-only) |
| [`kubernetes-operations`](.claude/skills/kubernetes-operations/) | Kubernetes debugging, resource management, and cluster operations with token-efficient scripts |
| [`kubernetes-health`](.claude/skills/kubernetes-health/) | Comprehensive cluster health diagnostics using dynamic API discovery with operator-specific agents |
| [`grafana-plugin-scaffolding`](.claude/skills/grafana-plugin-scaffolding/) | Scaffold Grafana plugins (panel, data source, app, backend) with Docker dev environment |
| [`grafana-billing`](.claude/skills/grafana-billing/) | Query Prometheus and Loki billing metrics from Grafana Cloud for cost analysis and optimization |

**Creating new skills:**
- Use the `skill-creator` agent: `> Use the skill-creator to create a skill for [purpose]`
- Or copy the skeleton template: `cp -r templates/skill-skeleton .claude/skills/my-skill`

See [`docs/claude-code/agent-skills.md`](docs/claude-code/agent-skills.md) for detailed guidance.

### Agents

<details>
<summary><b>📖 View All 50+ Agents</b> (Meta, Core, Research, Orchestrators, Universal, Specialized)</summary>

#### Meta Agent

| Agent | Description |
|-------|-------------|
| [`meta-agent`](.claude/agents/meta-agent.md) | Generates new, complete Claude Code sub-agent configuration files from descriptions using Opus |

#### Core Agents

| Agent | Description |
|-------|-------------|
| [`code-reviewer`](.claude/agents/core/code-reviewer.md) | Rigorous, security-aware code review after features, bug-fixes, or pull-requests |
| [`code-archaeologist`](.claude/agents/core/code-archaeologist.md) | Explores and documents unfamiliar, legacy, or complex codebases |
| [`fact-checker`](.claude/agents/core/fact-checker.md) | Validates agent outputs to prevent hallucinations and ensure accuracy |
| [`documentation-specialist`](.claude/agents/core/documentation-specialist.md) | Crafts and updates READMEs, API specs, architecture guides, and user manuals |
| [`performance-optimizer`](.claude/agents/core/performance-optimizer.md) | Identifies bottlenecks and applies optimizations for high-performance systems |

#### Research Agents

| Agent | Description |
|-------|-------------|
| [`research-coordinator`](.claude/agents/deep-research/research-coordinator.md) | Plans and coordinates complex research tasks across specialists |
| [`academic-researcher`](.claude/agents/deep-research/academic-researcher.md) | Searches scholarly sources, peer-reviewed papers with citation tracking |
| [`data-analyst`](.claude/agents/deep-research/data-analyst.md) | Quantitative analysis, statistical insights, data visualization |
| [`technical-researcher`](.claude/agents/deep-research/technical-researcher.md) | Analyzes code repositories, technical docs, implementation details |
| [`web-researcher`](.claude/agents/deep-research/web-researcher.md) | Current news, industry reports, market trends, real-time intelligence |

#### Orchestrators

| Agent | Description |
|-------|-------------|
| [`tech-lead-orchestrator`](.claude/agents/orchestrators/tech-lead-orchestrator.md) | Strategic project analysis, coordinates multi-step tasks across sub-agents |
| [`project-analyst`](.claude/agents/orchestrators/project-analyst.md) | Detects frameworks, tech stacks, architecture for proper routing |
| [`team-configurator`](.claude/agents/orchestrators/team-configurator.md) | Sets up AI teams, selects specialists, updates CLAUDE.md config |

#### Universal (Framework-Agnostic)

| Agent | Description |
|-------|-------------|
| [`api-architect`](.claude/agents/universal/api-architect.md) | RESTful design, GraphQL schemas, OpenAPI specs |
| [`backend-developer`](.claude/agents/universal/backend-developer.md) | Server-side code across any language or stack |
| [`frontend-developer`](.claude/agents/universal/frontend-developer.md) | Responsive UIs with React, Vue, Angular, Svelte, or vanilla JS |
| [`tailwind-css-expert`](.claude/agents/universal/tailwind-css-expert.md) | Tailwind CSS styling and utility-first refactors |

#### Specialized: React

| Agent | Description |
|-------|-------------|
| [`react-component-architect`](.claude/agents/specialized/react/react-component-architect.md) | React 19+ patterns, hooks, component design |
| [`react-nextjs-expert`](.claude/agents/specialized/react/react-nextjs-expert.md) | Next.js SSR, SSG, ISR, full-stack React |
| [`tanstack-start-expert`](.claude/agents/specialized/react/tanstack-start-expert.md) | TanStack Start, Router, server functions |

#### Specialized: Vue

| Agent | Description |
|-------|-------------|
| [`vue-component-architect`](.claude/agents/specialized/vue/vue-component-architect.md) | Vue 3 Composition API, composables |
| [`vue-nuxt-expert`](.claude/agents/specialized/vue/vue-nuxt-expert.md) | Nuxt.js SSR, SSG, full-stack Vue |

#### Specialized: Django

| Agent | Description |
|-------|-------------|
| [`django-backend-expert`](.claude/agents/specialized/django/django-backend-expert.md) | Models, views, services, Django implementations |
| [`django-api-developer`](.claude/agents/specialized/django/django-api-developer.md) | DRF and GraphQL API development |
| [`django-orm-expert`](.claude/agents/specialized/django/django-orm-expert.md) | ORM optimization, complex queries, migrations |

#### Specialized: Python

| Agent | Description |
|-------|-------------|
| [`typer-expert`](.claude/agents/specialized/python/typer-expert.md) | Typer CLI development, validation, testing |

#### Specialized: Temporal.io

| Agent | Description |
|-------|-------------|
| [`temporal-core`](.claude/agents/specialized/temporal/temporal-core.md) | Core concepts, architecture, determinism |
| [`temporal-python`](.claude/agents/specialized/temporal/temporal-python.md) | Python SDK async/await, pytest, AsyncIO |
| [`temporal-go`](.claude/agents/specialized/temporal/temporal-go.md) | Go SDK workflow-safe primitives, context |
| [`temporal-typescript`](.claude/agents/specialized/temporal/temporal-typescript.md) | TypeScript SDK proxyActivities, type safety |
| [`temporal-testing`](.claude/agents/specialized/temporal/temporal-testing.md) | Testing strategies, time-skipping, mocking |
| [`temporal-troubleshooting`](.claude/agents/specialized/temporal/temporal-troubleshooting.md) | Error diagnosis, non-determinism issues |

#### Specialized: Go

| Agent | Description |
|-------|-------------|
| [`go-google-style-expert`](.claude/agents/specialized/go/go-google-style-expert.md) | Google Go style guide, conventions, Go 1.25+ |

#### Specialized: Anthropic

| Agent | Description |
|-------|-------------|
| [`claude-agent-sdk-typescript-expert`](.claude/agents/specialized/anthropic/claude-agent-sdk-typescript-expert.md) | Claude Agent SDK for TypeScript/Node.js |
| [`claude-agent-sdk-python-expert`](.claude/agents/specialized/anthropic/claude-agent-sdk-python-expert.md) | Claude Agent SDK for Python |

#### Specialized: Cloudflare

| Agent | Description |
|-------|-------------|
| [`cloudflare-workers-expert`](.claude/agents/specialized/cloudflare/cloudflare-workers-expert.md) | Workers, edge computing, KV, D1, R2, Durable Objects |
| [`cloudflare-workers-ai-expert`](.claude/agents/specialized/cloudflare/cloudflare-workers-ai-expert.md) | Workers AI, model selection, RAG, streaming |
| [`cloudflare-workers-for-platforms-expert`](.claude/agents/specialized/cloudflare/cloudflare-workers-for-platforms-expert.md) | Multi-tenant architectures, dispatch namespaces |
| [`cloudflare-workflows-expert`](.claude/agents/specialized/cloudflare/cloudflare-workflows-expert.md) | Durable execution, step APIs, DAG workflows |
| [`cloudflare-ai-agents-sdk-expert`](.claude/agents/specialized/cloudflare/cloudflare-ai-agents-sdk-expert.md) | AI Agents SDK, WebSockets, MCP servers |

#### Specialized: Crossplane

| Agent | Description |
|-------|-------------|
| [`crossplane-upgrade-agent`](.claude/agents/specialized/crossplane/crossplane-upgrade-agent.md) | Crossplane v1 to v2 migrations |
| [`crossplane-aws-rds-expert`](.claude/agents/specialized/crossplane/crossplane-aws-rds-expert.md) | AWS RDS provider, Aurora, compositions |

#### Specialized: Kubernetes Health

| Agent | Description |
|-------|-------------|
| [`k8s-health-orchestrator`](.claude/agents/specialized/kubernetes/k8s-health-orchestrator.md) | Orchestrates cluster health diagnostics, dispatches sub-agents based on API discovery |
| [`k8s-core-health-agent`](.claude/agents/specialized/kubernetes/k8s-core-health-agent.md) | Core Kubernetes health checks: nodes, pods, deployments, services, PVCs |
| [`k8s-crossplane-health-agent`](.claude/agents/specialized/kubernetes/k8s-crossplane-health-agent.md) | Crossplane health: providers, compositions, claims, managed resources |
| [`k8s-argocd-health-agent`](.claude/agents/specialized/kubernetes/k8s-argocd-health-agent.md) | ArgoCD health: applications, sync status, app projects |
| [`k8s-certmanager-health-agent`](.claude/agents/specialized/kubernetes/k8s-certmanager-health-agent.md) | Cert-manager health: certificates, issuers, expiry warnings |
| [`k8s-prometheus-health-agent`](.claude/agents/specialized/kubernetes/k8s-prometheus-health-agent.md) | Prometheus health: instances, alertmanagers, service monitors |

#### Specialized: Grafana

| Agent | Description |
|-------|-------------|
| [`grafana-plugin-expert`](.claude/agents/specialized/grafana/grafana-plugin-expert.md) | Grafana plugin development (panel, data source, app, backend), SDK patterns, React/Go |

</details>

### Hooks

**Python hooks** using `uv run --script` for zero-config dependency management.

| Hook | Event | Purpose |
|------|-------|---------|
| [`pre_tool_use.py`](.claude/hooks/pre_tool_use.py) | PreToolUse | 🔒 Blocks dangerous commands, protects `.env` files, audit logging |
| [`post_tool_use.py`](.claude/hooks/post_tool_use.py) | PostToolUse | 📝 Logs executions, triggers auto-linting on file changes |
| [`session_start.py`](.claude/hooks/session_start.py) | SessionStart | 🚀 Injects git status and project context |
| [`user_prompt_submit.py`](.claude/hooks/user_prompt_submit.py) | UserPromptSubmit | 📊 Logs and validates user prompts |
| [`pre_compact.py`](.claude/hooks/pre_compact.py) | PreCompact | 💾 Preserves info before context compaction |
| [`stop.py`](.claude/hooks/stop.py) | Stop | 🏁 Runs when main agent finishes |
| [`subagent_stop.py`](.claude/hooks/subagent_stop.py) | SubagentStop | 🔄 Executes when subagent completes |
| [`notification.py`](.claude/hooks/notification.py) | Notification | 🔔 Handles Claude Code notifications |
| [`slack_notification.py`](.claude/hooks/slack_notification.py) | All events | 💬 Sends Slack DMs for Claude Code events (requires `SLACK_BOT_TOKEN`, `SLACK_USER_ID`). **Note:** Caches transcript path on SessionStart to work around [stale path bug](https://github.com/anthropics/claude-code/issues/8069) in resumed sessions |
| [`lint/check.py`](.claude/hooks/lint/check.py) | (Auto-triggered) | ⚡ Auto-lints: `ruff`, `golangci-lint`, `biome` |

**Utilities**: LLM integrations (Anthropic, OpenAI, Ollama), TTS engines (pyttsx3, OpenAI, ElevenLabs)

## 📖 Documentation

- **[CLAUDE.md](./CLAUDE.md)** - Complete guide for creating extensions
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - How to contribute to this project
- **[docs/claude-code/](./docs/claude-code/)** - Official Claude Code documentation

## 📋 Requirements

- [Claude Code](https://claude.ai/code) CLI
- [uv](https://github.com/astral-sh/uv) - Python package manager
- Python 3.11+

## 🎯 Usage Examples

**Auto Code Review**
```
> Review my recent changes
```
The code-reviewer agent automatically analyzes your git diff.

**Desktop Notifications**
Configure hooks for desktop alerts when Claude needs input (see [CLAUDE.md](./CLAUDE.md#creating-hooks)).

**Test Hooks Locally**
```bash
echo '{"tool_name": "Bash", "tool_input": {"command": "ls"}}' > test.json
uv run ./.claude/hooks/pre_tool_use.py < test.json
echo $?  # 0 = allowed, 2 = blocked
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for:
- Development setup
- Testing guidelines
- Pull request process
- Style guidelines

**Quick tips**:
- Use the meta-agent to create new agents
- Follow existing patterns in `.claude/hooks/`
- Test thoroughly before submitting
- Update documentation with your changes

## 📦 Project Structure

```
.claude/
├── agents/           # 50+ specialized AI assistants
├── skills/           # Model-invoked capabilities
├── hooks/            # Lifecycle automation scripts
├── commands/         # Reusable slash commands
├── output-styles/    # Custom system prompts
└── settings.json     # Hook configuration

templates/
└── skill-skeleton/   # Starter template for new skills

docs/                 # Claude Code official docs
install_extensions.py # Interactive installer CLI
```

## 🔗 Resources

- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)
- [Report Issues](../../issues/new)

## 📄 License

[MIT License](LICENSE) - Free for everyone, including commercial use.

**What this means:**
- ✅ Use it anywhere - personal projects, startups, Fortune 500 companies
- ✅ Modify it however you want
- ✅ No permission needed
- ✅ Just keep the copyright notice

**That's it.** Use it, learn from it, build amazing things. 🚀