# Contributing to Claude Code Extensions

Thank you for your interest in contributing to Claude Code Extensions! This project thrives on community contributions—whether you're fixing bugs, adding new agents, improving documentation, or sharing feedback.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [License](#license)
- [Ways to Contribute](#ways-to-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Creating Extensions](#creating-extensions)
- [Testing Your Changes](#testing-your-changes)
- [Submitting Changes](#submitting-changes)
- [Style Guidelines](#style-guidelines)
- [Community](#community)

## Code of Conduct

This project follows the Contributor Covenant Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

**In short**: Be respectful, inclusive, and constructive. We're all here to build better tools together.

## License

This project is licensed under the **[MIT License](https://opensource.org/licenses/MIT)**.

### What This Means for Contributors

**By contributing, you agree that:**
- Your contributions will be licensed under MIT License
- Anyone can use your contributions for any purpose, including commercial use
- Your contributions remain free and open source
- Attribution to contributors is maintained

This is one of the most permissive open-source licenses - it maximizes adoption and lets anyone build on this work.

## Ways to Contribute

### 🐛 Report Bugs

Found a bug? Please [open an issue](../../issues/new) with:

- **Clear title** describing the problem
- **Steps to reproduce** the behavior
- **Expected behavior** vs. actual behavior
- **Environment details** (OS, Claude Code version, Python version)
- **Relevant logs** from `.claude/logs/` if applicable

### 💡 Suggest Features

Have an idea for a new agent, hook, or command? We'd love to hear it!

- [Open a feature request](../../issues/new)
- Describe the use case and problem it solves
- If proposing an agent, explain what domain expertise it would provide
- Check existing issues first to avoid duplicates

### 📝 Improve Documentation

Documentation improvements are always welcome:

- Fix typos or clarify confusing sections
- Add examples or use cases
- Improve README or CLAUDE.md
- Create tutorials or guides

### 🛠️ Add New Extensions

The best contributions are new, high-quality extensions:

- **Agents**: Specialized AI assistants for specific domains
- **Hooks**: Lifecycle automation for safety, logging, or workflows
- **Commands**: Reusable slash commands for common tasks
- **Output Styles**: Custom system prompts for different behaviors

### 🔍 Review Pull Requests

Help review open PRs—test changes, provide feedback, suggest improvements.

## Getting Started

### Prerequisites

- [Claude Code](https://claude.ai/code) CLI installed
- [uv](https://github.com/astral-sh/uv) for Python dependency management
- Python 3.11 or higher
- Git for version control

### Fork and Clone

1. **Fork this repository** on GitHub
2. **Clone your fork locally**:

   ```bash
   git clone https://github.com/YOUR-USERNAME/claude-code-extensions.git
   cd claude-code-extensions
   ```

3. **Add upstream remote**:

   ```bash
   git remote add upstream https://github.com/ORIGINAL-OWNER/claude-code-extensions.git
   ```

### Install Development Tools

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python (if needed)
uv python install 3.11

# Test the installer
./install_extensions.py --help
```

## Development Workflow

### Creating a Branch

Always create a new branch for your work:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

**Branch naming conventions**:
- `feature/` - New features or extensions
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions or improvements

### Keeping Your Fork Updated

Regularly sync with the upstream repository:

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## Creating Extensions

### Creating Agents

**Use the meta-agent** for best results:

```bash
# In Claude Code, from this repository
> Use the meta-agent to create a [description] expert agent
```

The meta-agent will:
- Fetch latest Claude Code documentation
- Generate a complete, production-ready agent
- Write to `.claude/agents/` with proper structure

**Manual creation**:

1. Choose the right category: `core/`, `orchestrators/`, `universal/`, or `specialized/<tech>/`
2. Use this template:

```markdown
---
name: your-agent-name
description: When this agent should be invoked (be specific and action-oriented)
tools: Read, Grep, Glob, Bash  # Optional - omit to inherit all tools
---

# Agent System Prompt

Your agent's instructions here...
```

3. Follow the [agent best practices](#agent-guidelines)

### Creating Hooks

1. **Choose the right lifecycle event**: PreToolUse, PostToolUse, SessionStart, UserPromptSubmit, PreCompact, Stop, SubagentStop, Notification

2. **Use Python with uv script format**:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

import json
import sys

def main():
    try:
        input_data = json.load(sys.stdin)
        # Your hook logic here
        sys.exit(0)  # 0 = success, 2 = block operation
    except Exception:
        sys.exit(0)  # Always fail gracefully

if __name__ == '__main__':
    main()
```

3. **Make it executable**: `chmod +x .claude/hooks/your_hook.py`

4. **Test it locally** (see [Testing Hooks](#testing-hooks))

### Creating Commands

1. Create a markdown file in `.claude/commands/`:

```markdown
---
description: Brief description of what this command does
argument-hint: [arg1] [arg2]  # Optional
allowed-tools: Bash(git:*)  # Optional
model: claude-3-5-haiku-20241022  # Optional
---

Your command prompt here. Use:
- $ARGUMENTS for all arguments
- $1, $2, $3 for individual arguments
- @file/path for file references
- !`bash command` for executed commands
```

2. Test the command: `/your-command-name`

### Creating Output Styles

1. Create a markdown file in `.claude/output-styles/`:

```markdown
---
name: Style Name
description: Brief description of what this style does
---

# Custom System Prompt

You are an interactive CLI tool that helps users with [specific purpose].

## Behaviors

[Define specific behaviors, tone, output format]
```

## Testing Your Changes

### Testing Hooks

Create test input and verify exit codes:

```bash
# Example: Test pre_tool_use.py
echo '{"tool_name": "Bash", "tool_input": {"command": "ls"}}' > test.json
uv run ./.claude/hooks/pre_tool_use.py < test.json
echo $?  # Should be 0 (allow) or 2 (block)

# Test with dangerous command
echo '{"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}}' > test.json
uv run ./.claude/hooks/pre_tool_use.py < test.json
echo $?  # Should be 2 (blocked)
```

### Testing Agents

1. Install the agent in a test project:

   ```bash
   ./install_extensions.py install --type agent --category core ~/test-project
   ```

2. Test invocation in Claude Code:

   ```
   > Use the [your-agent-name] agent to [perform task]
   ```

3. Verify it produces expected results and follows its instructions

### Testing Commands

```bash
# In Claude Code
/your-command-name arg1 arg2
```

### Testing the Installer

```bash
# Dry run to preview changes
./install_extensions.py install --dry-run ~/test-project

# Test specific extension type
./install_extensions.py install --type hook --no-interactive ~/test-project
```

## Plugin Development

This repository supports both **plugin** and **standalone** installation modes. When making changes, ensure compatibility with both.

### Plugin Structure

The repository provides **5 focused plugins** (Phase 1):
- `cce-core` - Essential foundation
- `cce-kubernetes` - Kubernetes operations
- `cce-cloudflare` - Cloudflare development
- `cce-esphome` - ESPHome IoT
- `cce-web-react` - React ecosystem

Each plugin has a manifest at `.claude-plugin/plugins/<name>/plugin.json`.

### When to Update Plugin Versions

Follow semantic versioning for plugin manifests:

- **MAJOR (2.0.0)**: Breaking changes to plugin structure or extension APIs
- **MINOR (1.1.0)**: New agents, skills, commands, hooks (backward-compatible additions)
- **PATCH (1.0.1)**: Bug fixes, documentation updates, hook improvements

**Version synchronization**:
- Update version in ALL affected plugin manifests (`.claude-plugin/plugins/*/plugin.json`)
- Update marketplace version (`.claude-plugin/marketplace.json`)
- Create git tag: `git tag -a v1.1.0 -m "Description"`

### Assigning Extensions to Plugins

When adding new extensions, assign them to the correct plugin:

| Extension Type | Plugin Assignment |
|----------------|-------------------|
| Core agents (code-reviewer, etc.) | cce-core |
| Framework agents (react, vue, django) | cce-web-react, cce-web-vue, cce-django |
| Platform agents (cloudflare, k8s) | cce-cloudflare, cce-kubernetes |
| IoT agents (esphome) | cce-esphome |
| Hooks, core commands | cce-core |
| Domain-specific skills/commands | Corresponding domain plugin |

### Testing Plugin Changes

```bash
# 1. Validate plugin structure
/plugin validate .

# 2. Test plugin mode installation
/plugin marketplace add /path/to/claude-code-extensions
/plugin install cce-core@cce-marketplace

# 3. Test with namespaced commands
/cce:git-commit

# 4. Test standalone mode (existing workflow)
./install_extensions.py install --dry-run ~/test-project
./install_extensions.py install ~/test-project

# 5. Verify dual-mode compatibility
cd ~/test-project && claude
> /git-commit  # Should work unprefixed in standalone mode
```

**Critical**: Always test both plugin and standalone modes to ensure backward compatibility.

### Hook Path Syntax

When modifying hooks, use the dual-mode path syntax:

```json
{
  "command": "uv run \"${CLAUDE_PLUGIN_ROOT:-$CLAUDE_PROJECT_DIR}\"/.claude/hooks/your_hook.py"
}
```

This syntax works in both:
- **Plugin mode**: Uses `${CLAUDE_PLUGIN_ROOT}` (plugin cache path)
- **Standalone mode**: Falls back to `$CLAUDE_PROJECT_DIR` (project path)

## Submitting Changes

### Before You Submit

- [ ] **Test your changes** thoroughly
- [ ] **Update documentation** (README.md, CLAUDE.md, or create new docs)
- [ ] **Follow style guidelines** (see below)
- [ ] **Update the README** if adding new extensions
- [ ] **Check for typos** and formatting issues
- [ ] **Ensure hooks fail gracefully** (always `sys.exit(0)` on errors)
- [ ] **Verify agents have clear descriptions** with "MUST BE USED" or "use PROACTIVELY" where appropriate
- [ ] **Validate plugin structure** if modifying plugin manifests: `/plugin validate .`
- [ ] **Test dual-mode compatibility** if modifying hooks or core extensions
- [ ] **Update plugin versions** if making breaking changes (see Plugin Development below)

### Commit Messages

Write clear, descriptive commit messages following conventional commits:

```
type(scope): Brief description

Longer description if needed, explaining:
- Why this change is necessary
- What problem it solves
- Any breaking changes or important notes
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples**:
- `feat(agents): add security audit specialist agent`
- `fix(hooks): prevent pre_tool_use from crashing on missing fields`
- `docs(readme): clarify installation instructions`
- `refactor(installer): improve settings.json merge logic`

### Pull Request Process

1. **Push your branch** to your fork:

   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open a Pull Request** on GitHub

3. **Fill out the PR template** with:
   - Clear description of changes
   - Related issue numbers (e.g., "Fixes #123")
   - Testing steps you performed
   - Screenshots or examples if applicable

4. **Wait for review**:
   - Maintainers will review your PR
   - Address any requested changes
   - Be responsive to feedback

5. **Squash commits** if requested before merging

### What Happens Next?

- **Automated checks** may run (if configured)
- **Maintainers review** your code and provide feedback
- **Iterate** on feedback until approved
- **Merge** - Your contribution becomes part of the project!

## Style Guidelines

### Agent Guidelines

- **Single responsibility**: Each agent should have one clear purpose
- **Explicit triggers**: Use "MUST BE USED" or "use PROACTIVELY" in descriptions
- **Tool restrictions**: Only grant necessary tools for security and focus
- **Clear instructions**: Write step-by-step workflows in the system prompt
- **Delegation patterns**: Orchestrators delegate; specialists implement
- **Output formats**: Define structured output for reports/analysis

### Hook Guidelines

- **Fail gracefully**: Always `sys.exit(0)` on errors to prevent blocking Claude Code
- **Log everything**: Append to `logs/<hook_name>.json` for audit trails
- **Fast execution**: Hooks should complete quickly (< 1 second ideal)
- **Use type hints**: Make Python code maintainable with proper typing
- **Document safety**: Explain any blocking logic in comments

### Command Guidelines

- **Clear argument hints**: Use `argument-hint` to guide users
- **Minimal tool access**: Only request `allowed-tools` you need
- **Self-documenting**: Write clear prompts that explain what they do
- **Examples in description**: Help users understand when to use the command

### Python Code Style

- **PEP 8 compliant**: Follow Python style guidelines
- **Use type hints**: Improve code clarity and catch errors
- **Descriptive names**: Functions and variables should be self-documenting
- **Comments for "why"**: Explain reasoning, not what (code shows what)
- **Error handling**: Catch specific exceptions, always have fallbacks

### Documentation Style

- **Clear headings**: Use proper markdown hierarchy
- **Code examples**: Include working examples for every feature
- **Concise**: Get to the point quickly
- **Scannable**: Use bullets, tables, and formatting for easy reading
- **Complete**: Don't assume prior knowledge

## Community

### Getting Help

- **GitHub Discussions**: Ask questions, share ideas
- **Issues**: Bug reports and feature requests
- **Claude Code Docs**: [Official documentation](https://docs.anthropic.com/en/docs/claude-code)

### Recognition

Contributors are recognized in several ways:

- Listed in GitHub contributors
- Mentioned in release notes for significant contributions
- Credit in documentation for major features

### Contributor Rights

By contributing, you:
- Retain copyright to your contributions
- License your contributions under the MIT License
- Allow anyone to use, modify, and distribute your contributions freely
- Understand this is a volunteer, open-source project

Your contributions become part of the free and open-source ecosystem.

## Questions?

If you have questions about contributing, please:

1. Check existing documentation and issues
2. Ask in GitHub Discussions
3. Reach out to maintainers via issue comments

**Thank you for making Claude Code Extensions better!** 🎉
