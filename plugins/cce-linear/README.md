# CCE Linear Plugin

Linear ticket, project, milestone, document, and PR coordination workflows for Claude Code.

## Overview

The **cce-linear** plugin packages the repository's Linear workflow tooling into a self-contained plugin. It includes the `linear` skill with wrapper scripts for `linearis`, plus commands for triage and Linear-linked PR creation.

## Included Components

### Skill

- `linear`

### Commands

- `/cce-linear:triage`
- `/cce-linear:create-linear-pr`
- `/cce-linear:existing-linear`

## Installation

### Plugin Mode

```bash
/plugin marketplace add github:nodnarbnitram/claude-code-extensions
/plugin install cce-linear@cce-marketplace
```

### Standalone Mode

```bash
git clone https://github.com/nodnarbnitram/claude-code-extensions.git
cd claude-code-extensions
./install_extensions.py install ~/your-project
```

## Requirements

- `linearis` CLI installed
- `LINEAR_API_TOKEN` configured
- `gh` CLI authenticated for PR flows

## Structure

This plugin is self-contained under `plugins/cce-linear/` with local `commands/` and `skills/linear/` content for marketplace installs.

## License

MIT License - see [LICENSE](../../../LICENSE) for details.
