---
allowed-tools: Read, Write
argument-hint: <automation-id-or-file>
description: Convert a Home Assistant automation into a reusable blueprint
---

# Create Home Assistant Blueprint

Convert an existing Home Assistant automation into a reusable blueprint: $ARGUMENTS

## Your Task

Transform the specified automation into a parameterizable blueprint by analyzing its structure and identifying which values should become inputs with appropriate selectors.

### Step 1: Analyze the Automation

**Location**: The argument can be:
- An automation file path (e.g., `/path/to/automation.yaml`)
- An automation ID from `automations.yaml` (we'll help you locate it)
- A direct YAML automation configuration

**Analysis checklist**:
1. Identify all **hardcoded values** (entity IDs, timeouts, thresholds, scenes, etc.)
2. Determine which values should be **parameterized** (user-configurable inputs)
3. Recognize **selector types** appropriate for each input:
   - `entity`: Single entity ID (default device/area/domain filtering)
   - `device`: Device selection with driver support
   - `area`: Home Assistant area selection
   - `number`: Numeric input with min/max/unit_of_measurement
   - `text`: Free-form text input (domain, name, label)
   - `boolean`: True/false toggle
   - `select`: Predefined list of options
   - `object`: Complex structured data
   - `template`: Jinja2 template as input

4. Document **automation structure**:
   - Trigger type(s) (state, numeric_state, time, time_pattern, sun, event, mqtt, device, etc.)
   - Condition(s) if present (state, numeric_state, time, template, etc.)
   - Action(s) (service call, script, automation trigger, etc.)
   - Mode (single, restart, queued, parallel)

### Step 2: Design Blueprint Schema

Create the blueprint's **input section** with appropriate selector types:

**Principles**:
- Use most **specific selector** (entity > object)
- Entity inputs should filter by domain when possible (light:, climate:, etc.)
- Numeric inputs should include min, max, step, unit_of_measurement
- Text inputs should have maxlength and placeholder hints
- Boolean inputs should have clear icon/description labels

**Example selector types**:
```yaml
inputs:
  light_entity:
    name: "Light to control"
    selector:
      entity:
        domain: light

  brightness_level:
    name: "Brightness"
    selector:
      number:
        min: 0
        max: 100
        unit_of_measurement: "%"
        step: 5

  delay_minutes:
    name: "Delay (minutes)"
    selector:
      number:
        min: 1
        max: 60
        mode: box

  automation_mode:
    name: "Execution mode"
    selector:
      select:
        options:
          - single
          - restart
          - queued
          - parallel

  enable_logging:
    name: "Enable debug logging"
    selector:
      boolean:
```

### Step 3: Create Blueprint Structure

Generate blueprint YAML with proper frontmatter:

```yaml
blueprint:
  name: "Blueprint Name"
  description: "Clear description of what this automation does"
  domain: automation
  source_url: "Optional: URL where blueprint is hosted"

  input:
    # ... input definitions from Step 2

trigger:
  # Replace hardcoded values with !input substitutions
  platform: state
  entity_id: !input trigger_entity
  to: !input trigger_state

condition:
  # Use !input for parameterized conditions
  condition: state
  entity_id: !input condition_entity
  state: !input condition_value

action:
  # Use !input for all parameterized values
  service: light.turn_on
  target:
    entity_id: !input light_entity
  data:
    brightness_pct: !input brightness_level
```

### Step 4: Input Substitution Pattern

**Critical**: Replace all hardcoded values with `!input parameter-name`:

**Before (hardcoded)**:
```yaml
trigger:
  platform: state
  entity_id: light.living_room
  to: 'on'
action:
  service: light.turn_on
  target:
    entity_id: light.kitchen
  data:
    brightness_pct: 80
```

**After (parameterized)**:
```yaml
trigger:
  platform: state
  entity_id: !input trigger_light
  to: !input trigger_state

action:
  service: light.turn_on
  target:
    entity_id: !input action_light
  data:
    brightness_pct: !input brightness_level
```

### Step 5: Selector Type Selection Guide

| Scenario | Selector | Example |
|----------|----------|---------|
| Pick a light/switch/climate entity | entity (domain: light/switch/climate) | `entity: {domain: light}` |
| Pick a device (e.g., for device_id) | device | `device: {}` (no filter) |
| Pick a Home Assistant area | area | `area: {}` |
| Numeric value (0-100, minutes, temp) | number | `number: {min: 0, max: 100}` |
| Single line text (name, label, message) | text | `text: {maxlength: 50}` |
| Boolean on/off toggle | boolean | `boolean: {}` |
| Predefined options (light mode, mode type) | select | `select: {options: [option1, option2]}` |
| Complex object (scene selection with details) | object | `object: {}` |
| Template expression with Jinja2 | template | `template: {}` |

### Step 6: Validation

Before finalizing, verify:
- [ ] All hardcoded values are replaced with `!input`
- [ ] Input names are descriptive (snake_case: `trigger_entity`, `brightness_level`)
- [ ] Each input has `name:` (user-friendly label)
- [ ] Each input has `selector:` with appropriate type
- [ ] Entity selectors filter by domain when relevant
- [ ] Number inputs include min/max/unit_of_measurement
- [ ] Boolean inputs have clear descriptions
- [ ] Blueprint has proper metadata (name, description, domain: automation)
- [ ] Trigger, condition, and action sections use `!input` correctly
- [ ] Mode is set appropriately (single/restart/queued/parallel)

## Best Practices

### Input Naming
```yaml
# Good: Clear, descriptive, shows input purpose
trigger_entity: "Entity to monitor"
action_entity: "Entity to control"
delay_seconds: "Delay in seconds"

# Bad: Ambiguous or unclear
entity1: "Entity"
value: "Number"
thing: "Thing to do"
```

### Selector Defaults
```yaml
# Always include helpful defaults and labels
inputs:
  target_light:
    name: "Light to control"
    description: "The light entity to turn on when triggered"
    default: light.living_room
    selector:
      entity:
        domain: light
```

### Group Related Inputs
```yaml
# Organize inputs logically - triggers first, then conditions, then actions
inputs:
  # Trigger group
  trigger_entity:
    name: "Entity to monitor"

  # Condition group
  condition_entity:
    name: "Entity to check"

  # Action group
  action_entity:
    name: "Entity to control"
```

### Include Meaningful Descriptions
```yaml
inputs:
  brightness_level:
    name: "Brightness"
    description: "Set to 0% to turn off, 100% for full brightness"
    selector:
      number:
        min: 0
        max: 100
        unit_of_measurement: "%"
```

## Output Location

Write the generated blueprint to: `.config/homeassistant/blueprints/automation/<category>/<blueprint-name>.yaml`

**Example paths**:
- `.config/homeassistant/blueprints/automation/lighting/motion-activated-light.yaml`
- `.config/homeassistant/blueprints/automation/climate/temperature-threshold-alarm.yaml`
- `.config/homeassistant/blueprints/automation/notifications/event-notifier.yaml`

## Completion Checklist

After generating the blueprint, provide:
- [ ] Path to generated blueprint file
- [ ] Blueprint name and description
- [ ] List of inputs created with their selector types
- [ ] Before/after comparison (hardcoded vs parameterized)
- [ ] Suggested usage instructions for end-users
- [ ] Any warnings about deprecated patterns or improvements
