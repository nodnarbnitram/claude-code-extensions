# Home Assistant Automation Skill

> Create, debug, and optimize Home Assistant automations, scripts, blueprints, and Jinja2 templates.

| | |
|---|---|
| **Status** | Production Ready |
| **Version** | 1.0.0 |
| **Last Updated** | 2025-12-31 |
| **Confidence** | 5/5 |
| **Domain** | Home Assistant |

## What This Skill Does

This skill provides comprehensive guidance for Home Assistant automation development, covering:
- **Automation YAML syntax** - Triggers, conditions, actions, and modes
- **Jinja2 templating** - Template syntax, filters, and debugging
- **Blueprint creation** - Converting automations to reusable blueprints
- **Scripts and actions** - Complex automation sequences and logic
- **Troubleshooting** - Common errors and debugging techniques

### Core Capabilities

- Create automations with correct YAML structure and best practices
- Write Jinja2 templates with proper variable references and filters
- Convert automations to blueprints with parameterized inputs
- Debug template syntax using Developer Tools
- Optimize automation modes for performance and reliability
- Handle complex action sequences with choose, repeat, parallel

## Auto-Trigger Keywords

### Primary Keywords
Exact terms that strongly trigger this skill:
- automation
- trigger
- condition
- action
- blueprint
- script
- jinja2
- template
- automation yaml
- ha automation

### Secondary Keywords
Related terms that may trigger in combination:
- home assistant
- state change
- entity
- service call
- automation mode
- yaml syntax
- device trigger
- automations.yaml

### Error-Based Keywords
Common error messages that should trigger this skill:
- "Invalid YAML in automations.yaml"
- "template error"
- "entity not found"
- "trigger not working"
- "blueprint input mismatch"
- "jinja2 syntax error"

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| Template shows "Error" in UI | Undefined variable or incorrect filter | Use `\| default()` filter and verify entity IDs in Developer Tools |
| Automation never triggers | Wrong entity ID or state value format | Verify exact state in States tab, use `for:` to prevent false triggers |
| Blueprint inputs don't work | Missing `!input` tag or wrong selector type | Use YAML 1.2 `!input` syntax, match selector to input type |
| Action fails silently | Missing target entity or wrong service name | Verify service exists with correct target format |
| Condition always false | Logic error in condition syntax | Use `and`/`or`/`not` operators correctly, test with template condition |

## When to Use

### Use This Skill For
- Creating new automations from requirements or specifications
- Converting standalone automations into reusable blueprints
- Debugging automation triggers, conditions, or actions
- Writing Jinja2 templates for dynamic values and logic
- Optimizing automation modes (single/restart/queued/parallel)
- Explaining automation YAML syntax and best practices

### Don't Use This Skill For
- Installing Home Assistant or integration setup
- Dashboard UI configuration (use ha-dashboard skill)
- Frigate camera setup or NVR configuration (use frigate-configurator skill)
- General Home Assistant troubleshooting unrelated to automations

## Quick Usage

### Test a Jinja2 Template
Use Developer Tools > Template in Home Assistant UI:
```jinja2
{{ states('light.bedroom') }}
{{ state_attr('light.bedroom', 'brightness') }}
{{ (now() | as_timestamp) | round(0) }}
```

### Basic Automation
```yaml
- alias: "Turn on bedroom light at sunset"
  trigger:
    platform: sun
    event: sunset
  action:
    - service: light.turn_on
      target:
        entity_id: light.bedroom
      data:
        brightness: 200
```

### Automation with Condition
```yaml
- alias: "Turn off lights if away"
  trigger:
    platform: state
    entity_id: person.john
    to: not_home
  condition:
    - condition: numeric_state
      entity_id: sensor.house_brightness
      below: 100
  action:
    - service: light.turn_off
      target:
        entity_id: light.bedroom
```

## Token Efficiency

| Approach | Estimated Tokens | Time |
|----------|-----------------|------|
| Manual Implementation | ~2500 | 20-30 min |
| With This Skill | ~1200 | 5-10 min |
| **Savings** | **50%** | **15-25 min** |

The skill prevents syntax errors, suggests best practices, and provides ready-to-use patterns.

## File Structure

```
ha-automation/
├── SKILL.md        # Complete instruction set and reference
├── README.md       # This file - auto-trigger keywords and quick start
└── [future] references/  # Advanced reference documentation
```

## Dependencies

No external dependencies required. This skill uses built-in Home Assistant features:
- YAML configuration
- Jinja2 templating engine (included in Home Assistant)
- Blueprint system (available in Home Assistant 2021.1+)

## Official Documentation

- [Home Assistant Automation](https://www.home-assistant.io/docs/automation/)
- [Jinja2 Templating](https://www.home-assistant.io/docs/automation/templating/)
- [Blueprint Documentation](https://www.home-assistant.io/docs/blueprint/)
- [Script Integration](https://www.home-assistant.io/docs/scripts/)
- [Developer Tools](https://www.home-assistant.io/docs/developer-tools/)

## Related Skills

- `ha-dashboard` - Configure Lovelace dashboards and UI
- `frigate-configurator` - Set up Frigate NVR with cameras

---

**License:** MIT
