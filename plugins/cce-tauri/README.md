# CCE Tauri Plugin

Tauri v2 desktop and mobile app development with Rust backend, IPC, capabilities, and security guidance.

## Overview

The **cce-tauri** plugin packages the repository's Tauri expertise into a self-contained plugin for Claude Code. It includes the Tauri specialist agent and the `tauri-v2` skill so marketplace installs work without depending on the repo-root `.claude` tree.

## Included Components

### Agent

- `tauri-v2-expert`

### Skill

- `tauri-v2`

## Installation

### Plugin Mode

```bash
/plugin marketplace add github:nodnarbnitram/claude-code-extensions
/plugin install cce-tauri@cce-marketplace
```

### Standalone Mode

```bash
git clone https://github.com/nodnarbnitram/claude-code-extensions.git
cd claude-code-extensions
./install_extensions.py install ~/your-project
```

## Use Cases

- IPC command design with `#[tauri::command]`
- Frontend/backend boundary design for Rust + web UI apps
- Capability and permission configuration
- Multi-window apps, plugins, and sidecars
- Build, packaging, and security troubleshooting

## Structure

This plugin is self-contained under `plugins/cce-tauri/` with local `agents/` and `skills/` directories for marketplace installs.

## License

MIT License - see [LICENSE](../../../LICENSE) for details.
