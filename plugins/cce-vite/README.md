# CCE Vite Plugin

Vite v8 and Vitest v4 guidance for Vite projects, including config, plugins, Browser Mode, coverage, and migration patterns.

## Overview

The **cce-vite** plugin packages the repository's current Vite ecosystem expertise into a self-contained plugin for Claude Code. It includes the `vite-v8` and `vitest-v4` skills so marketplace installs can use both build/runtime and test-runner guidance without depending on the repo-root `.claude` tree.

## Included Components

### Skill

- `vite-v8`
- `vitest-v4`

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
# Install into your project, then select the vite-v8 and/or vitest-v4 skills for your Vite workflows
./install_extensions.py install ~/your-project
```

In standalone installs, keep the scope the same as the plugin package: install/select **only `vite-v8` and `vitest-v4`** from this plugin's content rather than unrelated skills.

## Use Cases

- Configuring and migrating `vite.config.ts` for Vite 8
- Authoring or debugging Vite plugins with environments, hook filters, and modern HMR hooks
- Creating or fixing `vitest.config.ts` in Vite projects
- Writing unit, integration, and Browser Mode tests with Vitest 4
- Configuring coverage, worker settings, and setup files
- Migrating older Rollup/esbuild or pre-Vitest-4 patterns
- Troubleshooting browser providers, mock leakage, and watch-mode hangs

## Structure

This plugin is self-contained under `plugins/cce-vite/` with a local `skills/` directory for marketplace installs.

## License

MIT License - see [LICENSE](../../LICENSE) for details.
