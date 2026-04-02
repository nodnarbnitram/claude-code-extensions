# Home Assistant Dashboard Skill

> Configure Lovelace dashboards, cards, views, and themes for Home Assistant.

| | |
|---|---|
| **Status** | Active |
| **Version** | 1.0.0 |
| **Last Updated** | 2025-12-17 |
| **Confidence** | 4/5 |
| **Production Tested** | Home Assistant 2024.x+ |

## What This Skill Does

Provides expert guidance for configuring Home Assistant Lovelace dashboards, including card selection, view layouts, theming, and custom card development.

### Core Capabilities

- Dashboard and view configuration (Masonry, Panel, Sections, Sidebar layouts)
- Built-in card configuration (40+ card types)
- Theme customization and CSS variables
- Custom card development guidance (LitElement/web components)
- HACS frontend integration recommendations

## Auto-Trigger Keywords

### Primary Keywords
Exact terms that strongly trigger this skill:
- lovelace
- dashboard
- card
- view
- theme
- panel

### Secondary Keywords
Related terms that may trigger in combination:
- tile
- button-card
- mushroom
- mini-graph-card
- entities card
- glance
- gauge
- weather-forecast
- picture-elements
- horizontal-stack
- vertical-stack
- conditional
- yaml mode

### Error-Based Keywords
Common error messages that should trigger this skill:
- "Unknown card type"
- "card configuration invalid"
- "Custom element doesn't exist"
- "Invalid YAML"
- "Entity not found"

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| YAML indentation errors | Using tabs or inconsistent spacing | Always use 2-space indentation |
| Unknown card type | Custom card not loaded | Add resource to `lovelace.resources` |
| Entity unavailable | Incorrect entity ID format | Use `domain.entity_name` format |
| Theme not applying | Wrong variable name or syntax | Check CSS variable spelling |
| Blank dashboard | YAML syntax error | Validate YAML before reloading |

## When to Use

### Use This Skill For
- Creating or modifying Lovelace dashboards
- Configuring cards (entities, buttons, tiles, gauges, etc.)
- Setting up view layouts (masonry, panel, sections, sidebar)
- Applying or creating themes
- Developing custom Lovelace cards
- Troubleshooting dashboard display issues

### Don't Use This Skill For
- Home Assistant automations and scripts
- Integration setup and configuration
- Backend YAML configuration (not dashboard-related)
- Add-on installation and management
- Entity configuration (device/entity settings)

## Quick Usage

```yaml
# Basic dashboard with entities card
views:
  - title: Home
    cards:
      - type: entities
        title: Lights
        entities:
          - light.living_room
          - light.bedroom
```

## Token Efficiency

| Approach | Estimated Tokens | Time |
|----------|-----------------|------|
| Manual Implementation | ~8000 | 30+ min |
| With This Skill | ~4800 | 10 min |
| **Savings** | **40%** | **20+ min** |

## File Structure

```
ha-dashboard/
├── SKILL.md        # Detailed instructions and patterns
├── README.md       # This file - discovery and quick reference
├── references/     # Supporting documentation
│   ├── card-reference.md     # Built-in card YAML examples
│   ├── view-types.md         # View layout comparison
│   ├── theme-variables.md    # CSS variables for theming
│   └── common-patterns.md    # Conditionals, stacks, entity rows
└── assets/
    ├── dashboard-template.yaml   # Starter dashboard config
    └── card-snippets.yaml        # Copy-paste card configs
```

## Dependencies

| Package | Version | Verified |
|---------|---------|----------|
| Home Assistant | 2023.1+ | 2025-12-17 |

## Official Documentation

- [Dashboards Overview](https://www.home-assistant.io/dashboards/)
- [Card Types](https://www.home-assistant.io/dashboards/cards/)
- [Views](https://www.home-assistant.io/dashboards/views/)
- [Themes](https://www.home-assistant.io/integrations/frontend/)
- [Custom Cards (Developer)](https://developers.home-assistant.io/docs/frontend/custom-ui/lovelace-custom-card)

## Related Skills

- `ha-automation` - Home Assistant automations and scripts (if available)
- `ha-integration` - Home Assistant integration setup (if available)

---

**License:** MIT
