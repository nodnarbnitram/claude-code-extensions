# CCE Home Assistant Plugin

Home Assistant automation, integrations, dashboards, add-ons, APIs, voice, and energy workflows for Claude Code.

## Overview

The **cce-homeassistant** plugin packages the full Home Assistant toolkit into one self-contained plugin. It includes specialist agents for every major HA surface area plus the skills and commands needed to build automations, dashboards, integrations, energy setups, voice flows, and Frigate-assisted camera workflows.

## Included Components

### Agents (7)

- `ha-addon-developer`
- `ha-api-expert`
- `ha-automation-expert`
- `ha-dashboard-expert`
- `ha-energy-expert`
- `ha-integration-developer`
- `ha-voice-expert`

### Skills (8)

- `ha-addon`
- `ha-api`
- `ha-automation`
- `ha-dashboard`
- `ha-energy`
- `ha-integration`
- `ha-voice`
- `frigate-configurator`

### Commands (3)

- `/cce-homeassistant:ha-automation-lint`
- `/cce-homeassistant:ha-blueprint-create`
- `/cce-homeassistant:ha-integration-scaffold`

## Installation

### Plugin Mode

```bash
/plugin marketplace add github:nodnarbnitram/claude-code-extensions
/plugin install cce-homeassistant@cce-marketplace
```

### Standalone Mode

```bash
git clone https://github.com/nodnarbnitram/claude-code-extensions.git
cd claude-code-extensions
./install_extensions.py install ~/your-project
```

## What It Covers

- Lovelace dashboards and themes
- Automations, scripts, blueprints, and Jinja templates
- REST and WebSocket API integrations
- Custom integrations and config flows
- Add-on development with Docker and Supervisor APIs
- Assist pipelines, wake words, TTS/STT, and voice satellites
- Energy dashboards and utility meters
- Frigate configuration and object-detection workflows

## Structure

This plugin is now self-contained under `plugins/cce-homeassistant/` with local `agents/`, `skills/`, and `commands/` directories for marketplace installs.

## License

MIT License - see [LICENSE](../../../LICENSE) for details.
