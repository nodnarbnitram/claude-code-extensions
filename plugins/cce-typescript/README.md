# cce-typescript

TypeScript and frontend tooling plugin for Claude Code, providing expert assistance with Braintrust AI testing, fumadocs documentation, and modern TypeScript development workflows.

## Overview

The **cce-typescript** plugin delivers specialized agents for TypeScript development, focusing on two critical areas:

1. **AI Application Testing & Observability** - Complete Braintrust SDK integration for LLM evaluation, production logging, and distributed tracing
2. **Documentation Sites** - fumadocs framework expertise for building MDX-powered documentation with TanStack Start/Router

## Features

### Braintrust TypeScript Expert

The `braintrust-typescript-expert` agent provides comprehensive guidance on:

- **Evaluation Framework**: Dataset creation, task definition, scorer configuration, and evaluation execution
- **Production Logging**: Logger initialization, LLM provider wrapping (OpenAI, Anthropic, Vercel AI SDK, Google GenAI), and automatic instrumentation
- **Distributed Tracing**: Cross-service trace propagation using span export/import
- **Streaming Support**: Automatic streaming logging with `finalValue()` patterns
- **Attachments**: Large file handling (images, audio, video) without trace payload bloat
- **Troubleshooting**: Common issues like missing traces, incorrect nesting, and flush timing

**Key Capabilities**:
- Automatic delegation when users mention Braintrust, LLM testing, evaluation, or observability
- Complete code examples with imports, initialization, and error handling
- Best practices for production deployments
- Integration patterns for all major LLM providers
- Performance optimization guidance

### Fumadocs TanStack Expert

The `fumadocs-tanstack-expert` agent specializes in:

- **TanStack Start Integration**: Dual loader pattern (server validation + client MDX loading)
- **MDX Compilation**: Vite configuration, plugin ordering, and content collections
- **UI Components**: Full fumadocs component library integration (Tabs, Callout, Cards, Steps, etc.)
- **Search Integration**: Orama Cloud and static search setup
- **Internationalization**: Multi-language documentation routing
- **Layout Configuration**: DocsLayout, page trees, and navigation setup

**Critical Architecture Knowledge**:
- TanStack Start does NOT support React Server Components (RSC)
- MDX loads client-side via `createClientLoader()` (not server-side like Next.js)
- Provides TanStack-specific patterns, never Next.js RSC patterns

**Key Capabilities**:
- Automatic delegation when users work with fumadocs or MDX documentation
- Complete project setup from scratch
- Troubleshooting common issues (plugin order, missing components, search failures)
- Performance optimization with preloading
- Type-safe frontmatter schemas with Zod

## Installation

### Via Claude Code Plugin System

```bash
# Add the marketplace (if not already added)
/plugin marketplace add https://github.com/nodnarbnitram/claude-code-extensions

# Install the TypeScript plugin
/plugin install cce-typescript@cce-marketplace
```

### Standalone Installation

Clone the repository and symlink agents to your project:

```bash
git clone https://github.com/nodnarbnitram/claude-code-extensions.git
cd claude-code-extensions

# Copy agents to your project
cp -r .claude/agents/specialized/braintrust ~/.claude/agents/specialized/
cp -r .claude/agents/specialized/frontend ~/.claude/agents/specialized/
```

## Usage

### Using the Braintrust Expert

The agent activates automatically when you work with Braintrust-related tasks:

```
# Automatic delegation
> I need to set up Braintrust evaluation for my LLM chatbot

# Explicit invocation
> Use the braintrust-typescript-expert to help me implement distributed tracing
```

**Example Use Cases**:
- "Set up Braintrust evaluation with custom scorers"
- "Add production logging to my OpenAI integration"
- "Implement distributed tracing across my microservices"
- "Debug why my Braintrust traces aren't appearing"
- "Add streaming support with Vercel AI SDK"

### Using the Fumadocs Expert

The agent activates automatically when you work with fumadocs or MDX documentation:

```
# Automatic delegation
> I want to create a documentation site with fumadocs and TanStack Start

# Explicit invocation
> Use the fumadocs-tanstack-expert to help me configure search
```

**Example Use Cases**:
- "Set up fumadocs with TanStack Start from scratch"
- "Add Orama search to my documentation site"
- "Configure syntax highlighting with Shiki"
- "Create multi-language documentation"
- "Fix MDX components not rendering"

## Agent Details

### braintrust-typescript-expert

**Trigger Keywords**: Braintrust, evaluation, LLM testing, production logging, distributed tracing, observability, prompt management

**Tools**: Read, Write, Edit, Grep, Glob, Bash, WebFetch

**Model**: Inherits from session

**Color**: Purple

### fumadocs-tanstack-expert

**Trigger Keywords**: fumadocs, MDX documentation, TanStack Start, documentation site, content collections, search integration

**Tools**: Read, Write, Edit, Grep, Glob, Bash, WebFetch

**Model**: Inherits from session

**Color**: Cyan

## Plugin Architecture

This plugin follows the dual-mode architecture of Claude Code Extensions:

- **Plugin Mode**: Agents namespaced under plugin (no commands in this plugin)
- **Standalone Mode**: Agents available directly in `.claude/agents/`
- **Shared Source**: Both modes use the same agent files

### Directory Structure

```
.claude-plugin/plugins/cce-typescript/
├── plugin.json          # Plugin manifest
└── README.md            # This file

.claude/agents/specialized/
├── braintrust/
│   └── braintrust-typescript-expert.md
└── frontend/
    └── fumadocs-tanstack-expert.md
```

## Integration with Other Plugins

The **cce-typescript** plugin complements other Claude Code Extensions plugins:

- **cce-core**: Use together for git workflows and code quality checks
- **cce-web-react**: Combine with React expertise for full-stack TypeScript development
- **cce-cloudflare**: Integrate Braintrust logging with Cloudflare Workers AI

## Best Practices

### Braintrust Development

1. **Always flush before exit**: Use `await flush()` in `beforeExit` handler
2. **Wrap LLM clients early**: Immediately after client creation for best instrumentation
3. **Use traced() for nesting**: Maintain parent-child relationships in async contexts
4. **Attachments for large data**: Prevent trace payload bloat with images/files
5. **Distributed tracing requires explicit linking**: Use `span.export()` and `traced({ parent })`

### Fumadocs Development

1. **MDX plugin MUST be first**: In `vite.config.ts`, place `mdx()` before `tanstackStart()`
2. **Dual loader pattern**: Server for validation, client for MDX component loading
3. **Type-safe frontmatter**: Define Zod schemas in `source.config.ts`
4. **TanStack-specific providers**: Use `fumadocs-ui/provider/tanstack`, not Next.js providers
5. **Preload for performance**: Enable `preload: true` in `createClientLoader`

## Troubleshooting

### Common Braintrust Issues

**Missing traces**:
- Verify `flush()` is called before process exit
- Check that at least one root span exists per trace
- Ensure async context is maintained

**Incorrect nesting**:
- Use `wrapTraced()` or `traced()` for all functions
- Don't break async/await chains
- Verify parent spans export correctly in distributed setups

### Common Fumadocs Issues

**MDX not rendering**:
- Check MDX plugin is first in Vite config
- Verify `clientLoader` with `preload: true` exists
- Ensure `.source` directory is generated (run `npm run dev`)

**Search not working**:
- Verify Orama credentials are set
- Check search index generation
- Ensure `search.enabled: true` in DocsLayout

## Documentation

### Braintrust Resources
- [Braintrust TypeScript SDK](https://www.braintrust.dev/docs)
- [Autoevals Library](https://github.com/braintrustdata/autoevals)
- [API Reference](https://www.braintrust.dev/docs/reference/libs/nodejs)

### Fumadocs Resources
- [Fumadocs Core APIs](https://fumadocs.dev/docs/headless)
- [UI Components](https://fumadocs.dev/docs/ui)
- [MDX Configuration](https://fumadocs.dev/docs/mdx)
- [TanStack Start Examples](https://github.com/fuma-nama/fumadocs/tree/dev/examples)

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for guidelines.

When contributing to this plugin:
1. Follow the agent creation patterns in [CLAUDE.md](../../../CLAUDE.md)
2. Test in both plugin and standalone modes
3. Update this README with new features
4. Ensure agents have clear trigger descriptions

## License

MIT License - see [LICENSE](../../../LICENSE) for details

## Support

- **Issues**: [GitHub Issues](https://github.com/nodnarbnitram/claude-code-extensions/issues)
- **Discussions**: [GitHub Discussions](https://github.com/nodnarbnitram/claude-code-extensions/discussions)
- **Documentation**: [Project README](../../../README.md)

## Version History

### 1.0.0 (Initial Release)
- Added `braintrust-typescript-expert` agent
- Added `fumadocs-tanstack-expert` agent
- Complete evaluation, logging, and tracing support
- Full fumadocs + TanStack Start integration patterns
- Comprehensive troubleshooting guides
