# cce-temporal

Temporal.io workflow development across Python, Go, and TypeScript SDKs with comprehensive testing and troubleshooting support.

## Overview

The **cce-temporal** plugin provides a complete suite of specialized agents for Temporal.io development, covering all major SDKs and critical development workflows. Whether you're building durable workflows in Python, Go, or TypeScript, this plugin provides expert guidance on implementation, testing, and troubleshooting.

## Features

### Multi-SDK Support
- **Python SDK** (v1.18.0+): AsyncIO patterns, pytest testing, activity execution modes
- **Go SDK** (v1.36.0+): Workflow-safe primitives, determinism patterns, testsuite framework
- **TypeScript SDK** (v1.13.0+): Type-safe proxyActivities, Jest testing, Promise patterns

### Comprehensive Agent Suite

This plugin includes **6 specialized agents** that automatically activate based on context:

1. **temporal-core**: Universal Temporal concepts and architecture patterns
2. **temporal-python**: Python SDK specialist for async/await patterns
3. **temporal-go**: Go SDK specialist for workflow-safe concurrency
4. **temporal-typescript**: TypeScript SDK specialist for type-safe development
5. **temporal-testing**: Cross-SDK testing strategies and patterns
6. **temporal-troubleshooting**: Error diagnosis and production debugging

### Key Capabilities

- **Workflow Development**: Implement deterministic workflows following best practices
- **Activity Patterns**: Create idempotent activities with proper retry strategies
- **Testing Strategies**: Unit tests, integration tests, replay tests, and CI/CD setup
- **Troubleshooting**: Diagnose non-determinism, payload limits, history size issues
- **Performance**: Optimize schedule-to-start latency and worker efficiency
- **Architecture**: Saga patterns, Continue-As-New, child workflow partitioning

## Installation

### Via Plugin Marketplace

```bash
# Add the CCE marketplace (if not already added)
/plugin marketplace add https://github.com/nodnarbnitram/claude-code-extensions

# Install the Temporal plugin
/plugin install cce-temporal@cce-marketplace
```

### From Local Repository

```bash
# Clone the repository
git clone https://github.com/nodnarbnitram/claude-code-extensions.git
cd claude-code-extensions

# Add local marketplace
/plugin marketplace add /path/to/claude-code-extensions

# Install plugin
/plugin install cce-temporal@cce-marketplace
```

## Usage

The agents in this plugin activate automatically based on context. You can also explicitly invoke them:

### Automatic Activation

The agents will automatically activate when you:
- Ask about Temporal workflows, activities, or architecture
- Request help with Python/Go/TypeScript SDK implementation
- Need testing strategies or debugging assistance
- Mention specific Temporal concepts (determinism, signals, queries, etc.)

### Explicit Invocation

You can call agents directly using the `@` syntax:

```
@temporal-core explain workflow versioning strategies
@temporal-python help me implement an async workflow
@temporal-go fix this map iteration non-determinism
@temporal-typescript configure proxyActivities with type safety
@temporal-testing create pytest tests with time-skipping
@temporal-troubleshooting diagnose this "workflow task failed" error
```

### Command Namespacing

Commands are namespaced as `/cce-temporal:*`:

```bash
# Example: If future commands are added
/cce-temporal:workflow-init
/cce-temporal:test-replay
```

## Agent Details

### temporal-core
**Universal Temporal expert for core concepts applicable across all SDKs**

Covers:
- Workflows vs Activities decision matrix
- Task queues and routing patterns
- Determinism requirements and anti-patterns
- Retry policies and error handling
- Versioning strategies (Worker Versioning, Patching)
- Continue-As-New pattern for long-running workflows
- Saga pattern for distributed transactions

### temporal-python
**Python SDK specialist (v1.18.0+)**

Covers:
- Async/await patterns with AsyncIO
- Activity execution modes (async, threaded, multiprocess)
- Common pitfalls: blocking libraries, gevent incompatibility
- Pytest integration with WorkflowEnvironment
- Time-skipping for long-duration workflows
- Exception handling with ApplicationError
- Type hints and dataclass patterns

### temporal-go
**Go SDK specialist (v1.36.0+)**

Covers:
- Workflow-safe primitives (workflow.Go, workflow.Channel, workflow.Select)
- Map iteration determinism (sorting required)
- Context patterns (workflow.Context vs context.Context)
- Interface-based activity definitions
- Testing with testsuite package
- Selector pattern for multi-channel operations
- Common non-determinism errors

### temporal-typescript
**TypeScript SDK specialist (v1.13.0+)**

Covers:
- Type-safe proxyActivities with full inference
- defineSignal/defineQuery patterns
- Jest testing configuration (Node environment required)
- Common pitfalls: missing startToCloseTimeout
- Monorepo package structure (@temporalio/*)
- Promise-based async patterns
- Time-skipping tests with TestWorkflowEnvironment

### temporal-testing
**Cross-SDK testing specialist**

Covers:
- Testing pyramid (unit, integration, replay tests)
- Time-skipping for fast workflow tests
- Activity mocking strategies
- Replay testing against production histories
- CI/CD integration (GitHub Actions, GitLab CI)
- Docker Compose test environments
- Signal/query testing patterns

### temporal-troubleshooting
**Error diagnosis and debugging specialist**

Covers:
- Non-determinism error diagnosis (most common issue)
- Workflow task failures and infinite retries
- Payload size limit errors (2MB/4MB/50MB limits)
- History size limit errors (51,200 events / 50MB)
- AsyncIO blocking issues (Python-specific)
- Performance troubleshooting (schedule-to-start latency)
- Temporal Web UI and CLI debugging tools

## Common Workflows

### Creating a New Workflow

```python
# Python example - agent provides complete guidance
> I need to create a workflow that processes payments with retry logic

# The temporal-python agent will guide you through:
# 1. Workflow definition with @workflow.defn
# 2. Activity implementation for payment processing
# 3. Proper timeout configuration
# 4. Retry policies
# 5. Error handling with ApplicationError
# 6. Pytest tests with mocked activities
```

### Debugging Non-Determinism

```
> I'm getting "Workflow execution history doesn't match workflow definition"

# The temporal-troubleshooting agent will:
# 1. Identify common non-deterministic patterns
# 2. Check for time/random functions
# 3. Verify workflow-safe primitives usage
# 4. Suggest replay testing setup
# 5. Provide SDK-specific fixes
```

### Testing Strategies

```
> How do I test a workflow that sleeps for 7 days?

# The temporal-testing agent will:
# 1. Demonstrate time-skipping environments
# 2. Provide complete test examples for your SDK
# 3. Show activity mocking patterns
# 4. Configure CI/CD integration
# 5. Set up replay testing
```

## SDK Version Compatibility

- **Python**: v1.18.0+ (requires Python 3.9+, 3.13 supported)
- **Go**: v1.36.0+ (built-in slog integration)
- **TypeScript**: v1.13.0+ (monorepo structure with @temporalio/* packages)

## Best Practices Enforced

The agents in this plugin enforce Temporal best practices:

1. **Determinism First**: All workflow code must be deterministic
2. **Activities for Side Effects**: External calls, I/O, non-deterministic operations go in activities
3. **Idempotent Activities**: Design for unlimited retries by default
4. **Proper Timeouts**: Always set activity timeouts (especially TypeScript)
5. **Continue-As-New**: Implement for workflows approaching history limits
6. **Replay Testing**: Test code changes against production histories before deployment
7. **Type Safety**: Leverage SDK type systems (especially TypeScript)
8. **Testing Pyramid**: 70% unit, 20% integration, 10% E2E tests

## Troubleshooting

### Common Issues

**"Agents not loading"**
- Verify plugin installed: `/plugin list`
- Check installation: `/plugin install cce-temporal@cce-marketplace`
- Restart Claude Code session

**"Wrong agent activating"**
- Agents delegate based on context
- Explicitly invoke with `@temporal-<agent-name>`
- Core agent delegates to SDK specialists automatically

**"Missing SDK-specific guidance"**
- Mention your SDK explicitly: "using Python SDK" or "TypeScript Temporal"
- Check SDK version compatibility above
- SDK specialists auto-activate on SDK keywords

## Contributing

This plugin is part of the [claude-code-extensions](https://github.com/nodnarbnitram/claude-code-extensions) project.

To contribute:
1. Fork the repository
2. Create agents in `.claude/agents/specialized/temporal/`
3. Update plugin manifest if adding new agents
4. Test with `/plugin validate .`
5. Submit pull request

## Documentation

### Official Temporal Docs
- [Temporal Documentation](https://docs.temporal.io/)
- [Python SDK](https://github.com/temporalio/sdk-python)
- [Go SDK](https://github.com/temporalio/sdk-go)
- [TypeScript SDK](https://github.com/temporalio/sdk-typescript)

### Agent Reference
All agents are documented with:
- When to use (description field)
- Core competencies
- Common patterns
- Anti-patterns to avoid
- Delegation strategy

See agent source files in `.claude/agents/specialized/temporal/` for complete documentation.

## License

MIT License - See repository LICENSE file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/nodnarbnitram/claude-code-extensions/issues)
- **Discussions**: [GitHub Discussions](https://github.com/nodnarbnitram/claude-code-extensions/discussions)
- **Temporal Community**: [community.temporal.io](https://community.temporal.io/)

## Changelog

### v1.0.0 (Initial Release)
- 6 specialized agents covering all major SDKs
- Universal architecture guidance (temporal-core)
- Python SDK specialist (v1.18.0+)
- Go SDK specialist (v1.36.0+)
- TypeScript SDK specialist (v1.13.0+)
- Comprehensive testing strategies
- Production troubleshooting and debugging
