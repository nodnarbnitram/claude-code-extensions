# Card Reference

Complete reference for Home Assistant Lovelace built-in card types with YAML examples.

## Entity Display Cards

### Entities Card

Display a list of entities with optional header toggle.

```yaml
type: entities
title: Living Room
show_header_toggle: true
state_color: true
entities:
  - entity: light.living_room
    name: Main Light
    icon: mdi:ceiling-light
  - entity: switch.fan
    secondary_info: last-changed
  - type: divider
  - type: section
    label: Climate
  - entity: climate.thermostat
```

### Glance Card

Compact overview of multiple entities.

```yaml
type: glance
title: At a Glance
columns: 4
show_name: true
show_state: true
show_icon: true
entities:
  - entity: sensor.temperature
    name: Temp
  - entity: sensor.humidity
    name: Humidity
  - entity: binary_sensor.motion
    show_last_changed: true
  - entity: light.bedroom
    tap_action:
      action: toggle
```

### Button Card

Single entity button with customizable actions.

```yaml
type: button
entity: light.living_room
name: Living Room
icon: mdi:lightbulb
show_name: true
show_icon: true
show_state: true
tap_action:
  action: toggle
hold_action:
  action: more-info
double_tap_action:
  action: call-service
  service: light.turn_on
  data:
    brightness_pct: 100
    entity_id: light.living_room
```

### Tile Card

Modern entity control with features.

```yaml
type: tile
entity: light.living_room
name: Living Room Light
icon: mdi:lightbulb
color: amber
show_entity_picture: false
vertical: false
features:
  - type: light-brightness
  - type: light-color-temp
```

**Tile Features by Domain:**
- `light`: `light-brightness`, `light-color-temp`
- `climate`: `climate-hvac-modes`, `target-temperature`
- `cover`: `cover-open-close`, `cover-position`, `cover-tilt`
- `fan`: `fan-speed`
- `vacuum`: `vacuum-commands`
- `select`/`input_select`: `select-options`
- `lawn_mower`: `lawn-mower-commands`

### Sensor Card

Sensor with optional graph.

```yaml
type: sensor
entity: sensor.temperature
name: Temperature
icon: mdi:thermometer
graph: line
hours_to_show: 24
detail: 2
```

## Gauge & Statistics Cards

### Gauge Card

Circular gauge for numeric values.

```yaml
type: gauge
entity: sensor.cpu_usage
name: CPU Usage
unit: "%"
min: 0
max: 100
severity:
  green: 0
  yellow: 60
  red: 80
needle: true
```

**Gauge with Segments:**
```yaml
type: gauge
entity: sensor.battery
segments:
  - from: 0
    color: red
  - from: 20
    color: orange
  - from: 40
    color: yellow
  - from: 60
    color: green
```

### Statistic Card

Display statistical values over time.

```yaml
type: statistic
entity: sensor.energy_usage
stat_type: mean
period:
  calendar:
    period: month
name: Average Energy This Month
```

**stat_type options:** `mean`, `min`, `max`, `sum`, `state`, `change`

### Statistics Graph Card

Historical statistics visualization.

```yaml
type: statistics-graph
title: Energy Statistics
entities:
  - sensor.daily_energy
stat_types:
  - mean
  - min
  - max
period:
  calendar:
    period: day
days_to_show: 7
```

## Media Cards

### Weather Forecast Card

Weather with forecast display.

```yaml
type: weather-forecast
entity: weather.home
show_current: true
show_forecast: true
forecast_type: daily
secondary_info_attribute: humidity
```

**forecast_type options:** `daily`, `hourly`, `twice_daily`

### Media Control Card

Media player controls.

```yaml
type: media-control
entity: media_player.living_room
```

### Picture Card

Static image display.

```yaml
type: picture
image: /local/images/floorplan.png
tap_action:
  action: navigate
  navigation_path: /lovelace/floorplan
```

### Picture Entity Card

Entity represented by an image.

```yaml
type: picture-entity
entity: camera.front_door
camera_view: live
show_name: true
show_state: true
tap_action:
  action: more-info
```

### Picture Glance Card

Image with entity state overlay.

```yaml
type: picture-glance
title: Living Room
image: /local/images/living-room.jpg
entities:
  - entity: light.living_room
  - entity: binary_sensor.motion
  - entity: sensor.temperature
```

### Picture Elements Card

Interactive image with positioned elements.

```yaml
type: picture-elements
image: /local/images/floorplan.png
elements:
  - type: state-badge
    entity: binary_sensor.motion_living
    style:
      top: 30%
      left: 40%
  - type: state-icon
    entity: light.living_room
    tap_action:
      action: toggle
    style:
      top: 50%
      left: 60%
  - type: state-label
    entity: sensor.temperature
    style:
      top: 70%
      left: 20%
      color: white
```

## Information Cards

### Markdown Card

Render markdown content with templates.

```yaml
type: markdown
title: Welcome
content: |
  ## Hello {{ user }}!

  The temperature is **{{ states('sensor.temperature') }}°C**

  {% if is_state('binary_sensor.motion', 'on') %}
  Motion detected!
  {% endif %}
```

### Logbook Card

Entity history log.

```yaml
type: logbook
entities:
  - binary_sensor.front_door
  - lock.front_door
hours_to_show: 24
```

### History Graph Card

Historical state graph.

```yaml
type: history-graph
title: Temperature History
entities:
  - entity: sensor.indoor_temp
    name: Indoor
  - entity: sensor.outdoor_temp
    name: Outdoor
hours_to_show: 48
```

### Calendar Card

Calendar events display.

```yaml
type: calendar
entities:
  - calendar.family
  - calendar.work
initial_view: listWeek
```

### Map Card

Entity location map.

```yaml
type: map
entities:
  - entity: device_tracker.phone
  - entity: zone.home
  - entity: zone.work
aspect_ratio: 16:9
default_zoom: 14
dark_mode: true
```

### Iframe Card

Embed external content.

```yaml
type: iframe
url: https://grafana.local/d/dashboard
aspect_ratio: 16:9
```

## Climate Cards

### Thermostat Card

Climate control interface.

```yaml
type: thermostat
entity: climate.living_room
features:
  - type: climate-hvac-modes
    hvac_modes:
      - heat
      - cool
      - auto
      - "off"
```

### Humidifier Card

Humidity control.

```yaml
type: humidifier
entity: humidifier.bedroom
features:
  - type: humidifier-modes
```

## Layout Cards

### Horizontal Stack

Cards side by side.

```yaml
type: horizontal-stack
cards:
  - type: button
    entity: light.living_room
  - type: button
    entity: light.bedroom
  - type: button
    entity: light.kitchen
```

### Vertical Stack

Cards stacked vertically.

```yaml
type: vertical-stack
cards:
  - type: entities
    entities:
      - light.living_room
  - type: history-graph
    entities:
      - sensor.temperature
```

### Grid Card

Grid layout for cards.

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
```

## Conditional & Filter Cards

### Conditional Card

Show card based on conditions.

```yaml
type: conditional
conditions:
  - condition: state
    entity: binary_sensor.home_occupied
    state: "on"
  - condition: numeric_state
    entity: sensor.temperature
    above: 20
card:
  type: entities
  entities:
    - climate.thermostat
```

### Entity Filter Card

Dynamic entity list based on state.

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

## Special Cards

### Alarm Panel Card

Alarm control interface.

```yaml
type: alarm-panel
entity: alarm_control_panel.home
states:
  - arm_home
  - arm_away
  - arm_night
```

### Light Card

Simple light control.

```yaml
type: light
entity: light.living_room
name: Living Room
icon: mdi:ceiling-light
```

### Shopping List Card

Shopping list management.

```yaml
type: shopping-list
title: Grocery List
```

### Todo List Card

Todo list display.

```yaml
type: todo-list
entity: todo.shopping
title: Shopping List
```

### Energy Cards

Energy dashboard cards (require energy integration).

```yaml
# Energy Distribution
type: energy-distribution
link_dashboard: true

# Energy Usage Graph
type: energy-usage-graph

# Energy Solar Graph
type: energy-solar-graph
```

## Card Actions Reference

All cards support these action types:

```yaml
tap_action:
  action: toggle              # Toggle entity state
  # OR
  action: more-info           # Open entity dialog
  # OR
  action: navigate            # Navigate to view
  navigation_path: /lovelace/bedroom
  # OR
  action: url                 # Open URL
  url_path: https://example.com
  # OR
  action: call-service        # Call Home Assistant service
  service: light.turn_on
  data:
    entity_id: light.bedroom
    brightness_pct: 50
  # OR
  action: none                # Disable action
```

Actions available on most cards:
- `tap_action` - Single tap/click
- `hold_action` - Long press/hold
- `double_tap_action` - Double tap/click
