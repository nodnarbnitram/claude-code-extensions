# CCE Python Plugin

Python CLI development with Typer for type-hint driven applications, validation, and testing.

## Overview

The **cce-python** plugin provides expert Typer CLI development capabilities for building robust, type-safe Python command-line applications with rich formatting, validation, and comprehensive testing.

## Features

- **Type-Hint Driven**: Automatic CLI generation from Python type hints
- **Rich Terminal UI**: Progress bars, tables, colors, panels via Rich integration
- **Validation**: Comprehensive input validation patterns
- **Testing**: pytest integration with Click's CliRunner
- **Documentation**: Auto-generated help from docstrings
- **Distribution**: Packaging for PyPI with setuptools/poetry

## Plugin Components

### Agents (1)

- **typer-expert**: Complete Typer CLI development specialist
  - Command structure and organization
  - Type annotations and validation
  - Rich terminal formatting
  - Configuration file handling
  - Testing strategies
  - Distribution and packaging

## Installation

### From Marketplace (Recommended)

```bash
# Add the CCE marketplace
/plugin marketplace add github:nodnarbnitram/claude-code-extensions

# Install Python plugin
/plugin install cce-python@cce-marketplace
```

### From Local Source

```bash
git clone https://github.com/nodnarbnitram/claude-code-extensions.git
/plugin marketplace add /path/to/claude-code-extensions
/plugin install cce-python@cce-marketplace
```

## Usage

### Agents (Automatic Activation)

```bash
> Create a Typer CLI app for managing tasks
# Uses typer-expert

> Add rich progress bars to the upload command
# Uses typer-expert with Rich integration

> Implement file path validation with type hints
# Uses typer-expert validation patterns

> Add comprehensive tests for the CLI commands
# Uses typer-expert testing strategies
```

### Example Workflows

**Basic CLI App:**
```bash
> Create a Typer app with commands: list, add, delete for managing tasks
# Generates type-hint driven CLI with automatic help
```

**Rich Terminal UI:**
```bash
> Add a progress bar for the file processing command using Rich
# Implements Progress context manager with rich formatting
```

**Validation:**
```bash
> Validate that the port argument is between 1024 and 65535
# Uses Annotated[int, typer.Argument(min=1024, max=65535)]
```

**Configuration:**
```bash
> Add support for reading config from ~/.myapp/config.toml
# Implements config loading with validation
```

**Testing:**
```bash
> Write pytest tests for all CLI commands using CliRunner
# Creates comprehensive test suite with fixtures
```

## Requirements

- **Claude Code**: Latest version
- **Python**: 3.11+ (for advanced type hints)
- **Typer**: 0.9.0+
- **Optional**: Rich (for terminal formatting), pytest (for testing)

## Key Capabilities

**Command Patterns:**
- Single command apps
- Multi-command apps with subcommands
- Command groups and nesting
- Callback functions for shared setup

**Type Annotations:**
- Automatic type conversion
- Optional parameters with defaults
- Variadic arguments (*args)
- Choices with Literal types
- Custom validators

**Rich Integration:**
- Progress bars
- Tables and panels
- Syntax highlighting
- Markdown rendering
- Prompts and confirmations

**Validation:**
- Range validation (min/max)
- File/path existence checks
- Email, URL validation patterns
- Custom validators with callbacks

**Testing:**
- CliRunner for command testing
- Fixture patterns for CLI apps
- Mocking external dependencies
- Output verification

## Example Code

```python
import typer
from typing import Annotated
from rich.progress import track

app = typer.Typer()

@app.command()
def process(
    files: Annotated[list[Path], typer.Argument(exists=True)],
    output: Annotated[Path, typer.Option("--output", "-o")],
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False
):
    """Process multiple files with progress tracking."""
    for file in track(files, description="Processing..."):
        # Processing logic
        if verbose:
            typer.echo(f"Processing {file}")
```

## License

MIT License - see [LICENSE](../../../LICENSE) for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/nodnarbnitram/claude-code-extensions/issues)
- **Documentation**: [Repository README](../../../README.md)
- **Typer Docs**: [typer.tiangolo.com](https://typer.tiangolo.com)
