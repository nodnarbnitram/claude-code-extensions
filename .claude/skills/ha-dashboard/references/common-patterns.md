# Common Patterns Reference

Frequently used Lovelace dashboard patterns and configurations.

## Conditional Visibility

### Conditional Card

Show card based on entity state:

```yaml
type: conditional
conditions:
  - condition: state
    entity: binary_sensor.someone_home
    state: "on"
card:
  type: entities
  title: Home Controls
  entities:
    - light.living_room
    - climate.thermostat
```

### Multiple Conditions (AND)

All conditions must be true:

```yaml
type: conditional
conditions:
  - condition: state
    entity: binary_sensor.someone_home
    state: "on"
  - condition: numeric_state
    entity: sun.sun
    attribute: elevation
    below: 0
card:
  type: entities
  title: Evening Home
  entities:
    - light.living_room
```

### State Not Equal

```yaml
type: conditional
conditions:
  - condition: state
    entity: alarm_control_panel.home
    state_not: disarmed
card:
  type: alarm-panel
  entity: alarm_control_panel.home
```

### Numeric State Conditions

```yaml
type: conditional
conditions:
  - condition: numeric_state
    entity: sensor.temperature
    above: 25
card:
  type: entities
  title: It's Hot!
  entities:
    - climate.ac
```

### Screen Width Conditions

```yaml
type: conditional
conditions:
  - condition: screen
    media_query: "(min-width: 768px)"
card:
  type: entities
  title: Desktop Only
  entities:
    - light.living_room
```

### User Conditions

```yaml
type: conditional
conditions:
  - condition: user
    users:
      - user_id_1
      - user_id_2
card:
  type: entities
  title: Admin Only
  entities:
    - input_boolean.admin_mode
```

## Entity Filtering

### Entity Filter Card

Dynamic list based on state:

```yaml
type: entity-filter
entities:
  - light.living_room
  - light.bedroom
  - light.kitchen
  - light.bathroom
state_filter:
  - "on"
card:
  type: glance
  title: Lights On
show_empty: false
```

### Filter by Attribute

```yaml
type: entity-filter
entities:
  - sensor.phone_battery
  - sensor.tablet_battery
  - sensor.laptop_battery
state_filter:
  - operator: "<"
    value: 20
card:
  type: entities
  title: Low Battery Devices
```

### Filter Operators

```yaml
state_filter:
  # Exact match
  - "on"

  # Not equal
  - operator: "!="
    value: "off"

  # Numeric comparisons
  - operator: "<"
    value: 50
  - operator: ">"
    value: 100
  - operator: "<="
    value: 25
  - operator: ">="
    value: 75

  # Regex
  - operator: "regex"
    value: ".*running.*"
```

## Stack Layouts

### Horizontal Stack

Cards side by side:

```yaml
type: horizontal-stack
cards:
  - type: button
    entity: light.living_room
    name: Living
    icon: mdi:sofa
    tap_action:
      action: toggle
  - type: button
    entity: light.bedroom
    name: Bedroom
    icon: mdi:bed
    tap_action:
      action: toggle
  - type: button
    entity: light.kitchen
    name: Kitchen
    icon: mdi:silverware-fork-knife
    tap_action:
      action: toggle
```

### Vertical Stack

Cards stacked vertically:

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: "## Living Room"
  - type: entities
    entities:
      - light.living_room
      - switch.living_room_fan
  - type: history-graph
    entities:
      - sensor.living_room_temperature
    hours_to_show: 24
```

### Nested Stacks

Create complex layouts:

```yaml
type: vertical-stack
cards:
  - type: horizontal-stack
    cards:
      - type: gauge
        entity: sensor.temperature
        name: Temp
      - type: gauge
        entity: sensor.humidity
        name: Humidity
  - type: entities
    entities:
      - climate.thermostat
```

### Grid Layout

```yaml
type: grid
columns: 3
square: true
cards:
  - type: button
    entity: light.one
  - type: button
    entity: light.two
  - type: button
    entity: light.three
  - type: button
    entity: light.four
  - type: button
    entity: light.five
  - type: button
    entity: light.six
```

## Entity Row Types

### Basic Entity Row

```yaml
type: entities
entities:
  - entity: light.living_room
    name: Main Light
    icon: mdi:ceiling-light
    secondary_info: last-changed
```

### Attribute Row

Display specific attribute:

```yaml
type: entities
entities:
  - type: attribute
    entity: sun.sun
    attribute: next_rising
    name: Sunrise
    icon: mdi:weather-sunset-up
```

### Button Row

Multiple buttons in entities card:

```yaml
type: entities
entities:
  - light.living_room
  - type: buttons
    entities:
      - entity: scene.relax
        name: Relax
        icon: mdi:sofa
      - entity: scene.bright
        name: Bright
        icon: mdi:brightness-7
      - entity: scene.movie
        name: Movie
        icon: mdi:movie
```

### Call Service Row

```yaml
type: entities
entities:
  - type: call-service
    name: Restart Home Assistant
    icon: mdi:restart
    action_name: Restart
    service: homeassistant.restart
```

### Divider and Section

```yaml
type: entities
entities:
  - light.living_room
  - light.bedroom
  - type: divider
  - type: section
    label: Climate
  - climate.thermostat
  - sensor.temperature
```

### Web Link Row

```yaml
type: entities
entities:
  - type: weblink
    name: Home Assistant
    url: https://www.home-assistant.io
    icon: mdi:home-assistant
```

### Custom Secondary Info

```yaml
type: entities
entities:
  - entity: sensor.temperature
    secondary_info: last-changed

  - entity: light.living_room
    secondary_info: last-updated

  - entity: media_player.tv
    secondary_info: entity-id

  - entity: climate.thermostat
    secondary_info: attribute
    attribute: current_temperature
```

## Actions

### Tap Actions

```yaml
# Toggle entity
tap_action:
  action: toggle

# Open more info dialog
tap_action:
  action: more-info

# Navigate to another view
tap_action:
  action: navigate
  navigation_path: /lovelace/bedroom

# Open external URL
tap_action:
  action: url
  url_path: https://example.com

# Call service
tap_action:
  action: call-service
  service: light.turn_on
  data:
    entity_id: light.living_room
    brightness_pct: 100
    color_name: blue

# Do nothing
tap_action:
  action: none

# Fire DOM event (for custom cards)
tap_action:
  action: fire-dom-event
  browser_mod:
    service: browser_mod.popup
```

### Confirmation Dialog

```yaml
tap_action:
  action: call-service
  service: script.dangerous_action
  confirmation:
    text: "Are you sure you want to run this?"
```

### Hold and Double-Tap

```yaml
tap_action:
  action: toggle
hold_action:
  action: more-info
double_tap_action:
  action: call-service
  service: light.turn_on
  data:
    brightness_pct: 100
    entity_id: light.bedroom
```

## Templates in Markdown

### Basic Templates

```yaml
type: markdown
content: |
  ## Welcome {{ user }}!

  The temperature is **{{ states('sensor.temperature') }}°C**

  Time: {{ now().strftime('%H:%M') }}
```

### Conditionals

```yaml
type: markdown
content: |
  {% if is_state('binary_sensor.door', 'on') %}
  **Door is open!**
  {% else %}
  Door is closed
  {% endif %}
```

### Loops

```yaml
type: markdown
content: |
  ## Lights On:
  {% for state in states.light if state.state == 'on' %}
  - {{ state.name }}
  {% endfor %}
```

### Attributes

```yaml
type: markdown
content: |
  Battery: {{ state_attr('sensor.phone', 'battery_level') }}%

  Weather: {{ state_attr('weather.home', 'temperature') }}°C,
  {{ state_attr('weather.home', 'humidity') }}% humidity
```

## Card Header/Footer

### Buttons Footer

```yaml
type: entities
title: Living Room
entities:
  - light.living_room
  - switch.fan
footer:
  type: buttons
  entities:
    - entity: scene.relax
      icon: mdi:sofa
    - entity: scene.bright
      icon: mdi:brightness-7
```

### Graph Footer

```yaml
type: entities
title: Climate
entities:
  - climate.thermostat
footer:
  type: graph
  entity: sensor.temperature
  hours_to_show: 24
  detail: 2
```

### Picture Header

```yaml
type: entities
title: Room
header:
  type: picture
  image: /local/images/room.jpg
  tap_action:
    action: navigate
    navigation_path: /lovelace/room-detail
entities:
  - light.room
```

## Picture Elements Patterns

### State Badge

```yaml
type: picture-elements
image: /local/floorplan.png
elements:
  - type: state-badge
    entity: binary_sensor.motion
    style:
      top: 30%
      left: 40%
```

### State Icon with Toggle

```yaml
- type: state-icon
  entity: light.living_room
  tap_action:
    action: toggle
  style:
    top: 50%
    left: 60%
    "--paper-item-icon-color": yellow
```

### State Label

```yaml
- type: state-label
  entity: sensor.temperature
  style:
    top: 70%
    left: 20%
    color: white
    font-size: 16px
```

### Conditional Element

```yaml
- type: conditional
  conditions:
    - entity: binary_sensor.motion
      state: "on"
  elements:
    - type: icon
      icon: mdi:motion-sensor
      style:
        top: 30%
        left: 40%
        color: red
```

## Utility Patterns

### Empty State Message

```yaml
type: entity-filter
entities:
  - light.living_room
  - light.bedroom
state_filter:
  - "on"
show_empty: true
card:
  type: markdown
  content: "No lights are on"
```

### Loading Placeholder

```yaml
type: conditional
conditions:
  - condition: state
    entity: sensor.data
    state: unavailable
card:
  type: markdown
  content: "Loading data..."
```

### Responsive Columns

```yaml
type: glance
columns: 4  # Desktop: 4 columns, mobile: fewer
entities:
  - sensor.one
  - sensor.two
  - sensor.three
  - sensor.four
```
