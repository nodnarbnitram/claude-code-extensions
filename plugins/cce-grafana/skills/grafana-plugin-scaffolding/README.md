# Grafana Plugin Scaffolding Skill

Automates Grafana plugin project creation using the official `@grafana/create-plugin` scaffolder.

## Overview

This skill handles:
- Project scaffolding for all plugin types (panel, data source, app, backend)
- Docker-based development environment setup
- Initial plugin configuration
- Development workflow automation

## Auto-Trigger Keywords

### Primary Keywords
- grafana plugin
- create-plugin
- panel plugin
- data source plugin
- datasource plugin
- app plugin
- grafana scaffolding
- scaffold grafana

### Secondary Keywords
- grafana development
- plugin scaffolding
- grafana sdk
- grafana-plugin-sdk
- @grafana/create-plugin
- plugin-e2e
- grafana playwright

### Error Pattern Keywords
- plugin not appearing
- grafana plugin unsigned
- backend plugin error
- plugin.json invalid
- gpx binary missing

## Requirements

- Node.js v18+
- npm or pnpm
- Docker (optional, recommended for development)
- Go 1.21+ (for backend plugins)

## Files

```
grafana-plugin-scaffolding/
├── SKILL.md          # Main skill instructions
├── README.md         # This file
├── scripts/
│   ├── create_plugin.sh   # Plugin scaffolding wrapper
│   └── dev_server.sh      # Docker dev environment
├── templates/
│   ├── docker-compose.yaml    # Docker Compose with watch/hot-reload
│   ├── panel-plugin.json      # Panel plugin config template
│   ├── datasource-plugin.json # Data source config template
│   ├── app-plugin.json        # App plugin config template
│   └── backend-plugin.json    # Backend plugin config template
└── references/
    ├── sdk-patterns.md        # Common SDK patterns (v12.x+)
    ├── e2e-testing.md         # Playwright E2E testing with @grafana/plugin-e2e
    ├── troubleshooting.md     # Common issues and solutions
    ├── plugin-types.md        # When to use each plugin type
    └── signing-publishing.md  # Guide to signing/publishing
```

## Usage

This skill auto-triggers when users mention Grafana plugin development. For complex architectural decisions, the skill delegates to the `grafana-plugin-expert` agent.

## Version Support

**Grafana v12.x+ only** - For older versions, consult official migration guides.
