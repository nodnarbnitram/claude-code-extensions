# Theme Variables Reference

CSS variables for Home Assistant Lovelace theming.

## Theme Configuration

Themes are defined in `configuration.yaml`:

```yaml
frontend:
  themes:
    my_theme:
      # Variables go here
      primary-color: "#1976D2"
```

Or in a separate themes file:

```yaml
# configuration.yaml
frontend:
  themes: !include_dir_merge_named themes/

# themes/my_theme.yaml
my_theme:
  primary-color: "#1976D2"
```

## Core Colors

### Primary & Accent

```yaml
primary-color: "#03A9F4"              # Main UI color
accent-color: "#FF5722"               # Accent/highlight color
primary-text-color: "#212121"         # Main text
secondary-text-color: "#727272"       # Secondary/muted text
text-primary-color: "#FFFFFF"         # Text on primary color background
```

### Background Colors

```yaml
primary-background-color: "#FAFAFA"   # Main background
secondary-background-color: "#FFFFFF" # Cards/surfaces
card-background-color: "#FFFFFF"      # Card background
paper-dialog-background-color: "#FFFFFF" # Dialog background
```

### Dividers & Borders

```yaml
divider-color: "rgba(0, 0, 0, 0.12)"  # Divider lines
disabled-text-color: "#BDBDBD"        # Disabled elements
```

## State Colors

### Domain-Specific State Colors

```yaml
# Format: state-{domain}-{state}-color
state-light-on-color: "#FFD700"
state-light-off-color: "#9E9E9E"
state-switch-on-color: "#4CAF50"
state-switch-off-color: "#9E9E9E"
state-cover-open-color: "#2196F3"
state-cover-closed-color: "#9E9E9E"
state-lock-locked-color: "#4CAF50"
state-lock-unlocked-color: "#F44336"
state-binary_sensor-on-color: "#4CAF50"
state-binary_sensor-off-color: "#9E9E9E"
```

### Device Class Colors

```yaml
# Format: state-{domain}-{device_class}-{state}-color
state-binary_sensor-motion-on-color: "#FF9800"
state-binary_sensor-door-on-color: "#F44336"
state-binary_sensor-window-on-color: "#2196F3"
state-sensor-battery-low-color: "#F44336"
```

### Generic State Colors

```yaml
state-icon-color: "#44739E"           # Default icon color
state-icon-active-color: "#FDD835"    # Active state icon
state-icon-unavailable-color: "#BDBDBD"
state-on-color: "#66BB6A"             # Generic on state
state-off-color: "#BDBDBD"            # Generic off state
state-unavailable-color: "#BDBDBD"
state-unknown-color: "#9E9E9E"
```

## Card Styling

### Card Appearance

```yaml
ha-card-background: "#FFFFFF"
ha-card-border-radius: "12px"
ha-card-border-color: "transparent"
ha-card-border-width: "0px"
ha-card-box-shadow: "0px 2px 4px rgba(0,0,0,0.1)"
```

### Card Header

```yaml
ha-card-header-color: "#212121"
ha-card-header-font-size: "24px"
```

## Sidebar Styling

```yaml
sidebar-background-color: "#FAFAFA"
sidebar-text-color: "#212121"
sidebar-selected-background-color: "rgba(0,0,0,0.08)"
sidebar-selected-icon-color: "#03A9F4"
sidebar-icon-color: "#757575"
```

## Header (App Bar)

```yaml
app-header-background-color: "#03A9F4"
app-header-text-color: "#FFFFFF"
app-header-selection-bar-color: "#FFFFFF"
```

## Dashboard Background

```yaml
# Solid color
lovelace-background: "#E8E8E8"

# Image
lovelace-background: "center / cover no-repeat url('/local/background.jpg') fixed"

# Gradient
lovelace-background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
```

## Typography (2025+)

New typography tokens replacing legacy Polymer variables:

```yaml
# Font families
ha-font-family-body: "Roboto, sans-serif"
ha-font-family-code: "Roboto Mono, monospace"

# Font sizes
ha-font-size-s: "12px"
ha-font-size-m: "14px"
ha-font-size-l: "16px"
ha-font-size-xl: "20px"
ha-font-size-2xl: "24px"
ha-font-size-4xl: "34px"

# Font weights
ha-font-weight-normal: "400"
ha-font-weight-medium: "500"
ha-font-weight-bold: "700"

# Line heights
ha-line-height-condensed: "1.2"
ha-line-height-normal: "1.5"

# Smoothing
ha-font-smoothing: "antialiased"
```

### Legacy Variable Migration

| Old Variable | New Variable |
|-------------|--------------|
| `--code-font-family` | `--ha-font-family-code` |
| `--paper-font-display1_-_font-size` | `--ha-font-size-4xl` |
| `--paper-font-headline_-_font-size` | `--ha-font-size-2xl` |
| `--paper-font-title_-_font-size` | `--ha-font-size-xl` |
| `--paper-font-subhead_-_font-size` | `--ha-font-size-l` |
| `--paper-font-body1_-_font-size` | `--ha-font-size-m` |
| `--paper-item-icon-color` | `--state-icon-color` |

## Dark Mode

Define dark mode variants within theme:

```yaml
frontend:
  themes:
    my_theme:
      # Light mode (default)
      primary-color: "#1976D2"
      primary-background-color: "#FAFAFA"
      primary-text-color: "#212121"

      modes:
        dark:
          # Dark mode overrides
          primary-color: "#90CAF9"
          primary-background-color: "#121212"
          primary-text-color: "#E0E0E0"
          card-background-color: "#1E1E1E"
```

## Complete Theme Example

```yaml
frontend:
  themes:
    modern_blue:
      # Primary
      primary-color: "#1976D2"
      accent-color: "#FF5722"

      # Text
      primary-text-color: "#212121"
      secondary-text-color: "#757575"
      text-primary-color: "#FFFFFF"

      # Backgrounds
      primary-background-color: "#F5F5F5"
      secondary-background-color: "#FFFFFF"
      card-background-color: "#FFFFFF"

      # Cards
      ha-card-border-radius: "16px"
      ha-card-box-shadow: "0 2px 8px rgba(0,0,0,0.08)"

      # States
      state-light-on-color: "#FFC107"
      state-switch-on-color: "#4CAF50"

      # Dashboard
      lovelace-background: "linear-gradient(180deg, #E3F2FD 0%, #F5F5F5 100%)"

      # Dark mode
      modes:
        dark:
          primary-color: "#90CAF9"
          primary-text-color: "#E0E0E0"
          secondary-text-color: "#9E9E9E"
          primary-background-color: "#121212"
          secondary-background-color: "#1E1E1E"
          card-background-color: "#252525"
          ha-card-box-shadow: "0 2px 8px rgba(0,0,0,0.3)"
          lovelace-background: "#121212"
```

## Per-View Theme

Apply theme to specific view:

```yaml
views:
  - title: Dark Room
    theme: my_dark_theme
    cards: [...]
```

## Per-Card Theme

Apply theme to single card:

```yaml
- type: entities
  theme: my_theme
  entities:
    - light.living_room
```

## Actions

### Set Theme via Automation

```yaml
action: frontend.set_theme
data:
  name: my_theme
  mode: dark
```

### Reload Themes

```yaml
action: frontend.reload_themes
```

## Troubleshooting

**Theme not applying:**
1. Check variable names (no typos)
2. Ensure theme is defined in `configuration.yaml`
3. Reload themes: Developer Tools > Services > `frontend.reload_themes`
4. Clear browser cache

**Variables not working:**
1. CSS variables require `--` prefix in CSS, but not in YAML themes
2. Check if variable is supported in your HA version
3. Some variables require specific card types
