# CCE Vite Plugin

Vitest 4 testing guidance for Vite projects, including Browser Mode, coverage, and migration patterns.

## Overview

The **cce-vite** plugin packages the repository's current Vite ecosystem testing expertise into a self-contained plugin for Claude Code. Right now it includes the `vitest-4` skill so marketplace installs can use the new Vitest guidance without depending on the repo-root `.claude` tree.

## Included Components

### Skill

- `vitest-4`

## Installation

### Plugin Mode

```bash
/plugin marketplace add github:nodnarbnitram/claude-code-extensions
/plugin install cce-vite@cce-marketplace
```

### Standalone Mode

```bash
git clone https://github.com/nodnarbnitram/claude-code-extensions.git
cd claude-code-extensions
# Install into your project, then select only the vitest-4 skill for Vite testing workflows
./install_extensions.py install ~/your-project
```

In standalone installs, keep the scope the same as the plugin package: install/select **only `vitest-4`** from this plugin's content rather than unrelated skills.

## Use Cases

- Creating or fixing `vitest.config.ts` in Vite projects
- Writing unit, integration, and Browser Mode tests with Vitest 4
- Configuring coverage, worker settings, and setup files
- Migrating older Jest or pre-Vitest-4 testing patterns
- Troubleshooting browser providers, mock leakage, and watch-mode hangs

## Structure

This plugin is self-contained under `plugins/cce-vite/` with a local `skills/` directory for marketplace installs.

## License

MIT License - see [LICENSE](../../LICENSE) for details.
