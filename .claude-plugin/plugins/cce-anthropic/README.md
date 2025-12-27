# cce-anthropic

Anthropic Claude Agent SDK development for Python and TypeScript autonomous agents.

## Overview

This plugin provides expert agents for building autonomous AI agents using Anthropic's official Claude Agent SDK. Released in October 2025, the SDK enables developers to create sophisticated agent applications with custom tools, permission systems, hooks, and MCP server integration.

## Features

### Specialized Agents

#### Python SDK Expert (`claude-agent-sdk-python-expert`)
Expert in async Python agent development with comprehensive support for:
- **SDK Architecture**: `query()` functions, `ClaudeSDKClient` class, `@tool` decorator
- **Async Patterns**: Full asyncio, trio, and anyio support
- **Type Safety**: mypy strict mode with dataclasses
- **Custom Tools**: In-process MCP tools with direct Python state access
- **Permission System**: Dynamic control with permission callbacks
- **Hooks**: Lifecycle event handling (PreToolUse, PostToolUse, etc.)
- **Web Integration**: FastAPI and Django Channels patterns

**Auto-triggers on:**
- Python Agent SDK implementation requests
- Async Python agent development
- MCP tool creation
- Agent architecture design
- SDK debugging and troubleshooting

#### TypeScript SDK Expert (`claude-agent-sdk-typescript-expert`)
Expert in TypeScript/Node.js autonomous agent development with:
- **Type-Safe Tools**: Zod schema validation for all tool inputs
- **Streaming Responses**: Async generator patterns for real-time output
- **Permission Modes**: plan, default, acceptEdits, bypassPermissions
- **MCP Servers**: createSdkMcpServer for external tool integration
- **Autonomous Loops**: Gather → Act → Verify patterns
- **Subagent Delegation**: Context management and task distribution

**Auto-triggers on:**
- TypeScript/Node.js Agent SDK requests
- Tool creation with Zod schemas
- Streaming agent implementations
- MCP server setup
- Autonomous agent loop design

## Installation

### From Marketplace (Recommended)

```bash
# Add the CCE marketplace
claude plugin marketplace add https://github.com/nodnarbnitram/claude-code-extensions

# Install the Anthropic plugin
claude plugin install cce-anthropic@cce-marketplace
```

### From Local Source

```bash
# Clone the repository
git clone https://github.com/nodnarbnitram/claude-code-extensions.git
cd claude-code-extensions

# Install the plugin
claude plugin install ./.claude-plugin/plugins/cce-anthropic
```

## Usage

Once installed, the agents automatically activate when you work on Claude Agent SDK projects.

### Python SDK Usage

```python
# The Python expert agent activates when you mention:
"Create a Python agent using the Claude SDK"
"Build an async agent with custom tools"
"Implement MCP server in Python"
"Add permission callbacks to my agent"
```

**Example tasks:**
- Building query-based batch processing agents
- Creating bidirectional conversation agents with ClaudeSDKClient
- Designing custom tools with @tool decorator
- Implementing permission callbacks for security
- Adding hooks for logging and safety checks
- Integrating with FastAPI or Django Channels

### TypeScript SDK Usage

```typescript
// The TypeScript expert agent activates when you mention:
"Create a TypeScript agent using the Claude SDK"
"Build a streaming agent with Zod validation"
"Set up MCP server in Node.js"
"Implement autonomous agent loop"
```

**Example tasks:**
- Building type-safe streaming agents
- Creating tools with Zod schema validation
- Configuring permission modes for different use cases
- Implementing autonomous Gather → Act → Verify loops
- Setting up MCP servers for external integrations
- Managing context with subagent delegation

## Plugin Commands

This plugin provides agents, not slash commands. The agents automatically activate based on context:

| Agent | Namespace | Trigger Context |
|-------|-----------|-----------------|
| Python SDK Expert | `cce-anthropic:` | Python Agent SDK development |
| TypeScript SDK Expert | `cce-anthropic:` | TypeScript/Node.js Agent SDK |

## SDK Requirements

### Python SDK

```bash
# Python 3.10+ required
pip install claude-agent-sdk

# Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Environment
export ANTHROPIC_API_KEY="your-api-key"
```

### TypeScript SDK

```bash
# Node.js 18+ required
npm install @anthropic-ai/claude-agent-sdk zod

# Environment
export ANTHROPIC_API_KEY="your-api-key"
```

## Key Capabilities

### Python SDK Features
- **Query Pattern**: Unidirectional async iterations for batch tasks
- **Client Pattern**: Bidirectional conversations with state management
- **Custom Tools**: @tool decorator with direct Python state access
- **Async Runtimes**: Support for asyncio, trio, and anyio
- **Type Safety**: Full mypy strict mode compatibility
- **Web Frameworks**: FastAPI and Django Channels integration
- **Error Handling**: Comprehensive AbortError and exception patterns

### TypeScript SDK Features
- **Streaming**: Async generators for real-time responses
- **Type Safety**: Zod schemas for runtime validation
- **Permission Modes**: Fine-grained control over agent actions
- **Autonomous Patterns**: Built-in Gather → Act → Verify loops
- **MCP Integration**: createSdkMcpServer for external tools
- **Context Management**: Subagent delegation and compaction
- **Runtime Flexibility**: Node.js, Bun, and Deno support

## Architecture Patterns

### Python: Basic Query Pattern
```python
from claude_agent_sdk import query, tool, ClaudeAgentOptions
import anyio

@tool
async def custom_tool(data: str) -> str:
    """Custom tool with state access."""
    return f"Processed: {data}"

async def main():
    options = ClaudeAgentOptions(
        system_prompt="You are an assistant.",
        allowed_tools=["custom_tool"],
        permission_mode="acceptEdits"
    )

    async for event in query("Your prompt", options=options):
        if event.type == "text":
            print(event.content)

anyio.run(main)
```

### TypeScript: Streaming with Tools
```typescript
import { query, tool } from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod';

const customTool = tool({
  name: 'custom_tool',
  description: 'Process data',
  inputSchema: z.object({
    data: z.string().describe('Data to process')
  }),
  async execute({ input }) {
    return { result: `Processed: ${input.data}` };
  }
});

for await (const chunk of query('Your prompt', {
  tools: [customTool],
  permissions: 'acceptEdits'
})) {
  console.log(chunk);
}
```

## Best Practices

### Python Development
- Use anyio for runtime flexibility over asyncio
- Implement comprehensive error handling for AbortError
- Apply type hints with mypy strict mode
- Test tools and hooks independently
- Monitor context limits and API costs
- Use dataclasses for configuration
- Implement graceful shutdown handlers

### TypeScript Development
- Always use TypeScript strict mode
- Leverage Zod for runtime validation
- Design tools as primary actions, not utilities
- Implement verification in autonomous loops
- Use plan mode for safe exploration
- Manage context with subagent delegation
- Handle API errors with fallback strategies

## Documentation

- **Python SDK**: https://docs.claude.com/en/api/agent-sdk/python
- **TypeScript SDK**: https://docs.claude.com/en/api/agent-sdk/typescript
- **Plugin Source**: https://github.com/nodnarbnitram/claude-code-extensions
- **Bug Reports**: https://github.com/nodnarbnitram/claude-code-extensions/issues

## Version History

### 1.0.0 (Initial Release)
- Python Agent SDK expert agent
- TypeScript Agent SDK expert agent
- Comprehensive SDK pattern documentation
- Auto-trigger descriptions for both languages

## License

MIT License - See repository for details

## Contributing

Contributions welcome! See [CONTRIBUTING.md](https://github.com/nodnarbnitram/claude-code-extensions/blob/main/CONTRIBUTING.md) for guidelines.

## Support

For issues or questions:
1. Check the [official Claude Agent SDK documentation](https://docs.claude.com/en/api/agent-sdk)
2. Review agent system prompts in `.claude/agents/specialized/anthropic/`
3. Open an issue on the [GitHub repository](https://github.com/nodnarbnitram/claude-code-extensions/issues)

---

**Note**: The Claude Agent SDK was released in October 2025 and is rapidly evolving. Always verify against the latest official documentation for the most current patterns and best practices.
